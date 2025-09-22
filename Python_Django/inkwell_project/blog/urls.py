from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)  # Like router.get('/posts', ...)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Includes all registered routes
]