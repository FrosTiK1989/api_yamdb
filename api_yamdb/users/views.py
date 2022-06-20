from random import randint

from django.core.mail import send_mail
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdministrator
from .models import User
from .serializers import (ApiLoginSerializer, RegisterUserSerializer,
                          UserListSerializer)


class RegisterUserView(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.AllowAny,)

    def post(self, *args, **kwargs):
        serializer = RegisterUserSerializer(data=self.request.data)
        if serializer.is_valid():
            confirmation_code = randint(0, 10000)
            User.objects.create_user(
                **serializer.validated_data,
                confirmation_code=confirmation_code
            )
            send_mail(
                'Ваш ключ для регистрации',
                f'Код: {confirmation_code}',
                'from@example.com',
                [serializer.validated_data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)


class LoginApiView(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.AllowAny,)

    def post(self, *args, **kwargs):
        serializer = ApiLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
            if user.confirmation_code != confirmation_code:
                return Response(status=HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            result = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(status=HTTP_200_OK, data=result)
        return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)


class UsersListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAdministrator,)
    pagination_class = LimitOffsetPagination
    page_size = 5
    lookup_field = 'username'
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserListSerializer(request.user, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = UserListSerializer(
            request.user,
            data=request.data,
            partial=True,
            many=False
        )
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
