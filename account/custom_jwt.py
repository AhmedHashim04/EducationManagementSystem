from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from datetime import datetime, timezone as dt_timezone

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        pwd_changed = user.profile.password_changed_at

        token_iat = validated_token.get("iat")

        if token_iat is not None:
            token_time = datetime.fromtimestamp(token_iat, dt_timezone.utc)
            if pwd_changed and pwd_changed > token_time:
                raise AuthenticationFailed("Token is no longer valid. Password has been changed.")

        return user
