from rest_framework import serializers
from users.models import Medico, UserProfileExample


class UserProfileExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileExample
        fields = ['id', 'address', 'phone_number', 'birth_date', 'user']


class MedicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico
        fields = "__all__"


class MedicoCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=140)
    crm = serializers.CharField(max_length=12)
    departamento = serializers.CharField(max_length=140)
    login = serializers.CharField(max_length=100)
    senha = serializers.CharField(max_length=100)
