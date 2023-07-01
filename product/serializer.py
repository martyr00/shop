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


class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    features = FeaturesSerializer(many=True)
    category = serializers.CharField()
    category_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "category",
            "category_id",
            "features",
        )


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductRating
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.CharField()
    features = FeaturesSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "text",
            "price",
            'category',
            'category_id',
            "description",
            "features",
            'rating',
        )

    def get_rating(self, obj):
        current_user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        print()
        return {
            'like_count': ProductRating.objects.filter(product=obj.id, grade=True).count(),
            'dislike_count': ProductRating.objects.filter(product=obj.id, grade=False).count(),
            'current_user_likes': bool(ProductRating.objects.filter(product=obj.id, grade=True, user=current_user)),
            'current_user_dislikes': bool(ProductRating.objects.filter(product=obj.id, grade=False, user=current_user)),
        }
