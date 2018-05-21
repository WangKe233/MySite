from django.core import paginator
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import  Paginator
# Create your views here.
from blog.models import Blog,BlogType


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,10)  # 每10页进行分页
    page_num = request.GET.get('page',1)   #拿到GET请求的page,默认显示第一页,这里设置的首页显示前10条
    page_of_blogs = paginator.get_page(page_num)  #得到第几页的博客列表 ,

    context = {}
    # context['blogs'] =page_of_blogs.object_list
    context['page_of_blogs'] =page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)




def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk= blog_pk)

    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_types'] = BlogType.objects.all()
    return  render_to_response('blog/blogs_with_type.html', context)