from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Parol hash qilinadi
        else:
            raise serializers.ValidationError({"password": "Parol kiritilishi shart."})
        user.save()
        return user


