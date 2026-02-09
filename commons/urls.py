from django.urls import path
from commons.views import (
    ContactListView,
    ContactDetailView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView
)

app_name = 'commons'

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/update/', ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
]

