from django.urls import path
from .views import NewsList, PostDetail, NewsSearch, PostAdd, PostEdit, PostDelete, PostCategory, subscribe_to_category, \
    CategoryList

subscribe_to_category(), CategoryList

app_name = 'news'
urlpatterns = [

    path('', NewsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search.html', NewsSearch.as_view()),
    path('add.html', PostAdd.as_view()),
    path('<int:pk>/edit', PostEdit.as_view()),
    path('<int:pk>/delete', PostDelete.as_view())
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>/', PostCategory.as_view()),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe')

]


