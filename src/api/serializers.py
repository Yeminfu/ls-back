from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from mediafiles.models import MediaFile
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    nickname = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value

    def validate_nickname(self, value):
        value = value or None
        if value and User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError(
                "This nickname is already taken."
            )
        return value

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            nickname=validated_data.get("nickname") or None,
        )


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    is_active = serializers.BooleanField(required=False, default=True)
    nickname = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value

    def validate_nickname(self, value):
        value = value or None
        if value and User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError(
                "This nickname is already taken."
            )
        return value

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "password",
            "is_active",
        )

    def create(self, validated_data):
        is_active = validated_data.pop("is_active", True)
        return User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            is_active=is_active,
            nickname=validated_data.get("nickname") or None,
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "nickname",
        )

    def validate_nickname(self, value):
        value = value or None
        if value:
            qs = User.objects.filter(nickname=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "This nickname is already taken."
                )
        return value


User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "name")


class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "nickname",
            "avatar",
            "groups",
        )

    def get_avatar(self, obj):
        request = self.context.get("request")

        media = (
            MediaFile.objects
            .filter(
                links__entity_type="user_avatar",
                links__entity_id=obj.id,
            )
            .first()
        )

        if not media:
            return None

        if request:
            return request.build_absolute_uri(media.file.url)

        return media.file.url