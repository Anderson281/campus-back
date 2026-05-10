from rest_framework import serializers
from django.contrib.auth import get_user_model

from djangoapi.settings import DJANGO_SUPERUSER_USERNAME

class BaseUserSerializer(serializers.Serializer):
    def get_creator_user(self):
        request = self.context.get('request')
        
        # self.instance es el objeto de la DB. 
        # Si existe, estamos en un UPDATE (PUT/PATCH).
        # Si es None, estamos en un CREATE (POST).
        if self.instance is None:
            if request and request.user.is_authenticated:
                return request.user
            else:
                return get_user_model().objects.all().get(username=DJANGO_SUPERUSER_USERNAME)
        else:
            # En un PUT/PATCH, nos aseguramos de que el campo 'user' 
            # no se altere o mantenga el valor que ya tenía el objeto.
            return self.instance.user
            
    