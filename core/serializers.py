import datetime
from django.conf import settings
from rest_framework import serializers

from core import models
from core.utils import Ca


class SiteCrtCreate(serializers.ModelSerializer):
    validity_period = serializers.DateField()

    class Meta:
        model = models.SiteCrt
        fields = ["cn", "validity_period"]

    def save(self):
        ca = Ca()
        if ca.get_type_alt_names(self.validated_data["cn"]):
            ca.generate_site_crt(
                self.validated_data["cn"],
                self.validated_data["validity_period"],
                alt_name="IP",
            )
        else:
            ca.generate_site_crt(
                self.validated_data["cn"], self.validated_data["validity_period"]
            )


class SiteCrtList(serializers.ModelSerializer):
    crt = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    class Meta:
        model = models.SiteCrt
        fields = ["cn", "crt", "key"]

    @staticmethod
    def get_crt(obj):
        return obj.crt

    @staticmethod
    def get_key(obj):
        return obj.key


class SiteCrt(serializers.Serializer):
    cn = serializers.CharField()

    def get_or_create(self):
        instance = models.SiteCrt.objects.filter(cn=self.validated_data["cn"])
        if not instance:
            validity_period = (
                datetime.datetime.now() + datetime.timedelta(days=settings.VALIDITY_PERIOD_CRT)
            ).date()
            ca = Ca()
            if ca.get_type_alt_names(self.validated_data["cn"]):
                instance = ca.generate_site_crt(
                    self.validated_data["cn"], validity_period, alt_name="IP"
                )
            else:
                instance = ca.generate_site_crt(
                    self.validated_data["cn"], validity_period
                )
        else:
            instance = instance.first()

        return instance
