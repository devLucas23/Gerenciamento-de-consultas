import pytest
from rest_framework import status
from django.contrib.auth.models import User, Group
from users.models import Medico
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestMedicoViewSet:
    """Testa o ViewSet de Medico"""
    
    @pytest.fixture
    def user(self):
        """Criação de usuário para os testes"""
        return User.objects.create_user(username="medico_user", password="password")

    @pytest.fixture
    def group(self):
        """Criação de grupo 'Medicos'"""
        return Group.objects.create(name="Medicos")
    
    @pytest.fixture
    def medico_data(self):
        """Dados para criação de um médico"""
        return {
            "nome": "Dr. João Silva",
            "crm": "123456",
            "departamento": "Cardiologia",
            "login": "joaosilva",
            "senha": "securepassword123"
        }

    @pytest.fixture
    def client(self):
        """Criação do cliente de testes"""
        return APIClient()

    @pytest.mark.django_db
    def test_get_medicos(self, client, user):
        """Testa a listagem de médicos."""
        # Criação de um médico no banco de dados
        Medico.objects.create(
            nome="Dr. Ana Maria",
            crm="654321",
            departamento="Pediatria",
            user=user
        )

        # Realizando a requisição GET para listar médicos
        response = client.get("/api/medicos/")
        
        # Verificando se a resposta foi bem-sucedida
        assert response.status_code == status.HTTP_200_OK
        
        # Verificando se ao menos um médico é retornado
        assert len(response.data) >= 1
        
        # Verificando se o médico criado está presente na lista
        assert any(medico["nome"] == "Dr. Ana Maria" for medico in response.data)