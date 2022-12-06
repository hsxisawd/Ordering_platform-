from django.urls import path

from mobile.views import index,member

urlpatterns = [
    path('', index.index, name="mobile_index"),#移动端首页

    #会员注册/登录
    path('register', index.register, name="mobile_register"),#移动端注册登陆
    
    path('doregister', index.doRegister, name="mobile_doregister"),#执行移动端注册登陆
    #店铺选择
    path('shop', index.shop, name="mobile_shop"),#移动端选择店铺
    path('shop/select', index.selectShop, name="mobile_selectShop"),#执行移动端选择店铺
    #订单处理
    path('orders/add', index.addOrders, name="mobile_addorders"),#移动端下单页面
    #会员中心
    path('member', member.index, name="mobile_member_index"),#个人中心首页
    path('member/orders', member.orders, name="mobile_member_orders"),#个人中心浏览订单
    path('member/detail', member.detail, name="mobile_member_detail"),#个人中心的订单详情
    path('member/logout', member.logout, name="mobile_member_logout"),#执行会员退出
]