from django.contrib.auth.models import Group, User
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Medico, UserProfileExample


class UserProfileExampleViewSetTests(APITestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criação de usuário para os testes
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = UserProfileExample.objects.create(
            phone_number="1234567890",
            address="Rua Exemplo, 123",
            birth_date="1990-01-01",
            user=self.user
        )
        self.profile_url = f"/api/userprofiles/{self.profile.id}/"

    def test_get_user_profiles(self):
        """Testa a listagem dos perfis de usuário."""
        response = self.client.get("/api/userprofiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_user_profile(self):
        """Testa a atualização de um perfil de usuário."""
        updated_data = {
            "phone_number": "9876543210", 
            "address": "Rua Nova, 456", 
            "birth_date": "1991-02-02"
        }
        response = self.client.put(self.profile_url, {**updated_data, "user": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], updated_data["phone_number"])
        self.assertEqual(response.data["address"], updated_data["address"])


class MedicoViewSetTests(APITestCase):
    def setUp(self):
        """Configuração inicial para os testes de Médico"""
        # Criação de grupo e usuário para os testes
        self.group = Group.objects.create(name="Medicos")
        self.user = User.objects.create_user(username="medico_user", password="password")
        self.user.groups.add(self.group)

        self.medico_data = {
            "nome": "Dr. João Silva",
            "crm": "123456",
            "departamento": "Cardiologia",
            "login": "joaosilva",
            "senha": "securepassword123"
        }

        self.client.login(username="medico_user", password="password")

    def test_create_medico(self):
        """Testa a criação de um novo médico."""
        response = self.client.post("/api/medicos/", self.medico_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Info", response.data)
        self.assertIn("Cadastro realizado!", response.data["Info"])
        self.assertEqual(Medico.objects.count(), 1)

    def test_get_medicos(self):
        """Testa a listagem de médicos."""
        Medico.objects.create(
            nome="Dr. Ana Maria",
            crm="654321",
            departamento="Pediatria",
            user=self.user
        )
        response = self.client.get("/api/medicos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_medico(self):
        """Testa a atualização dos dados de um médico."""
        medico = Medico.objects.create(
            nome="Dr. Pedro Alves",
            crm="789123",
            departamento="Dermatologia",
            user=self.user
        )
        updated_data = {
            "nome": "Dr. Pedro Augusto",
            "crm": "789123",
            "departamento": "Dermatologia"
        }
        response = self.client.put(f"/api/medicos/{medico.id}/", {**updated_data, "user": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], updated_data["nome"])
        self.assertEqual(response.data["departamento"], updated_data["departamento"])