from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer,CropSerializer,ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from .models import Embedded,Crops,UserImage
from .serializers import EmbeddedSerializer,ImgSerializer,UpdateUserSerializer
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import redirect,render
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import UserCreationForm
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from . import serializers
from django.contrib.auth import login



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer   








# Class based view to Get User Details using Token Authentication
class UserDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})






class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
@permission_classes([AllowAny])
def embeddedCreate(request):
   data = request.data
   embedded = Embedded.objects.create(
     temperature=data['temperature'],
     humidity=data['humidity'],
     light=data['light'],
     rainfall=data['rainfall'],
     soil_moisture=data['soil_moisture'],
     pump_on=data['pump_on']
   )
   serializer = EmbeddedSerializer(embedded, many=False)
   return Response(serializer.data)

@api_view(['GET'])
def embeddedViews(request):
   embedded = Embedded.objects.all()
   serializer = EmbeddedSerializer(embedded, many=True)
   return Response(serializer.data)
@api_view(['GET'])
def embeddedView(request):
   embedded = Embedded.objects.order_by('-updated').first()
   serializer = EmbeddedSerializer(embedded, many=False)
   return Response(serializer.data)
@api_view(['PUT'])
def embeddedUpdate(request,pk):
   data = request.data
   embedded = Embedded.objects.get(id=pk)
   serializer = EmbeddedSerializer(embedded, data=request.data)
   if serializer.is_valid():
         serializer.save()
   return Response(serializer.data)


@api_view(['DELETE','GET'])
def embeddedDelete(request):
   if request.method == 'DELETE':
    embedded = Embedded.objects.order_by('-updated').first()
    embedded.delete()
    return Response('file is deleted')
   elif request.method == 'GET':
       embedded = Embedded.objects.order_by('-updated').first()
       serializer = EmbeddedSerializer(embedded, many=False)
       return Response(serializer.data)

@api_view(['GET'])
def cropViews(request):
    crop = Crops.objects.all()
    serializer = CropSerializer(crop, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def userImg(request):
   if request.method == 'POST':
      serializer = ImgSerializer(request.POST, request.FILES)
      if serializer.is_valid():
            serializer.save()
            return redirect('success')

def success(request):
    return Response('successfully uploaded') 

@api_view(['GET'])
def userviewImg(request):
   if request.method == 'GET':
      image = UserImage.objects.order_by('name').first()
      serializer = ImgSerializer(image , many=False)
      return Response(serializer.data)



def register_user(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():

        inactive_user = send_verification_email(request, form)
        email= inactive_user.cleaned_data['email']
        return Response(email)
    return Response({'errors': form.errors})



class UpdateProfileView(generics.UpdateAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    def get_object(self):
        return self.request.user


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)



    



