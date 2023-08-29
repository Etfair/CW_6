from django.urls import path

from mailing.views import MailListView, MailCreateView, MailUpdateView, MailDeleteView, MailDetailView, \
    main, MailingCreateView, MailingListView

urlpatterns = [
    path('main/', main, name='main'),
    path('', MailListView.as_view(), name='mail'),
    path('create/', MailCreateView.as_view(), name='create_mail'),
    path('update/<int:pk>/', MailUpdateView.as_view(), name='update_mail'),
    path('delete/<int:pk>/', MailDeleteView.as_view(), name='delete_mail'),
    path('view/<int:pk>/', MailDetailView.as_view(), name='view_mail'),
    path('creating/', MailingCreateView.as_view(), name='create'),
    path('mailing/', MailingListView.as_view(), name='list'),
]
