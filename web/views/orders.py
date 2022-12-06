#订单页面
import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import  HttpResponse
from django.shortcuts import redirect
from  django.urls import reverse
from  myadmin.models import *
from  datetime import datetime
# Create your views here.

def index(request,pIndex=1):
    #浏览订单信息
    umod =Orders.objects
    #获取当前店铺id
    sid=request.session['shopinfo']['id']
    ulist = umod.filter(shop_id=sid)  # 查询出除已经删除外的数据
    mywhere = []  # 数据维持
    status = request.GET.get('status', '')
    # 获取判断并封装status搜索条件
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)
    ulist = ulist.order_by('id')
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以每页十条数据分页
    maxpage = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpage:
        pIndex = maxpage
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    for vo in  list2:
        if vo.user_id==0:
            vo.nickname="无"
        else:
            user=User.objects.only("nickname").get(id=vo.user_id)
            vo.nickname=user.nickname
    # 数据封装
    context = {'orderslist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpage, 'mywhere': mywhere}

    return render(request, 'web/list.html', context)
def insert(request):
    # 执行订单添加
    try:
        ob = Orders()
        ob.shop_id = request.session["shopinfo"]['id']
        ob.member_id = 0
        ob.user_id = request.session["webuser"]['id']
        ob.money = request.session["total_money"]
        ob.status = 1   #订单状态:1过行中/2无效/3已完成
        ob.payment_status=2# 支付状态:1未支付/2已支付/3已退款
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()

        #执行支付信息添加
        op=Payment()
        op.order_id=ob.id
        op.member_id=0
        op.type=2
        op.bank=request.GET.get('bank',3) #收款银行渠道:1微信/2余额/3现金/4支付宝
        op.money = request.session["total_money"]
        op.status = 2  # 订单状态:1过行中/2无效/3已完成
        op.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        op.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        op.save()

        #执行订单详情添加
        cartlist=request.session.get("cartlist",{})#获取购物车中的菜品信息
        for item in cartlist.values():
            ov=OrderDetail()
            ov.order_id=ob.id #订单id
            ov.product_id=item["id"] #菜品id
            ov.product_name=item["name"]#菜品名称
            ov.price=item['price']#菜品价格
            ov.quantity=item["num"]#数量
            ov.status=1 #状态：1正常9删除
            ov.save()


        del request.session['cartlist']#支付完成清除购物车信息
        del request.session['total_money']#支付完成清除总金额
        return HttpResponse("Y")

    except Exception as err:
        print(err)
        return HttpResponse("N")

def detali(request):
    # 加载订单详情
    oid= request.GET.get("oid",0)
    dlist=OrderDetail.objects.filter(order_id=oid)
    context={"detaillist":dlist}
    return render(request,"web/detail.html",context)
def status(request):
    #修改订单状态
    try:
        oid=request.GET.get('oid',0)
        od = Orders.objects.get(id=oid)
        od.status = request.GET['status']
        od.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")
