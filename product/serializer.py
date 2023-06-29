from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from product.models import Product, Features, Category, ProductRating


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    features = serializers.ManyRelatedField(child_relation=FeaturesSerializer())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "text",
            "price",
            "description",
            "category",
            "features",
            'rating'
        )

    def get_rating(self, obj):
        current_user = self.context['request'].user if self.context['request'].user == AnonymousUser else None
        return {
            'like_count': ProductRating.objects.filter(product=obj.id, grade=True).count(),
            'dislike_count': ProductRating.objects.filter(product=obj.id, grade=False).count(),
            'current_user_likes': bool(ProductRating.objects.filter(product=obj.id, grade=True, user=current_user)),
            'current_user_dislikes': bool(ProductRating.objects.filter(product=obj.id, grade=False, user=current_user)),
        }
