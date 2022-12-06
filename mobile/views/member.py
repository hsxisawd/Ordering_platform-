from django.shortcuts import render
from django.http import  HttpResponse
from django.shortcuts import redirect
from  django.urls import reverse
# Create your views here.

def index(request):
    #个人中心首页
    return render(request,"mobile/member.html")

def orders(request):
    #个人中心浏览订单
    return render(request,"mobile/member_orders.html")

def detail(request):
    #个人中心的订单详情
    return render(request,"mobile/member_detail.html")

def logout(request):
    #执行会员退出
    return render(request,"mobile/register.html")