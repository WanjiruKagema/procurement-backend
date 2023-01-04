from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from authentication.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


# Create your views here.

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)

        # Generate tokens for existing users
        for user in User.objects.all():
            if not user:
                break
            else:
                try:
                    Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    Token.objects.create(user=user)

        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            token = Token.objects.create(user=user)

            groups = ', '.join(map(str, user.groups.all()))

            # print(user.get_user_permissions())
            return Response(
                {
                    "user": {
                        "id": user_serializer.data["id"],
                        "first_name": user_serializer.data["first_name"],
                        "last_name": user_serializer.data["last_name"],
                        "email": user_serializer.data["email"],
                    },
                    "status": status.HTTP_200_OK,
                    "token": token.key,
                    'permissions': {},
                    'Groups': groups
                }
            )
        return Response(
            {
                "error": user_serializer.errors,
                "status": f"{status.HTTP_203_NON_AUTHORITATIVE_INFORMATION}",
            }
        )


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_permissions = []
        if user.is_staff:
            user_permissions.append('staff')
        if user.is_head_department:
            user_permissions.append('head_of_department')
        if user.is_procurement_officer:
            user_permissions.append('procurement_officer')
        if user.is_head_of_finance:
            user_permissions.append('head_of_finance')
        if user.is_procurement_committee:
            user_permissions.append('procurement_committee')
        if user.is_ceo:
            user_permissions.append('is_ceo')

        return Response({
            'user': {
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "status": status.HTTP_200_OK,
            'token': token.key,
            'permissions': user_permissions
        })


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "{} Logged out successfully".format(request.user.username)}, status=status.HTTP_200_OK)
