from django.shortcuts import render
from django.http import  HttpResponse
from django.shortcuts import redirect
from  django.urls import reverse
# Create your views here.

def index(request):
    #移动端首页
    return render(request,"mobile/index.html")

def register(request):
    #移动端会员注册/登录表单
    return render(request,"mobile/register.html")

def doRegister(request):
    #执行会员注册/登录
    pass


def shop(request):
    #移动端选择店铺页面
    return render(request,"mobile/shop.html")


def selectShop(request):
    #移动端首页
    pass

def addOrders(request):
    #移动端下单页面
    return render(request, "mobile/addOrders.html")