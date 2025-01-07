import pytest
from rest_framework import status
from django.contrib.auth.models import User, Group
from users.models import Medico, UserProfileExample
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserProfileExampleViewSet:
    """Testa o ViewSet de UserProfileExample"""
    
    @pytest.fixture
    def user(self):
        """Criação de usuário para os testes"""
        return User.objects.create_user(username="testuser", password="password")

    @pytest.fixture
    def profile(self, user):
        """Criação de profile para os testes"""
        return UserProfileExample.objects.create(
            phone_number="1234567890",
            address="Rua Exemplo, 123",
            birth_date="1990-01-01",
            user=user
        )

    @pytest.fixture
    def client(self):
        """Criação do cliente de testes"""
        return APIClient()

    @pytest.mark.django_db
    def test_get_user_profiles(self, client):
        """Testa a listagem dos perfis de usuário."""
        response = client.get("/api/userprofiles/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    @pytest.mark.django_db
    def test_update_user_profile(self, client, profile):
        """Testa a atualização de um perfil de usuário."""
        updated_data = {
            "phone_number": "9876543210", 
            "address": "Rua Nova, 456", 
            "birth_date": "1991-02-02"
        }
        response = client.put(f"/api/userprofiles/{profile.id}/", {**updated_data, "user": profile.user.id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["phone_number"] == updated_data["phone_number"]


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
    def test_create_medico(self, client, user, medico_data):
        """Testa a criação de um novo médico."""
        client.login(username="medico_user", password="password")
        response = client.post("/api/medicos/", medico_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "Info" in response.data
        assert "Cadastro realizado!" in response.data["Info"]
        assert Medico.objects.count() == 1

    @pytest.mark.django_db
    def test_get_medicos(self, client, user):
        """Testa a listagem de médicos."""
        Medico.objects.create(
            nome="Dr. Ana Maria",
            crm="654321",
            departamento="Pediatria",
            user=user
        )
        response = client.get("/api/medicos/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    @pytest.mark.django_db
    def test_update_medico(self, client, user):
        """Testa a atualização dos dados de um médico."""
        medico = Medico.objects.create(
            nome="Dr. Pedro Alves",
            crm="789123",
            departamento="Dermatologia",
            user=user
        )
        updated_data = {
            "nome": "Dr. Pedro Augusto",
            "crm": "789123",
            "departamento": "Dermatologia"
        }
        response = client.put(f"/api/medicos/{medico.id}/", {**updated_data, "user": user.id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == updated_data["nome"]