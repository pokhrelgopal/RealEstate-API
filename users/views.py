from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from .models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        User can only view all users if they are superuser.
        endpoint [GET] : http://127.0.0.1:8000/api/v1/user/
        """
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        """
        User can only view their own data. But superuser can view any user.
        endpoint [GET] : http://127.0.0.1:8000/api/v1/user/:id/
        """
        user = self.get_object()
        if request.user.is_banned:
            return Response(
                {"detail": "User is banned"}, status=status.HTTP_403_FORBIDDEN
            )

        if request.user.is_superuser or request.user == user:
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """
        User can only update their own data. But superuser can update any user.

        If user is not superuser, they cannot modify is_suspended and is_banned fields.

        endpoint [PATCH] : http://127.0.0.1:8000/api/v1/user/:id/
        """
        user = self.get_object()
        if not request.user.is_superuser:
            if "is_suspended" in request.data or "is_banned" in request.data:
                raise PermissionDenied(
                    "You do not have permission to modify these fields."
                )
        if request.user.is_superuser or request.user == user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """
        User can only delete their own data. But superuser can delete any user.

        endpoint [DELETE] : http://127.0.0.1:8000/api/v1/user/:id/
        """
        user = self.get_object()
        if request.user.is_superuser or request.user == user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=["GET"])
    def get_user_by_email(self, request):
        """
        Find a user by email
        endpoint [GET] : http://127.0.0.1:8000/api/v1/user/get_user_by_email/?email=johndoe@gmail.com
        """
        email = request.query_params.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            return Response(UserSerializer(user).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["GET"])
    def get_user(self, request):
        """
        Get the current user
        endpoint [GET] : http://127.0.0.1:8000/api/v1/user/get_user
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(request.user).data)

    def get_permissions(self):
        """
        If user is trying to list or create a user, no authentication is required.
        For all other actions, user must be authenticated.
        """
        if self.action == "list" or self.action == "create":
            self.permission_classes = []

        return super().get_permissions()
