from io import BytesIO

from clarifai import rest

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sunflower.api.base.serializers.cookbook import CookBookSerializer
from sunflower.api.base.serializers.ingredient import IngredientSerializer
from sunflower.api.base.serializers.recipe import (RecipeGetSerializer,
                                                   RecipeCreateUpdateSerializer)
from sunflower.api.base.serializers.recipe_comment import (
    RecipeCommentSerializer)
from sunflower.api.base.serializers.recipe_step import RecipeStepSerializer
from sunflower.api.base.serializers.tag import TagSerializer
from sunflower.api.base.serializers.user import UserSerializer

from sunflower.models import CustomUser
from sunflower.permissions import IsOwnerOrReadOnly
from sunflower.services.service.cookbook import CookBookService
from sunflower.services.service.ingredient import IngredientService
from sunflower.services.service.recipe import RecipeService
from sunflower.services.service.recipe_comment import RecipeCommentService
from sunflower.services.service.recipe_rating import RecipeRatingService
from sunflower.services.service.recipe_step import RecipeStepService
from sunflower.services.service.tag import TagService
from sunflower import settings


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
        recipe_id = self.request.query_params.get('recipe_id', None)
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

        context = {
            "request": request,
        }

        serializer = TagSerializer(data=request.data, context=context)
        if serializer.is_valid():
            title = request.data['title']
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

        context = {
            "request": request,
        }

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

    @staticmethod
    def put(request, ingredient_id: int):
        user: CustomUser = request.user
        ingredient = IngredientService.update(user.pk, ingredient_id,
                                              request.data)
        serializer = IngredientSerializer(ingredient)
        Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, ingredient_id: int):
        user: CustomUser = request.user
        IngredientService.delete(user.pk, ingredient_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

        context = {
            "request": request,
        }

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

    @staticmethod
    def put(request, recipe_step_id: int):
        user: CustomUser = request.user
        recipe_step = RecipeStepService.update(user.pk, recipe_step_id,
                                               request.data)
        serializer = RecipeStepSerializer(recipe_step)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, recipe_step_id: int):
        user: CustomUser = request.user
        RecipeStepService.delete(user.pk, recipe_step_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return RecipeCommentService.get_all_by_recipe_id(
            self.kwargs['recipe_id'])

    @staticmethod
    def post(request, recipe_id: int):
        data = request.data
        data['recipe'] = recipe_id

        context = {
            "request": request,
        }

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
    def put(request, comment_id: int):
        user: CustomUser = request.user
        comment = RecipeCommentService.update(user.pk, comment_id, request.data)
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

        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = RecipeService.get_all_by_user_id(user_id)

        tag_id = self.request.query_params.get('tag_id', None)
        if tag_id:
            queryset = RecipeService.get_all_by_tag_id(tag_id)

        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            queryset = RecipeService.get_all_by_product_id(product_id)

        return queryset

    @staticmethod
    def post(request):
        context = {
            "request": request,
        }

        serializer = RecipeCreateUpdateSerializer(data=request.data,
                                                  context=context)
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
    def put(request, recipe_id: int):
        user: CustomUser = request.user
        updated_recipe = RecipeService.update(user.pk, recipe_id, request.data)
        serializer = RecipeCreateUpdateSerializer(updated_recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, recipe_id: int):
        user: CustomUser = request.user
        RecipeService.delete(user.pk, recipe_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CookBookRecipeList(generics.ListAPIView):
    """
    API endpoint that allows cookbook recipes to be viewed and
    to add new recipe to cookbook.
    GET cookbooks/:id/recipes/:id
    POST cookbooks/:id/recipes/:id
    """
    serializer_class = RecipeGetSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return RecipeService.get_all_by_cookbook_id(self.kwargs['cookbook_id'])


class CookBookRecipeDetail(APIView):
    """
    API endpoint that allows recipe tag to delete tag from recipe.
    DELETE cookbooks/:id/recipes/:id
    """

    @staticmethod
    def post(request, cookbook_id, recipe_id):
        user: CustomUser = request.user
        recipe = RecipeService.get(recipe_id)
        CookBookService.add_recipe(user.pk, cookbook_id, recipe)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, cookbook_id, recipe_id):
        user: CustomUser = request.user
        CookBookService.remove_recipe(user.pk, cookbook_id, recipe_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CookBookList(generics.ListAPIView):
    """
    API endpoint that allows all cookbook to be viewed and
    to add new recipe.
    GET cookbooks/
    POST cookbooks/
    """
    serializer_class = CookBookSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the cookbooks
        for the currently authenticated user.
        """
        user: CustomUser = self.request.user
        return CookBookService.get_all_by_user_id(user.pk)

    @staticmethod
    def post(request):
        context = {
            "request": request,
        }

        serializer = CookBookSerializer(data=request.data,
                                        context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookBookDetail(APIView):
    """
    API endpoint that allows recipe to be viewed or edited.
    GET cookbooks/:id
    PUT cookbooks/:id
    DELETE cookbook/:id
    """

    @staticmethod
    def get(request, cookbook_id: int):
        cookbook = CookBookService.get(cookbook_id)
        serializer = CookBookSerializer(cookbook)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, cookbook_id: int):
        user: CustomUser = request.user
        cookbook = CookBookService.update(user.pk, cookbook_id, request.data)
        serializer = CookBookSerializer(cookbook)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, cookbook_id: int):
        user: CustomUser = request.user
        CookBookService.delete(user.pk, cookbook_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FoodPhoto(APIView):

    def post(self, *args, **kwargs):
        app = rest. ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
        model = app.models.get(settings.DATASET)

        files = self.request.FILES
        print(files)
        images = []
        for file in files.values():
            images.append(rest.Image(file_obj=BytesIO(file.read())))
            print(images)

        ingredients = []
        for image in images:
            predictions = model.predict([image])
            concepts = predictions["outputs"][0]["data"]["concepts"]

            for product in concepts:
                name, value = product["name"], product["value"]
                if value >= settings.VALUE_PRECISION:
                    ingredients.append((name, value))

        return Response(data=ingredients, status=status.HTTP_200_OK)



# class RecipeSuggestion(APIView):
#
#     def post(self):







