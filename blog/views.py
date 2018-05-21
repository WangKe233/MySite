from django.core import paginator
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import  Paginator
from django.conf import settings
# Create your views here.
from blog.models import Blog,BlogType



def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,settings.EACH_BLOGS_PAGE_NUM)  # 每2页进行分页
    page_num = request.GET.get('page',1)   #拿到GET请求的page,默认显示第一页,这里设置的首页显示前10条
    page_of_blogs = paginator.get_page(page_num)  #得到第几页的博客列表 ,
    current_num = page_of_blogs.number          #当前博客为第几页
    max_page = paginator.num_pages
    #获取当前页码的前后两页
    page_range =list(range(max(current_num-2,1),current_num))+ list(range(current_num,min(current_num+2,paginator.num_pages)+1))

    #加上省略号标志
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')

    #加上首页和尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['blogs'] =page_of_blogs.object_list
    context['page_of_blogs'] =page_of_blogs
    context['page_range'] =page_range
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)




def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk= blog_pk)
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, settings.EACH_BLOGS_PAGE_NUM)  # 每10页进行分页
    page_num = request.GET.get('page', 1)  # 拿到GET请求的page,默认显示第一页,这里设置的首页显示前10条
    page_of_blogs = paginator.get_page(page_num)  # 得到第几页的博客列表 ,
    current_num = page_of_blogs.number  # 当前博客为第几页
    max_page = paginator.num_pages
    # 获取当前页码的前后两页
    page_range = list(range(max(current_num - 2, 1), current_num)) + list(
        range(current_num, min(current_num + 2, paginator.num_pages) + 1))

    # 加上省略号标志
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()





    return  render_to_response('blog/blogs_with_type.html', context)