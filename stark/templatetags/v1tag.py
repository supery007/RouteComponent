#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery

from django.template import Library
from stark.service import v1
from django.conf.urls import url
from django.shortcuts import HttpResponse,redirect,render

register = Library()



@register.inclusion_tag('tag.html')
def changelist_view(self,request,*args,**kwargs):
    data_list = self.model_class.objects.all()
    new_data_list = []
    for row in data_list:
        temp = []
        for field_name in self.list_display:
            if isinstance(field_name, str):
                val = getattr(row, field_name)
            else:
                val = field_name(self, row)
            temp.append(val)
        new_data_list.append(temp)
    return new_data_list