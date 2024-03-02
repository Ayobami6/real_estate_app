from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def validate(self, data):
        errors = {}
        email = data.get('email')
        username = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        if CustomUser.objects.filter(email__iexact=email):
            errors['error'] = _('The email address is already in use')
            raise serializers.ValidationError(errors)
        if CustomUser.objects.filter(username__iexact=username):
            errors['error'] = _('Username is taken!')
            raise serializers.ValidationError(errors)
        if password1 != password2:
            errors['error'] = _('The two password fields didn\'t match.')
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data['password1']
        user = CustomUser.objects.create_user(email=email, password=password, username=username)
        # print(f'This is user id {user.pkid}')
        print(user)
        return user

class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(label='Username', required=False)
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        if email:
            user = CustomUser.objects.filter(email__iexact=email).first()
            if user and user.check_password(password):
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError({'error': 'Invalid credentials'})
        else:
            user = CustomUser.objects.filter(username__iexact=username).first()
            if user and user.check_password(password):
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError({'error': 'Invalid credentials'})


    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')

