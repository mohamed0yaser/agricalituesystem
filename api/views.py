from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated 
from .models import Embedded,UserImage
from .serializers import EmbeddedSerializer,ImgSerializer
from rest_framework.decorators import api_view
from django.shortcuts import redirect


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer    








# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenObtainPairSerializer,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer






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
def embeddedCreate(request):
   data = request.data
   embedded = Embedded.objects.create(
     temperature=data['temperature'],
     humidity=data['humidity'],
     light=data['light'],
     rainfall=data['rainfall'],
     soil_moisture=data['soil_moisture']
   )
   serializer = EmbeddedSerializer(embedded, many=False)
   return Response(serializer.data)

@api_view(['GET'])
def embeddedViews(request):
   embedded = Embedded.objects.all()
   serializer = EmbeddedSerializer(embedded, many=True)
   return Response(serializer.data)
@api_view(['GET'])
def embeddedView(request,pk):
   embedded = Embedded.objects.get(id=pk)
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
@api_view(['DELETE'])
def embeddedDelete(request,pk):
   embedded = Embedded.objects.get(id=pk)
   embedded.delete()
   return Response('file is deleted')



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
def imgViews(request):
   imgView = UserImage.objects.all()
   serializer = ImgSerializer(imgView)
   return Response(serializer.data)



