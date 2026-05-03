from rest_framework import serializers
from ...models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords Does NOT Match!"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)  # type: ignore


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:  # type: ignore
                raise serializers.ValidationError(
                    {"detail": "User is not verified! :("}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:  # type: ignore
            raise serializers.ValidationError({"detail": "User is not verified! :("})
        validated_data["email"] = self.user.email  # type: ignore
        validated_data["user_id"] = self.user.id  # type: ignore
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Passwords Does NOT Match!"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "description",
        )


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User does not exist!"})
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is already activated and verified!"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        user_obj = User.objects.get(email=email)
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")

        # Check Password match!
        if password != password1:
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        # Validate password strength (Django validators)
        validate_password(password)

        # Get uid & token from context
        uid = self.context.get("uid")
        token = self.context.get("token")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))  # type: ignore
            user = User.objects.get(id=user_id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid UID"})

        # Check token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Token is invalid or expired"})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get("password")  # type: ignore
        user = self.validated_data.get("user")  # type: ignore

        user.set_password(password)  # type: ignore
        user.save()  # type: ignore

        return user
