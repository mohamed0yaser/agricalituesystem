from django.urls import path
from .views import MyTokenObtainPairView,UserDetailAPI,RegisterUserAPIView,ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

urlpatterns = [    
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/get-details",UserDetailAPI.as_view()),
    path('api/register/',RegisterUserAPIView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/embedded/',views.embeddedViews),
    path('api/embedded/create/',views.embeddedCreate),
    path('api/embedded/<str:pk>/',views.embeddedView),
    path('api/embedded/<str:pk>/update/',views.embeddedUpdate),
    path('api/embedded/<str:pk>/delete/',views.embeddedDelete),
    path('api/uploadImage/',views.userImg),
    path('api/viewImage/',views.imgViews),

]