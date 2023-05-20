from django.urls import path
from .views import MyTokenObtainPairView,UserDetailAPI,RegisterUserAPIView,ChangePasswordView,UpdateProfileView,APILogoutView,LoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views
x=5
urlpatterns = [    
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_details/',UserDetailAPI.as_view()),
    path('api/sign_up/',RegisterUserAPIView.as_view()),
    path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/embeddeds/',views.embeddedViews),
    path('api/embedded/create/',views.embeddedCreate),
    path('api/embedded/',views.embeddedView),
    path('api/embedded/update/',views.embeddedUpdate),
    path('api/embedded/delete/',views.embeddedDelete),
    path('api/uploadImage/',views.userImg),
    path('api/update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('api/logout/',APILogoutView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/cropView/',views.cropViews),
    


]
