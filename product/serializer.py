from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from product.models import Product, Features, Category, ProductRating


class FeaturesSerializerForProduct(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'id')


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductRating
        fields = '__all__'


class FeaturesSerializer(serializers.ModelSerializer):
    key = serializers.CharField(validators=[UniqueValidator(queryset=Features.objects.all())])
    options = serializers.SerializerMethodField()

    class Meta:
        model = Features
        fields = ('key', 'options')

    def get_options(self, obj):
        return Features.objects.filter(
            product__category_id=self.context['view'].kwargs['category_id'],
            key=obj.get('key')
        ).values('value', 'id').distinct()


class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    features = FeaturesSerializerForProduct(many=True)
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


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.CharField()
    features = FeaturesSerializerForProduct(many=True)

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
