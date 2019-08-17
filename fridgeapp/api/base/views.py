from clarifai.rest import ClarifaiApp, Image
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fridgeapp.api.base.serializers.ingredient import IngredientSerializer
from fridgeapp.api.base.serializers.recipe import (RecipeCreateUpdateSerializer,
                                                   RecipeGetSerializer)
from fridgeapp.api.base.serializers.recipe_comment import \
    RecipeCommentSerializer
from fridgeapp.api.base.serializers.recipe_step import RecipeStepSerializer
from fridgeapp.api.base.serializers.tag import TagSerializer
from fridgeapp.api.base.serializers.user import UserSerializer
from fridgeapp.models import CustomUser
from fridgeapp.permissions import IsOwnerOrReadOnly
from fridgeapp.services.service.ingredient import IngredientService
from fridgeapp.services.service.recipe import RecipeService
from fridgeapp.services.service.recipe_comment import RecipeCommentService
from fridgeapp.services.service.recipe_rating import RecipeRatingService
from fridgeapp.services.service.recipe_step import RecipeStepService
from fridgeapp.services.service.tag import TagService

DATASET = "food-items-v1.0"


class UserDetail(APIView):
    """
    API endpoint that allows get user_id by token
    GET users/
    """

    @staticmethod
    def get(request):
        user: CustomUser = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagList(generics.ListAPIView):
    """
    API endpoint that allows all tags to be viewed.
    GET tags/
    GET tags/?recipe_id=<value>
    """

    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned tag to a given user,
        by filtering against a `recipe_id` query parameter in the URL.
        """
        queryset = TagService.get_all()
        recipe_id = self.request.query_params.get("recipe_id", None)
        if recipe_id:
            queryset = TagService.get_all_by_recipe_id(recipe_id)
        return queryset


class TagDetail(APIView):
    """
    API endpoint that allows tag to be viewed.
    GET tags/:id/
    """

    @staticmethod
    def get(request, tag_id):
        tag = TagService.get(tag_id)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeTagList(APIView):
    """
    API endpoint that allows all recipe tags to add new tag to recipe.
    POST recipes/:id/tags/
    """

    @staticmethod
    def get(request, recipe_id: int):
        tags = TagService.get_all_by_recipe_id(recipe_id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, recipe_id: int):
        user: CustomUser = request.user

        context = {"request": request}

        serializer = TagSerializer(data=request.data, context=context)
        if serializer.is_valid():
            title = request.data["title"]
            tag = TagService.get_by_title(title=title)
            if not tag:
                tag = serializer.save()
            TagService.add_to_recipe(user.pk, recipe_id, tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeTagDetail(APIView):
    """
    API endpoint that allows recipe tag to delete tag from recipe.
    DELETE recipes/:id/tags/:id
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def delete(request, recipe_id: int, tag_id: int):
        user: CustomUser = request.user
        tag = TagService.get(tag_id)
        TagService.remove_from_recipe(user.pk, recipe_id, tag)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeIngredientList(APIView):
    """
    API endpoint that allows all ingredients to be viewed and to
    add new ingredient to recipe.
    GET recipes/:id/ingredients/
    POST recipes/:id/ingredients/
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def get(request, recipe_id: int):
        ingredients = IngredientService.get_all_by_recipe_id(recipe_id)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, recipe_id: int):
        user: CustomUser = request.user

        context = {"request": request}

        serializer = IngredientSerializer(data=request.data, context=context)
        if serializer.is_valid():
            ingredient = serializer.save()
            RecipeService.add_ingredient(user.pk, recipe_id, ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetail(APIView):
    """
    API endpoint that allows recipe ingredient to be viewed or edited.
    GET ingredients/:id
    PUT ingredients/:id
    DELETE ingredients/:id
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def get(request, ingredient_id: int):
        ingredient = IngredientService.get(ingredient_id)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeStepList(APIView):
    """
    API endpoint that allows all recipe steps to be viewed and
    to add new step to recipe.
    GET recipes/:id/steps/
    POST recipes/:id/steps/
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def get(request, recipe_id: int):
        recipe_steps = RecipeStepService.get_all_by_recipe_id(recipe_id)
        serializer = RecipeStepSerializer(recipe_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, recipe_id: int):
        data = request.data
        user: CustomUser = request.user

        context = {"request": request}

        serializer = RecipeStepSerializer(data=data, context=context)
        if serializer.is_valid():
            recipe_step = serializer.save()
            RecipeService.add_recipe_step(user.pk, recipe_id, recipe_step)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeStepDetail(APIView):
    """
    API endpoint that allows recipe step to be viewed or edited.
    GET steps/:id
    PUT steps/:id
    DELETE steps/:id
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def get(request, recipe_step_id: int):
        recipe_step = RecipeStepService.get(recipe_step_id)
        serializer = RecipeStepSerializer(recipe_step)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeCommentList(generics.ListAPIView):
    """
    API endpoint that allows all recipe comments to be viewed and
    to add new comment to recipe.
    GET recipes/:id/comments/
    POST recipes/:id/comments/
    """

    serializer_class = RecipeCommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return RecipeCommentService.get_all_by_recipe_id(self.kwargs["recipe_id"])

    @staticmethod
    def post(request, recipe_id: int):
        data = request.data
        data["recipe"] = recipe_id

        context = {"request": request}

        serializer = RecipeCommentSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    API endpoint that allows comment to be viewed or edited.
    GET comments/:id
    PUT comments/:id
    DELETE comments/:id
    """

    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def get(request, comment_id: int):
        comment = RecipeCommentService.get(comment_id)
        serializer = RecipeCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, comment_id: int):
        user: CustomUser = request.user
        RecipeCommentService.delete(user.pk, comment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeRatingDetail(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def put(request, recipe_id):
        RecipeRatingService.update(recipe_id, request.data)
        return Response(status=status.HTTP_200_OK)


class RecipeList(generics.ListAPIView):
    """
    API endpoint that allows all recipe to be viewed and
    to add new recipe.
    GET recipes/
    POST recipes/
    """

    serializer_class = RecipeGetSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """
        Optionally restricts the returned recipes to a given user,
        by filtering against a `user_id`, `tag_id` or `product_id`
        query parameter in the URL.
        """

        queryset = RecipeService.get_all()

        tag_id = self.request.query_params.get("tag_id", None)
        if tag_id:
            queryset = RecipeService.get_all_by_tag_id(tag_id)

        return queryset

    @staticmethod
    def post(request):
        context = {"request": request}

        serializer = RecipeCreateUpdateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    """
    API endpoint that allows recipe to be viewed or edited.
    GET recipes/:id
    PUT recipes/:id
    DELETE recipes/:id
    """

    @staticmethod
    def get(request, recipe_id: int):
        recipe = RecipeService.get(recipe_id)
        serializer = RecipeGetSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, recipe_id: int):
        user: CustomUser = request.user
        RecipeService.delete(user.pk, recipe_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Fridge(APIView):
    def post(self):
        app = ClarifaiApp(api_key="be355c0550a94e6282fb8adcb83f6a49")
        model = app.models.get(DATASET)

        file = self.request.FILES[0]
        image = Image(filename=file)

        predictions = model.predict([image])
        concepts = predictions["outputs"][0]["data"]["concepts"]

        predictions = []
        for product in concepts:
            name, value = concepts["name"], concepts["value"]
            predictions.append((name, value))
