import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail



def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):  # 获取cookie,总阅读数加1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 +1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)  # created 创建的为true,获取的为false
        readDetail.read_num += 1
        readDetail.save()

    return key


def get_pre_sevenday_readdata(content_type):
    today = timezone.now().date()
    days = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        days.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)  # 得到前7天每天的阅读明细
        result = read_details.aggregate(read_num_sum=Sum('read_num'))               # 根据read_num 这个字段，用aggregate聚合函数，统计当天阅读的总数
        read_nums.append(result['read_num_sum'] or 0)
    return days, read_nums