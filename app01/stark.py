#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery

from stark.service import v1
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe

from app01 import models


class UserInfoConfig(v1.StarkConfig):


    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s"'%(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'
        return mark_safe('<a href="/edit/%s">编辑</a>'%(obj.id,))

    list_display = [checkbox,'id','username',edit]



v1.site.register(models.UserInfo,UserInfoConfig)

class UserTypeConfig(v1.StarkConfig):
    list_display = ['caption',]

v1.site.register(models.UserType,UserTypeConfig)
class RoleConfig(v1.StarkConfig):
    list_display = ['name',]
v1.site.register(models.Role,RoleConfig)

v1.site.register(models.Article)