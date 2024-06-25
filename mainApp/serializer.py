# serializers.py

from rest_framework import serializers

class LeadSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    # Add other fields as necessary
