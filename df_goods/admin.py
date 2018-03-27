from django.contrib import admin
from df_goods.models import TypeInfo, GoodsInfo, Comment


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gkucun', 'gcontent', 'gtype']


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'content', 'uid', 'gid']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(Comment, CommentAdmin)
