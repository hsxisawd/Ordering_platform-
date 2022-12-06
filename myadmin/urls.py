from django.urls import path
from myadmin.views import index
from myadmin.views import user,shop,category,product,member

urlpatterns = [
    # 后台首页
    path('', index.index, name="myadmin_index"),
    #后台管理员登录，退出路由
    path('login',index.login,name="myadmin_login"),#加载登录表单
    path('dologin',index.dologin,name='myadmin_dologin'),#执行登录
    path('logout',index.logout,name='myadmin_logout'),#管理员登出
    path('verify', index.verify, name="myadmin_verify"), #验证码
    #员工信息管理路由
    path('user/<int:pIndex>',user.index,name='myadmin_user_index'),#浏览
    path('user/add',user.add,name='myadmin_user_add'),#添加表单
    path('user/insert',user.insert,name='myadmin_user_insert'),#执行添加
    path('user/del/<int:uid>',user.delete,name='myadmin_user_delete'),#执行删除
    path('user/edit/<int:uid>',user.edit,name='myadmin_user_edit'),#加载编辑表单
    path('user/update/<int:uid>',user.update,name='myadmin_user_update'),#执行编辑
    #店铺信息管理路由
    path('shop/<int:pIndex>',shop.index,name='myadmin_shop_index'),#浏览
    path('shop/add',shop.add,name='myadmin_shop_add'),#添加表单
    path('shop/insert',shop.insert,name='myadmin_shop_insert'),#执行添加
    path('shop/del/<int:sid>',shop.delete,name='myadmin_shop_delete'),#执行删除
    path('shop/edit/<int:sid>',shop.edit,name='myadmin_shop_edit'),#加载编辑表单
    path('shop/update/<int:sid>',shop.update,name='myadmin_shop_update'),#执行编辑
    #菜品类别信息管理路由
    path('category/<int:pIndex>',category.index,name='myadmin_category_index'),#浏览
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"),#分类菜单路由
    path('category/add',category.add,name='myadmin_category_add'),#添加表单
    path('category/insert',category.insert,name='myadmin_category_insert'),#执行添加
    path('category/del/<int:cid>',category.delete,name='myadmin_category_delete'),#执行删除
    path('category/edit/<int:cid>',category.edit,name='myadmin_category_edit'),#加载编辑表单
    path('category/update/<int:cid>',category.update,name='myadmin_category_update'),#执行编辑
    # 菜品信息管理
    path('product/<int:pIndex>', product.index, name="myadmin_product_index"),
    path('product/add', product.add, name="myadmin_product_add"),
    path('product/insert', product.insert, name="myadmin_product_insert"),
    path('product/del/<int:pid>', product.delete, name="myadmin_product_delete"),
    path('product/edit/<int:pid>', product.edit, name="myadmin_product_edit"),
    path('product/update/<int:pid>', product.update, name="myadmin_product_update"),
    #会员管理路由
    path('member/<int:pIndex>', member.index, name="myadmin_member_index"), #浏览会员
]