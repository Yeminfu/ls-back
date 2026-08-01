from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

class VolunteerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

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
        
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        nickname = validated_data.pop("nickname", None) or None

        user = User.objects.create_user(
            **validated_data,
            password=password,
            nickname=nickname,
        )

        volunteers_group = Group.objects.get(
            name="volunteers"
        )

        user.groups.add(volunteers_group)

        return user