from rest_framework import serializers
from ...models import Category, Post

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField()
    # content = serializers.CharField(read_only=True)
    class Meta:
        model = Post
        fields = ['id','author','title','content','category','status','created_date','published_date']
        read_only_fields = ['content']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']