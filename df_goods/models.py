from django.db import models
from tinymce.models import HTMLField
from system.storage import ImageStorage


# 分类表
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20, unique=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


# 商品信息表
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods/images/', storage=ImageStorage())
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle


# 评论表
class Comment(models.Model):
    content = HTMLField()
    uid = models.ForeignKey('df_user.UserInfo')
    gid = models.ForeignKey(GoodsInfo)

    def __str__(self):
        return self.content



