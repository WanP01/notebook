import re

from django.core.cache import cache, caches
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class visitlimit(MiddlewareMixin):

    #可以用类属性存访问值，缺点是必须关闭才能释放
    #visit_time={}

    #如果用缓存(session/COOKIES也行，只是一般存的时间不宜过长)可以好一点，可以规定存储的时间
    visit_time = caches['default']

    def process_request(self,request):

        #获取访问的IP地址和访问的path
        ip_address = request.META['REMOTE_ADDR']
        path_url = request.path_info

        #正则匹配
        if not re.match('^/note/all',path_url):
            return

        #下面是类属性的计数方法
        # times = self.visit_time.get('ip_address',0)
        #self.visit_time['ip_address'] = times + 1

        #通过内存来限制访问次数（这里定义的是10秒内不能访问过多）
        times = self.visit_time.get('ip_address',0)
        self.visit_time.set('ip_address',times+1,10)


        if self.visit_time.get('ip_address',0)>5:
            return HttpResponse('你短时间访问过多次了')
        return
