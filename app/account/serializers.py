
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username','phone_number','first_name'
            ,'last_name','profile_image','about_me')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
        
class UserRegisterSeralizer(RegisterSerializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    username = serializers.CharField()


    @transaction.atomic
    def save(self, request,**kwargs) :
        adapter = get_adapter()
        user = adapter.new_user(request)
        user.phone_number = self.validated_data.get('phone_number')
        user.email = self.validated_data.get('email')
        user.username = self.validated_data.get('username')
        password = self.validated_data.get('password1')
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    '''Serializer for the user authentication object'''

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type' : 'password'},    )

    def validate(self, attrs):
        '''Validate and authenticate the user'''

        email = attrs.get('email')
        password = attrs.get('password')
        print(email,password)
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )
        print(user)
        if not user:
            msg = ('Unable to authenticate with provided credentials !')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
