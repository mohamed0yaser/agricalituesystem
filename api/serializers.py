from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Embedded, UserImage,Crops,SelectedCrop,ReportPlant
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate





class ImgSerializer(serializers.ModelSerializer):

    image_url = serializers.ImageField(required=False)

    class Meta:
        model = UserImage
        fields = ['image_url']

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "username"]








#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True},
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
  

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)





class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        

        instance.save()

        return instance
    


class EmbeddedSerializer(ModelSerializer):
  class Meta:
    model = Embedded
    fields = ['temperature','humidity','light','rainfall','soil_moisture','updated','created','pump_on']


class CropSerializer(ModelSerializer):
   class Meta:
      model = Crops
      fields = ['crop_name','soil_moisture_min','soil_moisture_max']
      

class SelectedCropSerializer(ModelSerializer):
   soil_moisture_min = serializers.ReadOnlyField()
   soil_moisture_max = serializers.ReadOnlyField()
   class Meta:
      model = SelectedCrop
      fields = ['soil_moisture_min','soil_moisture_max']
      read_only_fields = ('soil_moisture_min', 'soil_moisture_max')
   def pre_save(self, instance):
        if instance.crop_id:
            crop = Crops.objects.get(id=instance.crop_id)
            instance.soil_moisture_min = crop.soil_moisture_min
            instance.soil_moisture_max = crop.soil_moisture_max



class LoginSerializer(serializers.Serializer):
   username = serializers.CharField(
        label="Username",
        write_only=True
   )
   password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
   def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs



class ReportSerializer(serializers.ModelSerializer):
   class Meta:
      model = ReportPlant
      fields = '__all__'

