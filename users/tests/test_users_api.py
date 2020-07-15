from django.contrib.auth import get_user_model

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only':True, 'min-length':5}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email']
                name=validated_data['name']

            )
            user.set_password(validated_data['password'])
            user.save()
            return user
