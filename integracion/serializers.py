from rest_framework import serializers


class CloudinaryImageSerializer(serializers.Serializer):
    public_id = serializers.CharField(max_length=255)
    url = serializers.URLField()
    created_at = serializers.DateTimeField()
    description = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)