from rest_framework import serializers

from product.models import Product, Features, Category, ProductRating, ProductImage


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
    key = serializers.CharField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Features
        fields = ('key', 'options')

    def get_options(self, obj):
        return Features.get_unique_features_value_by_keys(self.context['view'].kwargs['category_id'], obj.get('key'))


class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    features = FeaturesSerializerForProduct(many=True)
    category = serializers.CharField()
    category_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'category',
            'category_id',
            'features',
        )


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'image',
        )

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.CharField()
    features = FeaturesSerializerForProduct(many=True)
    media = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'text',
            'price',
            'category',
            'category_id',
            'description',
            'features',
            'media',
            'rating',
        )

    def get_media(self, obj):
        list_images_urls = list(ProductImage.get_all_images_urls_for_one_product(obj.id))
        return list(map(lambda image_url: '/media/' + str(image_url), list_images_urls))

    def get_rating(self, obj):
        rating_counters = {
            'like_count': ProductRating.get_count_rating_for_one_product(obj.id, True),
            'dislike_count': ProductRating.get_count_rating_for_one_product(obj.id, False),
        }

        current_user = self.context['request'].user if self.context['request'].user.is_authenticated else None

        current_user_rating_for_product = ProductRating.get_rating_from_user(obj.id, current_user)
        if current_user_rating_for_product:
            current_user_rating = 'like' if current_user_rating_for_product.grade else 'dislike'
            return {
                **rating_counters,
                'current_user_rating': current_user_rating
            }
        return {
            **rating_counters,
            'current_user_rating': None
        }
