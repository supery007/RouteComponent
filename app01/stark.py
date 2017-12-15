#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery


from stark.service import v1
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.forms import ModelForm

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
    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="/edit/%s">删除</a>'%(obj.id,))

    def extra_url(self):
        url_list = [
            url(r'^xxxxx/$',self.func)
        ]
        return url_list
    def func(self,request):
        return HttpResponse('...')

    list_display = ['name','email','ut']

class HostModeForm(ModelForm):
    class Meta:
        model = models.Host
        fields = ['id','hostname','ip','port']
        error_messages ={
            'hostname':{
                'required':'主机名不能为空',
            },
            'ip':{
                'required':'IP不能为空',
                'invalid':'IP格式错误',
            }
        }

class HostConfig(v1.StarkConfig):
    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return '自定义列'
        return '%s:%s'%(obj.ip,obj.port,)
    list_display = ['id','hostname','ip','port',ip_port]
    show_add_btn = True

    model_form_class = HostModeForm


v1.site.register(models.UserInfo,UserInfoConfig)

class UserTypeConfig(v1.StarkConfig):
    list_display = ['caption',]

v1.site.register(models.UserType,UserTypeConfig)
class RoleConfig(v1.StarkConfig):
    list_display = ['name',]
v1.site.register(models.Role,RoleConfig)

v1.site.register(models.Host,HostConfig)