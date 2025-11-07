from django.shortcuts import render,redirect
from django.urls import reverse
#from . serializers import  Client_Serializer,User_Serializer
from .models import SignUp_info,Cookie_Handler,Visa_Info,Funds_info,Client_Billing,Administrator_Info,Notifications,Call_Record
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Q
import shutil
from time import *
import uuid
import requests
import random
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from django.http import HttpResponseRedirect
from PIL import Image
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent

#--------------------- Extra ----------------------
from . Extra import admin_get as get
#--------------------- Extra ----------------------

  
class Dashboard_Rec(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)  
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Administrator_Info.objects.get(id=data_id["Data"])
           
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           total = Visa_Info.objects.all()
              
           context={"User":data,"Rand":rand,"Total":total}
           return render(request , "Rec/index.html",context)
        
        #except:
          
         #  return redirect('login')
       return redirect('rec_login')


class Profile_User_Rec(APIView):
    def get(self , request,pk):
       data_id = get(request)  
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Administrator_Info.objects.get(id=data_id["Data"])
           
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           selected = Visa_Info.objects.get(id=pk)
           rec = Call_Record.objects.filter(User=pk).order_by('id').reverse()
           listed = []
           for i in rec:
             admin = Administrator_Info.objects.get(id=i.Admin)
             listed.append({
               "id":i.id,"time":i.time,"date":i.date,"Name":admin.Full_Name
             })
           context={"User":data,"Rand":rand,"Date":current_date,"Selected":selected,"Rec":listed}
           return render(request , "Rec/order.html",context)
        
        #except:
          
         #  return redirect('login')
       return redirect('rec_login')
    def post(self , request,pk):
    
       data_id = get(request)  
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Administrator_Info.objects.get(id=data_id["Data"])
           rec = Call_Record.objects.create(User=pk,Admin=data.id)
           uploading_file = request.FILES['AUD']
           fs = FileSystemStorage()
           fs.save("Audios//"+str(rec.id)+".mp3",uploading_file) 
           return redirect(reverse('profile_user_rec',kwargs={"pk":pk}))
        #except:
          
         #  return redirect('login')
       return redirect('rec_login')


class Prompt(APIView):
    def get(self , request):
      
         return render(request, "Pannel/prompt.html") 



class Rec_Login(APIView):
    def get(self , request):
      data = get(request) 
      if data["Stat"] ==  "Ok":
          return redirect("rec_dashboard")
      else:
         return render(request, "Rec/login.html") 
    def post(self , request):
          current_time = strftime("%H:%M:%S %p")
       #try:    
          data = Administrator_Info.objects.get(User=request.data['User'], Password=request.data['Password'])
            
          response =  redirect('rec_dashboard')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Admin")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Admin")
          response.set_cookie('csrf-admin-token',generated_uuid)
          Notifications.objects.create(Type = "Login",User = data.id,Name = "Login Prompt!", Info=f"You have successfully logged in on {current_time}.",Link = "#")
          return response 
       #except:
        # return render (request, 'Administrator/pages/samples/error-404.html')
 
 
 
class Client_Logout(APIView):
    def get(self , request):
      response = redirect("client_login")
      response.delete_cookie('cookie_session_idd')
      return response


  
class Payment_User_List(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)  
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           listed = Funds_info.objects.filter(User=data.id)
           context={"User":data,"Rand":rand,"Date":current_date,"Funds":listed}
           return render(request , "Pannel/list.html",context)
        
        #except:
          
         #  return redirect('login')
       return redirect('rec_login')
