#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery
from django.conf.urls import url
from django.shortcuts import HttpResponse, render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse


class StarkConfig(object):
    list_display = []

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s"' % (obj.id,))

    def edit(self, obj=None, is_header=False):
        if is_header:
            return '编辑'

        return mark_safe('<a href="%s/change/">编辑</a>' % (obj.id,))

    def delete(self, obj=None, is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s/delete/">删除</a>' % (obj.id,))

    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    # 2. 是否显示添加按钮
    show_add_btn = True
    def get_show_add_btn(self):
        return self.show_add_btn


    # 3. model_form_class
    model_form_class =None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class
        from django.forms import ModelForm
        class TestModelForm(ModelForm):
            class Meta:
                model =self.model_class
                fields = '__all__'
        return TestModelForm

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
        url_patterns.extend(self.extra_url())

        return url_patterns


    def extra_url(self):
        return []



    def get_change_url(self,nid):
        name = 'stark:%s_%s_change'%((self.model_class._meta.app_label,self.model_class._meta.model_name))
        edit_url = reverse(name,args=(nid,))
        return edit_url

    def get_list_url(self):
        name = 'stark:%s_%s_change_list'%((self.model_class._meta.app_label,self.model_class._meta.model_name))
        edit_url = reverse(name)
        return edit_url

    def get_add_url(self):
        name = 'stark:%s_%s_add'%((self.model_class._meta.app_label,self.model_class._meta.model_name))
        edit_url = reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name = 'stark:%s_%s_delete'%((self.model_class._meta.app_label,self.model_class._meta.model_name))
        edit_url = reverse(name,args=(nid,))
        return edit_url



    @property
    def urls(self):
        return self.get_urls()

    def get_head_list(self):

        if len(self.list_display) == 0:
            yield self.model_class._meta.model_name.upper()
        else:
            for field_name in self.get_list_display():
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
                for field_name in self.get_list_display():
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
            for field_name in self.get_list_display():
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
                for field_name in self.get_list_display():
                    if isinstance(field_name, str):
                        val = getattr(row, field_name)
                    else:
                        val = field_name(self, row)
                    temp.append(val)
            new_data_list.append(temp)

        return render(request, 'stark/changelist.html',
                      {'data_list': self.get_data_list(), 'head_list': self.get_head_list(),'add_url':self.get_add_url(),'show_add_btn':self.get_show_add_btn()})



    def add_view(self, request, *args, **kwargs):

        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form  = model_form_class()
            return render(request,'stark/add_view.html',{'form':form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
        return render(request,'stark/add_view.html',{'form':form})

    def delete_view(self, request,nid, *args, **kwargs):
        self.model_class.objects.filter(pk=nid).delete()

        return redirect(self.get_list_url())

    def change_view(self, request,nid, *args, **kwargs):
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request,'stark/change_view.html',{'form':form})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())

            return render(request,'stark/change_view.html',{'form':form})


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
