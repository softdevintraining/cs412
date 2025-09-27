# blog/urls.py
from django.urls import path
from .views import * #ShowAllView, ArticleView, RandomArticleView

# URL patterns for this app:
urlpatterns = [
    path('', RandomArticleView.as_view(), name=""),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
]