from PIL.Image import Image
import django
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from api.permissions.common import IsJWTAuthenticated
from django.views.static import serve


class MediaViewSet(viewsets.ViewSet):
    """ Default permission: Any """
    permission_classes = AllowAny

    @action(methods=['GET', ])
    def get_media(request, path, document_root=None):
        """ Get media:

                | **permission**: authenticated
                | **endpoint**: /media/path/
                | **method**: GET
                | **http return**:
                |       - 200 OK
                |       - 404 Not allowed
                | **data return**:
                |       - bytecode

        """
        #response = HttpResponse()
        #image = Image.open(path)
        #image.save(response, 'PNG')
        #return response
        return serve(request, path, document_root)
