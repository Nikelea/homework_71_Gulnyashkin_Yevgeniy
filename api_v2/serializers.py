from rest_framework import serializers
from publications.models import Publication
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['__all__', ]


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        exclude = ['password', ]


class PubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = ['id', 'description', 'image', 'user', 'likes', ]
        read_only_fields = ['id']
