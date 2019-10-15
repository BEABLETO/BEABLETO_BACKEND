from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from information.serializers import LocationSerializer
from information.models import Location
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.http import QueryDict


class LocationSaveView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # query_dict = QueryDict('', mutable=True)
        # query_dict.update(request.data)
        # query_dict.appendlist('user', request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'Message': 'Saved'}, status=status.HTTP_201_CREATED, headers=headers)

