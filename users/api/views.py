from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied,NotAuthenticated
import users.api.errors as ERRORS
from users.api.serializers import (MedicoCreateSerializer, MedicoSerializer,
                                   UserProfileExampleSerializer)
from users.models import Medico, UserProfileExample


class UserProfileExampleViewSet(ModelViewSet):
    """Class representing a person"""
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
# pylint: disable=E1101
    queryset = UserProfileExample.objects.all()
    http_method_names = ['get', 'put']


class MedicoViewSet(ModelViewSet):
    """Class representing a person"""
    serializer_class = MedicoSerializer
    permission_classes = [IsAdminUser]
# pylint: disable=E1101
    queryset = Medico.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = MedicoCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            novo_user = User.objects.create_user(
                username=serializer.validated_data['login'],
                password=serializer.validated_data['senha'],
            )
            grupo_medicos = Group.objects.get(name="Medicos")
            novo_user.groups.add(grupo_medicos)
# pylint: disable=E1101
            novo_medico = Medico.objects.create(
                nome=serializer.validated_data['nome'],
                crm=serializer.validated_data['crm'],
                departamento=serializer.validated_data['departamento'],
                user=novo_user
            )

            serializer_saida = MedicoSerializer(novo_medico)
            return Response(
                {"Info": "Cadastro realizado!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED)

        except ValueError:
            return Response(
                {"Erro": ERRORS.DADOS_INVALIDOS}, status=status.HTTP_409_CONFLICT
            )

        except KeyError:
            return Response(
                {"Erro": ERRORS.DADOS_FALTANDO},
                status=status.HTTP_400_BAD_REQUEST
            )

        except PermissionError:
            return Response(
                {"Erro": ERRORS.ERRO_DE_PERMISSOES},
                status=status.HTTP_403_FORBIDDEN
             )

        except PermissionDenied:
            return Response(
                {"Error": ERRORS.PERMISSAO_NEGADA},
                status=status.HTTP_403_FORBIDDEN
            )

        except NotAuthenticated:
            return Response(
                {"Error": ERRORS.NAO_AUTORIZADO},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except ImportError as e:
            return Response({"error": str(e)}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)
