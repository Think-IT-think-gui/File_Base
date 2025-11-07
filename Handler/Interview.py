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



#======================================================== Dashboard ===========================================================

from . Extra import *

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



class Interview_Page(APIView):
    def get(self , request):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          manager =  Interview_Session.objects.filter(User=user.id)
          pd =  Interview_Session.objects.filter(User=user.id,Status='Pending')
          cm =  Interview_Session.objects.filter(User=user.id,Status='Completed')
          ap =  Interview_Session.objects.filter(User=user.id,Answer='Accepted')
          dc =  Interview_Session.objects.filter(User=user.id,Answer='Rejected')

          current_date = strftime("%Y-%m-%d")
          t_pd =  Interview_Session.objects.filter(User=user.id,Status='Pending',Dated=current_date)
          t_cm =  Interview_Session.objects.filter(User=user.id,Status='Completed',Dated=current_date)
          t_ap =  Interview_Session.objects.filter(User=user.id,Answer='Accepted',Dated=current_date)
          t_dc =  Interview_Session.objects.filter(User=user.id,Answer='Rejected',Dated=current_date)
          pk = user.id
          res1 =  Interview_Session.objects.filter(User=pk,Status='Pending Medicals')
          res2 =  Interview_Session.objects.filter(User=pk,Status='Missed Interview')
          res3 =  Interview_Session.objects.filter(User=pk,Status='Incomplete Medicals')
          res4 =  Interview_Session.objects.filter(User=pk,Status='Medicals Issues')
          res =  Interview_Session.objects.filter(User=pk,Status='Rescheduled')




          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:
            try:
             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer
             })
            except:
                pass

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"All Scheduled Clients",'page_obj': page_obj,'Total':manager.count(),'All_Pending':pd.count(),'All_Completed':cm.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(),'All_Approved':ap.count(),'All_Declined':dc.count(),

            'Pending_Medicals':res1.count(),'Missed_Interview':res2.count(),'Incomplete_Medicals':res3.count(),'Medicals_Issues':res4.count(),
            'T_Pending':t_pd.count(),'T_Completed':t_cm.count(),'T_Approved':t_ap.count(),'T_Declined':t_dc.count(), 'Rescheduled':res.count()
            }
          return render(request , "New/interview_home.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')








class Interview_Page_Group(APIView):
    def get(self , request,pk,pk2):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          if pk == 'Status':
           manager =  Interview_Session.objects.filter(User=user.id,Status=pk2)
          else:
            manager =  Interview_Session.objects.filter(User=user.id,Answer=pk2)


          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:

             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer
             })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),"Note":pk2,'page_obj': page_obj}
          return render(request , "New/interview_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')




class Interview_Page_Find(APIView):
    def post(self , request):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          r = request.data
          manager =  Interview_Session.objects.filter(User=user.id)
          x = []
          f = Visa_Info.objects.filter(Full_Name__icontains=r["Key"]) | Visa_Info.objects.filter(Contact__icontains=r['Key'])
          for i in f:
              x.append(i.id)

          hm = []

          for id in manager:

            try:
             current_date = strftime("%Y-%m-%d")

             i = Visa_Info.objects.get(id=id.Client)
             if i.id in x:

              hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer
              })
            except:
                pass

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),"Note":f'Searched Results For {r["Key"]}','page_obj': ''}
          return render(request , "New/interview_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')



class Interview_Page_Filter(APIView):
    def post(self , request):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)
          r = request.data
          try:
           manager =  Interview_Session.objects.filter(User=user.id,Status=r["Status"],Dated=r["Date"])
          except:
            manager =  Interview_Session.objects.filter(User=user.id,Status=r["Status"])


          hm = []

          for id in manager:
            try:
             current_date = strftime("%Y-%m-%d")
             i = Visa_Info.objects.get(id=id.Client)
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":id.Dated,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,'Start':convert_to_am_pm(id.Start),"End":convert_to_am_pm(id.End),"Status":id.Status,'idd':id,"Answer":id.Answer
             })
            except:
                pass

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),"Note":'Filtered Results','page_obj': ''}
          return render(request , "New/interview_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')



class Interview_Login(APIView):
    def get(self , request):
      if 'csrf-interview-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-interview-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Interview")
          User_data = Interview_Account.objects.get(id=int(find.User))

          return redirect('interview_page')
         except:
           return render(request , "New/login2.html")
      else:
         return render(request , "New/login2.html")

    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try:
          data = Interview_Account.objects.get(Email=request.data['Email'], Password=request.data['Password'])

          response =  redirect('interview_page')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Interview")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Interview")
          response.set_cookie('csrf-interview-token',generated_uuid)
        #  Notifications.objects.create(Type = "Login",User = data.id,Name = "Login Prompt!", Info=f"You have successfully logged in on {current_time}.",Link = "#")
          return response
       except:
         return render (request, 'Administrator/pages/samples/error-404.html')


class Interview_Logout(APIView):
    def get(self , request):
      response = redirect("interview_login")
      response.delete_cookie('csrf-interview-token')

      return response




class Interview_Profile(APIView):
    def get(self , request,pk):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])



          inter =  Interview_Session.objects.get(id=int(pk))
          User_data = Visa_Info.objects.get(id=inter.Client)
          edu = Extra_Info.objects.filter(Profile=User_data.id,Type="School")
          work = Extra_Info.objects.filter(Profile=User_data.id,Type="Work")


          q = Question.objects.filter(Group=inter.Question)
          qm = Question_Group.objects.filter(id=inter.Question)
          c1 = Remarks.objects.filter(Group='Medical',Mark=int(inter.Medicals))
          c2 = Remarks.objects.filter(Group='Practical Experience',Mark=int(inter.Practical))
          c3 = Remarks.objects.filter(Group='Confidence',Mark=int(inter.Confidence))
          c4 = Remarks.objects.filter(Group='Knowledge',Mark=int(inter.Knowledge))
          c5 = Remarks.objects.filter(Group='Communication',Mark=int(inter.Communication))
          c6 = Remarks.objects.filter(Group='Commitment',Mark=int(inter.Commitment))
          context = {"Data":User_data,"Education":edu,"Work":work,'i':inter,'Q':q,'M':qm,
          'C1':c1,'C2':c2,'C3':c3,'C4':c4,'C5':c5,'C6':c6,}
          return render(request, "Cv/cv.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")
    def post(self , request,pk):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])
          data = request.data
          Interview_Session.objects.filter(id=int(pk)).update(
                Appearance=data['appearance']['value'],
                Appearance_Remark=data['appearance']['remark'],
                Communication=data['skill']['value'],
                Communication_Remark=data['skill']['remark'],
                Practical=data['practical']['value'],
                Practical_Remark=data['practical']['remark'],
                Knowledge=data['knowledge']['value'],
                Knowledge_Remark=data['knowledge']['remark'],
                Medicals=data['medicals']['value'],
                Medicals_Remark=data['medicals']['remark'],
                Confidence=data['confidence']['value'],
                Confidence_Remark=data['confidence']['remark'],
                Commitment=data['commitment']['value'],
                Commitment_Remark=data['commitment']['remark'],
                Status=data['info']['status'],
                Answer=data['info']['answer'],
              )

          return Response('Ok')
         #except:
         # return redirect("login")
      else:
        return Response('Error')



class Interview_File(APIView):
    def post(self , request,pk):
      data = interview_get(request)
      if data["Stat"] ==  "Ok":
          user = Interview_Account.objects.get(id = data["Data"])
          data = request.data
          try:
            os.remove(f'{BASE_DIR}/media/Interview_Files/{pk}.mp4')
          except:
             pass
          uploading_file = request.FILES['file']
          fs = FileSystemStorage()
          fs.save("Interview_Files//"+str(pk)+".mp4",uploading_file)

          return Response('Ok')
         #except:
         # return redirect("login")
      else:
        return Response('Error')

