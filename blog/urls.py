from django.urls import path
from . import views
urlpatterns=[

    path('',views.blog_list,name='blog_list'), #首页点击博客后,显示的博客列表
    path('<int:blog_pk>',views.blog_detail,name="blog_detail"),      #博客详情,
    path('type/<int:blog_type_pk>',views.blogs_with_type,name="blogs_with_type"),   #博客类型
]