#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from repository import models
from web import forms

from web.service import asset


class AssetListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        print(response.__dict__)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    @method_decorator(csrf_exempt)
    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class EditAssetView(View):
    def get(self, request, device_type_id, asset_nid):
        username = request.session.get('username')
        condition = {"device_type_id": device_type_id, "id": asset_nid}
        asset = models.Asset.objects.filter(**condition).first()
        obj_form = forms.AssetModelForm(instance=asset)
        return render(request, "asset_change.html", locals())

    def post(self, request, device_type_id, asset_nid):
        condition = {"device_type_id": device_type_id, "id": asset_nid}
        asset = models.Asset.objects.filter(**condition).first()
        obj_form = forms.AssetModelForm(request.POST, instance=asset)
        if obj_form.is_valid():
            obj_form.save()
            print(obj_form.errors.as_json())
        return render(request, "asset_change.html", locals())


class AddAssetView(View):
    def get(self, request):
        username = request.session.get('username')
        obj_form = forms.AssetModelForm()
        return render(request, "asset_add.html", locals())

    def post(self, request):
        obj_form = forms.AssetModelForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
        return render(request, "asset_add.html", locals())
