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

from django.db.models import Sum

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



class Agent_Page(APIView):
    def get(self , request):
      data = agent_get(request)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])

          current_date = strftime("%Y-%m-%d")
          t_0 =  Agent_Account_Link.objects.filter(User=user.id,date=current_date,Type="Agent")
          t_1 =  Agent_Account_Link.objects.filter(User=user.id,Status='Pending',Type="Agent")
          t_2 =  Agent_Account_Link.objects.filter(User=user.id,Status='Completed',Type="Agent")
          t_3 =  Agent_Account_Link.objects.filter(User=user.id,Type="Agent")


          rand = random.randint(0,1000)



          manager =  Agent_Account_Link.objects.filter(User=user.id,Type="Agent")
          hm = []
          paginator = Paginator(manager, 30)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for id in page_obj:
             i = Visa_Info.objects.get(id=id.Client)
             current_date = strftime("%Y-%m-%d")

             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,
                "Address":i.Address,"City":i.City,"Status":''
             })
          man1 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Agent",User=user.id,Completed="Pending").count()
          man2 = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Agent",User=user.id,Completed="Completed").count()
          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),
            "Note":"Clients Filling",'page_obj': page_obj,'Total':t_3.count(),'Today':t_0.count(),'Pending':t_1.count(),'Completed':t_2.count(),'Pending_Pay':man1*30,'Sent_Pay':man2*30
            }
          return render(request , "New/agent_home.html", context)
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



class Agent_Login(APIView):
    def get(self , request):
      if 'csrf-agent-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-agent-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          User_data = Agent_Account.objects.get(id=int(find.User))

          return redirect('agent_page')
         except:
           return render(request , "New/login3.html")
      else:
         return render(request , "New/login3.html")

    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try:
          data = Agent_Account.objects.get(Email=request.data['Email'], Password=request.data['Password'])

          response =  redirect('agent_page')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Agent")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Agent")
          response.set_cookie('csrf-agent-token',generated_uuid)
        #  Notifications.objects.create(Type = "Login",User = data.id,Name = "Login Prompt!", Info=f"You have successfully logged in on {current_time}.",Link = "#")
          return response
       except:
         return render (request, 'Administrator/pages/samples/error-404.html')


class Agent_Logout(APIView):
    def get(self , request):
      response = redirect("agent_login")
      response.delete_cookie('csrf-agent-token')

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













class Agent_Fill_Page(APIView):
    def get(self , request):
      data = agent_get(request)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)


          hm = []
          rand = random.randint(0,1000)

          manager =  Visa_Info.objects.filter(Agent=user.id,Agent_Type="Agent")

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
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Agent",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj}
          return render(request , "New/agent_page_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')









class Agent_Client_Group(APIView):
    def get(self , request,pk):
      data = agent_get(request)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])


          rand = random.randint(0,1000)


          hm = []
          rand = random.randint(0,1000)


          if pk == 'All':
           manager =  Agent_Account_Link.objects.filter(User=user.id,Type="Agent")
          elif pk == 'Paid':
              manager = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Agent",User=user.id)
          else:
             manager =  Agent_Account_Link.objects.filter(User=user.id,Status=pk,Type="Agent")
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
             man = Agent_Form_Funds.objects.filter(Status='Recieved',Type="Agent",User=user.id,Client=i.id)
             if man.count() > 0:
                 lock = 'No'
             else:
                 lock = 'Yes'
             hm.append({
                "Full_Name":i.Full_Name,"id":i.id,"SEP":i.SEP,"date":i.date,'Time':i.time,"Contact":i.Contact,"Email":i.Email,"Group":i.Group,"Week":x,'Main':i.Main_ID,"Type":p,"Call":am,"Stat":cc,"Address":i.Address,"City":i.City,'Count':count2,'Percent':round(pp,2),'Lock':lock
              })

          context = {
            "Data":user,"Rand":rand,"Listed":hm,"Theme":data["Theme"],"Color":data["Color"],"Count":manager.count(),'page_obj': page_obj,'Name':pk}
          return render(request , "New/agent_page_list.html", context)
         #except:
          # return redirect('interview_page')
      else:
         return redirect('interview_page')








#=================================================== Edit ===========================================================
class Agent_Edit(APIView):
    def get(self , request,pk):

      if 'csrf-agent-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-agent-token']
          admin_token = admin_get(request)
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          user = Agent_Account.objects.get(id=int(find.User))


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
            "Extra":images,"ID":id,"Listed":client_bills,"Bills":bills,"Theme":admin_token["Theme"],"Color":admin_token["Color"]
            ,'P1':L_V1,'P2':L_V2,'P3':L_V3,
            }
          return render(request , "New/profile_agent.html", context)
       #  except:
        #   return render (request, 'New/profile.html')

      else:
         return redirect('agent_login')

    def post(self , request,pk):

      if 'csrf-agent-token' in request.COOKIES:
          print('2')
          user1_check = request.COOKIES['csrf-agent-token']
          admin_token = admin_get(request)
          print('2')
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          user = Agent_Account.objects.get(id=int(find.User))
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

             Gender=request.data['Gender'],





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


          return redirect(reverse('agent_edit',kwargs={"pk":pk}))
         #except:
           #  return render (request, 'Administrator/pages/samples/error-401.html')

      else:
          return redirect('admin_login')
    def put(self , request,pk):
      if 'csrf-agent-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-agent-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          user = Agent_Account.objects.get(id=int(find.User))
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
      if 'csrf-agent-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-agent-token']
          admin_token = admin_get(request)
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          user = Agent_Account.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          Client_Billing.objects.get(id=request.data["id"]).delete()
          return Response('OK')
        # except:
       #      return Response('No')
      else:
          return Response('No')

#______________________________________________________________________________________________________



    def update(self , request,pk):
      if 'csrf-agent-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-agent-token']
         admin_token = admin_get(request)
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Admin")
          user = Agent_Account.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          data = request.data
          File_Link.objects.filter(Post = pk).update(Link=data["Link"])
          return redirect('agent_page')
         except:
             return render (request, 'Administrator/pages/samples/error-401.html')

      else:
          return redirect('admin_login')

#______________________________________________________________________________________________________




class Agent_Edit_Update(APIView):


    def post(self , request):

      if 'csrf-agent-token' in request.COOKIES:
         print('2')
         user1_check = request.COOKIES['csrf-agent-token']
         admin_token = admin_get(request)
         print('2')
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check, Type="Agent")
          user = Agent_Account.objects.get(id=int(find.User))
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
             Gender=request.data['Gender'],
             Skill_Level=request.data["Skill_Level"],
             Marital=request.data['Marital'],

             Job_Choice1=request.data['Job_Choice1'],
             Country1=request.data['Country1'],
             Job_Choice2=request.data['Job_Choice2'],
             Country2=request.data['Country2'],
             Job_Choice3=request.data['Job_Choice3'],
             Country3=request.data['Country3'],




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



class Agent_Add_Booking(APIView):
    def get(self , request):

      data = agent_get(request)
   #   print(data)

      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])
          print(data)
          now = timezone.now()
          today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
          last_week_start = now - timedelta(days=7)
          last_month_start = now - timedelta(days=30)
          current_date = strftime("%Y-%m-%d")
          total = Booking.objects.all().count()
          day = Booking.objects.filter(Agent=user.id,Schedule_Date=current_date).count()
          week = Booking.objects.filter(Agent=user.id,Schedule_Date__gte=last_week_start).count()
          month = Booking.objects.filter(Agent=user.id,Schedule_Date__gte=last_month_start).count()
          rand = random.randint(0,1000)
          branch = Booking.objects.filter(Agent=user.id).order_by('id').reverse()
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
          context = {"Data":user,"Rand":rand,"Booking":listed,"Total2":branch.count(),"Theme":data["Theme"],"Color":data["Color"],"ID":inter,"Point":point,'page_obj':page_obj,
          'Day':day,'Week':week,'Month':month,'Total':total
          }
          return render(request, "New/book-list-agent.html",context)
      else:
         return redirect("login")


    def post(self , request):
      data = agent_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
            user = Agent_Account.objects.get(id = data["Data"])
            print(data)
            req = request.data

            c = Visa_Info.objects.get(id=int(req["Client"]))
            branch = Booking.objects.create(
              Name=c.Full_Name,User=c.id,Admin=1,Agent=user.id,Contact=c.Contact,About=req["About"],Location=c.Address,Type=req["Client"],
              Topic=req["Topic"],Gender=c.Gender,Schedule_Date=req["Date"],Schedule_Time=req["Time"],Remark="Pending",Status="Not In"
           )

            return redirect('agent_fill_page')
      else:
         return redirect("agent_login")


class Agent_Delete_Booking(APIView):
    def post(self , request):
      data = agent_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])
          print(data)
          req = request.data

          Booking.objects.filter(id=req["id"]).delete()

          return Response('Ok')
      else:
         return Response("No")









class Agent_Add_Call_Logs(APIView):
    def get(self , request,pk):

      data = agent_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])
          rand = random.randint(0,1000)

          busy =0
          next =0
          picked =0
          ans = 0
          mem = Visa_Info.objects.get(id=pk)

          calls = Call_Logs.objects.filter(Agent=user.id,Member=pk)
          for i in calls:
              if i.Status == "Picked Up":
                  picked+=1
              elif i.Status == "Rescheduled":
                  next+=1
              elif i.Status == "Unanswered":
                  ans+=1

              else:
                  busy+=1


          context = {"Data":user,"Rand":rand,"Member":mem,"Calls":calls,"Total":calls.count(),"Busy":busy,'Answer':ans,"Next":next,"Picked":picked,"Theme":data["Theme"],"Color":data["Color"]}
          return render(request, "New/agent_call_profiles.html",context)
      else:
         return redirect("login")


    def post(self , request,pk):
      data = agent_get(request)
   #   print(data)
      if data["Stat"] ==  "Ok":
          user = Agent_Account.objects.get(id = data["Data"])
          print(data)
          req = request.data
          mem = Visa_Info.objects.get(id=pk)
          if req["Audio"] == '':
            Call_Logs.objects.create(
                Name=mem.Full_Name,User=1,Agent=user.id,Member=pk,About=req["About"],Status=req["Status"],
                Contact=mem.Contact,Location=mem.Address,Gender=mem.Gender,
                Start_Time=req["Start_Time"],End_Time=req["End_Time"],Type="Text"
            )
          else:
            call = Call_Logs.objects.create(
                Name=mem.Full_Name,User=1,Agent=user.id,Member=pk,About=req["About"],Status=req["Status"],
                Contact=mem.Contact,Location=mem.Address,Gender=mem.Gender,
                Start_Time=req["Start_Time"],End_Time=req["End_Time"],Type="Audio"
            )
            uploading_file = request.FILES['Audio']
            fs = FileSystemStorage()
            fs.save("Call_Logs//"+str(call.id)+".mp3",uploading_file)


          return redirect(reverse('agent_add_call_logs',kwargs={"pk":pk}))
      else:
         return redirect("login")

