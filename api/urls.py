from django.urls import path
from .views import MyTokenObtainPairView,UserDetailAPI,RegisterUserAPIView,ChangePasswordView,UpdateProfileView,LoginView,MyModelViewSet,ReportViews,UserImg,SelectedUpdate
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

urlpatterns = [    
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_details/',UserDetailAPI.as_view()),
    path('api/sign_up/',RegisterUserAPIView.as_view()),
    path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/embeddeds/',views.embeddedViews),
    path('api/embedded/create/',views.embeddedCreate),
    path('api/embedded/',views.embeddedView),
    path('api/uploadImage/',MyModelViewSet.as_view({'get':'list'})),
    path('api/uploadedImage/',UserImg.as_view()),
    path('api/update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('api/logout/',views.User_logout),
    path('api/login/', LoginView.as_view()),
    path('api/cropView/',views.cropViews),
    path('api/select/',views.selectedViews),
    path('api/selectup/',SelectedUpdate.as_view()),
    path('api/reportML/',views.report_create),
    path('api/reportF/',ReportViews.as_view()),

    
]

