from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from myadmin.models import User


# 后台首页
def index(request):
    return render(request, 'myadmin/index/index.html')


# 管理员登录表单
def login(request):
    return render(request, 'myadmin/index/login.html')


# 执行管理员登录
def dologin(request):
    global context
    try:
        #验证码校验
        if request.POST['code'] != request.session['verifycode']:
            context = {'info': '验证码错误！'}
            return render(request, 'myadmin/index/login.html', context)
        # 根据登录账号获取登录者信息
        user = User.objects.get(username=request.POST['username'])
        # 判断当前用户是不是管理员
        if user.status == 6:
            import hashlib,random
            md5=hashlib.md5()
            s=request.POST.get('pass')+str(user.password_salt)#从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8'))#将要产生md5的子串放进去
            if user.password_hash ==md5.hexdigest():#密码判断
                #把用户信息写入session
                request.session['adminuser']=user.toDict()
                #重定向到管理员首页
                return  redirect(reverse('myadmin_index'))
            else:
                context = {'info': '账号或者密码错误！'}
        else:
            context = {'info': '不是管理员账号！'}

    except Exception as err:
        print(err)
        context = {'info': '登录账号不存在！'}
    return render(request, 'myadmin/index/login.html', context)


# 管理员登出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))


# 会员登录表单
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')