from django.shortcuts import render
from django.http import  HttpResponse
from  myadmin.models import User
from django.core.paginator import Paginator#分页模块
from django.db.models import Q #多条件的查询
from datetime import datetime


# Create your views here.
#员工信息
def index(request,pIndex=1):#浏览
    umod=User.objects
    ulist=umod.filter(status__lt=9)#查询出除已经删除外的数据
    mywhere=[]#数据维持
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        #搜索框账号，模糊查询(username__contains=kw)
        #搜索框昵称，模糊查询(nickname__contains=kw)
        ulist=ulist.filter(Q(username__contains=kw)|Q(nickname__contains=kw))#或者的条件查询
        mywhere.append('keyword='+kw)
    status = request.GET.get('status','')
    #获取判断并封装status搜索条件
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
    ulist=ulist.order_by('id')
    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,5)#以每页五条数据分页
    maxpage=page.num_pages#获取最大页数
    #判断当前页是否越界
    if pIndex>maxpage:
        pIndex=maxpage
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)#获取当前页数据
    plist=page.page_range#获取页码列表信息
    #数据封装
    context={'userlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage,'mywhere':mywhere}

    return render(request,'myadmin/user/index.html',context)


def add(request):#添加表单
    return render(request,'myadmin/user/add.html')

def insert(request):#执行添加

        try:
            n_pw=request.POST.get('password')
            o_pw=request.POST.get('repassword')
            if  n_pw==o_pw:#密码验证
                ob=User()
                ob.username=request.POST.get('username')
                ob.nickname=request.POST.get('nickname')

                #将当前员工信息密码做MD5 处理
                import hashlib,random
                md5=hashlib.md5()
                n=random.randint(100000,999999)
                s=request.POST.get('password')+str(n)#从表单中获取密码并添加干扰值
                md5.update(s.encode('utf-8'))#将要产生md5的子串放进去
                ob.password_hash=md5.hexdigest()#生成md5值
                ob.password_salt=n

                ob.status=1
                ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.save()
                context={'info':"添加成功！",'info1':"添加页面",'info2':"add",'info4':'员工页面'}
                return render(request,"myadmin/info.html",context)
            else:
                context={'info':"密码错误！",'info1':"添加页面",'info2':"add",'info4':'员工页面'}
                return render(request,"myadmin/info.html",context)
        except Exception as err:
            print(err)


def delete(request,uid):#执行删除
    try:
        od=User.objects.get(id=uid)
        od.status=9
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"删除成功！",'info1':'','info4':'员工页面'}
    except Exception as err:
        print(err)
        context={"info":"删除失败！",'info1':'','info4':'员工页面'}
    return render(request,'myadmin/info.html',context)

def edit(request,uid):#加载编辑表单
    try:
        od=User.objects.get(id=uid)
        context={"user":od}
        return render(request,'myadmin/user/edit.html',context)
    except Exception as err:
        print(err)
        context={"info":"没有找到要修改的信息！",'info1':'','info4':'员工页面'}
        return render(request,'myadmin/info.html',context)
def update(request,uid):#执行编辑
    try:
        od=User.objects.get(id=uid)
        od.nickname=request.POST['nickname']
        od.status=request.POST['status']
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()
        context={"info":"修改成功！",'info1':"",'info4':'员工页面'}
    except Exception as err:
        print(err)
        context={"info":"修改失败！",'info1':"",'info4':'员工页面'}
    return render(request,'myadmin/info.html',context)


