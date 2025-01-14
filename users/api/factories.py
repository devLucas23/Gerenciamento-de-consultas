import factory
from django.contrib.auth.models import User
from users.models import Medico, UserProfileExample
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory para criar usuários."""
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'senha123')


class MedicoFactory(factory.django.DjangoModelFactory):
    """Factory para criar médicos."""
    class Meta:
        model = Medico

    nome = factory.Faker("name")
    crm = factory.Faker("bothify", text="#####")
    departamento = factory.Faker("word")
    user = factory.SubFactory(UserFactory)


class UserProfileExampleFactory(factory.django.DjangoModelFactory):
    """Factory para criar exemplos de perfis de usuário."""
    class Meta:
        model = UserProfileExample

    nome_completo = factory.Faker("name")
    idade = factory.Faker("random_int", min=18, max=60)
    endereco = factory.Faker("address")