from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface
    path('api/blog/', include('blog.urls')),  # Like app.use('/api/blog', blogRoutes)
    path('api/users/', include('users.urls')),  # Like app.use('/api/users', userRoutes)
    path('', views.api_root, name='api-root'),  # Add root endpoint
]