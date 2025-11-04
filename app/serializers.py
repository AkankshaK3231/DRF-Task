from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class PostSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=200)
    content = serializers.CharField()

    category = CategorySerializer(read_only=True)  
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    author_email = serializers.EmailField()
    is_featured = serializers.BooleanField(default=False)
    rating = serializers.IntegerField(default=0)
    status = serializers.ChoiceField(choices=Post.STATUS_CHOICES, default='draft')
    created_at = serializers.ReadOnlyField()
   

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'category_id',
            'author_email', 'is_featured', 'rating', 'status',
            'created_at']
