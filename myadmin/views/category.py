from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from  myadmin.models import Category,Shop
from django.core.paginator import Paginator#分页模块
from datetime import datetime


# Create your views here.
#员工信息
def index(request,pIndex=1):#浏览
    umod=Category.objects
    ulist=umod.filter(status__lt=9)#查询出除已经删除外的数据
    mywhere=[]#数据维持
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        #搜索框账号，模糊查询(username__contains=kw)
        #搜索框昵称，模糊查询(nickname__contains=kw)

        mywhere.append('keyword='+kw)
    status = request.GET.get('status','')
    #获取判断并封装status搜索条件
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
    ulist=ulist.order_by('id')
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
    print(list2)
    plist=page.page_range#获取页码列表信息
    #遍历当前菜品分类信息并封装对应的店铺信息
    for vo in list2:
        try:
            sob =Shop.objects.get(id=vo.shop_id)#查询
            vo.shopname=sob.name #修改
        except Exception as err:
            print(err)
    #数据封装
    context={'categorylist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage,'mywhere':mywhere,}
    return render(request,'myadmin/category/index.html',context)

def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})

def add(request):#添加表单
    #获取当前店铺信息
    slist=Shop.objects.values("id","name")
    context={'shoplist':slist}
    return render(request,'myadmin/category/add.html',context)

def insert(request):#执行添加
        try:
            ob=Category()
            ob.shop_id=request.POST.get('shop_id')
            ob.name=request.POST.get('name')
            ob.status=1
            ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.save()
            context={'info':"添加成功！",'info1':"添加页面",'info2':"add",'info4':'菜品类别页面'}
        except Exception as err:
            print(err)
            context = {'info': "添加失败！", 'info1': "添加页面", 'info2': "add", 'info4':'菜品类别页面'}
        return render(request,"myadmin/info.html",context)

def delete(request,cid=0):#执行删除
    try:
        od=Category.objects.get(id=cid)
        od.status=9
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"删除成功！",'info1':'','info4':'菜品类别页面'}
    except Exception as err:
        print(err)
        context={"info":"删除失败！",'info1':'','info4':'菜品类别页面'}
    return render(request,'myadmin/info.html',context)

def edit(request,cid=0):#加载编辑表单

    try:
        od=Category.objects.get(id=cid)
        context={"category":od}
        slist = Shop.objects.values("id", "name")#查询店铺信息
        context['shoplist'] =slist
        return render(request,'myadmin/category/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":"没有找到要修改的信息！",'info1':'','info4':'菜品类别页面'}
        return render(request,'myadmin/info.html',context)
def update(request,cid=0):#执行编辑
    try:
        od=Category.objects.get(id=cid)
        od.shop_id=request.POST['shop_id']
        od.name=request.POST['name']
        od.status=request.POST['status']
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"修改成功！",'info1':"",'info4':'菜品类别页面'}
    except Exception as err:
        print(err)
        context={"info":"修改失败！",'info1':"",'info4':'菜品类别页面'}
    return render(request,'myadmin/info.html',context)


