# serializers.py
from rest_framework import serializers
from .models import Category, Product, Image, Comment


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'product', 'image', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    title = serializers.CharField(source='category.name', read_only=True)
    def get_likes(self, instance):
        user = self.context['request'].user

        if not user.is_authenticated:
            return False

        if user not in instance.likes.all():
            return False

        return True

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

