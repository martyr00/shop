from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .serializer import UserSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)