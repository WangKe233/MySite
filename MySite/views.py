from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_pre_sevenday_readdata
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    days, read_nums = get_pre_sevenday_readdata(blog_content_type)

    context = {}
    context['days'] = days
    context['read_nums'] = read_nums
    return render_to_response('home.html',context)