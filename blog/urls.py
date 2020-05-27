from django.urls import path

from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<int:id>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<int:id>/result/', PostResult.as_view(), name='post_result_url'),
    path('post/<int:id>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<int:id>/delete/', PostDelete.as_view(), name='post_delete_url'),
]