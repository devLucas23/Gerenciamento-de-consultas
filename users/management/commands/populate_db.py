from django.core.management.base import BaseCommand
from users.api.factories import MedicoFactory, UserProfileExampleFactory


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios'

    def handle(self, *args, **kwargs):
        # Criar 10 médicos
        self.stdout.write("Criando médicos...")
        MedicoFactory.create_batch(10)

        # Criar 15 perfis de usuário
        self.stdout.write("Criando perfis de usuários...")
        UserProfileExampleFactory.create_batch(15)

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))