from django.shortcuts import render
from django.http import  HttpResponse
from  myadmin.models import Product,Shop,Category
from django.core.paginator import Paginator#分页模块
from datetime import datetime
import time,os


# Create your views here.
#员工信息
def index(request,pIndex=1):#浏览
    pmod=Product.objects
    plist=pmod.filter(status__lt=9)#查询出除已经删除外的数据
    mywhere=[]#数据维持
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        plist = plist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    cid=request.GET.get('category_id',None)
    #获取并判断搜索菜品类别条件
    cid = request.GET.get('category_id', '')
    if cid != '':
        plist = plist.filter(category_id=cid)
        mywhere.append("category_id=" + cid)
    status = request.GET.get('status','')
    #获取判断并封装status搜索条件
    if status != '':
        ulist = plist.filter(status=status)
        mywhere.append("status="+status)
    ulist=plist.order_by('id')
    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,10)#以每页五条数据分页
    maxpage=page.num_pages#获取最大页数
    #判断当前页是否越界
    if pIndex>maxpage:
        pIndex=maxpage
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)#获取当前页数据
    plist=page.page_range#获取页码列表信息

    #遍历当前菜品分类信息并封装对应的店铺和菜品类别信息
    for vo in list2:
        sob =Shop.objects.get(id=vo.shop_id)#查询
        vo.shopname=sob.name #修改
        sob =Category.objects.get(id=vo.category_id)  # 查询
        vo.categoryname = sob.name  # 修改
    #数据封装
    context={'productlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage,'mywhere':mywhere,}
    return render(request,'myadmin/product/index.html',context)


def add(request):#添加表单
    #获取当前店铺信息
    slist=Shop.objects.values("id","name")
    context={'shoplist':slist}
    return render(request,'myadmin/product/add.html',context)

def insert(request):#执行添加
        try:
            ob=Product()
            ob.shop_id=request.POST.get('shop_id')
            ob.category_id=request.POST.get("category_id")
            ob.name=request.POST.get('name')
            ob.price=request.POST.get('price')

            myfile = request.FILES.get("cover_pic", None)
            if not myfile:
                return HttpResponse("没有店铺封面上传文件信息")
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            ob.cover_pic=cover_pic#存入数据库
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            ob.status=1
            ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.save()
            context={'info':"添加成功！",'info1':"添加页面",'info2':"add",'info4':'菜品信息页面'}
        except Exception as err:
            print(err)
            context = {'info': "添加失败！", 'info1': "添加页面", 'info2': "add", 'info4':'菜品信息页面'}
        return render(request,"myadmin/info.html",context)

def delete(request,pid=0):#执行删除
    try:
        od=Product.objects.get(id=pid)
        od.status=9
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"删除成功！",'info1':'','info4':'菜品信息页面'}
    except Exception as err:
        print(err)
        context={"info":"删除失败！",'info1':'','info4':'菜品信息页面'}
    return render(request,'myadmin/info.html',context)

def edit(request,pid=0):#加载编辑表单
    try:
        od=Product.objects.get(id=pid)
        context={"product":od}
        slist = Shop.objects.values("id", "name")#查询店铺信息
        context['shoplist'] =slist
        return render(request,'myadmin/product/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":"没有找到要修改的信息！",'info1':'','info4':'菜品信息页面'}
        return render(request,'myadmin/info.html',context)

def update(request,pid):
    '''执行编辑信息'''
    try:
        #获取原图片名
        oldpicname = request.POST['oldpicname']
        #判断是否有文件上传
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            cover_pic = oldpicname
        else:
            #图片的上传处理
            cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/product/"+cover_pic,"wb+")
            for chunk in myfile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        # 判断删除老图片
        if myfile:
            os.remove("./static/uploads/product/" + oldpicname)
        context={"info":"修改成功！",'info1':'','info4':'菜品信息页面'}
    except Exception as err:
        print(err)
        context={"info":"修改失败！",'info1':'','info4':'菜品信息页面'}
        # 判断删除刚刚上传的图片
        if myfile:
            os.remove("./static/uploads/product/" +cover_pic)

    return render(request,"myadmin/info.html",context)


