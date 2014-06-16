from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from api.authenticate import AuthUser

from api.permissions import IsJWTSelf, IsMemberManager, IsOwnerAndNotBanned, IsJWTAuthenticated
from core.models import Member
from api.serializers.serializers import MemberSerializer, MemberCreateSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """
    model = Member
    serializer_class = MemberSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MemberCreateSerializer
        return serializer_class

    def get_permissions(self):
        """
        An authenticated user can register itself as a new member of a community and list his memberships.
        Only a community owner or moderator can modify member status.
        Only a community owner can modify a member role.
        """
        if self.request.method == 'POST':
            return [IsJWTSelf()]
        elif self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsOwnerAndNotBanned()]
        else:
            return [IsMemberManager()]

    def list(self, request):
        """
        Overrides standard 'list' method to return only members belonging to user
        """
        user, _ = AuthUser().authenticate(request)
        queryset = Member.objects.filter(user=user.id)
        data = MemberSerializer(queryset)
        return Response(data.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Overrides standard 'create' method to avoid multiple identical members creation
        """
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            data = request.DATA
            if Member.objects.filter(user=data['user'], community=data['community']).exists():
                member = Member.objects.get(user=data['user'], community=data['community'])
                return Response(MemberSerializer(member).data, status=HTTP_200_OK)
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
