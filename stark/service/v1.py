#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery
from django.conf.urls import url
from django.shortcuts import HttpResponse, render


class StarkConfig(object):
    list_display = []

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site

    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        url_patterns = [
            url(r'^$', self.changelist_view, name='%s_%s_change_list' % app_model_name),
            url(r'^add/$', self.add_view, name='%s_%s_add' % app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % app_model_name),
        ]

        return url_patterns

    @property
    def urls(self):
        return self.get_urls()

    def get_head_list(self):

        if len(self.list_display) == 0:
            yield self.model_class._meta.model_name.upper()
        else:
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    yield self.model_class._meta.get_field(field_name).verbose_name
                else:
                    yield field_name(self, is_header=True)


    def get_data_list(self):
        data_list = self.model_class.objects.all()
        for row in data_list:
            temp = []
            if len(self.list_display) == 0:
                temp.append(row)
            else:
                for field_name in self.list_display:
                    if isinstance(field_name, str):
                        val = getattr(row, field_name)
                    else:
                        val = field_name(self, row)
                    temp.append(val)
            yield temp

    ############################### 处理请求的方法##############

    def changelist_view(self, request, *args, **kwargs):
        head_list = []

        if len(self.list_display) == 0:
            verbose_name = self.model_class._meta.model_name.upper()
            head_list.append(verbose_name)
        else:
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self, is_header=True)

                head_list.append(verbose_name)

        data_list = self.model_class.objects.all()
        new_data_list = []
        for row in data_list:
            temp = []
            if len(self.list_display) == 0:
                temp.append(row)
            else:
                for field_name in self.list_display:
                    if isinstance(field_name, str):
                        val = getattr(row, field_name)
                    else:
                        val = field_name(self, row)
                    temp.append(val)
            new_data_list.append(temp)

        return render(request, 'stark/changelist.html', {'data_list': self.get_data_list(), 'head_list': self.get_head_list()})

    def add_view(self, request, *args, **kwargs):
        return HttpResponse('添加')

    def delete_view(self, request, *args, **kwargs):
        return HttpResponse('删除')

    def change_view(self, request, *args, **kwargs):
        return HttpResponse('修改')


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model_class, stark_config_class=None):
        if not stark_config_class:
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class, self)

    def get_urls(self):
        url_pattern = []
        for model_class, start_config_obj in self._registry.items():
            # 为每一个类，创建四个URL
            '''
            /stark/app01/userinfo/
            /stark/app01/userinfo/add/
            /stark/app01/userinfo/(\d+)/delete/
            /stark/app01/userinfo/(\d+)/change/
            '''
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' % (app_name, model_name,), (start_config_obj.urls, None, None))
            url_pattern.append(curd_url)
        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(), None, 'stark')


site = StarkSite()
