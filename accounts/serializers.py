from .models import User, Address
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # آپدیت بقیه فیلدها
        instance = super().update(instance, validated_data)

        # اگر پسورد وجود داشت، هش کن
        if password:
            instance.set_password(password)
            instance.save()

        return instance


