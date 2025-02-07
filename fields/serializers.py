from rest_framework import serializers
from .models import Field
from users.models import User

class FieldSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    distance = serializers.FloatField(read_only=True, required=False) 
    
    class Meta:
        model = Field
        fields = ['id', 'name', 'lat', 'long', 'distance', 'owner']

    def create(self, validated_data):
        """
        Foydalanuvchi faylni yaratganda ownerni avtomatik ravishda 
        request.user bilan to'ldiramiz.
        Agar admin bo'lsa, ownerni qo'lda kiritishga ruxsat beramiz.
        """
        user = self.context['request'].user  # request'dan userni olish
        if user.role == 'admin' and 'owner' in validated_data:
            # Agar admin bo'lsa, ownerni qo'lda belgilash mumkin
            validated_data['owner'] = validated_data['owner']
        else:
            validated_data['owner'] = user  # Boshqa hollarda, ownerni avtomatik qo'shamiz
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Foydalanuvchi faylni yangilashda ham ownerni avtomatik qo'shish
        Agar admin bo'lsa, ownerni qo'lda o'zgartirishga ruxsat beramiz.
        """
        user = self.context['request'].user
        if user.role == 'admin' and 'owner' in validated_data:
            # Agar admin bo'lsa, ownerni qo'lda belgilash mumkin
            validated_data['owner'] = validated_data['owner']
        else:
            validated_data['owner'] = user  # Boshqa hollarda, ownerni avtomatik qo'shamiz
        return super().update(instance, validated_data)