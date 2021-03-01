from rest_framework import authentication, generics, permissions
from rest_framework.response import Response

from core import models, serializers


class SiteCrtCreate(generics.CreateAPIView):
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SiteCrtCreate
    queryset = models.SiteCrt.objects.all()


class SiteCrtList(generics.ListAPIView):
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SiteCrtList
    queryset = models.SiteCrt.objects.all()
    filter_fields = ("cn",)


class SiteCrt(generics.ListCreateAPIView):
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SiteCrt
    queryset = models.SiteCrt.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.get_or_create()

        return Response({"crt": instance.crt, "key": instance.key})
