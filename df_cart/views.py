from django.shortcuts import render, redirect
from df_user.islogin import islogin
from df_cart.models import CartInfo
from django.http import JsonResponse


# 购物车
@islogin
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts
    }
    return render(request, 'df_cart/cart.html', context)


# 添加购物车中的商品数量
@islogin
def add(request, gid, count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += count
    else:
        cart = CartInfo(user_id=uid, goods_id=gid, count=count)
    cart.save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id'])
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


# 编辑购物车中的商品数量
@islogin
def edit(request, cart_id, count):
    cart_id = int(cart_id)
    count = int(count)
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.count = count
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count}
    return JsonResponse(data)


# 删除购物车中的商品
@islogin
def delete(request, cart_id):
    cart_id = int(cart_id)
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
