from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.organization.api.serializers import OrganizationSerializer
from apps.events.models import Organization

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def create(self, request, *args, **kwargs):
        # Adicione lógica para associar o evento à organização atualmente logada
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Associe o evento à organização atualmente logada
            serializer.validated_data['organization'] = request.user.organization  
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
