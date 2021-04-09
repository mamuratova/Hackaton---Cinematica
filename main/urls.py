
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('genre/<str:slug>/', category_detail, name='category'),
    path('film_detail/<int:pk>/', film_detail, name='detail'),
    path('add_new_film/', create, name='create'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('search/', SearchListView.as_view(), name='search'),
    path('film_detail/<int:pk>/comment', leave_comment, name='leave_comment'),
    path('news/', main, name='parse_news'),
    path('watch/<int:pk>/', watch, name='watch')
]