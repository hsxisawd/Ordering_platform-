#自定义中间件类，（执行登录判断）
from  django.shortcuts import redirect
from  django.urls import  reverse
import re

class ShopMIddleware:
    def __init__(self,get_response):
        self.get_response=get_response

        print('ShopMIddleware')

    def __call__(self,request):
        path=request.path
        print(path)

        #判断管理后台是否登录
        #定义后台不登录也可以访问的URL列表
        urllist=["/myadmin/login","/myadmin/logout","/myadmin/dologin","/myadmin/verify"]
        #判断当前url是否是/myadmin开头
        if re.match('^/myadmin',path)and (path not in urllist):
            #判断是否登录
            if 'adminuser' not in request.session:

                #重定向到登录页
                return  redirect(reverse('myadmin_login'))

        #判断大堂点餐请求的判断，判断是否登录（session中是否有webuser）
        if re.match(r"^/web", path):
            # 判断当前用户是否没有登录
            if "webuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('web_login'))

        response = self.get_response(request)


        return response