from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = [
            'username',
            'full_name',
            'preferred_name',
            'email',
            'date_joined',
        ]
        read_only_fields = fields
