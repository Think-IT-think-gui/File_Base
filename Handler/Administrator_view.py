from django.shortcuts import render,redirect
from django.urls import reverse
#from . serializers import  Client_Serializer,User_Serializer
from .models import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Q
import shutil
from time import *
import requests
import uuid
import random
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import sqlite3
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent
import qrcode
import stripe
import statistics
from collections import defaultdict
from django.core.paginator import Paginator
import threading
import numpy as np
from PIL import Image, ImageDraw
from django.db.models import Sum
#======================================================== Dashboard ===========================================================
from .noti import *
from . Extra import *

from datetime import datetime

from django.utils import timezone
from datetime import timedelta
ET_URL ='https://color-difb.onrender.com'
#duplicate_data_thread()
#fix_postgres_sequences()
def set_id(id):
    s = Visa_Info.objects.get(id=id)
    date = s.date
    year = date.strftime("%y")  # Get last two digits of the year (e.g., 2025 → 25)
    month = date.strftime("%m")  # Get two-digit month (e.g., September → 09)

    # Pad the ID with leading zeros to ensure it's always 10 digits
    padded_id = str(id).zfill(4)  # Adjust 4 depending on your ID length expectations

    # Construct the Main_ID (always 10 digits)
    main_id = f'{year}{month}00{padded_id}'

    # Update the record
    Visa_Info.objects.filter(id=id).update(Main_ID=main_id)

def make_all():
 d = Visa_Info.objects.all()
 print(d)
 for i in d:
    set_id(i.id)


#thread = threading.Thread(target=make_all)
#thread.start()
#Visa_Info.objects.filter(id=9727).update(Account_Type='Main')
#Visa_Info.objects.filter(id=9726).update(Account_Type='Main')



def set_perms():
    a = Administrator_Info.objects.all()
    Side_Menu_Permission.objects.all().delete()
    for i in a:
      Side_Menu_Permission.objects.create(User=i.id,Menu=1,Status=i.New_Leads)
      Side_Menu_Permission.objects.create(User=i.id,Menu=2,Status=i.New_Applications)
      Side_Menu_Permission.objects.create(User=i.id,Menu=3,Status=i.Unreachable_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=4,Status=i.Pending_Applications)
      Side_Menu_Permission.objects.create(User=i.id,Menu=5,Status=i.Booked_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=6,Status=i.Briefed_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=7,Status=i.Decision)
      Side_Menu_Permission.objects.create(User=i.id,Menu=8,Status=i.Decision)
      Side_Menu_Permission.objects.create(User=i.id,Menu=9,Status=i.Medical)
      Side_Menu_Permission.objects.create(User=i.id,Menu=10,Status=i.Medical)
      Side_Menu_Permission.objects.create(User=i.id,Menu=11,Status=i.Ready_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=12,Status=i.Active_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=13,Status=i.Travelling)
      Side_Menu_Permission.objects.create(User=i.id,Menu=14,Status=i.Exiting)
      Side_Menu_Permission.objects.create(User=i.id,Menu=15,Status=i.Travelled)
      Side_Menu_Permission.objects.create(User=i.id,Menu=16,Status=i.Archived)
      Side_Menu_Permission.objects.create(User=i.id,Menu=17,Status=i.Declined_Applicants)
      Side_Menu_Permission.objects.create(User=i.id,Menu=18,Status='No')





def get_permission(id):
    main = []

    all = Side_Menu_Permission.objects.filter(User=id).all()
    for i in all:
        if i.Status == 'Yes':
          main.append(i.Menu)
    return main



class Manage_Files(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          client = Visa_Info.objects.get(id=pk)
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Client":client,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/add_file.html",context)
      else:
         return redirect("login")

    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          print(r)
          current_date = strftime("%Y-%m-%d")
          f = Uploaded_Files.objects.create(User=pk,Name=r["Name"],About=r["About"],Count=0,Status="Yes")
          fs = FileSystemStorage()
          c = 0
          for uploading_file in request.FILES.getlist('Files'):
            file_name, file_extension = os.path.splitext(uploading_file.name)
            v = Uploaded_Files_List.objects.create(User=user.id,File=f.id,Name=f"{file_name}{file_extension}",Extention=file_extension,Status="Yes")
            fs.save(f"Uploads/{str(v.id)}{file_extension}", uploading_file)
            c+=1
          Uploaded_Files.objects.filter(id=f.id).update(Count=c)


          return redirect(reverse('list_uploaded_files',kwargs={"pk":pk}))
         # return redirect(reverse('manage_files',kwargs={"pk":pk}))

      else:
         return redirect("login")


class List_Uploaded_Files(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          schedule = Uploaded_Files.objects.filter(User=pk)
          client = Visa_Info.objects.get(id=pk)

          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Schedule":schedule,"Client":client,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/list_files.html",context)
      else:
         return redirect("login")
    def delete(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)
          Uploaded_Files.objects.filter(id=req["id"]).delete()
          v = Uploaded_Files_List.objects.filter(File=req["id"])
          for i in v:
           try:
             os.remove(f'{BASE_DIR}/media/Uploads/{str(i.id)}{i.Extention}')
           except:
             pass
          Uploaded_Files_List.objects.filter(File=req["id"]).delete()
          return Response('Ok')
      else:
         return Response('Error')


class View_Uploaded_Files(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          schedule = Uploaded_Files_List.objects.filter(File=pk)
          f = Uploaded_Files.objects.get(id=pk)
          client = Visa_Info.objects.get(id=f.User)
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Files":schedule,"Client":client,"Table":f,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/view_files.html",context)
      else:
         return redirect("login")















#=============================================================================================================

class Manage_Files_Group_Edit(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          client = Visa_Info.objects.all()
          f = Uploaded_Files_Group.objects.get(id=pk)
          pm = []
          dt = Uploaded_Client_Group.objects.filter(File=f.id)
          for i in dt:
             try:
              cc =  Visa_Info.objects.get(id=i.User)
              pm.append({
                  'id':i.id,'Name':cc.Full_Name,'User':i.User
                  })
             except:
                 pass
          v = Uploaded_Files_List_Group.objects.filter(File=f.id)
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Client":client,"Side_Bar":side_bar,'Permission':get_permission(user.id),'Info':f,'Files':v,'Clients':pm}
          return render(request, "New/edit_group_file.html",context)
      else:
         return redirect("login")
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          print(r)
          current_date = strftime("%Y-%m-%d")

          f = Uploaded_Files_Group.objects.filter(id=pk).update(Name=r["Name"],About=r["About"])
          fs = FileSystemStorage()
          c = 0
          Uploaded_Client_Group.objects.filter(File=pk).delete()

          for i in r:
              if str(i).split('_')[0] == "Staff":
                  p =str(i).split('_')[1]
                  u =r[f'Staff_{p}']
                  Uploaded_Client_Group.objects.create(File=pk,User=u)

          try:
           for uploading_file in request.FILES.getlist('Files'):
            file_name, file_extension = os.path.splitext(uploading_file.name)
            v = Uploaded_Files_List_Group.objects.create(User=user.id,File=pk,Name=f"{file_name}{file_extension}",Extention=file_extension,Status="Yes")
            fs.save(f"Uploads_Group/{str(v.id)}{file_extension}", uploading_file)
            c+=1
           Uploaded_Files_Group.objects.filter(id=pk).update(Count=int(f.Count)+c)
          except:
              pass




        #  return redirect('list_uploaded_files_group')
          return redirect(reverse('manage_files_group_edit',kwargs={"pk":pk}))

      else:
         return redirect("login")



class Manage_Files_Group(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          client = Visa_Info.objects.all()
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Client":client,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/add_group_file.html",context)
      else:
         return redirect("login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          print(r)
          current_date = strftime("%Y-%m-%d")
          f = Uploaded_Files_Group.objects.create(User=user.id,Name=r["Name"],About=r["About"],Count=0,Status="Yes")
          fs = FileSystemStorage()
          c = 0
          for i in r:
              if str(i).split('_')[0] == "Staff":
                  p =str(i).split('_')[1]
                  u =r[f'Staff_{p}']
                  Uploaded_Client_Group.objects.create(File=f.id,User=u)


          for uploading_file in request.FILES.getlist('Files'):
            file_name, file_extension = os.path.splitext(uploading_file.name)
            v = Uploaded_Files_List_Group.objects.create(User=user.id,File=f.id,Name=f"{file_name}{file_extension}",Extention=file_extension,Status="Yes")
            fs.save(f"Uploads_Group/{str(v.id)}{file_extension}", uploading_file)
            c+=1
          Uploaded_Files_Group.objects.filter(id=f.id).update(Count=c)


          return redirect('list_uploaded_files_group')
         # return redirect(reverse('manage_files',kwargs={"pk":pk}))

      else:
         return redirect("login")


class List_Uploaded_Files_Group(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          schedule = Uploaded_Files_Group.objects.all()
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Uploaded_Files_Group.objects.filter().count()
          day = Uploaded_Files_Group.objects.filter(date__gte=today_start).count()
          week = Uploaded_Files_Group.objects.filter(date__gte=last_week_start).count()
          month = Uploaded_Files_Group.objects.filter(date__gte=last_month_start).count()

          a_total = Uploaded_Client_Group.objects.filter().count()
          a_day = Uploaded_Client_Group.objects.filter(date__gte=today_start).count()
          a_week = Uploaded_Client_Group.objects.filter(date__gte=last_week_start).count()
          a_month = Uploaded_Client_Group.objects.filter(date__gte=last_month_start).count()



          rand = random.randint(0,1000)

          listed = []

          paginator = Paginator(schedule, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             a = Uploaded_Client_Group.objects.filter(File=i.id).count()
             listed.append({
                 'id':i.id,'time':i.time,'date':i.date,'Name':i.Name,"User":i.User,'Count':a
                 })


          cro =  Administrator_Info.objects.all()
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Schedule":listed,'page_obj':page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id),"CRO":cro,
          'Day':day,'Week':week,'Month':month,'Total':total,'ADay':a_day,'AWeek':a_week,'AMonth':a_month,'ATotal':a_total

          }
          return render(request, "New/list_files_group.html",context)
      else:
         return redirect("login")
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = Uploaded_Files_Group.objects.filter(id=req["id"]).update(Name=req["Name"])

          return Response('Ok')
      else:
         return Response('Error')

    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)
          Uploaded_Files_Group.objects.filter(id=req["id"]).delete()
          v = Uploaded_Files_List.objects.filter(File=req["id"])
          for i in v:
           try:
             os.remove(f'{BASE_DIR}/media/Uploads_Group/{str(i.id)}{i.Extention}')
           except:
             pass
          Uploaded_Files_List_Group.objects.filter(File=req["id"]).delete()
          return Response('Ok')
      else:
         return Response('Error')



class List_Uploaded_Files_Group_Filter(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          r = request.data
          user = Administrator_Info.objects.get(id = data["Data"])
          schedule = Uploaded_Files_Group.objects.filter(User=r['CRO'],date__range=[r['Start'], r["End"]])
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Uploaded_Files_Group.objects.filter(User=r['CRO'],).count()
          day = Uploaded_Files_Group.objects.filter(User=r['CRO'],date__gte=today_start).count()
          week = Uploaded_Files_Group.objects.filter(User=r['CRO'],date__gte=last_week_start).count()
          month = Uploaded_Files_Group.objects.filter(User=r['CRO'],date__gte=last_month_start).count()

          a_total = Uploaded_Client_Group.objects.filter(User=r['CRO'],).count()
          a_day = Uploaded_Client_Group.objects.filter(User=r['CRO'],date__gte=today_start).count()
          a_week = Uploaded_Client_Group.objects.filter(User=r['CRO'],date__gte=last_week_start).count()
          a_month = Uploaded_Client_Group.objects.filter(User=r['CRO'],date__gte=last_month_start).count()



          rand = random.randint(0,1000)

          listed = []


          for i in schedule:
             a = Uploaded_Client_Group.objects.filter(File=i.id).count()
             listed.append({
                 'id':i.id,'time':i.time,'date':i.date,'Name':i.Name,"User":i.User,'Count':a
                 })


          cro =  Administrator_Info.objects.all()
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Schedule":listed,"Side_Bar":side_bar,'Permission':get_permission(user.id),"CRO":cro,
          'Day':day,'Week':week,'Month':month,'Total':total,'ADay':a_day,'AWeek':a_week,'AMonth':a_month,'ATotal':a_total

          }
          return render(request, "New/list_files_group.html",context)
      else:
         return redirect("login")

class View_Uploaded_Files_Group(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          schedule = Uploaded_Files_List_Group.objects.filter(File=pk)
          f = Uploaded_Files_Group.objects.get(id=pk)
          c = []
          l = Uploaded_Client_Group.objects.filter(File=pk)
          for i in l:
           try:
            client = Visa_Info.objects.get(id=i.User)
            c.append({"Full_Name":client.Full_Name,"id":client.id,"Group":client.Group})
           except:
               pass
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Files":schedule,"Client":c,"Table":f,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/view_files_group.html",context)
      else:
         return redirect("login")



#=============================================================================================================


class View_Client_Type(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)

          side_perm = Side_Menu.objects.get(id=pk)
          print(side_perm.Name)

          print('======================================')
          print(side_perm)
          all = Visa_Info.objects.filter(Group=side_perm.Name).count()
          sep = Visa_Info.objects.filter(SEP='S.E.P',Group=side_perm.Name).count()
          study = Visa_Info.objects.filter(SEP='Study Program',Group=side_perm.Name).count()
          business = Visa_Info.objects.filter(SEP='Business Travel',Group=side_perm.Name).count()
          tourist = Visa_Info.objects.filter(SEP='Tourist',Group=side_perm.Name).count()



          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],
              "General":all-(sep+study+business+tourist),"SEP":sep,"Study":study,"Business":business,"Tourist":tourist,"id":side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)

              }
          return render(request, "New/types.html",context)
      else:
         return redirect("login")






class View_Regions(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          Ashanti = Visa_Info.objects.filter(City='Ashanti').count()
          Bono = Visa_Info.objects.filter(City='Bono').count()
          Bono_East = Visa_Info.objects.filter(City='Bono East').count()
          Central = Visa_Info.objects.filter(City='Central').count()
          Eastern = Visa_Info.objects.filter(City='Eastern').count()
          Greater_Accra = Visa_Info.objects.filter(City='Greater Accra').count()
          Northern = Visa_Info.objects.filter(City='Northern').count()
          North_East = Visa_Info.objects.filter(City='North East').count()
          Oti = Visa_Info.objects.filter(City='Oti').count()
          Savannah = Visa_Info.objects.filter(City='Savannah').count()
          Upper_East = Visa_Info.objects.filter(City='Upper East').count()
          Upper_West = Visa_Info.objects.filter(City='Upper West').count()
          Volta = Visa_Info.objects.filter(City='Volta').count()
          Western = Visa_Info.objects.filter(City='Western').count()
          Western_North = Visa_Info.objects.filter(City='Western North').count()
          Ahafo = Visa_Info.objects.filter(City='Ahafo').count()
          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],
              "Ashanti":Ashanti,"Bono":Bono,"Bono_East":Bono_East,"Central":Central,"Eastern":Eastern,
              "Greater_Accra":Greater_Accra,"Northern":Northern,"North_East":North_East,"Oti":Oti,"Savannah":Savannah,
              "Upper_East":Upper_East,"Upper_West":Upper_West,"Volta":Volta,"Western":Western,"Western_North":Western_North ,
              "Ahafo":Ahafo,"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/regions.html",context)
      else:
         return redirect("login")









class Delete_Cookies(APIView):

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          Cookie_Handler.objects.filter(User=request.data["id"], Type="Admin").delete()
          return Response('Ok')
         except:
             return Response('No')
      else:
          return Response('No')


class Manager_Staff_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)

          manager =  Administrator_Info.objects.all()

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:


             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Location":i.Location,
             })

          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Note":"Staff List",'page_obj': page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list_staff.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Administrator_Info.objects.get(id=int(request.data["id"])).delete()
          try:
               os.remove(f'{BASE_DIR}/media/Admin/{request.data["id"]}.jpg')
          except:
              pass
          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')



class Add_Staff(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/add_staff.html",context)
      else:
         return redirect("login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          tp = Administrator_Info.objects.filter(Email=req["Email"]).count()
          if tp > 0:
              return render(request, 'New/authentication-error.html')

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Administrator_Info.objects.create(
              Full_Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
              Contact=req["Contact"],Password="pass",Gender=req["Gender"],Birth=req["Birth"],
             All_Applications=req["All_Applications"] ,Operation_Unit=req["Operation_Unit"],
              IELTS=req["IELTS"],Police_Report=req["Police_Report"],Medicals_Status=req["Medicals_Status"],
              Client_Booking=req["Client_Booking"],Financials=req["Financials"],Bills_Pricing=req["Bills_Pricing"],Briefing_Room=req["Briefing_Room"],Method=req['Method'],
              Call_Overview=req["Call_Overview"],Packages=req["Packages"],Traffic_Overview=req["Traffic_Overview"],Account_Management=req["Account_Management"],Account=0,Agent=req["Agent"],Confirm_Agent=req["Confirm_Agent"],
          )
          #------------------------------------------------------------


          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Admin//"+str(branch.id)+".jpg",uploading_file)
          return redirect('add_staff')
          #return redirect(reverse('view_Staff_account',kwargs={"pk":int(branch.id)}))
      else:
         return redirect("login")




class Edit_Staff(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          staff = Administrator_Info.objects.get(id =pk)

          p = Card_Point_Permission.objects.filter(User=pk)
          p_l = []
          for i in p:
             try:
              c = Card_Point.objects.get(id=i.Point)
              p_l.append({'id':i.id,'Name':c.Name})
             except:
                 pass

          point = Card_Point.objects.all()
          side_bar = Side_Menu.objects.all().order_by('Level')
          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Staff":staff,'Point':point,'Perm':p_l,'Permission':get_permission(user.id),"Side_Bar":side_bar,
              'Staff_Permission':get_permission(pk)
              }
          return render(request, "New/edit_staff.html",context)
      else:
         return redirect("login")

    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Administrator_Info.objects.filter(id=pk).update(
              Full_Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
              Contact=req["Contact"],Password=req["Password"],Gender=req["Gender"],Birth=req["Birth"],

              All_Applications=req["All_Applications"],



              Operation_Unit=req["Operation_Unit"],
              IELTS=req["IELTS"],Police_Report=req["Police_Report"],Medicals_Status=req["Medicals_Status"],
              Client_Booking=req["Client_Booking"],Financials=req["Financials"],Bills_Pricing=req["Bills_Pricing"],Method=req['Method'],
              Call_Overview=req["Call_Overview"],Packages=req["Packages"],Traffic_Overview=req["Traffic_Overview"],Account_Management=req["Account_Management"],
              Interview=req["Interview"],Profile_1=req["Profile_1"],Profile_2=req["Profile_2"],Profile_3=req["Profile_3"],Agent=req["Agent"],Confirm_Agent=req["Confirm_Agent"],


              Ashanti=req["Ashanti"],Bono=req["Bono"],Bono_East=req["Bono_East"],Central=req["Central"],Eastern=req["Eastern"],Greater_Accra=req["Greater_Accra"],
              Northern=req["Northern"],North_East=req["North_East"],Oti=req["Oti"],Savannah=req["Savannah"],Upper_East=req["Upper_East"],Upper_West=req["Upper_West"],
              Volta=req["Volta"],Western=req["Western"],Western_North=req["Western_North"],Ahafo=req["Ahafo"],Regional=req["Regional"]





          )



          #------------------------------------------------------------
          Side_Menu_Permission.objects.filter(User=pk).delete()
          print(req)
          for i in req:
              if str(i).split('_')[0] == "DATA":
                  p =str(i).split('_')[1]
                  Side_Menu_Permission.objects.create(User=pk,Menu=p,Status=req[f'DATA_{p}'])




          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/Admin/{pk}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Admin//"+str(pk)+".jpg",uploading_file)


          return redirect(reverse('edit_staff',kwargs={"pk":pk}))
      else:
         return redirect("login")



class Add_Completed_Data(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          r = request.data

          Completed_Logs.objects.create(User=user.id,Client=r["Client"],Type=r["Type"])


          return redirect(reverse('manager_edit',kwargs={"pk":int(r["Client"])}))
      else:
         return redirect("login")




class View_Logs(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          rand = random.randint(0,1000)

          branch = Applicant_Logs.objects.filter(Client=pk)
          listed = []
          c = 1
          client = Visa_Info.objects.get(id=pk)
          for i in branch:

              try:
                a = Administrator_Info.objects.get(id=i.User)
                name = a.Full_Name
              except:
                name= user.Full_Name
              use = i.User

              listed.append({
                  "Log":i.Log,"id":i.id,"Admin":name,"date":i.date,"User":use,"time":i.time
              })
              c+=1

          context = {"Data":user,"Rand":rand,"Client":client,"Listed":listed,"Total":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/logs.html",context)
      else:
         return redirect("login")



class Update_Email_Data(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Visa_Info.objects.filter(id=req["id"]).update(Contact_Email=req["Email"],Contact_Email_Password=req["Password"])


          return Response('Ok')
      else:
         return Response("No")

class Add_Log_Data(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Applicant_Logs.objects.create(User=user.id,Client=req["id"],Log=req["Log"])


          return Response('Ok')
      else:
         return Response("No")



class Add_Interview(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          r = request.data

          Interview_Session.objects.create(User=r["User"],Client=r["Client"],Start=r["Start"],End=r["End"],Dated=r["Dated"],
          Status="Pending",Answer="Pending",Appearance=0,Communication=0,Practical=0,Commitment=0,Medicals=0,Confidence=0,Knowledge=0,Question=r["Question"])


          return Response('Ok')
      else:
         return Response("No")


class Delete_Interview(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          r = request.data

          Interview_Session.objects.filter(id=r["id"]).delete()
          return Response('Ok')
      else:
         return Response("No")



class Status_Account_Group(APIView):
    def get(self , request, pk,pk2):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          side_perm = {
             'id':'No',
            'Status_Change':'Yes',
            'Call_Log':'Yes',
            'Book_Client':'Yes',
            'Interview':'Yes',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'Yes',
            'Opperation':'No',

              }
          if pk =="IELTS":
           if int(user.Account) == 1:
            manager =  Visa_Info.objects.filter(IELTS=pk2,Call=user.id)
           else:
            manager =  Visa_Info.objects.filter(IELTS=pk2)
          elif  pk =="Police" :
           if int(user.Account) == 1:
            manager =  Visa_Info.objects.filter(Police=pk2,Call=user.id)
           else:
            manager =  Visa_Info.objects.filter(Police=pk2)
          else :
           if int(user.Account) == 1:
            manager =  Visa_Info.objects.filter(Medicals=pk2,Call=user.id)
           else:
            manager =  Visa_Info.objects.filter(Medicals=pk2)


          notify = Notifications.objects.filter(User=user.id)
          hm = []
          for i in manager:
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(User=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"

             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,'Main':i.Main_ID,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
             })
          rand = random.randint(0,1000)
          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":pk,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Admins":adm,"Interview":inter,"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')



class Update_Applicant_Data(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          if req["Type"] == 1:
           Visa_Info.objects.filter(id=req["id"]).update(IELTS=req["Status"])
          elif req["Type"] == 2:
           Visa_Info.objects.filter(id=req["id"]).update(Police=req["Status"])
          elif req["Type"] == 3:
           Visa_Info.objects.filter(id=req["id"]).update(Medicals=req["Status"])
          else:
              if req["Status"] == 'ALL':
                  Visa_Info.objects.filter(id=req["id"]).update(SEP=None)
              else:
                  Visa_Info.objects.filter(id=req["id"]).update(SEP=req["Status"])

          return Response('Ok')
      else:
         return Response("No")


#-------------------------------------------------------------------- Booking ------------------------------------------------------------


class Booking_Find(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          now = timezone.now()
          current_date = strftime("%Y-%m-%d")
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Booking.objects.all().count()
          day = Booking.objects.filter(Schedule_Date=current_date).count()
          week = Booking.objects.filter(Schedule_Date__gte=last_week_start).count()
          month = Booking.objects.filter(Schedule_Date__gte=last_month_start).count()

          rand = random.randint(0,1000)
          branch = Booking.objects.filter(Name__icontains=request.data["Key"]) | Booking.objects.filter(Topic__icontains=request.data["Key"]) | Booking.objects.filter(Details__icontains=request.data["Key"])
          listed = []
          c = 1
          for i in branch:

              try:
                a = Administrator_Info.objects.get(id=i.Admin)
                name = a.Full_Name
              except:
                name= user.Full_Name
              use = i.Admin
              try:
               cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
              except:
                  cd='No'
              listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":i.Admin,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,'User':i.User,
                   "Card":cd
              })
              c+=1
          inter = ID_Card.objects.all()
          point = Card_Point.objects.all()

          context = {"Data":user,"Rand":rand,"Booking":listed,"Total2":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point,
          'Day':day,'Week':week,'Month':month,'Total':total
          }
          return render(request, "New/book-list.html",context)
      else:
         return redirect("login")



class Booking_Filter(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          now = timezone.now()
          current_date = strftime("%Y-%m-%d")
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Booking.objects.all().count()
          day = Booking.objects.filter(Schedule_Date=current_date).count()
          week = Booking.objects.filter(Schedule_Date__gte=last_week_start).count()
          month = Booking.objects.filter(Schedule_Date__gte=last_month_start).count()
          rand = random.randint(0,1000)
          if request.data["Key2"] == "All":
            branch = Booking.objects.filter(Schedule_Date=request.data["Key"]).order_by('Clock_In')
          else:
            branch = Booking.objects.filter(Schedule_Date=request.data["Key"],Status=request.data["Key2"]).order_by('Clock_In')
          listed = []
          c = 1
          for i in branch:

              try:
                a = Administrator_Info.objects.get(id=i.Admin)
                name = a.Full_Name
              except:
                name= user.Full_Name
              use = i.Admin
              try:
               cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
              except:
                  cd='No'

              listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":use,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,
                  "Card":cd,
              })
              c+=1
          inter = ID_Card.objects.all()
          point = Card_Point.objects.all()
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total2":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point,
          'Day':day,'Week':week,'Month':month,'Total':total
          }
          return render(request, "New/book-list.html",context)
      else:
         return redirect("login")



class Add_Booking(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)

      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          current_date = strftime("%Y-%m-%d")
          total = Booking.objects.all().count()
          day = Booking.objects.filter(Schedule_Date=current_date).count()
          week = Booking.objects.filter(Schedule_Date__gte=last_week_start).count()
          month = Booking.objects.filter(Schedule_Date__gte=last_month_start).count()
          rand = random.randint(0,1000)
          branch = Booking.objects.all().order_by('id').reverse()
          listed = []
          c = 1
          paginator = Paginator(branch, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

              try:
                a = Administrator_Info.objects.get(id=i.Admin)
                name = a.Full_Name
              except:
                name= user.Full_Name
              use = i.Admin
              try:
               cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
              except:
                  cd='No'

              listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":use,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,
                   "Card":cd
              })
              c+=1

          inter = ID_Card.objects.all()

          point = Card_Point.objects.all()
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total2":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point,'page_obj':page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id),
          'Day':day,'Week':week,'Month':month,'Total':total
          }
          return render(request, "New/book-list.html",context)
      else:
         return redirect("login")


    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          if req["Type"] == 'New':

           branch = Booking.objects.create(
              Name=req["Name"],User=user.id,Admin=user.id,Contact=req["Contact"],About=req["About"],Location=req["Location"],Type="New",
              Topic=req["Topic"],Gender=req["Gender"],Schedule_Date=req["Date"],Schedule_Time=req["Time"],Remark="Pending",Status="Not In"
           )
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Booking//"+str(branch.id)+".jpg",uploading_file)
          else:
            c = Visa_Info.objects.get(id=int(req["Client"]))
            branch = Booking.objects.create(
              Name=c.Full_Name,User=c.id,Admin=user.id,Contact=c.Contact,About=req["About"],Location=c.Address,Type=req["Client"],
              Topic=req["Topic"],Gender=c.Gender,Schedule_Date=req["Date"],Schedule_Time=req["Time"],Remark="Pending",Status="Not In"
           )



          return redirect('manage_booking')
      else:
         return redirect("login")



class View_Booking(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)

          rand = random.randint(0,1000)
          client = Booking.objects.get(id=pk)


          context = {"Data":user,"Rand":rand,"Client":client,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/view_booking.html",context)
      else:
         return redirect("login")
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Booking.objects.filter(id=pk).update(

              Details=req["Details"],Remark=req["Status"]
          )


          return redirect(reverse('view_booking',kwargs={"pk":int(pk)}))
      else:
         return redirect("login")


class Delete_Booking(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Booking.objects.filter(id=req["id"]).delete()
          try:
            os.remove(f'{BASE_DIR}/media/Booking/{req["id"]}.jpg')
          except:
             pass
          return Response('Ok')
      else:
         return Response("No")






class Confirm_Booking(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          now = timezone.now()
          current_date = strftime("%Y-%m-%d")
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Booking.objects.all().count()
          day = Booking.objects.filter(Schedule_Date=current_date).count()
          week = Booking.objects.filter(Schedule_Date__gte=last_week_start).count()
          month = Booking.objects.filter(Schedule_Date__gte=last_month_start).count()
          #Booking.objects.all().update(Status='Not In')
          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          branch = Booking.objects.filter(Schedule_Date=current_date).order_by('id').reverse()
          listed = []
          c = 1
          for i in branch:

                  name = Administrator_Info.objects.get(id=i.Admin).Full_Name
                  try:
                    cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
                  except:
                    cd='No'
                  listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":i.Admin,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,"Card":cd


                  })
                  c+=1
          inter = ID_Card.objects.all()

          point = Card_Point.objects.all()
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total2":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point,"Side_Bar":side_bar,'Permission':get_permission(user.id),
          'Day':day,'Week':week,'Month':month,'Total':total
          }
          return render(request, "New/clock2.html",context)
      else:
         return redirect("login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":

          r = request.data


          b = Booking.objects.get(id=r["id"])
          s_time = strftime('%H:%M')
          if b.Status == "Not In":
              Booking.objects.filter(id=b.id).update(Status="Clocked In",Clock_In=s_time)

          elif b.Status == "Clocked In":
              Booking.objects.filter(id=b.id).update(Status="Clocked Out",Clock_Out=s_time)


          return render(request, "New/clock_note.html")
      else:
         return redirect("staff")


class Confirm_Booking_Find(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          branch = Booking.objects.filter(Schedule_Date=current_date,Name__icontains=request.data["Key"]) | Booking.objects.filter(Schedule_Date=current_date,Contact__icontains=request.data["Key"])
          listed = []
          c = 1
          for i in branch:

                  name = Administrator_Info.objects.get(id=i.Admin).Full_Name
                  try:
                    cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
                  except:
                    cd='No'
                  listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":i.Admin,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,"Card":cd


                  })
                  c+=1
          inter = ID_Card.objects.all()

          point = Card_Point.objects.all()
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point}
          return render(request, "New/clock2.html",context)
      else:
         return redirect("login")



class Confirm_Booking_Filter(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          if request.data["Key"] == "All":
            branch = Booking.objects.filter(Schedule_Date=current_date)
          else:
           branch = Booking.objects.filter(Schedule_Date=current_date,Status=request.data["Key"])
          listed = []
          c = 1
          for i in branch:

                  name = Administrator_Info.objects.get(id=i.Admin).Full_Name
                  try:
                    cd = Card_Session.objects.filter(Status="Pending",Client=i.id).last().Card
                  except:
                    cd='No'
                  listed.append({
                  "Name":i.Name,"id":i.id,"Admin":name,"Date":i.Schedule_Date,"Contact":i.Contact,"User":i.Admin,"Time":i.Schedule_Time
                  ,"Title":i.Topic,"Remark":i.Remark,"Topic":i.Topic,"Location":i.Location,"Status":i.Status,"Count":c,'Type':i.Type,"Card":cd


                  })
                  c+=1
          inter = ID_Card.objects.all()

          point = Card_Point.objects.all()
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point}
          return render(request, "New/clock2.html",context)
      else:
         return redirect("login")




#------------------------------------------------------------ Booking --------------------------------------






class View_Cro_Call_Logs(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)


          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Status_Logs.objects.filter(User=pk).count()
          day = Status_Logs.objects.filter(User=pk,date__gte=today_start).count()
          week = Status_Logs.objects.filter(User=pk,date__gte=last_week_start).count()
          month = Status_Logs.objects.filter(User=pk,date__gte=last_month_start).count()
          rand = random.randint(0,1000)
          main = Status_Logs.objects.filter(User=pk)
          listed = []
          try:
           paginator = Paginator(main, 30)
           page_number = request.GET.get('page')
           try:
            page_obj = paginator.get_page(page_number)
           except PageNotAnInteger:
            page_obj = paginator.page(1)
           except EmptyPage:
               # If page is out of range, deliver last page of results
             page_obj = paginator.page(paginator.num_pages)
           for i in page_obj:


              staff = Administrator_Info.objects.get(id=i.User)
              client = Visa_Info.objects.get(id=i.Client)
              listed.append({
              "id":i.id,"Staff_id":staff.id,"Staff_Name":staff.Full_Name,"date":i.date,"time":i.time,"Client_id":client.id,"Client_Name":client.Full_Name,"Old":i.Old,"New":i.New
              })
          except:
              pass
          #------------------------------------ counter -------------------------------

          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Call_Logs.objects.filter(User=pk,date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Call_Logs.objects.filter(User=pk,date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Call_Logs.objects.filter(User=pk,date__gte=last_month_start).count()
          #------------------------------------ counter -------------------------------

          busy =0
          next =0
          picked =0
          ans =0
          total =0
          booked = 0
          cro = Administrator_Info.objects.get(id = pk)
          calls = []
          #mem = Visa_Info.objects.filter(Call=pk)
         # for a in mem:
          call = Call_Logs.objects.filter(User=pk,)

          for i in call:
             # calls.append({
             #  "id":i.id,"Member":i.Member,"Name":i.Name,"Contact":i.Contact,"Gender":i.Gender,"Location":i.Location,
              # "Start_Time":i.Start_Time,"End_Time":i.End_Time,"Status":i.Status,"Type":i.Type,"About":i.About,
              # "time":i.time,"date":i.date
             # })
              if i.Status == "Picked Up":
                  picked+=1
                  total+=1


              elif i.Status == "Rescheduled":
                  next+=1
                  total+=1

              elif i.Status == "Unanswered":
                  ans+=1
                  total+=1
              elif i.Status == "Booked":
                  booked+=1
                  total+=1

              else:
                  busy+=1
                  total+=1

          val_today2 = Completed_Logs.objects.filter(User=pk,date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week2 = Completed_Logs.objects.filter(User=pk,date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month2 = Completed_Logs.objects.filter(User=pk,date__gte=last_month_start).count()
          val_all2 = Completed_Logs.objects.filter(User=pk,)
          lp = []
          paginator = Paginator(val_all2, 20)
          page_number = request.GET.get('page')
          try:
            page_obj2 = paginator.get_page(page_number)
          except PageNotAnInteger:
            page_obj2 = paginator.page(1)
          except EmptyPage:
               # If page is out of range, deliver last page of results
             page_obj2 = paginator.page(paginator.num_pages)
          for o in page_obj2:
              client = Visa_Info.objects.get(id=o.Client)
              lp.append({
              "id":o.id,"date":o.date,"time":o.time,"Client_id":client.id,"Client_Name":client.Full_Name,"Type":o.Type
              })

          context = {"Data":user,"CRO":cro,"Rand":rand,"Calls":call,"Total":total,"Busy":busy,'Answer':ans,'Booked':booked,
          "Next":next,"Picked":picked,"Theme":data["Theme"],"Color":data["Color"]
          ,"Day":day,"Week":week,"Month":month,"Total2":total,"List":listed,"Call_Day":val_today,"Call_Week":val_last_week,"Call_Month":val_last_month,'page_obj':page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)
          ,"Com_Day":val_today2,"Com_Week":val_last_week2,"Com_Month":val_last_month2,'Com':lp,'Com_Count':val_all2.count(),'page_obj2':page_obj2
          }
          return render(request, "New/profiles2.html",context)
      else:
         return redirect("login")


    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)

          r = request.data
          start = r["Start"]
          end = r["End"]


          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          total = Status_Logs.objects.filter(User=pk).count()
          day = Status_Logs.objects.filter(User=pk,date__gte=today_start).count()
          week = Status_Logs.objects.filter(User=pk,date__gte=last_week_start).count()
          month = Status_Logs.objects.filter(User=pk,date__gte=last_month_start).count()
          rand = random.randint(0,1000)
          main = Status_Logs.objects.filter(User=pk,date__range=[start, end])
          listed = []
          try:
           paginator = Paginator(main, 30)
           page_number = request.GET.get('page')
           try:
            page_obj = paginator.get_page(page_number)
           except PageNotAnInteger:
            page_obj = paginator.page(1)
           except EmptyPage:
               # If page is out of range, deliver last page of results
             page_obj = paginator.page(paginator.num_pages)
           for i in page_obj:


              staff = Administrator_Info.objects.get(id=i.User)
              client = Visa_Info.objects.get(id=i.Client)
              listed.append({
              "id":i.id,"Staff_id":staff.id,"Staff_Name":staff.Full_Name,"date":i.date,"time":i.time,"Client_id":client.id,"Client_Name":client.Full_Name,"Old":i.Old,"New":i.New
              })
          except:
              pass
          #------------------------------------ counter -------------------------------

          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Call_Logs.objects.filter(User=pk,date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Call_Logs.objects.filter(User=pk,date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Call_Logs.objects.filter(User=pk,date__gte=last_month_start).count()
          #------------------------------------ counter -------------------------------

          busy =0
          next =0
          picked =0
          ans =0
          total =0
          booked = 0
          cro = Administrator_Info.objects.get(id = pk)
          calls = []
          #mem = Visa_Info.objects.filter(Call=pk)
         # for a in mem:
          call = Call_Logs.objects.filter(User=pk,date__range=[start, end])

          for i in call:
             # calls.append({
             #  "id":i.id,"Member":i.Member,"Name":i.Name,"Contact":i.Contact,"Gender":i.Gender,"Location":i.Location,
              # "Start_Time":i.Start_Time,"End_Time":i.End_Time,"Status":i.Status,"Type":i.Type,"About":i.About,
              # "time":i.time,"date":i.date
             # })
              if i.Status == "Picked Up":
                  picked+=1
                  total+=1


              elif i.Status == "Rescheduled":
                  next+=1
                  total+=1

              elif i.Status == "Unanswered":
                  ans+=1
                  total+=1
              elif i.Status == "Booked":
                  booked+=1
                  total+=1

              else:
                  busy+=1
                  total+=1



          context = {"Data":user,"CRO":cro,"Rand":rand,"Calls":call,"Total":total,"Busy":busy,'Answer':ans,'Booked':booked,
          "Next":next,"Picked":picked,"Theme":data["Theme"],"Color":data["Color"]
          ,"Day":day,"Week":week,"Month":month,"Total2":total,"List":listed,"Call_Day":val_today,"Call_Week":val_last_week,"Call_Month":val_last_month,'page_obj':page_obj}
          return render(request, "New/profiles2.html",context)
      else:
         return redirect("login")

    def delete(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Completed_Logs.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')


class Cro_Call_Logs(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          #------------------------------------ counter -------------------------------
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Call_Logs.objects.filter(date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Call_Logs.objects.filter(date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Call_Logs.objects.filter(date__gte=last_month_start).count()
          #------------------------------------ counter -------------------------------


          busy =0
          next =0
          picked =0
          ans = 0
          booked = 0
          mem = Administrator_Info.objects.all()
          calls = Call_Logs.objects.all()
          total = 0
          for i in calls:
              if i.Status == "Picked Up":
                  picked+=1
              elif i.Status == "Rescheduled":
                  next+=1
              elif i.Status == "Unanswered":
                  ans+=1
                  total+=1
              elif i.Status == "Booked":
                  booked+=1
                  total+=1
              else:
                  busy+=1


          context = {"Data":user,"Rand":rand,"Member":mem,"Total":calls.count(),"Busy":busy,'Answer':ans,'Booked':booked,
          "Next":next,"Picked":picked,"Theme":data["Theme"],"Color":data["Color"],"Day":val_today,"Week":val_last_week,"Month":val_last_month,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/log.html",context)
      else:
         return redirect("login")


class Generate_Code(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          admin_token = admin_get(request)
          user1_check = request.COOKIES['csrf-admin-token']
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          print('fff')
          r = request.data
          print(r["id"])
          s = Share_Link.objects.filter(User=user.id,Job=r["id"])
          if s.count() > 0:
            return Response({"Stat":'Ok',"Link":s.last().Link})
          current_date = strftime("%Y%m%d")
          lk = uuid.uuid1()
          nl = f'{lk}-{current_date}'
          Share_Link.objects.create(User=user.id,Job=r["id"],Link=nl)
          return Response({"Stat":'Ok',"Link":nl})
      else:
         return Response('No')


class Update_Call(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          print('fff')
          r = request.data
          print(r["id"])

          Visa_Info.objects.filter(id=r["id"]).update(Call=r["Status"])
          return Response('Ok')
      else:
         return Response('No')





class Manager_Find(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          side_bar = Side_Menu.objects.all().order_by('Level')
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          print(request.data["Key"])

          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Contact__icontains=request.data["Key"],Call=user.id) | Visa_Info.objects.filter(Full_Name__icontains=request.data["Key"],Call=user.id) | Visa_Info.objects.filter(Email__icontains=request.data["Key"],Call=user.id) | Visa_Info.objects.filter(Main_ID__icontains=str(request.data["Key"]).replace(' ',''),Call=user.id)
          else:
           manager =  Visa_Info.objects.filter(Contact__icontains=request.data["Key"]) | Visa_Info.objects.filter(Full_Name__icontains=request.data["Key"]) | Visa_Info.objects.filter(Email__icontains=request.data["Key"]) | Visa_Info.objects.filter(Main_ID__icontains=str(request.data["Key"]).replace(' ',''))
          notify = Notifications.objects.filter(User=user.id)
          hm = []
          for i in manager:
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3

             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"City":i.City,"Address":i.Address,"Week":x,"Type":p,"Call":am,"Stat":cc,"Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Seen":i.Seen,'Main':i.Main_ID,"SEP":i.SEP
             })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          side_perm = {
             'id':'No',
            'Status_Change':'Yes',
            'Call_Log':'Yes',
            'Book_Client':'Yes',
            'Interview':'Yes',
            'Chat_Files':'No',
            'Profile':'No',
            'Cv':'Yes',
            'Payment':'Yes',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'Yes',
            'Opperation':'No',

              }
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Admins":adm,"Note":'All',"Count":manager.count(),"Interview":inter,"Q":ql,"Side_Bar":side_bar,'Permission':get_permission(user.id),'Side_Perm':side_perm}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')




class Add_Call_Logs(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)

          busy =0
          next =0
          picked =0
          ans = 0
          mem = Visa_Info.objects.get(id=pk)
          if user.Account == '0':
           calls = Call_Logs.objects.filter(Member=pk)
          else:
           calls = Call_Logs.objects.filter(User=user.id,Member=pk)
          for i in calls:
              if i.Status == "Picked Up":
                  picked+=1
              elif i.Status == "Rescheduled":
                  next+=1
              elif i.Status == "Unanswered":
                  ans+=1

              else:
                  busy+=1


          context = {"Data":user,"Rand":rand,"Member":mem,"Calls":calls,"Total":calls.count(),"Busy":busy,'Answer':ans,"Next":next,"Picked":picked,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/profiles.html",context)
      else:
         return redirect("login")


    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          mem = Visa_Info.objects.get(id=pk)
          if req["Audio"] == '':
            Call_Logs.objects.create(
                Name=mem.Full_Name,User=user.id,Agent=0,Member=pk,About=req["About"],Status=req["Status"],
                Contact=mem.Contact,Location=mem.Address,Gender=mem.Gender,
                Start_Time=req["Start_Time"],End_Time=req["End_Time"],Type="Text"
            )
          else:
            call = Call_Logs.objects.create(
                Name=mem.Full_Name,User=user.id,Member=pk,Agent=0,About=req["About"],Status=req["Status"],
                Contact=mem.Contact,Location=mem.Address,Gender=mem.Gender,
                Start_Time=req["Start_Time"],End_Time=req["End_Time"],Type="Audio"
            )
            uploading_file = request.FILES['Audio']
            fs = FileSystemStorage()
            fs.save("Call_Logs//"+str(call.id)+".mp3",uploading_file)


          return redirect(reverse('add_call_logs',kwargs={"pk":pk}))
      else:
         return redirect("login")
    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)
          try:
            os.remove(f'{BASE_DIR}/media/Call_Logs/{req["id"]}.mp3')
          except:
             pass
          Call_Logs.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')



class Update_Theme(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          response =Response('Ok')
          r = request.data
          print(r["Value"])
          response.set_cookie(r["Type"],r["Value"])

          return response
      else:
         return Response('No')


class Job_View(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')

   #   print(data)
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          ap = Visa_Info.objects.filter(Link=pk)
          job = Job.objects.get(id=pk)



          context = {"Data":user,"Jobs":ap,"Job":job,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/package-select.html",context)
      else:
         return redirect("login")


class Job_Pannel_Manage(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          j = []

          jobs = Job.objects.all()
          for i in jobs:
            ls = Share_Link.objects.filter(User=user.id,Job=i.id)
            if ls.count() > 0:
              m = ls.last().Link
            else:
              m= "Null"

            j.append({
                "id":i.id,"Full_Name":i.Title,"date":i.date,"Min_Salary":i.Min_Salary,"Max_Salary":i.Max_Salary,"Link":m
                })
          context = {"Data":user,"Listed":j,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/view_package.html",context)
      else:
         return redirect("login")
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          r = request.data
          Job.objects.get(id=r["id"]).delete()
          try:
            os.remove(f'{BASE_DIR}/media/Jobs/{r["id"]}.jpg')
          except:
             pass

          return Response('Ok')
      else:
         return Response('Error')

class Job_Pannel(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          context = {"Data":user,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/package.html",context)
      else:
         return redirect("login")

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          r = request.data
          try:
              r["Check"]
              check = "Yes"
          except:
              check = "No"

          current_time = strftime("%H-%M-%S")
          uid =f'{str(uuid.uuid1())}-{str(current_time)}-{str(uuid.uuid1())[0:6]}'
          job = Job.objects.create(User=user.id,Title=r["Title"],Experience=r["Experience"],
                                   About=r["About"],Max_Salary=r["Max_Salary"],Min_Salary=r["Min_Salary"],
                                   Type=r["Type"],View_Salary=check,Link=uid,Group=r["Group"]
                                   )
          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Jobs//"+str(job.id)+".jpg",uploading_file)
          for i in r:
              if i[:2] == "RN":
                Job_Role.objects.create(Job=job.id,About=r[i])
              elif i[:2] == "SN":
                  Job_Skills.objects.create(Job=job.id,About=r[i])
              elif i[:2] == "BN":
                  Job_Benefits.objects.create(Job=job.id,About=r[i])
              print(i)
          return redirect('job_pannel_manage')
      else:
         return redirect("login")







class Manager_Account_Group_Filter_Region(APIView):
    def post(self , request, pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          r = request.data
          side_perm = Side_Menu.objects.get(id=pk)
          rand = random.randint(0,1000)
          if side_perm.Name == "All":
              manager =  Visa_Info.objects.filter(City=r["Key"])
          else:
              manager =  Visa_Info.objects.filter(Group=side_perm.Name,City=r["Key"])

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")

             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,'Main':i.Main_ID,"Email":i.Email,"Group":i.Group,"City":i.City,"Address":i.Address,"Week":x,"Type":p,"Call":am,"Stat":cc
                ,"Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Seen":i.Seen,"SEP":i.SEP,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
             })


          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":side_perm.Name,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Admins":adm,'page_obj': page_obj,"Count":manager.count(),"Interview":inter,"Q":ql,'Side_Perm':side_perm}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')







class Manager_Account_Group_Filter(APIView):
    def post(self , request, pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          r = request.data
          side_perm = Side_Menu.objects.get(id=pk)
          rand = random.randint(0,1000)
          if side_perm.Name == "All":
            if int(user.Account) == 1:
              manager =  Visa_Info.objects.filter(Call=user.id)
            else:
              manager =  Visa_Info.objects.all()
          else:
            if int(user.Account) == 1:
              manager =  Visa_Info.objects.filter(Group=side_perm.Name,Call=user.id)
            else:
              manager =  Visa_Info.objects.filter(Group=side_perm.Name)

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0


             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=r["Date"])
             if t.count() > 0:
               cc = "Called"
             else:
               cc="Not Called"
             if t.count() < 1 :
              if r["Key"] == "Not Called" :
               hm.append({
                "Full_Name":i.Full_Name,"SEP":i.SEP,"id":i.id,"date":i.date,"City":i.City,'Main':i.Main_ID,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p
                ,"Call":am,"Stat":cc,"Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Address":i.Address,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
               })
             else:
              if "Called" == r["Key"]:
                hm.append({
                "Full_Name":i.Full_Name,"SEP":i.SEP,"id":i.id,"date":i.date,"City":i.City,'Main':i.Main_ID,"Contact":i.Contact,"Email":i.Email,
                "Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,"Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Address":i.Address,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
               })
              else:
               if t.last().Status == r["Key"]:
                hm.append({
                "Full_Name":i.Full_Name,"SEP":i.SEP,"id":i.id,"date":i.date,"City":i.City,'Main':i.Main_ID,"Contact":i.Contact,"Email":i.Email
                ,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,"Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Address":i.Address,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
               })


          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":side_perm.Name,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Admins":adm,'page_obj': page_obj,"Count":manager.count(),"Interview":inter,"Q":ql,'Side_Perm':side_perm}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

#Visa_Info.objects.filter(City=None).update(City='Greater_Accra')
#City__in=main_list


class Manager_Account_Group(APIView):
    def get(self , request, pk,pk2):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          main_list = []
          side_perm = Side_Menu.objects.get(id=pk)

          regions = [
            'Ashanti', 'Bono', 'Bono_East', 'Central', 'Eastern',
            'Greater_Accra', 'Northern', 'North_East', 'Oti',
            'Savannah', 'Upper_East', 'Upper_West', 'Volta',
            'Western', 'Western_North', 'Ahafo'
          ]


          for region in regions:
                if getattr(user, region) == "Yes":
                    main_list.append(str(region).replace('_',' '))

          rand = random.randint(0,1000)
          if int(user.Account) == 5:

            manager =  Visa_Info.objects.filter(Group=side_perm.Name,SEP=pk2)
          elif int(user.Account) == 2:
              #if side_perm.Name == "Booked":
              # manager =  Visa_Info.objects.filter(Group=side_perm.Name,SEP=pk2)
              #else:
               manager =  Visa_Info.objects.filter(Group=side_perm.Name,SEP=pk2,Call=user.id)
          else:
            manager =  Visa_Info.objects.filter(Group=side_perm.Name,SEP=pk2,Call=user.id)
          if pk2 == "All":
           if int(user.Account) == 5:
            manager = Visa_Info.objects.filter(Group=side_perm.Name).exclude(SEP__in=['S.E.P','Study Program','Business Travel','Tourist' ])
           else:
             manager = Visa_Info.objects.filter(Group=side_perm.Name,Call=user.id).exclude(SEP__in=['S.E.P','Study Program','Business Travel','Tourist' ])

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)

          for i in page_obj:

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0

             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"




             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,'Main':i.Main_ID,
                "Group":i.Group,"City":i.City,"Address":i.Address,"Week":x,"Type":p,"Call":am,"Stat":cc,
                "Contact_Email":i.Contact_Email,"Contact_Email_Password":i.Contact_Email_Password,"Seen":i.Seen,"SEP":i.SEP
                ,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
             })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()


          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":side_perm.Name,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Admins":adm
            ,"Interview":inter,"Count":manager.count(),'page_obj': page_obj,"Count":manager.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')




class Manager_Account_Group_Region(APIView):
    def get(self , request, pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          if int(user.Account) == 1:
            manager =  Visa_Info.objects.filter(City=pk,Call=user.id)
          elif int(user.Account) == 2:
              if pk == "Booked":
               manager =  Visa_Info.objects.filter(City=pk)
              else:
               manager =  Visa_Info.objects.filter(City=pk,Call=user.id)


          else:
            manager =  Visa_Info.objects.filter(City=pk)

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")



             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,'Main':i.Main_ID,"Email":i.Email,"Group":i.Group,
                "City":i.City,"Address":i.Address,"Week":x,"Type":p,"Call":am,"Stat":cc,"Contact_Email":i.Contact_Email,
                "Contact_Email_Password":i.Contact_Email_Password,"Seen":i.Seen,"SEP":i.SEP,'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
             })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":pk,"Theme":admin_token["Theme"],"Color":admin_token["Color"],
            "Interview":inter,"Admins":adm,"Count":manager.count(),'page_obj': page_obj,"Count":manager.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')





class Update_Progress(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          try:
           find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
           user = Administrator_Info.objects.get(id=int(find.User))
           r = request.data

           c = Visa_Info.objects.get(id=r["id"])

           Status_Logs.objects.create(User=user.id,Client=r["id"],Old=c.Group,New=r["Status"])
           Visa_Info.objects.filter(id=r["id"]).update(Group=r["Status"])
           if r["Status"] == "S.E.P":
               Visa_Info.objects.filter(id=r["id"]).update(SEP=r["Status"])

           return Response('Ok')
          except:
           return Response('No')
      else:
         return Response('No')




def Check_Status(order_id):
   # try:
        data = Status_Logs.objects.get(id=order_id)
        order_date = data.date
        current_date = datetime.now().date()
        days_difference = (current_date - order_date).days
        return days_difference


class Movement_Issued(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
     #    try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          total = 0
          day = 0
          week = 0
          month = 0
          rand = random.randint(0,1000)
          main = Status_Logs.objects.all()
          #------------------------------------ counter -------------------------------
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Status_Logs.objects.filter(date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Status_Logs.objects.filter(date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Status_Logs.objects.filter(date__gte=last_month_start).count()
          #------------------------------------ counter -------------------------------

          paginator = Paginator(main, 50)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)

          listed = []
          for i in page_obj:


              staff = Administrator_Info.objects.get(id=i.User)
              client = Visa_Info.objects.get(id=i.Client)
              listed.append({
              "id":i.id,"Staff_id":staff.id,"Staff_Name":staff.Full_Name,"date":i.date,"time":i.time,"Client_id":client.id,"Client_Name":client.Full_Name,"Old":i.Old,"New":i.New
              })
          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":listed,
            "Theme":admin_token["Theme"],"Color":admin_token["Color"],"Day":val_today,"Week":val_last_week,"Month":val_last_month,"Total":main.count(),'page_obj':page_obj
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list_movements.html", context)
        # except:
        #   return redirect('admin_login')
      else:
         return redirect('admin_login')








class Manager_Paid(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          manager =  Visa_Info.objects.all()
          notify = Notifications.objects.filter(User=user.id)
          client = Visa_Info.objects.get(id=pk)
          deb = Funds_info.objects.filter(Status = "Recieved",User=client.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":manager,"Client":client,"Debit":deb,"Theme":admin_token["Theme"],"Color":admin_token["Color"]
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/paid.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')


class Manager_Debit(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          manager =  Visa_Info.objects.all()
          notify = Notifications.objects.filter(User=user.id)
          client = Visa_Info.objects.get(id=pk)
          deb = Debit_info.objects.filter(User=client.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":manager,"Client":client,"Debit":deb,"Theme":admin_token["Theme"],"Color":admin_token["Color"]
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/debit.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')
    def post(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          Debit_info.objects.create(User=pk,Amount=request.data["Amount"])



          return redirect(reverse('manager_debit',kwargs={"pk":pk}))
         #except:
          # return redirect('admin_login')
      else:
          return redirect('admin_login')


class Delete_Debit(APIView):
    def delete(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Debit_info.objects.get(id=int(request.data["id"])).delete()

          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')


#=============================================== Home Page =================================================

class Administrator_Dashboard(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      #thread = threading.Thread(target=duplicate_data)
      #thread.start()
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         side_bar = Side_Menu.objects.all().order_by('Level')
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          current_date = strftime("%Y-%m-%d")
          current_time = strftime("%I:%M %p")
          rand = random.randint(0,1000)


          total = Visa_Info.objects.all().order_by('id').reverse()

          total1 = Visa_Info.objects.filter(Group="Ready").count()
          total2 = Visa_Info.objects.filter(Group="New Applicant").count()

          total3 = Visa_Info.objects.filter(Group="Pending").count()

          total4 = Visa_Info.objects.filter(Group="Declined").count()
          total5 = Visa_Info.objects.filter(Group="Active").count()




          p = ((total3+total4)/(total.count()))*100
          all_t = (total3+total4)

          money = Funds_info.objects.filter(Status = "Recieved")
          job= Job.objects.all().count()
          bill = Billings.objects.all().count()
          pay_list =[]
          pay = Funds_info.objects.filter(Status = "Recieved").order_by('id').reverse()[0:5]
          for i in pay:
            pr = Visa_Info.objects.get(id=i.User)
            pay_list.append({
              "id":i.User,"Amount":i.Amount,"time":i.time,"date":i.date,"Name":pr.Full_Name,"Contact":pr.Contact,"Status":i.Status
            })

          profit = 0
          for i in money:

              profit+=i.Amount

          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Users":total[0:10],
           "Notify":notify,
            "Total":total.count(),"Funds":money.count(),"Ready":total1,"New":total2,
            "Date":current_date,"Time":current_time,"Profit":round(profit,3),"Pay":pay_list
            ,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Ini":money.count(),"Package":job,"Bill":bill,
            "Per":round(p,2),"All_T":all_t,"Decliend":total4,"Pending":total3,"Active":total5
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id),"Side_Bar":side_bar,'Permission':get_permission(user.id)

            }
          return render(request , "New/index.html", context)
         except:
          return render (request, 'Administrator/pages/samples/error-401.html')
      else:
         return redirect('admin_login')
#=============================================== Home Page =================================================


#================================================ Login =======================================================

class Administrator_Login(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          return redirect('admin_dashboard')
         except:
           return render(request , "New/login.html")
      else:
         return render(request , "New/login.html")

    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try:
          data = Administrator_Info.objects.get(Email=request.data['Email'], Password=request.data['Password'])

          response =  redirect('admin_dashboard')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Admin")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Admin")
          response.set_cookie('csrf-admin-token',generated_uuid)
          Notifications.objects.create(Type = "Login",User = data.id,Name = "Login Prompt!", Info=f"You have successfully logged in on {current_time}.",Link = "#")
          return response
       except:
         return render (request, 'Administrator/pages/samples/error-404.html')


class Administrator_Logout(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      response = redirect("admin_login")
      response.delete_cookie('csrf-admin-token')

      return response

#================================================ Login =======================================================



def Check_transaction(id):
   #---------------------------------------- Subscription ---------------------------------------------
          data = Funds_info.objects.get(id=id)
          current_date = strftime("%Y-%m-%d")
          years = (int(str(current_date).split("-")[0]) - int(str(data.date).split("-")[0]))*356
          months = (int(str(current_date).split("-")[1]) - int(str(data.date).split("-")[1]))*30
          days = (int(str(current_date).split("-")[2]) - int(str(str(data.date).split("-")[2]).split(" ")[0]))
          result = years+months+days
          print(result)
          return(result)


class Payments_Issued(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
     #    try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          total = 0
          day = 0
          week = 0
          month = 0
          rand = random.randint(0,1000)
          main = Funds_info.objects.filter(Status = "Recieved")
          main2 = Funds_info.objects.all()
          listed = []
          for i in main:
              if Check_transaction(i.id) < 1:
                  day+=i.Amount
                  total +=i.Amount
              elif Check_transaction(i.id) < 7  :
                  week+=i.Amount
                  total +=i.Amount
              elif Check_transaction(i.id) < 30  :
                  month+=i.Amount
                  total +=i.Amount
              else:
                  total +=i.Amount
          for i in main2:
            try:
             vendor = Visa_Info.objects.get(id=i.User)
             n = vendor.Full_Name
             idd = vendor.id
             cc= vendor.Contact
            except:
              n= "Deleted Member"
              idd = 0
              cc = "Deleted Member"
            listed.append({
              "id":i.id,"Amount":i.Amount,"date":i.date,"Name":n,"Image":idd,"Status":i.Status,"Type":cc,"time":i.time
            })
          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":listed,
            "Theme":admin_token["Theme"],"Color":admin_token["Color"],"Day":day,"Week":week,"Month":month,"Total":total,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/payments.html", context)
        # except:
        #   return redirect('admin_login')
      else:
         return redirect('admin_login')





#================================================== Account Code ============================================================


class Client_Password(APIView):

    def post(self , request):
       if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
     #    try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          r = request.data

          Visa_Info.objects.filter(id=r['id']).update(Password = r['Password'])
          return Response('Ok')
       return Response('Error')


#=============================================== Profile Page =================================================

class Manager_Profile(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
         #try:
          admin_token = admin_get(request)
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          user = SignUp_info.objects.get(id=int(find.User))
          if user.Verify == "Yes":
             pass
          else:
            return redirect('manager_verify')
          current_date = strftime("%Y-%m-%d")
          rand = random.randint(0,1000)

          notify = Notifications.objects.filter(User=user.id)

          context = {"Data":user,"Rand":rand,"Notify":notify,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "Manager/manager_profile.html", context)
       #  except:
      #     return render (request, 'Administrator/pages/samples/error-401.html')
      else:
         return redirect('manager_login')
    def post(self , request):
       if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
       #  try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          user = Visa_Info.objects.get(id=int(request.data["User"]))

          #current_date = strftime("%Y-%m-%d")
          Visa_Info.objects.filter(id= user.id).update(
             Name = request.data['Name'],
             Birth= request.data['Birth'],
             Email=request.data['Email'],
             City=request.data['City'],

             Adress = request.data['Address'],
             Contact = request.data['Contact'],
             Skill=request.data["Skill"],
             Experience=request.data["Experience"],
             Education=request.data["Education"],
             Skill_Level=request.data["Skill_Level"],


                   )
          #-----------------------------------------------
          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/User_Imgs/{user.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Profiles//"+str(user.id)+".jpg",uploading_file)
          #-----------------------------------------------

          #-----------------------------------------------
          if request.data["New_Img1"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(request.data["Extra_1"])
           except:
             ex = Extra_Images.objects.create(Type="Profile",Profile=user.id)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)
          #-----------------------------------------------


          return redirect('manager_profile')
       #  except:
         # return render (request, 'Administrator/pages/samples/error-401.html')
       else:
         return redirect('manager_login')


class Visitors(APIView):
    def post(self , request):

           D = request.data

           check = Traffic.objects.filter(Ip_Address =D["Address"])
           if check.count() > 0:
              pass
           else:
             Traffic.objects.create(Ip_Address=D["Address"],City=D["City"],Region=D["Region"],Country=D["Country"],Coordinate=D["Coordinate"])
           return Response('ok')

       # except:
        #   return Response('No')



#=============================================== Profile Page =================================================


class Lottery_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          manager =  Lottery_Info.objects.filter(Validate="Validated")
          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":manager,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "Administrator/pages/tables/lottery.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')
#================================================== Tables ============================================================

class Manager_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          side_perm = {
             'id':'No',
            'Status_Change':'Yes',
            'Call_Log':'Yes',
            'Book_Client':'Yes',
            'Interview':'Yes',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'Yes',
            'Opperation':'No',

              }





          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Call=user.id)
          else:
           manager =  Visa_Info.objects.all()

         # manager =  Visa_Info.objects.filter(City=)

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Main':i.Main_ID
             })
          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],
            "Interview":inter,"Admins":adm,"Count":manager.count(),"Note":"All",'page_obj': page_obj,"Count":manager.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Visa_Info.objects.get(id=int(request.data["id"])).delete()
          try:
               os.remove(f'{BASE_DIR}/media/Profiles/{request.data["id"]}.jpg')
          except:
              pass
          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')


#______________________________________________________________________________________________________



#______________________________________________________________________________________________________


#================================================== Table ============================================================


class Add_Bill(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          rand = random.randint(0,1000)
          notify = Notifications.objects.filter(User=user.id)
          bill = Billings.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":bill,
            "Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/bill.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")

          bill = Billings.objects.create(
             Name = request.data['Name'],
             Price = request.data['Price']
                   )
          return Response({"Stat":'Ok',"Data":{"Date":bill.date,"Time":bill.time,"Id":bill.id}})
         except:
             return Response({"Stat":'No'})
      else:
          return Response({"Stat":'No'})

    def put(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          Billings.objects.get(id=request.data["id"]).delete()
          return Response('OK')
         except:
             return Response('No')
      else:
          return Response('No')

#=================================================== Edit ===========================================================
class Manager_Edit(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          manager =  Visa_Info.objects.get(id=pk)
          notify = Notifications.objects.filter(User=user.id)
          profiles = Extra_Images.objects.filter(Profile=pk,Type="Profile")
          ids = Extra_Images.objects.filter(Profile=pk,Type="Id")
          id = []
          count= 1
          for i in ids:
            id.append({
              f"id_{count}":i.id
                }
            )
            count +=1
          print(id)
          images = []
          count= 1
          for i in profiles:
            images.append({
              f"id_{count}":i.id
                }
            )
            count +=1
          edu = Extra_Info.objects.filter(Profile=pk,Type="School")
          work = Extra_Info.objects.filter(Profile=pk,Type="Work")
          bills = Billings.objects.all().order_by('id').reverse()
          client_bills = Client_Billing.objects.filter(User=pk).order_by('id').reverse()
    #      print(new_list)
          L_1 = Completed_Logs.objects.filter(Client=pk,Type='1').count()
          L_2 = Completed_Logs.objects.filter(Client=pk,Type='2').count()
          L_3 = Completed_Logs.objects.filter(Client=pk,Type='3').count()

          if L_1 > 0:
              L_V1 = 'Yes'
          else:
              L_V1 = 'No'
          if L_2 > 0:
              L_V2 = 'Yes'
          else:
              L_V2 = 'No'
          if L_3 > 0:
              L_V3 = 'Yes'
          else:
              L_V3 = 'No'


          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Staff":manager,"Education":edu,"Work":work,
            "Extra":images,"ID":id,"Listed":client_bills,"Bills":bills,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)
            ,'P1':L_V1,'P2':L_V2,'P3':L_V3,
            }
          return render(request , "New/profile.html", context)
       #  except:
        #   return render (request, 'New/profile.html')

      else:
         return redirect('admin_login')

    def post(self , request,pk):

      if 'csrf-admin-token' in request.COOKIES:
          print('2')
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
          print('2')
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          print('2')
        #  print(request.data)
          Visa_Info.objects.filter(id= pk).update(
             Full_Name = request.data['Full_Name'],
             Birth= request.data['Birth'],
             Email=request.data['Email'],
             City=request.data['City'],
             Address = request.data['Address'],
             Contact = request.data['Contact'],
             Skill=request.data["Skill"],
             Experience=request.data["Experience"],
             Education=request.data["Education"],
             Skill_Level=request.data["Skill_Level"],
             Marital=request.data['Marital'],

             Job_Choice1=request.data['Job_Choice1'],
             Country1=request.data['Country1'],
             Job_Choice2=request.data['Job_Choice2'],
             Country2=request.data['Country2'],
             Job_Choice3=request.data['Job_Choice3'],
             Country3=request.data['Country3'],



             Garantor_Full_Name = request.data['Garantor_Name'],
             Garantor_Email=request.data['Garantor_Email'],
             Garantor_City=request.data['Garantor_City'],
             Garantor_Address = request.data['Garantor_Address'],
             Garantor_Contact = request.data['Garantor_Contact'],
             Garantor_Gender = request.data['Garantor_Gender'],



             Garantor_Birth = request.data['Garantor_Birth'],
             Garantor_ID = request.data['Garantor_ID'],
             Garantor_Job = request.data['Garantor_Job'],
             Garantor_Title = request.data['Garantor_Title'],
             Garantor_Job_Address = request.data['Garantor_Job_Address'],
             Garantor_Job_Contact = request.data['Garantor_Job_Contact'],
             Garantor_House = request.data['Garantor_House'],
             Garantor_Street = request.data['Garantor_Street'],
             Garantor_Landmark = request.data['Garantor_Landmark'],
             Garantor_Gps = request.data['Garantor_Gps'],



             Father_Full_Name = request.data['Father_Name'],
             Father_Birth=request.data['Father_Birth'],
             Father_City=request.data['Father_City'],
             Father_Address = request.data['Father_Address'],
             Father_Contact = request.data['Father_Contact'],

             Mother_Full_Name = request.data['Mother_Name'],
             Mother_Birth=request.data['Mother_Birth'],
             Mother_City=request.data['Mother_City'],
             Mother_Address = request.data['Mother_Address'],
             Mother_Contact = request.data['Mother_Contact'],


             Reference1_Full_Name = request.data['Reference1_Name'],
             Reference1_Job=request.data['Reference1_Job'],
             Reference1_Address = request.data['Reference1_Address'],
             Reference1_Contact = request.data['Reference1_Contact'],

             Reference2_Full_Name = request.data['Reference2_Name'],
             Reference2_Job=request.data['Reference2_Job'],
             Reference2_Address = request.data['Reference2_Address'],
             Reference2_Contact = request.data['Reference2_Contact'],

             Reference3_Full_Name = request.data['Reference3_Name'],
             Reference3_Job=request.data['Reference3_Job'],
             Reference3_Address = request.data['Reference3_Address'],
             Reference3_Contact = request.data['Reference3_Contact'],
             Password = request.data['Password'],




             Height = request.data['Height'],
             Hair = request.data['Hair'],
             Eye = request.data['Eye'],
             Birth_City = request.data['Birth_City'],
             Country_Birth = request.data['Country_Birth'],
             Postal_Code = request.data['Postal_Code'],

             Country_Recidence = request.data['Country_Recidence'],
             Postal_Code_Recidence = request.data['Postal_Code_Recidence'],

             Father_Living = request.data['Father_Living'],
             Mother_Living = request.data['Mother_Living'],

             Birth_Address = request.data['Birth_Address'],



             Weight = request.data['Weight'],
             Card_Id = request.data['Card_Id'],
             Gender=request.data['Gender'],








                   )





          #------------------------------------------------------------------------------------------------------
          print('2')
          Extra_Info.objects.filter(Profile=pk).delete()
          school = []
          school_start = []
          school_end = []

          work = []
          work_start =[]
          work_end = []


          for i in request.data:
            val = str(i).split('_')[0]
            print(val)
            if val == "School":
              school.append(request.data[i])
            elif val == "Commence":
              school_start.append(request.data[i])
            elif val == "Complete":
                school_end.append(request.data[i])
            elif val== "Work":
                work.append(request.data[i])
            elif val == "CommenceComp":
                work_start.append(request.data[i])
            elif val == "CompleteComp":
                work_end.append(request.data[i])

          print(school)
          c = 0
          for i in school:
            Extra_Info.objects.create(Profile=pk,Type="School",Name=i,Start=school_start[c],End=school_end[c])
            c += 1
          c = 0
          for i in work:
            Extra_Info.objects.create(Profile=pk,Type="Work",Name=i,Start=work_start[c],End=work_end[c])




          #------------------------------------------------------------------------------------------------------
          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/Profiles/{pk}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Profiles//"+str(pk)+".jpg",uploading_file)
          #-----------------------------------------------

          #-----------------------------------------------
          if request.data["New_Img1"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_1"])
           except:
             ex = Extra_Images.objects.create(Type="Profile",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img1']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)
          #--------------------------------------------------



          #-----------------------------------------------
          if request.data["New_Img2"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_2"])
           except:
             ex = Extra_Images.objects.create(Type="Profile",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img2']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)
          #--------------------------------------------------



          #-----------------------------------------------
          if request.data["New_Img3"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_3"])
           except:
             ex = Extra_Images.objects.create(Type="Profile",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img3']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)
          #--------------------------------------------------

           #-----------------------------------------------
          if request.data["New_Img4"] == '':
           pass
          else:

           try:
            os.remove(f'{BASE_DIR}/media/Ids/{pk}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img4']
           fs = FileSystemStorage()
           fs.save("Ids//"+str(pk)+".jpg",uploading_file)
          #--------------------------------------------------

          #-----------------------------------------------
          if request.data["New_Img5"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_4"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img5']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)

          if request.data["New_Img6"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_5"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img6']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)

          if request.data["New_Img7"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_7"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img7']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)

          if request.data["New_Img8"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_8"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img8']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)

          if request.data["New_Img9"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_9"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img9']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)

          if request.data["New_Img10"] == '':
           pass
          else:
           try:
             ex = Extra_Images.objects.get(id=request.data["Extra_10"])
           except:
             ex = Extra_Images.objects.create(Type="Id",Profile=pk)
           try:
            os.remove(f'{BASE_DIR}/media/Extra/{ex.id}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img10']
           fs = FileSystemStorage()
           fs.save("Extra//"+str(ex.id)+".jpg",uploading_file)
          #--------------------------------------------------


          return redirect(reverse('manager_edit',kwargs={"pk":pk}))
         #except:
           #  return render (request, 'Administrator/pages/samples/error-401.html')

      else:
          return redirect('admin_login')
    def put(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          data_bill = Billings.objects.get(id=request.data['id'])
          bill = Client_Billing.objects.create(
             User =pk,Name=data_bill.Name,Price=data_bill.Price
                   )
          return Response({"Stat":'Ok',"Data":{"Date":bill.date,"Time":bill.time,"Id":bill.id,"Name":data_bill.Name,"Price":data_bill.Price}})
         except:
             return Response({"Stat":'No'})
      else:
          return Response({"Stat":'No'})

    def delete(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          Client_Billing.objects.get(id=request.data["id"]).delete()
          return Response('OK')
        # except:
       #      return Response('No')
      else:
          return Response('No')

#______________________________________________________________________________________________________



    def update(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          data = request.data
          File_Link.objects.filter(Post = pk).update(Link=data["Link"])
          return redirect('staff_account')
         except:
             return render (request, 'Administrator/pages/samples/error-401.html')

      else:
          return redirect('admin_login')

#______________________________________________________________________________________________________



#----------------------------------------- Traffic ----------------------------------------------

class Traffic_Table(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
     #    try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          listed = Traffic.objects.all()
          paginator = Paginator(listed, 100)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)


          notify = Notifications.objects.filter(User=user.id)

          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":page_obj,"page_obj":page_obj,"Count":listed.count(),"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/traffic-list.html", context)
        # except:
        #   return redirect('admin_login')
      else:
         return redirect('admin_login')

class Traffic_Graph(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
     #    try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          listed1 = Traffic.objects.all()
          data = []
          for i in listed1:
            data.append({
              "name":i.City
            })

          grouped_data = defaultdict(list)
          for item in data:
            key = tuple(item.items())
            grouped_data[key].append(item)
          grouped_data = dict(grouped_data)
          listed = []
          for key, values in grouped_data.items():
           listed.append({
         "Location":values[0]["name"],"Count":len(values)
           })

          print(listed)
          rand = random.randint(0,1000)
          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":listed,"Count":listed1.count(),"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/traffic.html", context)
        # except:
        #   return redirect('admin_login')
      else:
         return redirect('admin_login')



class Applied_List(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)
          apply =  Visit.objects.all()

          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":apply,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "Administrator/pages/tables/visit.html", context)
        # except:
         #  return render (request, 'Administrator/pages/samples/error-401.html')
      else:
         return redirect('admin_login')



class Master_Class_Confirm(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          stat = Visit.objects.get(id= request.data["id"])
          if stat.Confirmation == "Yes":
           Visit.objects.filter(id= request.data["id"]).update(Confirmation="No")


           visit = "No"
          else:
            Visit.objects.filter(id= request.data["id"]).update(Confirmation="Yes")
            visit = "Yes"
          return Response({"id":visit,"Stat":"Ok"})
         except:
           return Response({"Stat":"Error"})
      else:
          return Response({"Stat":"Error"})


class Master_Class_Attend(APIView):
    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          stat = Visit.objects.get(id= request.data["id"])
          if stat.Attended == "Yes":
           Visit.objects.filter(id= request.data["id"]).update(Attended="No")
           visit = "No"
          else:
            Visit.objects.filter(id= request.data["id"]).update(Attended="Yes")
            visit = "Yes"
          return Response({"id":visit,"Stat":"Ok"})
         except:
           return Response({"Stat":"Error"})
      else:
          return Response({"Stat":"Error"})

#--------------------------------------------------- Recure ----------------------------------------------------


















class Add_Interviewer(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/add_interviewer.html",context)
      else:
         return redirect("login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          tp = Interview_Account.objects.filter(Email=req["Email"]).count()
          if tp > 0:
              return render(request, 'New/authentication-error.html')

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Interview_Account.objects.create(
              Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
              Contact=req["Contact"],Password="pass",Country=req["Country"],

          )
          #------------------------------------------------------------


          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Interview//"+str(branch.id)+".jpg",uploading_file)
          return redirect('add_interviewer')
          #return redirect(reverse('view_Staff_account',kwargs={"pk":int(branch.id)}))
      else:
         return redirect("login")




class Edit_Interviewer(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          staff = Interview_Account.objects.get(id =pk)



          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Staff":staff,"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/edit_interviewer.html",context)
      else:
         return redirect("login")

    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Interview_Account.objects.filter(id=pk).update(
            Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
            Contact=req["Contact"],Password=req["Password"],Country=req["Country"],

          )


          #------------------------------------------------------------

          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/Interview/{pk}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Interview//"+str(pk)+".jpg",uploading_file)


          return redirect(reverse('edit_interviewer',kwargs={"pk":pk}))
      else:
         return redirect("login")





class Manager_Interview_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)

          manager =  Interview_Account.objects.all()

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:


             hm.append({
                "Full_Name":i.Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Location":i.Location,
             })

          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Note":"Staff List",'page_obj': page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list_interviewer.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Interview_Account.objects.get(id=int(request.data["id"])).delete()
          try:
               os.remove(f'{BASE_DIR}/media/Interview/{request.data["id"]}.jpg')
          except:
              pass
          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')





class Manager_Questions(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)

          manager =  Question_Group.objects.all()

          notify = Notifications.objects.filter(User=user.id)
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)

          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":manager,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Note":"Staff List",'page_obj': page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list_question.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")

          Question_Group.objects.create(User=user.id,Name=request.data["Name"],About=request.data["About"],Status=request.data["Status"])

          return redirect("manager_questions")
         except:
           return redirect('admin_login')
      else:
          return Response('Error')
    def delete(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Question_Group.objects.get(id=int(request.data["id"])).delete()

          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')




class Manager_Questions_View(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)

          main =  Question_Group.objects.get(id=pk)
          manager =  Question.objects.filter(Group=pk)
          notify = Notifications.objects.filter(User=user.id)
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Main":main,"Listed":manager,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/questions.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")

          Question.objects.create(Group=pk,Question=request.data["Question"])



          return redirect(reverse('manager_questions_view',kwargs={"pk":pk}))
         except:
           return redirect('admin_login')
      else:
          return Response('Error')
    def delete(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Question.objects.get(id=int(request.data["id"])).delete()

          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')





















class Manager_Edit_Update(APIView):


    def post(self , request):

      if 'csrf-admin-token' in request.COOKIES:
         print('2')
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         print('2')
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")

          Visa_Info.objects.filter(id=request.data['id']).update(
             Full_Name = request.data['Full_Name'],
             Birth= request.data['Birth'],
             Email=request.data['Email'],
             City=request.data['City'],
             Address = request.data['Address'],
             Contact = request.data['Contact'],
             Skill=request.data["Skill"],
             Experience=request.data["Experience"],

             Skill_Level=request.data["Skill_Level"],
             Marital=request.data['Marital'],

             Job_Choice1=request.data['Job_Choice1'],
             Country1=request.data['Country1'],
             Job_Choice2=request.data['Job_Choice2'],
             Country2=request.data['Country2'],
             Job_Choice3=request.data['Job_Choice3'],
             Country3=request.data['Country3'],
             Gender=request.data['Gender'],


             Height = request.data['Height'],
             Hair = request.data['Hair'],
             Eye = request.data['Eye'],
             Birth_City = request.data['Birth_City'],
             Country_Birth = request.data['Country_Birth'],
             Postal_Code = request.data['Postal_Code'],

             Country_Recidence = request.data['Country_Recidence'],
             Postal_Code_Recidence = request.data['Postal_Code_Recidence'],

             Birth_Address = request.data['Birth_Address'],



             Weight = request.data['Weight'],
             Card_Id = request.data['Card_Id'],







                   )




          return Response('Ok')
         except:
             return Response('Ok')

      else:
          return Response('No')



from datetime import datetime

from django.utils import timezone
from datetime import timedelta



def convert_to_am_pm(time_24hr):
    # Split the input into hours and minutes
    hours, minutes = map(int, time_24hr.split(":"))

    # Determine AM or PM
    period = "AM" if hours < 12 else "PM"

    # Convert hours to 12-hour format
    hours = hours % 12 or 12

    # Format the result
    return f"{hours}:{minutes:02d} {period}"



class Interview_Paged(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          intr = Interview_Account.objects.get(id = pk)
          rand = random.randint(0,1000)
          manager =  Interview_Session.objects.filter(User=pk)
          pd =  Interview_Session.objects.filter(User=pk,Status='Pending')
          cm =  Interview_Session.objects.filter(User=pk,Status='Completed')
          res =  Interview_Session.objects.filter(User=pk,Status='Rescheduled')
          ap =  Interview_Session.objects.filter(User=pk,Answer='Accepted')
          dc =  Interview_Session.objects.filter(User=pk,Answer='Rejected')
          res1 =  Interview_Session.objects.filter(User=pk,Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(User=pk,Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(User=pk,Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(User=pk,Status='Medicals Issues')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(User=pk,Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(User=pk,Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(User=pk,Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(User=pk,Answer='Rejected',Dated=current_date)
          cm_id = list(cm.values_list('id', flat=True))
          pd_id = list(pd.values_list('id', flat=True))
          res_id = list(res.values_list('id', flat=True))
          res1_id = list(res1.values_list('id', flat=True))
          res2_id = list(res2.values_list('id', flat=True))
          res3_id = list(res3.values_list('id', flat=True))
          res4_id = list(res4.values_list('id', flat=True))
          t_pd_id = list(t_pd.values_list('id', flat=True))
          t_cm_id = list(t_cm.values_list('id', flat=True))
          t_ap_id = list(t_ap.values_list('id', flat=True))
          t_dc_id = list(t_dc.values_list('id', flat=True))


          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': page_obj,'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':pk,'Rescheduled':res.count()
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id),'Inter':intr,'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),
            'T_Pending_id':t_pd_id,'All_Completed_id':cm_id,'All_Pending_id':pd_id,'T_Completed_id':t_cm_id,'T_Approved_id':t_ap_id,'T_Declined_id':t_dc_id,'Rescheduled_id':res_id,'Pending_Medicals_id':res1_id,'Missed_Interview_id':res2_id,'Incomplete_Medicals_id':res3_id,'Medicals_Issues_id':res4_id,}
          return render(request , "New/manage_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')






class Interview_Profile_Admin(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])



          inter =  Interview_Session.objects.get(id=int(pk))
          user = Visa_Info.objects.get(id=inter.Client)
          edu = Extra_Info.objects.filter(Profile=user.id,Type="School")
          work = Extra_Info.objects.filter(Profile=user.id,Type="Work")


          q = Question.objects.filter(Group=inter.Question)
          qm = Question_Group.objects.filter(id=inter.Question)

          c1 = Remarks.objects.filter(Group='Medical',Mark=int(inter.Medicals))
          c2 = Remarks.objects.filter(Group='Practical Experience',Mark=int(inter.Practical))
          c3 = Remarks.objects.filter(Group='Confidence',Mark=int(inter.Confidence))
          c4 = Remarks.objects.filter(Group='Knowledge',Mark=int(inter.Knowledge))
          c5 = Remarks.objects.filter(Group='Communication',Mark=int(inter.Communication))
          c6 = Remarks.objects.filter(Group='Commitment',Mark=int(inter.Commitment))
          context = {"Data":user,"Education":edu,"Work":work,'i':inter,'Q':q,'M':qm,"Side_Bar":side_bar,'Permission':get_permission(user.id),
          'C1':c1,'C2':c2,'C3':c3,'C4':c4,'C5':c5,'C6':c6,
          }
          return render(request, "Cv/cv.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")




class Interview_Paged_Filter(APIView):
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          intr = Interview_Account.objects.get(id = pk)
          rand = random.randint(0,1000)

          pd =  Interview_Session.objects.filter(User=pk,Status='Pending')
          cm =  Interview_Session.objects.filter(User=pk,Status='Completed')
          res =  Interview_Session.objects.filter(User=pk,Status='Rescheduled')
          ap =  Interview_Session.objects.filter(User=pk,Answer='Accepted')
          dc =  Interview_Session.objects.filter(User=pk,Answer='Rejected')
          res1 =  Interview_Session.objects.filter(User=pk,Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(User=pk,Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(User=pk,Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(User=pk,Status='Medicals Issues')
          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(User=pk,Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(User=pk,Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(User=pk,Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(User=pk,Answer='Rejected',Dated=current_date)
          cm_id = list(cm.values_list('id', flat=True))
          pd_id = list(pd.values_list('id', flat=True))
          res_id = list(res.values_list('id', flat=True))
          res1_id = list(res1.values_list('id', flat=True))
          res2_id = list(res2.values_list('id', flat=True))
          res3_id = list(res3.values_list('id', flat=True))
          res4_id = list(res4.values_list('id', flat=True))
          t_pd_id = list(t_pd.values_list('id', flat=True))
          t_cm_id = list(t_cm.values_list('id', flat=True))
          t_ap_id = list(t_ap.values_list('id', flat=True))
          t_dc_id = list(t_dc.values_list('id', flat=True))


          hm = []
          r = request.data
          try:
           manager =  Interview_Session.objects.filter(User=pk,Status=r["Status"],Dated__range=[r['Start'],r['End']])
          except:
            manager =  Interview_Session.objects.filter(User=pk,Status=r["Status"])
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in manager:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,'Rescheduled':res.count(),
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': [],'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':pk,'Inter':intr,'Rescheduled':res.count(),
            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),
            'T_Pending_id':t_pd_id,'All_Completed_id':cm_id,'All_Pending_id':pd_id,'T_Completed_id':t_cm_id,'T_Approved_id':t_ap_id,'T_Declined_id':t_dc_id,'Rescheduled_id':res_id,'Pending_Medicals_id':res1_id,'Missed_Interview_id':res2_id,'Incomplete_Medicals_id':res3_id,'Medicals_Issues_id':res4_id,
            }
          return render(request , "New/manage_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')





class Client_Media(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          i = Visa_Info.objects.get(id=pk)
          image = Message.objects.filter(Sender=pk,Type='Image')
          video = Message.objects.filter(Sender=pk,Type='Video')
          file = Message.objects.filter(Sender=pk,Type='File')


          context = {"Data":user,"Rand":rand,"Client":i,"Image":image,"Video":video,"File":file,"Theme":data["Theme"],"Color":data["Color"],
          'C_Image':image.count(),'C_Video':video.count(),'C_File':file.count(),'Total':image.count()+video.count()+file.count(),"Side_Bar":side_bar,'Permission':get_permission(user.id)
          }
          return render(request, "New/media_files.html",context)
      else:
         return redirect("login")

    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          start = r["Start"]
          end = r["End"]
          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          i = Visa_Info.objects.get(id=pk)
          image = Message.objects.filter(Sender=pk,Type='Image',date__range=[start, end])
          video = Message.objects.filter(Sender=pk,Type='Video',date__range=[start, end])
          file = Message.objects.filter(Sender=pk,Type='File',date__range=[start, end])


          context = {"Data":user,"Rand":rand,"Client":i,"Image":image,"Video":video,"File":file,"Theme":data["Theme"],"Color":data["Color"],
          'C_Image':image.count(),'C_Video':video.count(),'C_File':file.count(),'Total':image.count()+video.count()+file.count()
          }
          return render(request, "New/media_files.html",context)
      else:
         return redirect("login")
"""
def create_card():
  for i in range(1,91):
    l = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
    c = ID_Card.objects.create(Link=l)
    make_qr(c.id,l)



import qrcode
import numpy as np
from PIL import Image, ImageDraw, ImageOps

import os  # Ensure BASE_DIR is defined


def make_qr(ID, link):
    # Define QR code data
    data = link

    # Create QR Code with HIGH error correction
    qr = qrcode.QRCode(
        version=7,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate a Black & White QR Code
    qr_img = qr.make_image(fill="black", back_color="white").convert("RGB")
    qr_size = qr_img.size[0]

    # Set Colors
    gold_color = (212, 175, 55)  # Gold
    black_color = (0, 0, 0)  # Black
    white_color = (255, 255, 255)  # White
    padding = 30  # Space around QR code
    rounded_size = qr_size + 2 * padding  # Final image size

    # Convert QR image to NumPy array (RGB)
    qr_data = np.array(qr_img)

    # Identify black pixels (QR code patterns) and change them to gold
    gold_qr = np.full_like(qr_data, black_color)  # Default to black background
    black_pixels = (qr_data[:, :, 0] == 0) & (qr_data[:, :, 1] == 0) & (qr_data[:, :, 2] == 0)
    gold_qr[black_pixels] = gold_color  # Change only black areas to gold

    # Convert back to an image
    qr_img = Image.fromarray(gold_qr)

    # Create a new black background with rounded corners
    final_img = Image.new("RGB", (rounded_size, rounded_size), black_color)
    mask = Image.new("L", (rounded_size, rounded_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, rounded_size, rounded_size), radius=40, fill=255)

    # Paste the QR code onto the new background
    final_img.paste(qr_img, (padding, padding))

    # Open and resize the logo
    logo_path = f'{BASE_DIR}/static/2a.jpg'  # Update the path
    logo_size = qr_size // 5  # Keep logo small for scannability
    logo_padding = 15  # Space around logo
    logo_final_size = logo_size + 2 * logo_padding  # Final size with padding

    logo = Image.open(logo_path).convert("RGBA")  # Ensure transparency
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Create a rounded-square white padding for the logo
    white_bg = Image.new("RGBA", (logo_final_size, logo_final_size), white_color)
    white_mask = Image.new("L", (logo_final_size, logo_final_size), 0)
    draw = ImageDraw.Draw(white_mask)
    draw.rounded_rectangle((0, 0, logo_final_size, logo_final_size), radius=20, fill=255)

    # Apply mask to make rounded corners
    white_bg.putalpha(white_mask)
    white_bg.paste(logo, (logo_padding, logo_padding), mask=logo)

    # Create a gold frame around the logo
    gold_bg_size = logo_final_size + 10
    gold_bg = Image.new("RGBA", (gold_bg_size, gold_bg_size), gold_color)
    gold_mask = Image.new("L", (gold_bg_size, gold_bg_size), 0)
    draw = ImageDraw.Draw(gold_mask)
    draw.rounded_rectangle((0, 0, gold_bg_size, gold_bg_size), radius=25, fill=255)

    # Apply mask and paste the white background onto the gold frame
    gold_bg.putalpha(gold_mask)
    gold_bg.paste(white_bg, (5, 5), mask=white_mask)

    # Paste the logo into the QR code
    x_center = (rounded_size - gold_bg_size) // 2
    y_center = (rounded_size - gold_bg_size) // 2
    final_img.paste(gold_bg, (x_center, y_center), mask=gold_mask)

    # Apply the rounded corners mask
    final_img.putalpha(mask)

    # Save the final QR Code
    output_path = f'{BASE_DIR}/media/ID_QR/{ID}.png'
    final_img.save(output_path)

    return output_path  # Return file path instead of "1" for better tracking

#create_card()"""


def make_qr_fix(ID, link):
    # Create QR Code with HIGH error correction
    qr = qrcode.QRCode(
        version=7,  # Smaller QR for easy scanning
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logos
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Set Colors
    gold_color = (212, 175, 55)  # Gold background
    black_color = (0, 0, 0)  # Black QR pattern
    white_color = (255, 255, 255)  # White
    padding = 30  # Space around QR code

    # Generate initial QR code (black on white)
    qr_img = qr.make_image(fill="black", back_color="white").convert("RGB")
    qr_size = qr_img.size[0]
    final_size = qr_size + 2 * padding  # Final image size

    # Convert QR image to NumPy array
    qr_data = np.array(qr_img)

    # Change white background to gold
    gold_qr = np.full_like(qr_data, gold_color)  # Default to gold background
    black_pixels = (qr_data[:, :, 0] == 0) & (qr_data[:, :, 1] == 0) & (qr_data[:, :, 2] == 0)
    gold_qr[black_pixels] = black_color  # Keep black QR pattern

    # Convert back to an image
    qr_img = Image.fromarray(gold_qr)

    # Create a gold background with rounded corners
    final_img = Image.new("RGB", (final_size, final_size), gold_color)
    mask = Image.new("L", (final_size, final_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, final_size, final_size), radius=40, fill=255)

    # Paste the QR code onto the background
    final_img.paste(qr_img, (padding, padding))

    # Add logo if provided

    try:
            logo = Image.open(f'{BASE_DIR}/static/2a.jpg').convert("RGBA")  # Open logo
            logo_size = qr_size // 5  # Set logo size (1/5 of QR code size)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # Create a curved white padding for the logo
            logo_padding = 15  # Space around logo
            logo_final_size = logo_size + 2 * logo_padding
            white_bg = Image.new("RGBA", (logo_final_size, logo_final_size), white_color)
            white_mask = Image.new("L", (logo_final_size, logo_final_size), 0)
            draw = ImageDraw.Draw(white_mask)
            draw.rounded_rectangle((0, 0, logo_final_size, logo_final_size), radius=20, fill=255)

            # Apply rounded mask to white background
            white_bg.putalpha(white_mask)
            white_bg.paste(logo, (logo_padding, logo_padding), mask=logo)

            # Create a curved gold border around the logo
            gold_bg_size = logo_final_size + 10
            gold_bg = Image.new("RGBA", (gold_bg_size, gold_bg_size), gold_color)
            gold_mask = Image.new("L", (gold_bg_size, gold_bg_size), 0)
            draw = ImageDraw.Draw(gold_mask)
            draw.rounded_rectangle((0, 0, gold_bg_size, gold_bg_size), radius=25, fill=255)

            # Apply mask and paste the white background onto the gold frame
            gold_bg.putalpha(gold_mask)
            gold_bg.paste(white_bg, (5, 5), mask=white_mask)

            # Center position for logo
            x_center = (final_size - gold_bg_size) // 2
            y_center = (final_size - gold_bg_size) // 2

            # Paste logo with curved border onto QR code
            final_img.paste(gold_bg, (x_center, y_center), mask=gold_mask)

    except Exception as e:
            print(f"Error loading logo: {e}")

    # Apply rounded corners
    final_img.putalpha(mask)

    # Save the QR code
    output_path = f'{BASE_DIR}/media/ID_QR/{ID}.png'
    final_img.save(output_path)

    return output_path

def fix_card():
  id =  ID_Card.objects.all()
  for i in id:

    make_qr_fix(i.id,i.Link)
#fix_card()




class Generate_ID_Card(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          i = ID_Card.objects.get(id=pk)


          context = {"Data":user,"Rand":rand,"Card":i,
          }
          return render(request, "Id/Card.html",context)
      else:
         return redirect("login")




class List_All_Cards(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])



          i =  ID_Card.objects.all()


          context = {"Data":user,"Listed":i,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/list_ids.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")




class Assign_Id_Cards(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          Card_Session.objects.filter(Card=r["Card"],Status="Pending").update(Status="Overide")
          c = Card_Session.objects.create(User=user.id,Client=r["id"],About=r["About"],Card=r["Card"],Status="Pending")

          for i in r:
              if str(i).split('_')[0] == "Mbox":
                  p =str(i).split('_')[1]
                  if r[f'Mbox_{p}'] == 'NO':
                      pass
                  else:
                   n = Card_Point.objects.get(id=int(r[f'Mbox_{p}']))
                   Card_Session_Point.objects.create(User=user.id,Name=n.Name,Client=r["id"],Session=c.id,Point=int(r[f'Mbox_{p}']),Status='Pending',
                   Set_Time="Pending",Set_Date="Pending"
                   )
          return Response('Ok')

         #except:
         # return redirect("login")
      else:
       return Response('No')



class Check_Assign_Id_Cards(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          c = Card_Session.objects.filter(Card=r["Card"],Status="Pending")
          if c.count() > 0:
              return Response('Ok')
          else:

           return Response('No')

         #except:
         # return redirect("login")
      else:
       return Response('No')







class Scan_ID_QR(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "Id/scan.html",context)
         #except:
         # return redirect("login")
      else:
         return redirect("login")
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          card = ID_Card.objects.get(Link=r["id"])
          c = Card_Session.objects.filter(Card=card.id,Status="Pending")
          if c.count() > 0:
              return Response({'Stat':'YES','Link':c.last().id,})
          else:

           return Response({'Stat':'NO','Link':0})
         #except:
         # return redirect("login")
      else:
       return Response({'Stat':'NO','Link':0})





class View_Scaned_Booking(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          rand = random.randint(0,1000)
          c = Card_Session.objects.get(id=pk)
          point = Card_Session_Point.objects.filter(Session=c.id)
          client = Booking.objects.get(id=c.Client)
          p = Card_Point_Permission.objects.filter(User=user.id)
          p_l = []
          pointed = []
          msg = []
          for i in p:
             try:
              c1 = Card_Point.objects.get(id=i.Point)
              p_l.append({'id':i.id,'Name':c1.Name,'Point':i.Point})
             except:
                 pass
          l = Card_Point_Message.objects.filter(Session=pk)
          for o in l:
              user_d = Administrator_Info.objects.get(id = o.User)
              msg.append({
                  'id':o.id,'User':o.User,'Name':user_d.Full_Name,'About':o.About
                  })

          for o in point:
              user_d = Administrator_Info.objects.get(id = o.User)
              pointed.append({
                  'id':o.id,'User':o.User,'Name':user_d.Full_Name,'Date':o.Set_Date,'Time':o.Set_Time,'Title':o.Name,'Status':o.Status
                  })

          context = {"Data":user,"Rand":rand,"Client":client,"Card":c,"Theme":data["Theme"],"Color":data["Color"],'Point':point,"Perm":p,'Remark':msg,
          "Sessions":pointed,"Side_Bar":side_bar,'Permission':get_permission(user.id)
          }
          return render(request, "New/scan_info.html",context)
      else:
         return redirect("login")
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Booking.objects.filter(id=pk).update(

              Details=req["Details"],Remark=req["Status"]
          )


          return redirect(reverse('view_booking',kwargs={"pk":int(pk)}))
      else:
         return redirect("login")



class Create_Card_Point_Message(APIView):
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Card_Point_Message.objects.create(User=user.id,Session=pk,About=request.data["About"])
          return redirect(reverse('view_scanned_booking',kwargs={"pk":pk}))
      else:
         return redirect("login")





class Set_Card_Point_Session(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          current_date = strftime("%Y-%m-%d")
          current_time = strftime("%H:%M:%S")
          Card_Session_Point.objects.filter(id=r["id"]).update(User=user.id,Status=r["Status"],Set_Time=current_time,Set_Date=current_date)
          return Response('Ok')
      else:
         return Response('Error')




class List_Card_Point(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Card_Point.objects.all()
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"List":l,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/point_list.html",context)
      else:
         return redirect("login")
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = Card_Point.objects.filter(id=req["id"]).update(Name=req["Name"])

          return Response('Ok')
      else:
         return Response('Error')

    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          req = request.data
          Card_Point.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')



class Create_Card_Point(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Card_Point.objects.create(Name=request.data["Name"])
          return redirect('list_card_point')
      else:
         return redirect("login")




class Set_Card_Point_Permission(APIView):

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          name = Card_Point.objects.get(id=req["Point"]).Name
          e_p = Card_Point_Permission.objects.filter(User=req["id"],Point=req["Point"])
          if e_p.count() > 0 :
              name_s = 'NO'

              id = e_p.last().id

          else:
            c = Card_Point_Permission.objects.create(User=req["id"],Point=req["Point"])
            name_s = 'YES'

            id = c.id


          return Response({'Stat':'OK','Name':name,'N_Stat':name_s,'ID':id})
      else:
         return Response('Error')

    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          req = request.data

          Card_Point_Permission.objects.filter(id=req["id"]).delete()

          return Response('OK')
      else:
         return Response('Error')



class List_Side_Menu(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Side_Menu.objects.all().order_by('Level')
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"List":l,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/menu_side.html",context)
      else:
         return redirect("login")
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = Side_Menu.objects.filter(id=req["id"]).update(
                Name=req["Name"],
                Level=req["Level"],
                Status_Change = req["Status_Change"],
                Call_Log = req["Call_Log"],
                Book_Client =  req["Book_Client"],
                Interview =  req["Interview"],
                Chat_Files =  req["Chat_Files"],
                Profile =  req["Profile"],
                Cv =  req["Cv"],
                Payment =  req["Payment"],
                Debit =  req["Debit"],
                Id_Card =  req["Id_Card"],
                Upload_Files =  req["Upload_Files"],
                View_Files =  req["View_Files"],
                Delete =  req["Delete"],
                Opperation =  req["Opperation"],
                Sign = req['Sign'],

              )

          return Response('Ok')
      else:
         return Response('Error')

    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          req = request.data
          Side_Menu.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')



class Create_Side_Menu(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Side_Menu.objects.create(Name=request.data["Name"],Level=request.data["Level"])
          return redirect('list_side_menu')
      else:
         return redirect("login")





class Manage_Issues(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          l = Issue_Logs.objects.all()
          context = {"Data":user,"Theme":data["Theme"],"Color":data["Color"],"List":l,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request, "New/issues.html",context)
      else:
         return redirect("login")


    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          req = request.data
          Issue_Logs.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          r = request.data
          print(r)
          current_date = strftime("%Y-%m-%d")
          f = Issue_Logs.objects.create(User=user.id,Name=r["Name"],About=r["About"],Status="Pending")
          fs = FileSystemStorage()
          c = 0
          for uploading_file in request.FILES.getlist('Files'):
            file_name, file_extension = os.path.splitext(uploading_file.name)
            v = Issue_Files_List.objects.create(User=user.id,Issue=f.id,Name=f"{file_name}{file_extension}",Extention=file_extension,Status="Yes")
            fs.save(f"Issue_Uploads/{str(v.id)}{file_extension}", uploading_file)
           # c+=1
         # Uploaded_Files.objects.filter(id=f.id).update(Count=c)


          return redirect(reverse('issues_media_view',kwargs={"pk":f.id}))
         # return redirect(reverse('manage_files',kwargs={"pk":pk}))

      else:
         return redirect("login")



class Issues_Media_View(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          print(current_date)
          image_extensions = [
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
                ".webp", ".heif", ".heic", ".svg", ".ico", ".jfif", ".avif"
            ]
          audio_extensions = [
            ".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a", ".wma",
            ".aiff", ".opus", ".amr", ".mid", ".midi"
            ]
          video_extensions = [
                ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm",
                ".mpeg", ".mpg", ".3gp", ".m4v", ".ts"
            ]

          i = Issue_Logs.objects.get(id=pk)
          image = Issue_Files_List.objects.filter(Issue=pk,Extention__in=image_extensions)
          video = Issue_Files_List.objects.filter(Issue=pk,Extention__in=video_extensions)
          audio = Issue_Files_List.objects.filter(Issue=pk,Extention__in=audio_extensions)

          file = Issue_Files_List.objects.filter(Issue=pk)


          context = {"Data":user,"Rand":rand,"Main":i,"Image":image,"Video":video,"Audio":audio,"File":file,"Theme":data["Theme"],"Color":data["Color"],
          'C_Image':image.count(),'C_Video':video.count(),'C_Audio':audio.count(),'C_File':file.count(),'Total':file.count(),"Side_Bar":side_bar,'Permission':get_permission(user.id)
          }
          return render(request, "New/issues_files.html",context)
      else:
         return redirect("login")




class Issue_Update(APIView):

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = Issue_Logs.objects.filter(id=req["id"]).update(Name=req["Name"])

          return Response('Ok')
      else:
         return Response('Error')

class Issue_Update_Status(APIView):

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = Issue_Logs.objects.filter(id=req["id"]).update(Status=req["Status"])

          return Response('Ok')
      else:
         return Response('Error')






class Decition_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          side_perm = {
             'id':'No',
            'Status_Change':'No',
            'Call_Log':'Yes',
            'Book_Client':'No',
            'Interview':'No',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'No',
            'Opperation':'No',

              }





          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Call=user.id)
          else:
           manager =  Visa_Info.objects.all()

         # manager =  Visa_Info.objects.filter(City=)
          all_count = Visa_Info.objects.filter(
            Q(Job_Choice1__isnull=False) & ~Q(Job_Choice1='') |
            Q(Country1__isnull=False) & ~Q(Country1='') |
            Q(Job_Choice2__isnull=False) & ~Q(Job_Choice2='') |
            Q(Country2__isnull=False) & ~Q(Country2='') |
            Q(Job_Choice3__isnull=False) & ~Q(Job_Choice3='') |
            Q(Country3__isnull=False) & ~Q(Country3='')
        )
          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

             count2 = 0
             fields = [
                    ('Job_Choice1', i.Job_Choice1),
                    ('Country1', i.Country1),
                    ('Job_Choice2', i.Job_Choice2),
                    ('Country2', i.Country2),
                    ('Job_Choice3', i.Job_Choice3),
                    ('Country3', i.Country3),
                ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              if value:  # Check if the field has a value
               count2 += 1
             if count2 > 0:
              pp = (count2/6)*100
              hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,'Main':i.Main_ID,"Week":x,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2)
              })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Type":'Decition','Type_Link':2,
            "Interview":inter,"Admins":adm,"Count":all_count.count(),"Note":"Decieded Applicants",'page_obj': page_obj,"Count":all_count.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')






class Proccess_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          side_perm = {
            'id':'No',
            'Status_Change':'No',
            'Call_Log':'Yes',
            'Book_Client':'No',
            'Interview':'No',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'No',
            'Opperation':'No',
              }





          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Call=user.id)
          else:
           manager =  Visa_Info.objects.all()

         # manager =  Visa_Info.objects.filter(City=)

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),
                ('Blocked', i.Blocked),
                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2)
              })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Type":'Decition',
            "Interview":inter,"Admins":adm,"Count":manager.count(),"Note":"Filling Process",'page_obj': page_obj,"Count":manager.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')





class Proccess_Account_Filter(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          side_perm = {
            'id':'No',
            'Status_Change':'No',
            'Call_Log':'Yes',
            'Book_Client':'No',
            'Interview':'No',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'No',
            'Opperation':'No',

              }





          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Call=user.id)
          else:
           manager =  Visa_Info.objects.all()

         # manager =  Visa_Info.objects.filter(City=)
          r=request.data
          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.POST.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),
                ('Blocked', i.Blocked),
                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             if float(r['Start']) <= pp <= float(r['End']):

               hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,"Contact":i.Contact,"Email":i.Email,'Main':i.Main_ID,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2)
                })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Type":'Decition',"Type_Down":'Decition',
            "Interview":inter,"Admins":adm,"Count":manager.count(),"Note":"Filling Process",'page_obj': page_obj,"Count":manager.count(),"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Start':r['Start'],'End':r['End']
            }
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')





class Filter_Decition_Account(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          r=request.data
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          side_perm = {
            'id':'No',
            'Status_Change':'No',
            'Call_Log':'Yes',
            'Book_Client':'No',
            'Interview':'No',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'No',
            'Opperation':'No',

              }





          rand = random.randint(0,1000)
          if int(user.Account) == 1:
           manager =  Visa_Info.objects.filter(Call=user.id)
          else:
           manager =  Visa_Info.objects.all()

         # manager =  Visa_Info.objects.filter(City=)
          all_count = Visa_Info.objects.filter(
            Q(Job_Choice1__isnull=False) & ~Q(Job_Choice1='') |
            Q(Country1__isnull=False) & ~Q(Country1='') |
            Q(Job_Choice2__isnull=False) & ~Q(Job_Choice2='') |
            Q(Country2__isnull=False) & ~Q(Country2='') |
            Q(Job_Choice3__isnull=False) & ~Q(Job_Choice3='') |
            Q(Country3__isnull=False) & ~Q(Country3='')
        )
          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.POST.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:

             count2 = 0
             fields = [
                    ('Job_Choice1', i.Job_Choice1),
                    ('Country1', i.Country1),
                    ('Job_Choice2', i.Job_Choice2),
                    ('Country2', i.Country2),
                    ('Job_Choice3', i.Job_Choice3),
                    ('Country3', i.Country3),
                ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              if value:  # Check if the field has a value
               count2 += 1
             if count2 > 0:
              pp = (count2/6)*100
              if float(r['Start']) <= pp <= float(r['End']):
               hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,"Contact":i.Contact,'Main':i.Main_ID,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2)
               })

          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Type":'Decition',"Type_Down":'Decition','Type_Link':2,
            "Interview":inter,"Admins":adm,"Count":all_count.count(),"Note":"Decieded Applicants",'page_obj': page_obj,"Count":all_count.count(),"Q":ql,'Start':r['Start'],'End':r['End'],
            'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')



class Interview_Page_Dashboard(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          manager =  Interview_Session.objects.all()
          pd =  Interview_Session.objects.filter(Status='Pending')
          cm =  Interview_Session.objects.filter(Status='Completed')
          res =  Interview_Session.objects.filter(Status='Rescheduled')

          res1 =  Interview_Session.objects.filter(Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(Status='Medicals Issues')


          ap =  Interview_Session.objects.filter(Answer='Accepted')
          dc =  Interview_Session.objects.filter(Answer='Rejected')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(Answer='Rejected',Dated=current_date)

          cm_id = list(cm.values_list('id', flat=True))
          pd_id = list(pd.values_list('id', flat=True))
          res_id = list(res.values_list('id', flat=True))
          res1_id = list(res1.values_list('id', flat=True))
          res2_id = list(res2.values_list('id', flat=True))
          res3_id = list(res3.values_list('id', flat=True))
          res4_id = list(res4.values_list('id', flat=True))
          t_pd_id = list(t_pd.values_list('id', flat=True))
          t_cm_id = list(t_cm.values_list('id', flat=True))
          t_ap_id = list(t_ap.values_list('id', flat=True))
          t_dc_id = list(t_dc.values_list('id', flat=True))

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': page_obj,'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(),'All_Completed_id':cm_id,

            'T_Pending':t_pd.count(),'T_Pending_id':t_pd_id,
            'T_Completed':t_cm.count(),'T_Completed_id':t_cm_id,
            'T_Approved':t_ap.count(),'T_Approved_id':t_ap_id,
            'T_Declined':t_dc.count(),'T_Declined_id':t_dc_id,
            'Rescheduled':res.count(),'Rescheduled_id':res_id,


            'Pending_Medicals':res1.count(),'Pending_Medicals_id':res1_id,
            'Missed_Interview':res2.count(),'Missed_Interview_id':res2_id,
            'Incomplete_Medicals':res3.count(),'Incomplete_Medicals_id':res3_id,
            'Medicals_Issues':res4.count(),'Medicals_Issues_id':res4_id,'All_Pending_id':pd_id,

            "Side_Bar":side_bar,'Permission':get_permission(user.id),'Inter':{'Name':'ALL'},'Type':1,'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':0
            }
          return render(request , "New/manage_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')




class Interview_Page_Dashboard_Filter(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)

          pd =  Interview_Session.objects.filter(Status='Pending')
          cm =  Interview_Session.objects.filter(Status='Completed')
          res =  Interview_Session.objects.filter(Status='Rescheduled')
          ap =  Interview_Session.objects.filter(Answer='Accepted')
          dc =  Interview_Session.objects.filter(Answer='Rejected')
          res1 =  Interview_Session.objects.filter(Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(Status='Medicals Issues')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(Answer='Rejected',Dated=current_date)
          cm_id = list(cm.values_list('id', flat=True))
          pd_id = list(pd.values_list('id', flat=True))
          res_id = list(res.values_list('id', flat=True))
          res1_id = list(res1.values_list('id', flat=True))
          res2_id = list(res2.values_list('id', flat=True))
          res3_id = list(res3.values_list('id', flat=True))
          res4_id = list(res4.values_list('id', flat=True))
          t_pd_id = list(t_pd.values_list('id', flat=True))
          t_cm_id = list(t_cm.values_list('id', flat=True))
          t_ap_id = list(t_ap.values_list('id', flat=True))
          t_dc_id = list(t_dc.values_list('id', flat=True))


          hm = []
          r = request.data

          try:
           if r['End'] == []:
            manager =  Interview_Session.objects.filter(Status=r["Status"])
           else:
            manager =  Interview_Session.objects.filter(Status=r["Status"],Dated__range=[r['Start'],r['End']])
          except:
           manager =  Interview_Session.objects.filter(Status=r["Status"])

          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in manager:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': [],'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(), 'Rescheduled':res.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':0,'Inter':{'Name':'ALL'},'Type':1,
            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),
            'T_Pending_id':t_pd_id,'All_Pending_id':pd_id,'T_Completed_id':t_cm_id,'T_Approved_id':t_ap_id,'T_Declined_id':t_dc_id,'Rescheduled_id':res_id,'Pending_Medicals_id':res1_id,'Missed_Interview_id':res2_id,'Incomplete_Medicals_id':res3_id,'Medicals_Issues_id':res4_id,
            }
          return render(request , "New/manage_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')






class Interview_Page_Dashboard_Find(APIView):
    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)

          pd =  Interview_Session.objects.filter(Status='Pending')
          cm =  Interview_Session.objects.filter(Status='Completed')
          res =  Interview_Session.objects.filter(Status='Rescheduled')
          ap =  Interview_Session.objects.filter(Answer='Accepted')
          dc =  Interview_Session.objects.filter(Answer='Rejected')
          res1 =  Interview_Session.objects.filter(Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(Status='Medicals Issues')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(Answer='Rejected',Dated=current_date)
          cm_id = list(cm.values_list('id', flat=True))
          pd_id = list(pd.values_list('id', flat=True))
          res_id = list(res.values_list('id', flat=True))
          res1_id = list(res1.values_list('id', flat=True))
          res2_id = list(res2.values_list('id', flat=True))
          res3_id = list(res3.values_list('id', flat=True))
          res4_id = list(res4.values_list('id', flat=True))
          t_pd_id = list(t_pd.values_list('id', flat=True))
          t_cm_id = list(t_cm.values_list('id', flat=True))
          t_ap_id = list(t_ap.values_list('id', flat=True))
          t_dc_id = list(t_dc.values_list('id', flat=True))


          hm = []
          r = request.data

          fil = Visa_Info.objects.filter(Full_Name__icontains=r['Key']) | Visa_Info.objects.filter(Contact__icontains=r['Key'])

          ccm = 0
          for a in fil:
           manager =  Interview_Session.objects.filter(Client=a.id)
           for id in manager:
             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })
             ccm+=1


          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":ccm,
            "Note":"All Scheduled Clients",'page_obj': [],'Total':ccm,'All_Pending':pd.count(),'All_Completed':cm.count(), 'Rescheduled':res.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':0,'Inter':{'Name':'ALL'},'Type':1,
            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),
            'T_Pending_id':t_pd_id,'All_Pending_id':pd_id,'T_Completed_id':t_cm_id,'T_Approved_id':t_ap_id,'T_Declined_id':t_dc_id,'Rescheduled_id':res_id,'Pending_Medicals_id':res1_id,'Missed_Interview_id':res2_id,'Incomplete_Medicals_id':res3_id,'Medicals_Issues_id':res4_id,
            }
          return render(request , "New/manage_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')





class Completed_Account_Group(APIView):
    def get(self , request, pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          side_perm = {
             'id':'No',
            'Status_Change':'Yes',
            'Call_Log':'Yes',
            'Book_Client':'Yes',
            'Interview':'Yes',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'Yes',
            'Opperation':'No',

              }


          com = Completed_Logs.objects.filter(Type=pk)
          total = 0
          day = 0
          week = 0
          month = 0
          rand = random.randint(0,1000)

          #------------------------------------ counter -------------------------------
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Completed_Logs.objects.filter(Type=pk,date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Completed_Logs.objects.filter(Type=pk,date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Completed_Logs.objects.filter(Type=pk,date__gte=last_month_start).count()

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(com, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for co in page_obj:

             i =  Visa_Info.objects.get(id=co.Client)
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(User=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc,
                'Medicals':i.Medicals,'Email':i.Email,'Job_Choice1':i.Job_Choice1,'Job_Choice2':i.Job_Choice2,'Job_Choice3':i.Job_Choice3,'Country1':i.Country1,
                'Country2':i.Country2,'Country3':i.Country3,'Birth':i.Birth
             })
          rand = random.randint(0,1000)
          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":f'Profile Group {pk}','IN':pk,"Theme":admin_token["Theme"],
            "Color":admin_token["Color"],"Admins":adm,"Interview":inter,"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            "Day":val_today,"Week":val_last_week,"Month":val_last_month,"Total":com.count(),'page_obj':page_obj
            }
          return render(request , "New/profile_group.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')






class Completed_Account_Group_Filter(APIView):
    def post(self , request, pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))

          side_perm = {
             'id':'No',
            'Status_Change':'Yes',
            'Call_Log':'Yes',
            'Book_Client':'Yes',
            'Interview':'Yes',
            'Chat_Files':'No',
            'Profile':'Yes',
            'Cv':'Yes',
            'Payment':'No',
            'Debit':'No',
            'Id_Card' :'No',
            'Upload_Files':'No',
            'View_Files' :'No',
            'Delete':'Yes',
            'Opperation':'No',

              }

          r = request.data
          com = Completed_Logs.objects.filter(Type=pk,date__range=[r['Start'],r['End']])
          total = 0
          day = 0
          week = 0
          month = 0
          rand = random.randint(0,1000)

          #------------------------------------ counter -------------------------------
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Completed_Logs.objects.filter(Type=pk,date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Completed_Logs.objects.filter(Type=pk,date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Completed_Logs.objects.filter(Type=pk,date__gte=last_month_start).count()

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(com, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for co in com:

             i =  Visa_Info.objects.get(id=co.Client)
             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(User=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,"Type":p,"Call":am,"Stat":cc
             })
          rand = random.randint(0,1000)
          adm = Administrator_Info.objects.all()
          inter = Interview_Account.objects.all()
          ql = Question_Group.objects.all()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Note":f'Profile Group {pk}','IN':pk,"Theme":admin_token["Theme"],
            "Color":admin_token["Color"],"Admins":adm,"Interview":inter,"Q":ql,'Side_Perm':side_perm,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            "Day":val_today,"Week":val_last_week,"Month":val_last_month,"Total":com.count(),'page_obj':page_obj
            }
          return render(request , "New/profile_group.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')





class View_Media_Posts(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          rand = random.randint(0,1000)
          post = Post_Info.objects.all()
          listed = []
          paginator = Paginator(post, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj :
           if i.Type == "Vid_Post":

                name = Administrator_Info.objects.get(id=i.User).Full_Name
                use = f'Admin/{i.User}'

                like = Likes.objects.filter(Post=i.id).count()
                Comment =Comments.objects.filter(Post=i.id).count()
                vid = Extra_Videos.objects.get(Post=i.id)

                listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"User":user,"Like":like,
                   "Comment":Comment,"Vid":vid.id,"id":i.id,"Admin":name,"date":i.date,"User":use,
                   })

           elif i.Type == "Img_Post":
                name = Administrator_Info.objects.get(id=i.User).Full_Name
                use = f'Admin/{i.User}'

                like =Likes.objects.filter(Post=i.id).count()
                Comment =Comments.objects.filter(Post=i.id).count()
                img = Extra_Images_Post.objects.get(Post=i.id)
                listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"User":user,"Like":like,
                   "Comment":Comment,"Img":img.id,"id":i.id,"Admin":name,"date":i.date,"User":use,
                   })
           elif i.Type == "Youtube":
              name = Administrator_Info.objects.get(id=i.User).Full_Name
              use = f'Admin/{i.User}'

              like =Likes.objects.filter(Post=i.id).count()
              Comment =Comments.objects.filter(Post=i.id).count()

              listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"User":user,"Like":like,"Link":i.Link,
                   "Comment":Comment,"id":i.id,"Admin":name,"date":i.date,"User":use,
                   })
           else:
              name = Administrator_Info.objects.get(id=i.User).Full_Name
              use = f'Admin/{i.User}'

              like =Likes.objects.filter(Post=i.id).count()
              Comment =Comments.objects.filter(Post=i.id).count()

              listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"User":user,"Like":like,
                   "Comments":Comment,"id":i.id,"Admin":name,"date":i.date,"User":use,
                   })




          context = {"User":user,"Data":user,"Rand":rand,"Posts":listed,"Total":post.count(),'page_obj':page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)
          ,"Theme":data["Theme"], "Color":data["Color"] }
          return render(request, "New/posts.html",context)
      else:
         return redirect("login")

    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Post_Info.objects.filter(id=req["id"]).delete()
          try:
            e = Extra_Images_Post.objects.get(Post=req["id"])
            os.remove(f'{BASE_DIR}/media/Posts/Images/{e.id}.jpg')
          except:
             pass
          try:
             e = Extra_Videos.objects.get(Post=req["id"])
             os.remove(f'{BASE_DIR}/media/Posts/Videos/{e.id}.mp4')
          except:
             pass
          return Response('Ok')
      else:
         return Response("No")



class Personal_Post(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          size =  len(str(request.data["Context"]))
          print(request.data)
          if request.data["vid"]=="":
            vid_stat="None"
            link = 'None'

          else:
            vid_stat = "Video_Post"
          if request.data["img"]=="":
              img_stat = "None"
              link = 'None'


          else:
            img_stat = "Image_Post"
            link = 'None'


          print(vid_stat,img_stat)
          if vid_stat == img_stat:
           if size == 0:
               return redirect('view_media_posts')
           if size > 100:
              Type = "Long_Text"
              link = 'None'
           else:
              Type = "Short_Text"
              link = 'None'

           if request.data["youtube"]=="":
              pass
           else:
              Type = 'Youtube'
              link = request.data["youtube"]
           Post_Info.objects.create(User=data["Data"],Context = request.data["Context"],Type=Type,Link=link)
           return redirect('view_media_posts')

          elif vid_stat == "None":
             Post_Info.objects.create(User=data["Data"],Context = request.data["Context"],Type="Img_Post")
             post = Post_Info.objects.last()
             idd = Extra_Images_Post.objects.create(Post=post.id)
             uploading_file = request.FILES['img']
             fs = FileSystemStorage()
             fs.save("Posts//Images//"+str(idd.id)+".jpg",uploading_file)
             return redirect('view_media_posts')
          else :
             Post_Info.objects.create(User=data["Data"],Context = request.data["Context"],Type="Vid_Post")
             post = Post_Info.objects.last()
             idd = Extra_Videos.objects.create(Post=post.id)

             uploading_file = request.FILES['vid']
             fs = FileSystemStorage()
             fs.save("Posts//Videos//"+str(idd.id)+".mp4",uploading_file)
             return redirect('view_media_posts')

      else:
         return redirect('view_media_posts')





class Delete_Message(APIView):

    def delete(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          req = request.data
          msg = Message.objects.get(id=req['id'])
          if msg.Type == 'Image':
           try:
             os.remove(f'{BASE_DIR}/media/Messages/Images/{str(msg.id)}.jpg')
           except:
             pass
           try:
             os.remove(f'{BASE_DIR}/media/Messages/Files/{str(msg.id)}.pdf')
           except:
             pass
           try:
             os.remove(f'{BASE_DIR}/media/Messages/Videos/{str(msg.id)}.mp4')
           except:
             pass

          Message.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response('Error')






import csv
import os
from django.db import models
from django.utils.timezone import make_aware
from datetime import datetime

def export_model_to_csv(model, start_date, end_date, file_name="exported_data.csv"):
    """
    Exports data from a Django model based on a date range into a CSV file.

    Parameters:
        model (Django Model): The Django model to export data from.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        file_name (str): The name of the CSV file to save the data.

    Returns:
        str: The file path of the exported CSV file.
    """

    # Convert date strings to datetime objects
    start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
    end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))

    # Get the queryset filtered by date range
  #  queryset = model.objects.filter(date__range=(start_date, end_date))  # Replace 'date_field' with the actual field name
   # queryset = model.objects.all().order_by("id")
    queryset = model.objects.using('sqlite').filter(id__range=(27, 200))
    # Define file path
    file_path = os.path.join(os.getcwd(), file_name)

    # Open a CSV file for writing
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header row
        fields = [field.name for field in model._meta.fields]
        writer.writerow(fields)

        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    print(f"Data exported successfully to {file_path}")
    return file_path

#export_model_to_csv(Side_Menu, "2025-04-01", "2025-06-1", "your_data.csv")





def import_csv_to_model(csv_file_path, model):
    """
    Imports data from a CSV file into a Django model, preserving ID and datetime fields.

    Parameters:
        csv_file_path (str): Path to the CSV file.
        model (Django Model): The model to insert data into.
    """

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Reads CSV into a dictionary format

        for row in reader:
            # Convert date field to datetime object (modify the field name & format if needed)
            #row['date'] = make_aware(datetime.strptime(row['date'], "%Y-%m-%d"))

            # Create or update the record in the database
            obj, created = model.objects.update_or_create(
                id=row['id'],  # Ensure same ID is used
                defaults=row
            )

            print(f"{'Created' if created else 'Updated'}: {row}")

    print("Import completed successfully!")

#import_csv_to_model("your_data.csv", Side_Menu)





class Interview_Page_Client(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          manager =  Interview_Session.objects.filter(Client=pk,)
          pd =  Interview_Session.objects.filter(Client=pk,Status='Pending')
          cm =  Interview_Session.objects.filter(Client=pk,Status='Completed')
          res =  Interview_Session.objects.filter(Client=pk,Status='Rescheduled')

          res1 =  Interview_Session.objects.filter(Client=pk,Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(Client=pk,Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(Client=pk,Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(Client=pk,Status='Medicals Issues')


          ap =  Interview_Session.objects.filter(Client=pk,Answer='Accepted')
          dc =  Interview_Session.objects.filter(Client=pk,Answer='Rejected')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(Client=pk,Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(Client=pk,Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(Client=pk,Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(Client=pk,Answer='Rejected',Dated=current_date)



          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })
          inn = Visa_Info.objects.get(id=pk)
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': page_obj,'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':0, 'Rescheduled':res.count()
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id),'Inter':{'Name':inn.Full_Name},'Type':1,
            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),'pk':pk
            }
          return render(request , "New/manage_client_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')





class Interview_Page_Client_Filter(APIView):
    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)

          pd =  Interview_Session.objects.filter(Client=pk,Status='Pending')
          cm =  Interview_Session.objects.filter(Client=pk,Status='Completed')
          res =  Interview_Session.objects.filter(Client=pk,Status='Rescheduled')
          ap =  Interview_Session.objects.filter(Client=pk,Answer='Accepted')
          dc =  Interview_Session.objects.filter(Client=pk,Answer='Rejected')
          res1 =  Interview_Session.objects.filter(Client=pk,Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(Client=pk,Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(Client=pk,Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(Client=pk,Status='Medicals Issues')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(Client=pk,Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(Client=pk,Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(Client=pk,Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(Client=pk,Answer='Rejected',Dated=current_date)



          hm = []
          r = request.data
          try:
           manager =  Interview_Session.objects.filter(Client=pk,Status=r["Status"],Dated__range=[r['Start'],r['End']])
          except:
            manager =  Interview_Session.objects.filter(Client=pk,Status=r["Status"])
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in manager:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': [],'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(), 'Rescheduled':res.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),'IN':0,'Inter':{'Name':'ALL'},'Type':1,
            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),'pk':pk
            }
          return render(request , "New/manage_client_interview.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')





class Interview_Profile_Admin_Report(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])



          inter =  Interview_Session.objects.get(id=int(pk))
          user = Visa_Info.objects.get(id=inter.Client)
          try:
           admin = Interview_Account.objects.get(id=inter.User)
          except:
              admin = {'Name':'Deleted Account','Location':'Deleted','Country':'Deleted'}




          c1 = Remarks.objects.filter(Group='Medical',Mark=int(inter.Medicals))
          c2 = Remarks.objects.filter(Group='Practical Experience',Mark=int(inter.Practical))
          c3 = Remarks.objects.filter(Group='Confidence',Mark=int(inter.Confidence))
          c4 = Remarks.objects.filter(Group='Knowledge',Mark=int(inter.Knowledge))
          c5 = Remarks.objects.filter(Group='Communication',Mark=int(inter.Communication))
          c6 = Remarks.objects.filter(Group='Commitment',Mark=int(inter.Commitment))

          # Calculate the total score and percentage
          total_score = (
            int(inter.Medicals) +
            int(inter.Practical) +
            int(inter.Confidence) +
            int(inter.Knowledge) +
            int(inter.Communication) +
            int(inter.Commitment)
          )

          maximum_score = 60
          percentage = (total_score / maximum_score) * 100

        # Determine grade based on percentage
          if percentage >= 90:
            pass_m = 'Excellent'
          elif percentage >= 80:
            pass_m = 'Very Good'
          elif percentage >= 70:
            pass_m = 'Good'
          elif percentage >= 60:
            pass_m = 'Satisfactory'
          elif percentage >= 50:
            pass_m = 'Needs Improvement'
          else:
            pass_m = 'Poor, You Will Have To Retake The Interview'


          context = {"Data":user,'Admin':admin,'i':inter,"Side_Bar":side_bar,'Permission':get_permission(user.id),
          'C1':c1,'C2':c2,'C3':c3,'C4':c4,'C5':c5,'C6':c6,'Score':pass_m,'Percent':round(percentage,2)
          }
          return render(request, "Cv/cv2.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")




class Interview_Page_Filter_List(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          r = request.data.get('List', [])
          if isinstance(r, str):
            import json
            r = json.loads(r)
          manager = Interview_Session.objects.filter(id__in=r)




          hm = []

          for id in manager:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer,'Rmark':id.Remark,
                'Birth':i.Birth,'Gender':i.Gender,'IELTS':i.IELTS,'Police':i.Police,'Medicals':i.Medicals,'Contact':i.Contact,

             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"Filter",'Total':manager.count()
            ,"Side_Bar":side_bar,'Permission':get_permission(user.id),'Inter':{'Name':'Filter'},'Type':1,'pk':0
            }
          return render(request , "New/manage_list_filter.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')








class Find_Completed_Logs(APIView):

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      side_bar = Side_Menu.objects.all().order_by('Level')
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)


          lp = []
          r=request.data
          fil = Visa_Info.objects.filter(Full_Name__icontains=r['Key']) | Visa_Info.objects.filter(Contact__icontains=r['Key'])

          for a in fil:
            val_all2 = Completed_Logs.objects.filter(Client=a.id)
            for o in val_all2:
              try:
               client = Visa_Info.objects.get(id=o.Client)
               lp.append({
               "id":o.id,"date":o.date,"time":o.time,"Client_id":client.id,"Client_Name":client.Full_Name,"Type":o.Type
               })

              except:
                  pass

          context = {"Data":user,"Com":lp,"Rand":rand,"Side_Bar":side_bar,"Theme":data["Theme"],"Color":data["Color"],'Name':r["Key"],'Count':len(lp)}
          return render(request, "New/find_completed.html",context)
      else:
         return redirect("login")





















#---------------------------------------- Agent----------------------------




class Add_Agent(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/add_agent.html",context)
      else:
         return redirect("login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          tp = Agent_Account.objects.filter(Email=req["Email"]).count()
          if tp > 0:
              return render(request, 'New/authentication-error.html')

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Agent_Account.objects.create(
              Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
              Contact=req["Contact"],Password="pass",Country=req["Country"],Link=u_id,Method=req['Method'],

          )
          #------------------------------------------------------------


          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Agent//"+str(branch.id)+".jpg",uploading_file)
          return redirect('add_agent')
          #return redirect(reverse('view_Staff_account',kwargs={"pk":int(branch.id)}))
      else:
         return redirect("login")




class Edit_Agent(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          rand = random.randint(0,1000)
          staff = Agent_Account.objects.get(id =pk)



          context = {
              "Data":user,"Rand":rand,"Theme":data["Theme"],"Color":data["Color"],"Staff":staff,"Side_Bar":side_bar,'Permission':get_permission(user.id)
              }
          return render(request, "New/edit_agent.html",context)
      else:
         return redirect("login")

    def post(self , request,pk):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data

          u_id = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
          branch = Agent_Account.objects.filter(id=pk).update(
            Name=req["Full_Name"],Email=req["Email"],Location=req["Location"],
            Contact=req["Contact"],Password=req["Password"],Country=req["Country"],Method=req['Method'],

          )


          #------------------------------------------------------------

          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/Agent/{pk}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Agent//"+str(pk)+".jpg",uploading_file)


          return redirect(reverse('edit_agent',kwargs={"pk":pk}))
      else:
         return redirect("login")





class Manager_Agent_Account(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))


          rand = random.randint(0,1000)

          manager =  Agent_Account.objects.all()

          notify = Notifications.objects.filter(User=user.id)
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:


             hm.append({
                "Full_Name":i.Name,"id":i.id,"date":i.date,"Contact":i.Contact,"Email":i.Email,"Location":i.Location,
             })

          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Listed":hm,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Note":"Staff List",'page_obj': page_obj,"Side_Bar":side_bar,'Permission':get_permission(user.id)}
          return render(request , "New/list_agent.html", context)
         #except:
          # return redirect('admin_login')
      else:
         return redirect('admin_login')

    def post(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-admin-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")


          Agent_Account.objects.get(id=int(request.data["id"])).delete()
          try:
               os.remove(f'{BASE_DIR}/media/Agent/{request.data["id"]}.jpg')
          except:
              pass
          return Response('Ok')
         except:
           return Response('Error')
      else:
          return Response('Error')


def set_agent(id):
 try:
  l = Last_Agent.objects.last()
 except:
    l = Last_Agent.objects.create(User=0)
 lst = []
 a = Agent_Account.objects.all()
 if a.count() > 1 :
  for i in a:
     if int(i.User) == l.id:
         pass
     else:
         lst.append(i.User)
  q = random.choice(lst)
 else:
     q= a.last().id
 x = Agent_Account_Link.objects.filter(Client=id)
 if x.count() > 0:
     x.update(User=q)
 else:
  Agent_Account_Link.objects.create(User=q,Client=id,Status='Pending')
 Visa_Info.objects.filter(id=id).update(Agent=q)
 Last_Agent.objects.filter(id=1).update(User=q)


#set_agent(98)
















class Preview_Pannel(APIView):
    def get(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          context = {"User":user}
          return render(request, "Main/preview.html",context)
      else:
         return redirect("admin_login")

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          r = request.data

          b = Visa_Info.objects.get(id=r["id"])
          bk = b.id
          nm =f'{b.Full_Name}'
          try:
           Preview_Board.objects.get(User=1)
           Preview_Board.objects.filter(User=1).update(Name=nm,Location=r["Location"],Count=0,Booking=bk)
          except:
            Preview_Board.objects.create(User=1,Name=nm,Location=r["Location"],Count=0,Booking=bk)
          return Response('Ok')
      else:
         return Response('No')
    def put(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          r = request.data

          try:
           p = Preview_Board.objects.get(User=1)
           if int(p.Count) < 3:
            stat = "Yes"
            d = {"Name":p.Name,"Location":p.Location,"id":p.Booking}
            Preview_Board.objects.filter(User=1).update(Count=int(p.Count)+1)
           else:
             stat = "No"
             d=""
          except:
             stat = "No"
             d=""

          return Response({"Stat":stat,"Data":d})
      else:
         return Response({"Stat":"No"})











class Staff_Agent_Client_Group(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=user.id,date=current_date,Type="Staff")
          t_1 =  Agent_Account_Link.objects.filter(User=user.id,Status='Pending',Type="Staff")
          t_2 =  Agent_Account_Link.objects.filter(User=user.id,Status='Completed',Type="Staff")
          t_3 =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")

          hm = []
          rand = random.randint(0,1000)
          if pk == 'All':
           manager =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")
          elif pk == 'Paid':
              manager = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id)
          else:
             manager =  Agent_Account_Link.objects.filter(User=user.id,Status=pk,Type="Staff")

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             i =  Visa_Info.objects.get(id=i.Client)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'




             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Completed="Completed").count()
          ag_list = []
          ad1 = Administrator_Info.objects.filter(Agent='Yes')
          for o in ad1:
              m1 = Agent_Form_Funds.objects.filter(User=o.id,Status='Recieved').count()
              ag_list.append({'id':o.id,'Name':o.Full_Name,'Data':m1})
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':pk,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Agent_Rank':ag_list}
          return render(request , "New/staff_agent_page.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')
















class Staff_Agent_Client_Group_Main(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=user.id,date=current_date,Type="Staff")
          t_1 =  Agent_Account_Link.objects.filter(User=user.id,Status='Pending',Type="Staff")
          t_2 =  Agent_Account_Link.objects.filter(User=user.id,Status='Completed',Type="Staff")
          t_3 =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")

          hm = []
          rand = random.randint(0,1000)
          side_perm = Side_Menu.objects.get(id=pk)
          print(side_perm.Name)
         # manager =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")
          manager =  Visa_Info.objects.filter(Group=side_perm.Name,Agent=user.id)


          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             i =  Visa_Info.objects.get(id=i.id)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'




             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })
          ag_list = []
          ad1 = Administrator_Info.objects.filter(Agent='Yes')
          for o in ad1:
              m1 = Agent_Form_Funds.objects.filter(User=o.id,Status='Recieved').count()
              ag_list.append({'id':o.id,'Name':o.Full_Name,'Data':m1})
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Completed="Completed").count()
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':side_perm.Name,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Agent_Rank':ag_list}
          return render(request , "New/staff_agent_page.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')















class Confirm_Manager_Edit(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Administrator_Info.objects.get(id=int(find.User))
          if user.Confirm_Agent == 'Yes':
              pass
          else:
              return redirect('admin_login')

          rand = random.randint(0,1000)
          manager =  Visa_Info.objects.get(id=pk)
          notify = Notifications.objects.filter(User=user.id)
          profiles = Extra_Images.objects.filter(Profile=pk,Type="Profile")
          ids = Extra_Images.objects.filter(Profile=pk,Type="Id")
          id = []
          count= 1
          for i in ids:
            id.append({
              f"id_{count}":i.id
                }
            )
            count +=1
          print(id)
          images = []
          count= 1
          for i in profiles:
            images.append({
              f"id_{count}":i.id
                }
            )
            count +=1
          edu = Extra_Info.objects.filter(Profile=pk,Type="School")
          work = Extra_Info.objects.filter(Profile=pk,Type="Work")
          bills = Billings.objects.all().order_by('id').reverse()
          client_bills = Client_Billing.objects.filter(User=pk).order_by('id').reverse()
    #      print(new_list)
          L_1 = Completed_Logs.objects.filter(Client=pk,Type='1').count()
          L_2 = Completed_Logs.objects.filter(Client=pk,Type='2').count()
          L_3 = Completed_Logs.objects.filter(Client=pk,Type='3').count()

          if L_1 > 0:
              L_V1 = 'Yes'
          else:
              L_V1 = 'No'
          if L_2 > 0:
              L_V2 = 'Yes'
          else:
              L_V2 = 'No'
          if L_3 > 0:
              L_V3 = 'Yes'
          else:
              L_V3 = 'No'

          if manager.Agent_Type == 'Agent':
             try:
              ag1 = Agent_Account.objects.get(id = manager.Agent)
              ag = {'id':ag1.id,'Name':ag1.Name,'Contact':ag1.Contact,'Type':'Agent Account'}
             except:
              ag = {'id':0,'Name':'Missing Account','Contact':'0000000000'}
          else:
             try:
              ag1 = Administrator_Info.objects.get(id = manager.Agent)
              ag = {'id':ag1.id,'Name':ag1.Full_Name,'Contact':ag1.Contact,'Type':'Staff Account'}
             except:
              ag = {'id':0,'Name':'Missing Account','Contact':'0000000000'}
          agl = Agent_Account_Link.objects.filter(Client=manager.id).last()
          context = {
            "Data":user,"Rand":rand,"Notify":notify,"Staff":manager,"Education":edu,"Work":work,
            "Extra":images,"ID":id,"Listed":client_bills,"Bills":bills,"Theme":admin_token["Theme"],"Color":admin_token["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id)
            ,'P1':L_V1,'P2':L_V2,'P3':L_V3,'Agent':ag,'Agent_Link':agl
            }
          return render(request , "New/confirm_profile.html", context)
       #  except:
        #   return render (request, 'New/profile.html')

      else:
         return redirect('admin_login')






















class Confirm_Agent_Client_Form(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=user.id,date=current_date,Type="Staff")
          t_1 =  Agent_Account_Link.objects.filter(User=user.id,Status='Pending',Type="Staff")
          t_2 =  Agent_Account_Link.objects.filter(User=user.id,Status='Completed',Type="Staff")
          t_3 =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")

          hm = []
          rand = random.randint(0,1000)

          manager = Agent_Form_Funds.objects.filter(Status='Recieved',Completed=pk)

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             i =  Visa_Info.objects.get(id=i.Client)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100



             if pp >= 90:
              hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2)
              })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':pk,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count()}
          return render(request , "New/confirm_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')




class Confirm_Forms(APIView):

    def post(self , request):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          if user.Confirm_Agent == "Yes":
           pass
          else:
           return Response('No')

          r = request.data

          b = Visa_Info.objects.get(id=r["id"])
          '''af = Agent_Form_Funds.objects.filter(Client=b.id).last()
          if af.Type == 'Agent':
             ag = Agent_Account.objects.get(id= ag.User)
             name =ag.Name
             email=ag.Email
             number=ag.Contact
             method = ag.Method
             type=af.Type
          else:
             ag =  Administrator_Info.objects.get(id= ag.User)
             name =ag.Full_Name
             email=ag.Email
             number=ag.Contact
             method = ag.Method
             type=af.Type

          x = Send_card(number,name,method,email,type)'''
          try:
            if  x['Data']['Stat'] == 'Completed':
                  st = 'Completed'
                  rf = x['Data']['Refrence']
            else:
                  st = 'Failed'
                  rf = 000000
          except:
              st = 'Failed'
              rf = 000000
          manager = Agent_Form_Funds.objects.filter(Client=b.id).update(Completed='Completed')
          Agent_Account_Link.objects.filter(Client=b.id).update(Status='Completed')



          return Response('Ok')
      else:
         return Response('No')


def Send_card(number,name,method,email,type):
        data2 = {
    "Number": number,
    'Name':name,
    'Method':method,
    'Email':email,
    'Type':type

           }

        url='https://www.omanager.world/transfare_sikobs_funds_api'
        response = requests.post(url, json=data2)
        print(response.json())
        return response.json()






#================================================ pass =====================================


class Staff_Agent_Dash(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(date=current_date)
          t_1 =  Agent_Account_Link.objects.filter(Status='Pending')
          t_2 =  Agent_Account_Link.objects.filter(Status='Completed')
          t_3 =  Agent_Account_Link.objects.all()

          hm = []
          rand = random.randint(0,1000)

          manager = Agent_Form_Funds.objects.filter(Status='Recieved')

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             i =  Visa_Info.objects.get(id=i.Client)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100

             lock = 'Yes'

             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'

             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock,
                'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
              })
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Completed="Completed").count()

          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=last_month_start).count()

          mant = Agent_Form_Funds.objects.filter(Status='Recieved').count()

          ag_list = []
          ad1 = Administrator_Info.objects.filter(Agent='Yes')
          for o in ad1:
              m1 = Agent_Form_Funds.objects.filter(User=o.id,Status='Recieved').count()
              ag_list.append({'id':o.id,'Name':o.Full_Name,'Data':m1})

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':'All Paid Client Data',"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Total_Pay':mant*150,'Today_Pay':val_today*150,'Week_Pay':val_last_week*150,'Month_Pay':val_last_month*150,'Agent_Rank':ag_list}
          return render(request , "New/staff_agent_dash.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')










class Find_Staff_Agent_Dash(APIView):
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(date=current_date)
          t_1 =  Agent_Account_Link.objects.filter(Status='Pending')
          t_2 =  Agent_Account_Link.objects.filter(Status='Completed')
          t_3 =  Agent_Account_Link.objects.all()

          hm = []
          rand = random.randint(0,1000)
          r = request.data
          manager = Visa_Info.objects.filter(Full_Name__icontains=r['Key'])

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in manager:
            ax = Agent_Form_Funds.objects.filter(Client=i.id,Status=r['Status'])
            if ax.count() > 0:
             #i =  Visa_Info.objects.get(id=i.id)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100

             lock = 'Yes'

             try:
              if i.Agent_Type == 'Staff':
                 agg = Administrator_Info.objects.get(id=i.Agent)
                 ag_n = agg.Full_Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Admin'
              else:
                 agg = Agent_Account.objects.get(id=i.Agent)
                 ag_n = agg.Name
                 ag_c = agg.Contact
                 ag_l = agg.Location
                 ag_k = 'Agent'
             except:
                 ag_n = 'Unassigned'
                 ag_c = 'Unassigned'
                 ag_l = 'Unassigned'
                 ag_k = 'Agent'

             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock,
                'Agent':i.Agent,'Agent_Type':i.Agent_Type,'Agent_Name':ag_n,'Agent_Contact':ag_c,'Agent_Location':ag_l,'Agent_Image':ag_k
              })
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Completed="Completed").count()

          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          val_today = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=today_start).count()
          last_week_start = now - timedelta(days=7)
          val_last_week = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=last_week_start).count()
          last_month_start = now - timedelta(days=30)
          val_last_month = Agent_Form_Funds.objects.filter(Status='Recieved',date__gte=last_month_start).count()

          mant = Agent_Form_Funds.objects.filter(Status='Recieved').count()

          ag_list = []
          ad1 = Administrator_Info.objects.filter(Agent='Yes')
          for o in ad1:
              m1 = Agent_Form_Funds.objects.filter(User=o.id,Status='Recieved').count()
              ag_list.append({'id':o.id,'Name':o.Full_Name,'Data':m1})

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":len(hm),'page_obj': page_obj,'Name':r['Status']+' Client Data',"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Total_Pay':mant*150,'Today_Pay':val_today*150,'Week_Pay':val_last_week*150,'Month_Pay':val_last_month*150,'Agent_Rank':ag_list}
          return render(request , "New/staff_agent_dash.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')




















#---------------------------------------------------------------------------- Signature -----------------------------------------------------------------





class Confirm_Documment_List(APIView):
    def get(self , request,pk):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  User_Signed_Document.objects.filter(User=pk,date=current_date)

          t_3 =  User_Signed_Document.objects.filter(User=pk)
          manager =  Visa_Info.objects.get(id=pk)

          rand = random.randint(0,1000)



          context = {
            "Data":user,"Rand":rand,"Client":manager,"Theme":data["Theme"],"Color":data["Color"],'Name':manager.Full_Name,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':10,'Today':t_0.count(),'Pending':10-t_3.count(),'Completed':t_3.count(),'Listed':t_3,'Pk':pk}

          return render(request , "New/legal_doc_view.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')









class Admin_Sign_File(APIView):
    def get(self , request,pk,pk2):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = admin_get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=pk2)
           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)

           #new = Debit_info.objects.filter(User=data.id)
           try:
               ad = Administrator_Info.objects.get(id=data.Call)
           except:
               ad = {'Full_Name':'Not Assigned','id':0}
           try:
               ea = User_Signed_Document.objects.get(Document=pk,User=data.id)
               e =ea.id
               dt = ea.date
               day =dt.day
               month = dt.strftime('%B')
               year = dt.strftime('%y')
               stat =ea.Status


           except:
               e = 0
               dt = strftime("%Y-%m-%d")
               day =strftime("%d")
               month = strftime("%B")
               year = strftime("%y")
               stat = 'Pending'

           try:
               e1 = Withness_Signed_Document.objects.get(Document=pk,User=data.id)

           except:
               e1 = {'id':0}

           type1 = 'Admin'
           context={"User":data,"Rand":rand,"Date":dt,'Admin':ad,'Main':pk,'Image':e,'Witness':e1,'Day':day,"Month":month,"Year":year,'Type1':type1,'Status':stat}
           return render(request , f"Signature/{pk}.html",context)


        #except:

         #  return redirect('login')
       return redirect('client_login')

    def post(self , request,pk,pk2):
      data = admin_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])
          print(data)
          req = request.data
          print(req)

          v = User_Signed_Document.objects.filter(id=req["id"]).update(Status=req["Status"])

          return Response('Ok')
      else:
         return Response('Error')




















class Manage_Staff_Agent_Client_Group_Main(APIView):
    def get(self , request,pk,pk2):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=pk2,date=current_date,Type="Staff")
          t_1 =  Agent_Account_Link.objects.filter(User=pk2,Status='Pending',Type="Staff")
          t_2 =  Agent_Account_Link.objects.filter(User=pk2,Status='Completed',Type="Staff")
          t_3 =  Agent_Account_Link.objects.filter(User=pk2,Type="Staff")

          hm = []
          rand = random.randint(0,1000)
          side_perm = Side_Menu.objects.get(id=pk)
          print(side_perm.Name)
         # manager =  Agent_Account_Link.objects.filter(User=user.id,Type="Staff")
          manager =  Visa_Info.objects.filter(Group=side_perm.Name,Agent=pk2)


          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
             i =  Visa_Info.objects.get(id=i.id)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'




             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=pk2,Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=pk2,Completed="Completed").count()

          stf = Administrator_Info.objects.get(id = pk2)
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':side_perm.Name,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Staff':stf}
          return render(request , "New/manage_staff_page_agent.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')











class Manage_Staff_Agent_Client_Group(APIView):
    def get(self , request,pk,pk2):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=pk2,date=current_date,Type="Staff")
          t_1 =  Agent_Account_Link.objects.filter(User=pk2,Status='Pending',Type="Staff")
          t_2 =  Agent_Account_Link.objects.filter(User=pk2,Status='Completed',Type="Staff")
          t_3 =  Agent_Account_Link.objects.filter(User=pk2,Type="Staff")

          hm = []
          rand = random.randint(0,1000)
          if pk == 'All':
           manager =  Agent_Account_Link.objects.filter(User=pk2,Type="Staff")
          elif pk == 'Paid':
              manager = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=pk2)
          else:
             manager =  Agent_Account_Link.objects.filter(User=pk2,Status=pk,Type="Staff")

          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
            try:
             i =  Visa_Info.objects.get(id=i.Client)
             count2 = 0
             count3 = 0
             fields = [
                ('Contact_Email', i.Contact_Email),
                ('Contact_Email_Password', i.Contact_Email_Password),
                ('IELTS', i.IELTS),
                ('Police', i.Police),
                ('Medicals', i.Medicals),
                ('Full_Name', i.Full_Name),
                ('Gender', i.Gender),
                ('Birth', i.Birth),
                ('Marital', i.Marital),
                ('Seen', i.Seen),
                ('Password', i.Password),
                ('Address', i.Address),
                ('City', i.City),
                ('Email', i.Email),
                ('Contact', i.Contact),
                ('Skill', i.Skill),
                ('Skill_Level', i.Skill_Level),
                ('Experience', i.Experience),
                ('Education', i.Education),
                ('Passport', i.Passport),
                ('Birth_Cert', i.Birth_Cert),
                ('Refrene_Code', i.Refrene_Code),
                ('Garantor_Full_Name', i.Garantor_Full_Name),
                ('Garantor_Gender', i.Garantor_Gender),
                ('Garantor_Address', i.Garantor_Address),
                ('Garantor_City', i.Garantor_City),
                ('Garantor_Email', i.Garantor_Email),
                ('Garantor_Contact', i.Garantor_Contact),
                ('Father_Full_Name', i.Father_Full_Name),
                ('Father_Address', i.Father_Address),
                ('Father_Birth', i.Father_Birth),
                ('Father_Contact', i.Father_Contact),
                ('Father_City', i.Father_City),
                ('Mother_Full_Name', i.Mother_Full_Name),
                ('Mother_Address', i.Mother_Address),
                ('Mother_Birth', i.Mother_Birth),
                ('Mother_Contact', i.Mother_Contact),
                ('Mother_City', i.Mother_City),
                ('Link', i.Link),
                ('Group', i.Group),
                ('Reference1_Full_Name', i.Reference1_Full_Name),
                ('Reference1_Address', i.Reference1_Address),
                ('Reference1_Job', i.Reference1_Job),
                ('Reference1_Contact', i.Reference1_Contact),
                ('Reference2_Full_Name', i.Reference2_Full_Name),
                ('Reference2_Address', i.Reference2_Address),
                ('Reference2_Job', i.Reference2_Job),
                ('Reference2_Contact', i.Reference2_Contact),
                ('Reference3_Full_Name', i.Reference3_Full_Name),
                ('Reference3_Address', i.Reference3_Address),
                ('Reference3_Job', i.Reference3_Job),
                ('Reference3_Contact', i.Reference3_Contact),
                ('Job_Choice1', i.Job_Choice1),
                ('Country1', i.Country1),
                ('Job_Choice2', i.Job_Choice2),
                ('Country2', i.Country2),
                ('Job_Choice3', i.Job_Choice3),
                ('Country3', i.Country3),
                ('Height', i.Height),
                ('Hair', i.Hair),
                ('Eye', i.Eye),
                ('Birth_City', i.Birth_City),
                ('Country_Birth', i.Country_Birth),
                ('Postal_Code', i.Postal_Code),
                ('Birth_Address', i.Birth_Address),

                ('Account_Type', i.Account_Type),
                ('Country_Recidence', i.Country_Recidence),
                ('Postal_Code_Recidence', i.Postal_Code_Recidence),
                ('Father_Living', i.Father_Living),
                ('Mother_Living', i.Mother_Living),
                ('Weight', i.Weight),
                ('Card_Id', i.Card_Id),
            ]

             x = int(weeks_until_7_months(i.id))
             if x < 10:
                p = 1
             elif x < 20:
                p=2
             else:
                p = 3
             try:
               ad = Administrator_Info.objects.get(id=i.Call)
               am = i.Call
             except:
               am=0
             current_date = strftime("%Y-%m-%d")
             t = Call_Logs.objects.filter(Member=i.id,date=current_date)
             if t.count() >0:
               cc = "Called"
             else:
               cc="Not Called"
             for field_name, value in fields:
              count3 += 1
              if value:  # Check if the field has a value
               count2 += 1

             pp = (count2/count3)*100
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'




             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })
            except:
                pass
          stf = Administrator_Info.objects.get(id = pk2)
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=pk2,Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Staff",User=pk2,Completed="Completed").count()
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':pk,"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*15,'Sent_Pay':man2*15,'Staff':stf}
          return render(request , "New/manage_staff_page_agent.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('admin_login')





class Agent_Pay_List(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")

          ls = []
          pay = 0
          manager =  Administrator_Info.objects.filter(Agent='Yes')
          for i in manager:
           a = Agent_Form_Funds.objects.filter(User=i.id,Completed='Completed',Transfared='Pending',Status='Recieved')
           ls.append({
               'id':i,'Amount':a.count()*15
               })
           pay+=a.count()*15




          context = {
            "Data":user,"Rand":rand,"Staff":ls,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':pay,}

          return render(request , "New/pay_agent.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('admin_login')










class Confirm_Payout(APIView):
    def post(self , request):
       rand = random.randint(0,1000)

       data =  admin_get(request)
       if data["Stat"] ==  "Ok":
         user = Administrator_Info.objects.get(id = data["Data"])
         r =request.data


         manager =  Administrator_Info.objects.get(id=r['ID'])
         a = Agent_Form_Funds.objects.filter(User=manager.id,Completed='Completed',Transfared='Pending',Status='Recieved')
         am=0
         for i in a:
          am+=15
         if am > 0:
          send_number = f'233{str(manager.Contact)[1:]}'
          data2 = {
    "Name": manager.Full_Name,
    "Number": send_number,
    "Email": manager.Email,
    "Type": manager.Method,
    "Amount": float(am),
    "Url": f'https://www.sikobs.world/confirm_manager_payout/{manager.id}',
    "ClientReference": i.Refrence
           }

          url=f'{ET_URL}/pay_transaction'
          response = requests.post(url, json=data2)

          if response.status_code == 401:
            print("Authentication failed. Check your API key.")
          else:
            try:
             if response.json()["Data"]["transactionStatus"]  == "success":
              Agent_Form_Funds.objects.filter(id=i.id).update(Transfared="Transfared")
            except:
                pass
         return Response('Ok')

         return Response("Error")
       return Response("Error")

class Confirm_Manager_Payout(APIView):
    def post(self , request,pk):
           print(request.data["ResponseCode"])
           print(request.data["Data"]['ClientReference'])
           if request.data["ResponseCode"] == '0000':
              Agent_Form_Funds.objects.filter(User=pk,Completed='Completed',Transfared='Pending',Status='Recieved').update(Transfared="Transfared")
              #t = Transactions.objects.get(id=pk)
            #  Notifications.objects.create(User=t.Receiver,Name="Topup Completed!",Info=f"You have completed a topup payment proccess to your church wallet successfuly. Thank You",Link=f'',Type="Topup")
           return Response(200)










#def aa():
#    Agent_Form_Funds.objects.filter(User=26,Completed='Completed',Transfared='Pending',Status='Recieved').update(Transfared="Transfared")

#aa()





class Overview_Report(APIView):
    def get(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")

          ls = []
          pay = 0
          manager =  Administrator_Info.objects.filter(Agent='Yes')
          for i in manager:
           a = Agent_Form_Funds.objects.filter(User=i.id,Completed='Completed',Transfared='Pending',Status='Recieved')
           calls1 = Call_Logs.objects.filter(User=i.id,Status="Picked Up").count()
           calls2 = Call_Logs.objects.filter(User=i.id, Status="Rescheduled").count()
         #  calls3 = Call_Logs.objects.filter(User=i.id,Status="Unanswered").count()
           book = Booking.objects.filter(Admin=i.id).count()
           calls = Call_Logs.objects.filter(User=i.id).count()

           ls.append({
               'id':i,'Pick':calls1,'Book':book,'Rec':calls2,'Calls':calls,
               })
           pay+=a.count()*15




          context = {
            "Data":user,"Rand":rand,"Staff":ls,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':pay,}

          return render(request , "New/o_report.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('admin_login')
    def post(self , request):
      side_bar = Side_Menu.objects.all().order_by('Level')
      data =  admin_get(request)
      if data["Stat"] ==  "Ok":
          user = Administrator_Info.objects.get(id = data["Data"])

          r = request.data
          rand = random.randint(0,1000)
          current_date = strftime("%Y-%m-%d")

          ls = []
          pay = 0
          manager =  Administrator_Info.objects.filter(Agent='Yes')
          for i in manager:
           a = Agent_Form_Funds.objects.filter(User=i.id,Completed='Completed',Transfared='Pending',Status='Recieved')
           calls1 = Call_Logs.objects.filter(User=i.id,Status="Picked Up",date__range=[r['Start'],r['End']]).count()
           calls2 = Call_Logs.objects.filter(User=i.id, Status="Rescheduled",date__range=[r['Start'],r['End']]).count()
         #  calls3 = Call_Logs.objects.filter(User=i.id,Status="Unanswered",date__range=[r['Start'],r['End']]).count()
           book = Booking.objects.filter(Admin=i.id,date__range=[r['Start'],r['End']]).count()
           calls = Call_Logs.objects.filter(User=i.id,date__range=[r['Start'],r['End']]).count()

           ls.append({
               'id':i,'Pick':calls1,'Book':book,'Rec':calls2,'Calls':calls,
               })
           pay+=a.count()*15




          context = {
            "Data":user,"Rand":rand,"Staff":ls,"Theme":data["Theme"],"Color":data["Color"],"Side_Bar":side_bar,'Permission':get_permission(user.id),
            'Total':pay,}

          return render(request , "New/o_report.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('admin_login')