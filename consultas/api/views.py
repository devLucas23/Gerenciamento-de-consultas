from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from consultas.api.serializers import ConsultaSerializer
from consultas.models import Consulta
from users.api.permissions import IsMedico


class ConsultaViewSet(ModelViewSet):
    """Class representing a person"""

    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAdminUser | IsMedico]

    @action(detail=False, methods=["get"], permission_classes=
            [IsAuthenticated])
    def listar_consultas(self, request):
        try:
            consultas = Consulta.objects.all()
            serializer = ConsultaSerializer(consultas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], permission_classes=
            [IsAuthenticated])
    def criar_consulta(self, request):
        serializer = ConsultaSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)  # Validação automática
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.
                            HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def detalhar_consulta(self, request, pk=None):
        try:
            consulta = self.get_object()
            serializer = ConsultaSerializer(consulta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Consulta.DoesNotExist:
            raise NotFound("Consulta não encontrada")

    @action(detail=True, methods=["put"], permission_classes=[IsAuthenticated])
    def atualizar_consulta(self, request, pk=None):
        try:
            consulta = self.get_object()
            serializer = ConsultaSerializer(consulta, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Consulta.DoesNotExist:
            raise NotFound("Consulta não encontrada")
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.
                            HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"], permission_classes=
            [IsAuthenticated])
    def deletar_consulta(self, request, pk=None):
        try:
            consulta = self.get_object()
            consulta.delete()
            return Response({"message": "Consulta removida com sucesso"}, 
                            status=status.HTTP_204_NO_CONTENT)
        except Consulta.DoesNotExist:
            raise NotFound("Consulta não encontrada")
        except Exception as e:
            return Response({"error": str(e)}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)