from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from datetime import datetime, timezone as dt_timezone

class CustomJWTAuthentication(JWTAuthentication):
    print("🔥 CustomJWTAuthentication called!")
    def get_user(self, validated_token):
        print("🔥 CustomJWTAuthentication.get_user called!")
        user = super().get_user(validated_token)
        pwd_changed = getattr(user.profile, 'password_changed_at', None)

        token_iat = validated_token.get("iat")
        if token_iat is not None and pwd_changed is not None:
            token_time = datetime.fromtimestamp(token_iat, dt_timezone.utc)
            if pwd_changed > token_time:
                raise AuthenticationFailed("Token is no longer valid. Password has been changed.")
        print("token_iat:", token_iat)
        print("token_time:", token_time)
        print("pwd_changed:", pwd_changed)
        print("pwd_changed > token_time?", pwd_changed > token_time)

        return user
