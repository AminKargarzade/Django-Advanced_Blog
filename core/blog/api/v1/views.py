from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
import rest_framework.permissions
from rest_framework.response import Response
from .serializers import PostSerializer
from ...models import Post
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets

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

"""
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET","POST"])
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
        return Response(serializer.data)
        
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
        """
        
# @api_view()
# def postDetail(request, id):
#     try:
#         post = Post.objects.get(pk=id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     except Post.DoesNotExist:
#         return Response({"detail":"post does not exist"}, status=status.HTTP_404_NOT_FOUND)
#  You can do the same functionality with the way that I wrote down below!
        

'''class PostList(APIView):
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
        return Response(serializer.data)'''
        
class PostList(ListCreateAPIView):
    """getting a list of posts and creating new posts"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


'''
class PostDetail(APIView):
    """ getting detail of a post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    def get(self,request,id):
        """ retrieving the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    
    def put(self,request,id):
        """ editing the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        """ deleting a post """
        post = get_object_or_404(Post,pk=id,status=True)
        post.delete()
        return Response({"detail":"item removed successfully"}, status=status.HTTP_204_NO_CONTENT)
'''

class PostDetail(RetrieveUpdateDestroyAPIView):
    """ getting detail of a post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    
    
# Example for ViewSet in CBV
class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    
    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        post_object = get_object_or_404(self.queryset,pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)
    
    def create(self,request):
        pass
    
    def update(self,request,pk=None):
        pass
    
    def partial_update(self,request,pk=None):
        pass
    
    def destroy(self,request,pk=None):
        pass