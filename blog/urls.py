from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_activity

app_name = BlogConfig.name


urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', cache_page(60)(BlogListView.as_view()), name='list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
    path('active/<int:pk>', toggle_activity, name='toggle_activity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
