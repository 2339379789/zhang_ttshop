from django.shortcuts import render
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from df_order.models import OrderInfo, OrderDetailInfo
from df_user.islogin import islogin
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.http import JsonResponse


# 订单列表
@islogin
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.filter(id=uid)
    print('*******************', user[0])
    # 获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面\
    orderid = request.GET.getlist('orderid')
    orderlist = []
    for id in orderid:
        orderlist.append(CartInfo.objects.get(id=int(id)))
    # 手机号
    # print('*******************',user.uphone)
    if user[0].uphone == '':
        uphone = ''
    else:
        uphone = user[0].uphone[0:4] + '****' + user[0].uphone[-4:]
    context = {
        'title': '提交订单',
        'page_name': 1,
        'orderlist': orderlist,
        'user': user[0],
        'ureceive_phone': uphone
    }
    return render(request, 'df_order/place_order.html', context)


# 下单操作
@transaction.atomic()  # 一旦操作失败则全部回退
@islogin
def order_handle(request):
    # 保存一个事物点,以便回退到这个点
    tran_id = transaction.savepoint()
    try:
        post = request.POST
        orderlist = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        # 创建订单对象
        order = OrderInfo()
        # 获取当前时间
        now = datetime.now()
        uid = request.session['user_id']
        # 生成订单号
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(total)
        order.oaddress = address
        order.save()
        # 遍历购物车中提交信息，创建订单详情表
        for orderid in orderlist:
            cartinfo = CartInfo.objects.get(id=orderid)
            good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)

            # 判断库存是否够
            if int(good.gkucun) >= int(cartinfo.count):
                # 库存够，移除购买数量并保存
                good.gkucun -= int(cartinfo.count)
                good.save()
                goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)
                # 创建订单详情表
                detailinfo = OrderDetailInfo()
                detailinfo.goods_id = int(goodinfo.id)
                detailinfo.order_id = int(order.oid)
                detailinfo.price = Decimal(int(goodinfo.gprice))
                detailinfo.count = int(cartinfo.count)
                detailinfo.save()

                # 循环删除购物车对象
                cartinfo.delete()
            else:
                # 库存不够出发事务回滚
                transaction.savepoint_rollback(tran_id)
                # 返回json供前台提示失败
                return JsonResponse({'status': 2})
    except Exception as e:
        print('==================%s' % e)
        transaction.savepoint_rollback(tran_id)
    # 返回json供前台提示成功
    return JsonResponse({'status': 1})


# @transaction.atomic()
@islogin
def pay(request, oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {'order': order}
    return render(request, 'df_order/pay.html', context)
