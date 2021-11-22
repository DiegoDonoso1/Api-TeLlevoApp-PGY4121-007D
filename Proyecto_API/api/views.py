from django.db import models
from django.db.models.base import Model
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
# Create your views here.

class UserView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,id=0):
        if(id > 0):
            users = list(User.objects.filter(id=id).values())
            if len(users) > 0:
                user = users[0]
                datos = {'message': "Success", 'users': user}
            else:
                datos = {'message': "User not found..."}
            return JsonResponse(datos)
        else:
            users = list(User.objects.values())
            if len(users) > 0:
                datos = {'message': "Success", 'users': users}
            else:
                datos = {'message': "User not found..."}
            return JsonResponse(datos)
    
    def post(self, request):
        print(request.body)
        print(request)
        jd = json.loads(request.body)
        if jd['action']=='login_progress':
            users = list(User.objects.filter(email=jd['email']))
            passwords = list(User.objects.filter(password=jd['password'],email=jd['email']))
            if users and passwords:
                datos={'message':"success"}
            else:
                datos = {'message': "User not found..."}
                print(datos)
            return JsonResponse(datos)
        # print(jd)
        elif jd['action']=='registration_progress':
            users = list(User.objects.filter(email=jd['email']))
            if users:
                datos = {'message': "user already registered"}
            else:
                User.objects.create(
                    email=jd['email'], password=jd['password'])
                datos={'message':"success"}
            print(datos)
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        users = list(User.objects.filter(id=id).values())
        user = list(User.objects.filter(email=jd['email']))
        if len(users) > 0 and len(user) == 0:
            user = User.objects.get(id=id)
            user.email = jd['email']
            user.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "User not found..."}
        print(datos);
        return JsonResponse(datos)

    def delete(self, request, id):
        users = list(User.objects.filter(id=id).values())
        if len(users) > 0:
            User.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "User not found..."}
        return JsonResponse(datos)
