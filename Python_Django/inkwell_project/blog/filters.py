import django_filters
from .models import Post
from django.contrib.auth.models import User

class PostFilter(django_filters.FilterSet):
    # Basic filters
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='exact')
    
    # Date range filtering (like createdAfter/createdBefore)
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    # Boolean filters (like has_comments)
    has_comments = django_filters.BooleanFilter(method='filter_has_comments')
    
    def filter_has_comments(self, queryset, name, value):
        if value:
            return queryset.filter(comments__isnull=False).distinct()
        return queryset.filter(comments__isnull=True)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'created_at']