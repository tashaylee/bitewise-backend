"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shared import views as sharedviews
from budget import views as budgetviews
from commitment import views as commitmentviews
from integrations import views as integrationviews
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'budgets', budgetviews.BudgetView, 'budget')
router.register(r'users', sharedviews.UserView, 'user')
router.register(r'commitmentcounts',
                commitmentviews.CommitmentCountView, 'commitmentcount')
router.register(r'mealcommitments',
                commitmentviews.MealCommitmentView, 'mealcommitments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', sharedviews.HomeView.as_view(), name ='home'),
    path('logout/', sharedviews.LogoutView.as_view(), name='logout'),
    path('recipes/', integrationviews.EdamamAPIView.as_view(), name='get_edamam_meals')
]
