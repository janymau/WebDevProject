from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    phoneNumber = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'age', 'phoneNumber']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        age = validated_data.get('age')
        phone = validated_data.get('phoneNumber')  # Используй phone, а не phoneNumber

        # Создаём пользователя
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Создаём участника
        Participant.objects.create(
            user=user,
            age=age,
            phoneNumber=phone  # Используй phone как здесь
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'age', 'phoneNumber', 'user']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'

class ListOfWaitingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfWaitingParticipant
        fields = ['id', 'event_id']
class EventTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventType
        fields = '__all__'
