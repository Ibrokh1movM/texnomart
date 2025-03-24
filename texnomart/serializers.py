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
        return instance.likes.filter(id=user.id).exists()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'likes', 'title']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products']


class CommentSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name if hasattr(obj, 'product') and obj.product else None

    class Meta:
        model = Comment
        fields = ['id', 'message', 'user', 'product', 'created_at', 'image', 'bad_comment', 'good_comment', 'rating',
                  'product_name']
        read_only_fields = ['product_name', 'created_at']
