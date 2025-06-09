from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from local_extentions.utils import jalali_converter
from .models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    jcreated_at: str = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_jcreated_at(self, obj: Reserve):
        if not hasattr(obj, "pk") or not obj.pk:
            return None
        return jalali_converter(obj.created_at)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = Reserve
        exclude = ("user",)
        read_only_fields = (
            "created_at",
            "jcreated_at",
            "is_delivered",
        )


class Today404OutputSerializer(serializers.Serializer):
    detail = serializers.CharField()
