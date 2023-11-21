from django.contrib import admin
from django.urls import path, include
from integrations import views as integrationviews
from ingredients import views as ingredient_views
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'recipes', integrationviews.EdamamAPIView, basename='recipes')
router.register(r'locations', integrationviews.LocationsAPIView, basename='locations')
router.register(r'shopping-lists', integrationviews.ShoppingListAPIView, basename='shopping-lists')
router.register(r'ingredients', ingredient_views.IngredientView, basename='ingredients')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
