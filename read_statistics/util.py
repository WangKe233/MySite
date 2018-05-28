from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):  # 获取cookie,不存在的话,数量加1
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk):  # 根据ReadNum这个model,用blog过滤出相应的bLog
            # 存在记录,则根据blog获取那个对应的blog
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在记录,则创建blog
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    return key