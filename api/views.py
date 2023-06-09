from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer,CropSerializer,ChangePasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Embedded,Crops,UserImage,SelectedCrop,ReportPlant
from .serializers import EmbeddedSerializer,ImgSerializer,UpdateUserSerializer,SelectedCropSerializer,ReportSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import views,viewsets
from rest_framework import permissions
from . import serializers
from django.contrib.auth import login
from .authentication import CsrfExemptSessionAuthentication







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
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = [AllowAny]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    if request.user.is_authenticated:
        logout(request)

    return Response('User Logged out successfully')




class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny]

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
@permission_classes([AllowAny])
def embeddedViews(request):
   embedded = Embedded.objects.all()
   serializer = EmbeddedSerializer(embedded, many=True)
   return Response({"embeddeds":serializer.data})
@api_view(['GET'])
@permission_classes([AllowAny])
def embeddedView(request):
   embedded = Embedded.objects.order_by('-updated').first()
   serializer = EmbeddedSerializer(embedded, many=False)
   return Response({"embedded":serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def cropViews(request):
    crop = Crops.objects.all()
    serializer = CropSerializer(crop, many=True)
    return Response({"crops":serializer.data})

@api_view(['GET'])
@permission_classes([AllowAny])
def selectedViews(request):
    selected = SelectedCrop.objects.order_by('crop').first()
    serializer = SelectedCropSerializer(selected, many=False)
    return Response(serializer.data)


class SelectedUpdate(APIView):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = [AllowAny]
  def put(self,request):
    if request.method == 'PUT':
        queryset = SelectedCrop.objects.prefetch_related('crop').order_by('crop').first()
        serializer = SelectedCropSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        




class MyModelViewSet(viewsets.ModelViewSet):
    queryset = UserImage.objects.order_by('-creation_date')
    serializer_class = ImgSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.AllowAny]
    
    

class UserImg(APIView):
 authentication_classes = (CsrfExemptSessionAuthentication,) 
 permission_classes = [AllowAny]
 parser_classes = [MultiPartParser,FormParser]
 def put(self,request,pk):
   if request.method == 'PUT':
      queryset = UserImage.objects.get(id=pk)
      serializer = ImgSerializer(queryset, many=False, data=request.data,)
      if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,content_type='image/jpeg')

 def success(self,request):
    return Response('successfully uploaded')  






class UpdateProfileView(generics.UpdateAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = UpdateUserSerializer
    def get_object(self):
        return self.request.user


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)



@api_view(['POST'])
@permission_classes([AllowAny])
def report_create(request):
   data = request.data
   report = ReportPlant.objects.create(
      plant_name=data['plant_name'],
      confidence=data['confidence'],
      description=data['description'],
   )
   serializer = ReportSerializer(report, many=False)
   return Response(serializer.data)    

class ReportViews(views.APIView):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = [AllowAny]
  def get(self,request):
    report = ReportPlant.objects.all()
    serializer = ReportSerializer(report, many=True)
    return Response({"Reports":serializer.data})


