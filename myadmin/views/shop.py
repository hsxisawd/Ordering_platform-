from datetime import datetime
from django.shortcuts import render
from django.http import  HttpResponse
from  myadmin.models import Shop
from django.core.paginator import Paginator#分页模块
import  time


# Create your views here.
#店铺信息
def index(request,pIndex=1):#浏览
    smod=Shop.objects
    slist=smod.filter(status__lt=9)#查询出除已经删除外的数据
    mywhere=[]#数据维持
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        #搜索框账号，模糊查询(username__contains=kw)
        #搜索框昵称，模糊查询(nickname__contains=kw)
        slist=slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)

    #获取判断并封装status搜索条件
    status = request.GET.get('status','')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status="+status)
    slist=slist.order_by('id')

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(slist,5)#以每页五条数据分页
    maxpage=page.num_pages#获取最大页数
    #判断当前页是否越界
    if pIndex>maxpage:
        pIndex=maxpage
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)#获取当前页数据
    plist=page.page_range#获取页码列表信息
    #数据封装
    context={'shoplist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage,'mywhere':mywhere}

    return render(request,'myadmin/shop/index.html',context)


def add(request):#添加表单
    return render(request,'myadmin/shop/add.html')

def insert(request):#执行添加

        try:
            # 店铺封面图片的上传处理
            myfile = request.FILES.get("cover_pic",None)
            if not myfile:
                return HttpResponse("没有店铺封面上传文件信息")
            cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/"+cover_pic,"wb+")
            for chunk in myfile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()

            # 店铺logo图片的上传处理
            myfile = request.FILES.get("banner_pic",None)
            if not myfile:
                return HttpResponse("没有店铺logo上传文件信息")
            banner_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/"+banner_pic,"wb+")
            for chunk in myfile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()

            ob=Shop()
            ob.username=request.POST.get('name')
            ob.address=request.POST.get('address')
            ob.phone=request.POST.get('phone')
            ob.cover_pic=cover_pic
            ob.banner_pic=banner_pic
            ob.status=1
            ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.save()
            context={'info':"添加成功！",'info1':"添加页面",'info2':"add",'info4':'店铺页面'}
            return render(request,"myadmin/info.html",context)
        except Exception as err:
            print(err)


def delete(request,sid=0):#执行删除
    try:
        od=Shop.objects.get(id=sid)
        od.status=9
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"删除成功！",'info1':'','info4':'店铺页面'}
    except Exception as err:
        print(err)
        context={"info":"删除失败！",'info1':'','info4':'店铺页面'}
    return render(request,'myadmin/info.html',context)

def edit(request,sid=0):#加载编辑表单
    try:
        od=Shop.objects.get(id=sid)
        context={"shop":od}
        return render(request,'myadmin/shop/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":"没有找到要修改的信息！",'info1':'','info4':'店铺页面'}
        return render(request,'myadmin/info.html',context)
def update(request,sid):#执行编辑
    try:
        od=Shop.objects.get(id=sid)
        od.username=request.POST.get('name')
        od.address=request.POST.get('address')
        od.phone=request.POST.get('phone')
        od.status=request.POST['status']
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"修改成功！",'info1':"",'info4':'店铺页面'}
    except Exception as err:
        print(err)

        context={"info":"修改失败！",'info1':"",'info4':'店铺页面'}
    return render(request,'myadmin/info.html',context)


