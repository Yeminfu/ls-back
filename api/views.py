from django.contrib.auth.models import User
from rest_framework import serializers, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Article
from api.serializers import ArticleSerializer


# Create your views here.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        article = self.get_object()
        article.disabled = True
        article.save()
        return Response({'status': 'disabled'})

    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        article = self.get_object()
        article.disabled = False
        article.save()
        return Response({'status': 'enabled'})
