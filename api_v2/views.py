from urllib import request
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from api_v2.serializers import PubSerializer
from publications.models import Publication
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.permissions import SAFE_METHODS



class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user


class PubViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PubSerializer
    permission_classes = [ ]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated] 
        elif self.action == 'like_it':
            permission_classes = [IsAuthenticated] 
        else:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]
    
    def like_it(self, *args, **kwargs):
        publication = get_object_or_404(Publication, id=kwargs.get('pk'))
        comments = publication.comments_counter
        if self.request.user in publication.likes.all():
            publication.likes.remove(self.request.user)
            result = False
            publication.likes_counter = publication.likes.count()
        else:
            publication.likes.add(self.request.user)
            result = True
            publication.likes_counter = publication.likes.count()
            
        publication.save()
        return Response({'status': 'ok', 'result': result, 'count': publication.likes_counter, 'comment': comments})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class PubListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Publication.objects.all()
        serializer = PubSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PubSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class PubDetailView(APIView):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Publication, pk=kwargs.get('pk'))
        serializer = PubSerializer(object)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        object = get_object_or_404(Publication, pk=kwargs.get('pk'))
        serializer = PubSerializer(object, data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(Publication, pk=kwargs.get('pk'))
        object.delete()
        return Response({'deleted': kwargs.get('pk') })
