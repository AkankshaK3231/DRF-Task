from rest_framework import serializers
from .models import Post, Category
from rest_framework.validators import UniqueTogetherValidator

def validate_title_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError("Title cannot contain numbers.")
    return value

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class PostSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)  
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    title = serializers.CharField(max_length=200,validators=[validate_title_no_numbers])
    content = serializers.CharField()
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
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title', 'category'],
                message="Each category must have unique post titles."
            )
        ]
        
    def validate(self, data):
        title = data.get('title', '').lower()
        content = data.get('content', '').lower()
        if title in content:
            raise serializers.ValidationError("Title should not appear in content.")
        return data
    
    
