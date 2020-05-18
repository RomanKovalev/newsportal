from django.urls import path

from .views import PostsListView, PostCreateView, PostDetailView, CommentCreateView, DashboardView, ChangePostStatusView, ChangePremoderationModeView

urlpatterns = [
    path('', PostsListView.as_view(), name='post-list'),
    path('post/create', PostCreateView.as_view(), name='post-add'),
    path('post/<pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<post_pk>/add', CommentCreateView.as_view(), name='comment-add'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/statuschange/<pk>/<status>', ChangePostStatusView.as_view(), name='dashboard-status-change'),
    path('dashboard/statuschange/<pk>/', ChangePremoderationModeView.as_view(), name='dashboard-premod-change'),
    
]
