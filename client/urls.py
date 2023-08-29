from django.urls import path

from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientDetailView, ClientDeleteView, ClientUpdateView

app_name = 'client'

urlpatterns = [
    path('', ClientListView.as_view(), name='client'),
    path('create/', ClientCreateView.as_view(), name='create_client'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
]
