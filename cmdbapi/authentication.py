from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header
from cmdbapi.exception import AuthException

class TokenBaseAuthentication(TokenAuthentication):

    token_is_null = "TOKEN为空"
    token_is_error = "TOKEN错误"
    user_is_not_active = "用户已锁"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise AuthException(detail=self.token_is_null)
        if len(auth) == 1:
            raise AuthException(detail=self.token_is_null)
        elif len(auth) > 2:
            raise AuthException(detail=self.token_is_error)
        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthException(detail=self.token_is_error)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthException(detail=self.token_is_error)
        if not token.user.is_active:
            raise AuthException(detail=self.user_is_not_active)
        return (token.user, token)
