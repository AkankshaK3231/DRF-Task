from django.shortcuts import render
from rest_framework import viewsets, permissions,  generics,  filters
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from rest_framework.authentication import TokenAuthentication , SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
@method_decorator(cache_page(60*5), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')  
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'categories'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle, ScopedRateThrottle]
    throttle_scope = 'posts'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author_email']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Post.objects.all()
        elif user.is_authenticated:
            return Post.objects.filter(created_by=user)
        else:
            return Post.objects.none()
        
    @method_decorator(cache_page(60*5)) 
    @method_decorator(vary_on_cookie, name='list')
    @method_decorator(vary_on_headers('Authorization'), name='list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
