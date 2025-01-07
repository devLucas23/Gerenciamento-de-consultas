import logging
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.views import Response
from .models import Medico, Consulta, UserProfile
from django.test import TestCase

logger = logging.getLogger("consultas")

class ConsultaViewSetTest(TestCase):
    """Testes para o ViewSet de Consulta"""
    def setUp(self):
        self.client = APIClient()
        self.medico = Medico.objects.create(nome="Dr. Teste", especialidade="Cardiologia")
        self.user_profile = UserProfile.objects.create(nome="Usuário Teste", email="teste@exemplo.com")
        self.consulta_data = {
            "medico": self.medico.id,
            "data": "2025-01-10T10:00:00Z"
        }

    def test_criar_consulta(self):
        """Teste para criação de consulta"""
        response = self.client.post("/api/consultas/criar_consulta/", self.consulta_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consulta.objects.count(), 1)

    def test_listar_consultas(self):
        """Teste para listagem de consultas"""
        Consulta.objects.create(medico=self.medico, data="2025-01-10T10:00:00Z")
        response = self.client.get("/api/consultas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_consulta(self):
        """Teste para atualização de consulta"""
        consulta = Consulta.objects.create(medico=self.medico, data="2025-01-10T10:00:00Z")
        updated_data = {"medico": self.medico.id, "data": "2025-02-10T10:00:00Z"}
        response = self.client.put(f"/api/consultas/{consulta.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        consulta.refresh_from_db()
        self.assertEqual(consulta.data, "2025-02-10T10:00:00Z")

    def test_delete_consulta(self):
        """Teste para exclusão de consulta"""
        consulta = Consulta.objects.create(medico=self.medico, data="2025-01-10T10:00:00Z")
        response = self.client.delete(f"/api/consultas/{consulta.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consulta.objects.count(), 0)

class MedicoViewSetTest(TestCase):
    """Testes para o ViewSet de Medico"""
    def setUp(self):
        self.client = APIClient()
        self.medico = Medico.objects.create(nome="Dr. Teste", especialidade="Cardiologia")

    def test_criar_medico(self):
        """Teste para criação de medico"""
        medico_data = {"nome": "Dr. Novo", "especialidade": "Pediatria"}
        response = self.client.post("/api/medicos/", medico_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medico.objects.count(), 2)

    def test_update_medico(self):
        """Teste para atualização de medico"""
        updated_data = {"nome": "Dr. Atualizado", "especialidade": "Neurologia"}
        response = self.client.put(f"/api/medicos/{self.medico.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medico.refresh_from_db()
        self.assertEqual(self.medico.nome, "Dr. Atualizado")

    def test_get_medicos(self):
        """Teste para obtenção de todos os médicos"""
        response = self.client.get("/api/medicos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

class UserProfileViewSetTest(TestCase):
    """Testes para o ViewSet de UserProfile"""
    def setUp(self):
        self.client = APIClient()
        self.user_profile = UserProfile.objects.create(nome="Usuário Teste", email="teste@exemplo.com")

    def test_update_user_profile(self):
        """Teste para atualização de perfil de usuário"""
        updated_data = {"nome": "Usuário Atualizado", "email": "atualizado@exemplo.com"}
        response = self.client.put(f"/api/usuarios/{self.user_profile.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.nome, "Usuário Atualizado")
