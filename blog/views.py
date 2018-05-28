
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import  Paginator
from django.conf import settings
from django.db.models import Count
# Create your views here.
from .models import Blog, BlogType
from read_statistics.util import read_statistics_once_read


def blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_BLOGS_PAGE_NUM)  # 每2页进行分页
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

    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    '''
    获取博客分类的对应博客数量,因为统计各类型的博客数量,
    blog_type关联Blog对象,所以Count()中的字符串也可以为Blog对象的小写
    '''
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return  context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_list_common_data(request,blogs_all_list)
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request , blog_type_pk):

    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return  render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)  #自定义过滤器
    context = blog_list_common_data(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog,pk= blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() #根据创建时间筛选,获取早于该博客的所有,然后拿到最后一个,即为上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()    #同上,获取下一条博客内容
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')#将看过的文章ID存储到cookie中,未设置过期时间,默认为退出浏览器该cookie过期
    return response