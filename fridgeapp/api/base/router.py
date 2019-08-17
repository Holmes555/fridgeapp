from django.contrib import admin
from django.urls import include, path

from fridgeapp.api.base import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rest_auth.urls")),
    path("registration/", include("rest_auth.registration.urls")),
    path("users/", views.UserDetail.as_view()),
    path("tags/", views.TagList.as_view()),
    path("tags/<int:tag_id>", views.TagDetail.as_view()),
    path("ingredients/<int:ingredient_id>", views.IngredientDetail.as_view()),
    path("recipes/", views.RecipeList.as_view()),
    path("recipes/<int:recipe_id>", views.RecipeDetail.as_view()),
    path("recipes/<int:recipe_id>/ingredients", views.RecipeIngredientList.as_view()),
    path("recipes/<int:recipe_id>/tags", views.RecipeTagList.as_view()),
    path("recipes/<int:recipe_id>/tags/<int:tag_id>", views.RecipeTagDetail.as_view()),
    path("recipes/<int:recipe_id>/steps", views.RecipeStepList.as_view()),
    path("steps/<int:recipe_step_id>", views.RecipeStepDetail.as_view()),
    path("recipes/<int:recipe_id>/comments", views.RecipeCommentList.as_view()),
    path("comments/<int:comment_id>", views.CommentDetail.as_view()),
    path("recipes/<int:recipe_id>/rate", views.RecipeRatingDetail.as_view()),
    path("fridge/", views.Fridge.as_view()),
    path("docs/", schema_view),
]


api_urlpatterns = urlpatterns
