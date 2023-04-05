from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
import base64
from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):
    # Поле зщыеы для вывода id постов принадлежащих группе
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    # Поле author для вывода username пользователя в комментарии
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('__all__')


class Base64ImageField(serializers.ImageField):
    """Класс для реализации передачи изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(
        many=True, required=False, read_only=True)
    group = serializers.SlugRelatedField(
        slug_field='id', queryset=Group.objects.all(), required=False)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('__all__')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('__all__')
        # Проверка UniqueConstraint на уровне сериализатора.
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        """Проверка чтобы нельзя было подписаться на себя."""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return data
