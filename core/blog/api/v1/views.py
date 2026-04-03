from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
import rest_framework.permissions
from rest_framework.response import Response
from .serializers import PostSerializer
from ...models import Post
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# @api_view(["GET","POST"])
# def postList(request):
#     if request.method == "GET":
#         posts = Post.objects.filter(status=True)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
# More compact of this code below

"""@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def postList(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""
        

class PostList(APIView):
    """getting a list of posts and creating new posts"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    def get(self,request):
        """retrieving a list of posts"""
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        """creating a post with provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
# @api_view()
# def postDetail(request, id):
#     try:
#         post = Post.objects.get(pk=id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     except Post.DoesNotExist:
#         return Response({"detail":"post does not exist"}, status=status.HTTP_404_NOT_FOUND)
#  You can do the same functionality with the way that I wrote down below!

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request, id):
    post = get_object_or_404(Post,pk=id,status=True)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail":"item removed successfully"}, status=status.HTTP_204_NO_CONTENT)