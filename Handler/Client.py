from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
#from . serializers import  Client_Serializer,User_Serializer
from .models import *
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
from django.core.paginator import Paginator
#--------------------- Extra ----------------------
from . Extra import get
from django.utils.timesince import timesince
from django.utils import timezone
import threading
from datetime import datetime
#--------------------- Extra ----------------------
#Visa_Info.objects.filter(id=8647).update(Account_Type='Main')
#Visa_Info.objects.filter(id=8646).update(Account_Type='Main')

class Dashboard_User(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           fund = Funds_info.objects.filter(User=data.id,Status="Recieved")

           total = 0
           new = Debit_info.objects.filter(User=data.id)

           for i in new:
             total+=i.Amount
           for i in fund:
              total+=float(i.Amount)

           bill = 0
           client_bill =Client_Billing.objects.filter(User=data.id)
           for i in client_bill:
             bill+=i.Price

           try:
            t1 = (total/bill)*100
           except:
             t1=0
           print(t1)

           if bill==0:
            balance = 0
           else:
            balance = float(bill) - float(total)

           context={"User":data,"Rand":rand,"Date":current_date,"Total":total,"Ballance":balance,"Funds":client_bill,"Value":t1-100}
           return render(request , "Pannel/index.html",context)

        #except:

         #  return redirect('login')
       return redirect('client_login')




class Payment_User_List2(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           new = Debit_info.objects.filter(User=data.id)

           listed = Funds_info.objects.filter(User=data.id)
           funds = []
           for i in listed:
             funds.append({
               "id":i.id,"Amount":i.Amount,"time":i.time,"date":i.date,"Status":i.Status
             })
           for i in new:
             funds.append({
               "id":i.id,"Amount":i.Amount,"time":i.time,"date":i.date,"Status":"Recieved"
             })

           context={"User":data,"Rand":rand,"Date":current_date,"Funds":funds}
           return render(request , "Pannel/list.html",context)


        #except:

         #  return redirect('login')
       return redirect('client_login')







class Profile_User(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])

           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)
           manager =  Visa_Info.objects.get(id=data_id["Data"])

           profiles = Extra_Images.objects.filter(Profile=data_id["Data"],Type="Profile")
           ids = Extra_Images.objects.filter(Profile=data_id["Data"],Type="Id")
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
           edu = Extra_Info.objects.filter(Profile=data_id["Data"],Type="School")
           work = Extra_Info.objects.filter(Profile=data_id["Data"],Type="Work")
           bills = Billings.objects.all().order_by('id').reverse()
           client_bills = Client_Billing.objects.filter(User=data_id["Data"]).order_by('id').reverse()
    #      print(new_list)
           L_1 = Completed_Logs.objects.filter(Client=data_id["Data"],Type='1').count()
           L_2 = Completed_Logs.objects.filter(Client=data_id["Data"],Type='2').count()
           L_3 = Completed_Logs.objects.filter(Client=data_id["Data"],Type='3').count()

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

           try:
               fund = Agent_Form_Funds.objects.get(Client=data.id)
               if fund.Status == 'Pending':
                   p_type = 'No'
               else:
                 if fund.Completed == 'Completed':
                     p_type = 'Yes'
                 else:
                   return render(request , "Pannel/prompt2.html")
           except:
             p_type = 'No'


           current_date = strftime("%Y-%m-%d")
           context={"User":data,"Rand":rand,"Date":current_date,"Rand":rand,"Staff":manager,"Education":edu,"Work":work,"Extra":images,"ID":id,"Listed":client_bills,"Bills":bills
           ,'P1':L_V1,'P2':L_V2,'P3':L_V3,'Fill_Account':p_type}
           return render(request , "Chat/my_profile.html",context)

        #except:

         #  return redirect('login')
       return redirect('client_login')
    def post(self , request):

       data_id = get(request)
       if data_id["Stat"] ==  "Ok":

          data_id = get(request)


          User_data = Visa_Info.objects.get(id=int(data_id["Data"]))
          current_date = strftime("%Y-%m-%d")
          print('2')
        #  print(request.data)
          pk = data_id["Data"]
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



 #========================================= PDF ============================================
          if request.data["PDF"] == '':
           pass
          else:

           try:
            os.remove(f'{BASE_DIR}/media/Medical_Results/{pk}.pdf')
           except:
             pass
           uploading_file = request.FILES['PDF']
           fs = FileSystemStorage()
           fs.save("Medical_Results//"+str(pk)+".pdf",uploading_file)
#========================================= PDF ============================================



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


          return redirect('client_profile')
         #except:
           #  return render (request, 'Administrator/pages/samples/error-401.html')

       else:
          return redirect('admin_login')
class Confirm_Payment(APIView):
    def post(self , request,pk):
     print(request.data["ResponseCode"])
     print(request.data["Data"]['ClientReference'])
     if request.data["ResponseCode"] == '0000':
         Funds_info.objects.filter(id=pk).update(Status="Recieved")
         return Response(200)
     else:
         Funds_info.objects.get(id=pk).delete()
         return Response(200)

class Payment_User(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")
           context={"User":data,"Rand":rand,"Date":current_date}
           return render(request , "Pannel/pay.html",context)

        #except:

         #  return redirect('login')
       return redirect('login')
    def post(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:

           data = Visa_Info.objects.get(id=data_id["Data"])
           fund = Funds_info.objects.create(User=data.id,Amount=request.data["pay"],Status="Pending")
           uid_val = f'{str(uuid.uuid1())[0:15]}-{fund.id}'
           url = "https://payproxyapi.hubtel.com/items/initiate"

           payload = {
    "totalAmount": request.data["pay"],
    "description": "OTravel Payments.",
    "callbackUrl": f"https://www.sikobs.world/confirm_payment/{fund.id}",
    "returnUrl": "https://www.sikobs.world/prompt",
    "cancellationUrl": "https://www.sikobs.world/client_dashboard",
    "merchantAccountNumber": "2017154",
    "clientReference": uid_val
           }
           headers = {
              "accept": "application/json",
              "content-type": "application/json",
              "authorization": "Basic MFlwelFCRzoyZWU3OGU5YWE2ZTM0NDQ0OGFmMzRjNTI1ODcwNTlkYg=="
           }
           response = requests.post(url, json=payload, headers=headers)
           print(response.json())
           return HttpResponseRedirect(response.json()['data']['checkoutUrl'])

       return redirect('client_login')

class Prompt(APIView):
    def get(self , request):

         return render(request, "Pannel/prompt.html")


class Client_New_Login(APIView):
    def get(self , request):
      data = get(request)
      if data["Stat"] ==  "Ok":

          return redirect("client")
      else:
         return render(request, "Pannel/login2.html")

    def post(self , request):
          print(request.data)
          try:
           data = Visa_Info.objects.get(Contact=request.data["Contact"],Password=request.data["Password"])
          except:
              return redirect('client_login')
          print(data)
          response = redirect("client")
          try:
             look_up = Cookie_Handler.objects.get(User=data.id, Type="User")
             generated_uuid = look_up.Cookie
          except:
             generated_uuid = uuid.uuid1()
          Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="User")
          response.set_cookie('cookie_session_id',generated_uuid)
          return response

class Client_Login(APIView):
    def get(self , request):
      data = get(request)
      if data["Stat"] ==  "Ok":

          return redirect("client")
      else:
         return render(request, "Pannel/login.html")


class Login_Authenticate(APIView):
    def post(self , request):
          print(request.data)
          data = Visa_Info.objects.get(Refrene_Code=request.data["id"])
          print(data)
          response = Response({"State":"Ok"})
          try:
             look_up = Cookie_Handler.objects.get(User=data.id, Type="User")
             generated_uuid = look_up.Cookie
          except:
             generated_uuid = uuid.uuid1()
          Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="User")
          response.set_cookie('cookie_session_id',generated_uuid)
          return response

class Client_Logout_Main(APIView):
    def get(self , request):
      response = redirect("client_login")
      response.delete_cookie('cookie_session_id')
      return response



class Site_Blog(APIView):
    def get(self , request):
        data_id = get(request)
        if data_id["Stat"] ==  "Ok":
      #  try:
          data = Visa_Info.objects.get(id=data_id["Data"])
          if data.Account_Type == 'Main':
               redirect('messages')
          rand = random.randint(0,1000)
          color = ["linear-gradient(to bottom right, blue, yellow)","linear-gradient(to bottom right, red, yellow)","linear-gradient(to bottom right, gray, black)"
                                      ,"linear-gradient(to bottom right, black, white)","linear-gradient(to bottom right, green, blue)","linear-gradient(to bottom right, pink, red)"]
          css_gradient_colors = [
    "linear-gradient(to right, #ff0000, #ffff00)",
    "linear-gradient(to right, #0000ff, #00ff00)",
    "linear-gradient(to right, #800080, #ff69b4)",
    "linear-gradient(to right, #ffa500, #ff0000)",
    "linear-gradient(to right, #008080, #0000ff)",
    "linear-gradient(to right, #00ff00, #ffff00)",
    "linear-gradient(to right, #00ffff, #800080)",
    "linear-gradient(to right, #ffff00, #ff69b4)",
    "linear-gradient(to right, #0000ff, #800080)",
    "linear-gradient(to right, #ff0000, #008080)",
    "linear-gradient(to right, #ff69b4, #00ff00)",
    "linear-gradient(to right, #ffa500, #ffff00)",
    "linear-gradient(to right, #0000ff, #00ffff)",
    "linear-gradient(to right, #800080, #ff0000)",
    "linear-gradient(to right, #00ff00, #008080)"
]


          extra = Extra_Images_Post.objects.all()
          post = Post_Info.objects.all().order_by('id').reverse()
          listed = []
          paginator = Paginator(post, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          for i in page_obj:
           timed1 = timezone.make_aware(datetime.combine(i.date, i.Time))
           timed = timesince(timed1) + " ago"
           if i.Type == "Vid_Post":
                name = Administrator_Info.objects.get(id=i.User).Full_Name
                use = f'Admin/{i.User}'

                like =Likes.objects.filter(Post=i.id).count()
                Comment =Comments.objects.filter(Post=i.id).count()
                vid = Extra_Videos.objects.get(Post=i.id)

                listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"Like":like,
                   "Comment":Comment,"Vid":vid.id,"id":i.id,"Admin":name,"date":i.date,"User":use,"Time":timed
                   })

           elif i.Type == "Img_Post":
                name = Administrator_Info.objects.get(id=i.User).Full_Name
                use = f'Admin/{i.User}'

                like =Likes.objects.filter(Post=i.id).count()
                Comment =Comments.objects.filter(Post=i.id).count()
                img = Extra_Images_Post.objects.get(Post=i.id)
                listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"Like":like,
                   "Comment":Comment,"Img":img.id,"id":i.id,"Admin":name,"date":i.date,"User":use,"Time":timed
                   })
           elif i.Type == "Youtube":
              name = Administrator_Info.objects.get(id=i.User).Full_Name
              use = f'Admin/{i.User}'

              like =Likes.objects.filter(Post=i.id).count()
              Comment =Comments.objects.filter(Post=i.id).count()

              listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"Like":like,"Link":i.Link,"Time":timed,
                   "Comment":Comment,"id":i.id,"Admin":name,"date":i.date,"User":use,
                   })
           else:
              name = Administrator_Info.objects.get(id=i.User).Full_Name
              use = f'Admin/{i.User}'

              like =Likes.objects.filter(Post=i.id).count()
              Comment =Comments.objects.filter(Post=i.id).count()
              rand_color = random.choice(css_gradient_colors)
              listed.append({
                   "id":i.id,"Type":i.Type,"Context":i.Context,"Like":like,
                   "Comments":Comment,"id":i.id,"Admin":name,"date":i.date,"User":use,"Time":timed,'Color':rand_color
                   })
          context = {"User":data,"Rand":rand,"Extra":extra,"Posts":listed,'page_obj':page_obj}
          return render(request, f"Chat/post.html",context)
        return redirect('client_login')




#------------------------------------------------------------------------------------------------




class Sign_File(APIView):
    def get(self , request,pk):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
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
               stat = ea.Status
               uid = ea.Uid


           except:
               e = 0
               dt = strftime("%Y-%m-%d")
               day =strftime("%d")
               month = strftime("%B")
               year = strftime("%y")
               stat = 'Pending'
               uid = 0

           try:
               e1 = Withness_Signed_Document.objects.get(Document=pk,User=data.id)

           except:
               e1 = {'id':0}


           context={"User":data,"Rand":rand,"Date":dt,'Admin':ad,'Main':pk,'Image':e,'Witness':e1,'Day':day,"Month":month,"Year":year,'Status':stat,'Uid':uid}
           return render(request , f"Signature/{pk}.html",context)


        #except:

         #  return redirect('login')
       return redirect('client_login')


    def post(self , request,pk):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
          data = Visa_Info.objects.get(id=data_id["Data"])
          print(data)
          req = request.data

          g = User_Signed_Document.objects.filter(Document=pk,User=data.id)
          if g.count() > 0:
           try:
            os.remove(f'{BASE_DIR}/media/Signature/{g.last().id}.png')
           except:
             pass
           uploading_file = request.FILES['signature']
           fs = FileSystemStorage()
           fs.save("Signature//"+str(g.last().id)+".png",uploading_file)
          else:
           e = User_Signed_Document.objects.create(Document=pk,User=data.id,Status='Pending',Uid=uuid.uuid1())
           uploading_file = request.FILES['signature']
           fs = FileSystemStorage()
           fs.save("Signature//"+str(e.id)+".png",uploading_file)


          return Response('Ok')
      else:
         return Response("No")


class Witness_Sign_File(APIView):
    def post(self , request,pk):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
          data = Visa_Info.objects.get(id=data_id["Data"])
          print(data)
          req = request.data

          g = Withness_Signed_Document.objects.filter(Document=pk,User=data.id)
          if g.count() > 0:
           try:
            os.remove(f'{BASE_DIR}/media/Witness_Signature/{g.last().id}.png')
           except:
             pass
           uploading_file = request.FILES['signature']
           fs = FileSystemStorage()
           fs.save("Witness_Signature//"+str(g.last().id)+".png",uploading_file)
           g.update(Name=request.data['Name'])
          else:
           e = Withness_Signed_Document.objects.create(Document=pk,User=data.id,Name=request.data['Name'])
           uploading_file = request.FILES['signature']
           fs = FileSystemStorage()
           fs.save("Witness_Signature//"+str(e.id)+".png",uploading_file)


          return Response('Ok')
      else:
         return Response("No")






class List_Sign_File(APIView):
    def get(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           if data.Account_Type == 'Main':
               redirect('messages')
           rand = random.randint(0,1000)
           current_date = strftime("%Y-%m-%d")

           context={"User":data,"Rand":rand,"Date":current_date,}
           return render(request , "Chat/list_documents.html",context)


        #except:

         #  return redirect('login')
       return redirect('client_login')








from django.db import transaction

def get_next_agent(last_user_id):
    """Returns the next available agent in round-robin order, skipping excluded IDs."""
    excluded_ids = [15,8,10]  # Exclude these always

    agents = Administrator_Info.objects.filter(Agent='Yes').exclude(id__in=excluded_ids).order_by('id')
    if not agents.exists():
        return None  # No agents available

    # Try to find the next agent with a higher ID than the last assigned one
    next_agent = agents.filter(id__gt=last_user_id).first()
    if next_agent:
        return next_agent

    # Wrap around to the first agent if we reached the end
    return agents.first()


def set_agent(client_id):
    try:
        with transaction.atomic():
            # Get or create the record tracking the last agent used
            last_agent_record, _ = Last_Agent.objects.get_or_create(id=1, defaults={'User': 0})
            last_agent_id = last_agent_record.User

            # Get next available agent
            next_agent = get_next_agent(last_agent_id)
            if not next_agent:
                print("❌ No agents available.")
                return

            # Check if agent link already exists
            existing_link = Agent_Account_Link.objects.filter(Client=client_id)

            if existing_link.exists():
                # Update existing agent-client links
              pp =  Agent_Form_Funds.objects.filter(Client=client_id)
              if pp.count() > 0:
                if pp.last().Status == 'Recieved':
                 print('================================= Paid=========================')
                 Visa_Info.objects.filter(id=client_id).update(Agent=next_agent.id, Agent_Type='Staff')
                 Agent_Account_Link.objects.filter(Client=client_id).update(User=next_agent.id, Type='Staff')
                 Agent_Form_Funds.objects.filter(Client=client_id).update(User=next_agent.id, Type='Staff')
              else:
                 print('================================= Paid  NONE =========================')
                 Visa_Info.objects.filter(id=client_id).update(Agent=next_agent.id, Agent_Type='Staff')
                 Agent_Account_Link.objects.filter(Client=client_id).update(User=next_agent.id, Type='Staff')
                # Agent_Form_Funds.objects.filter(Client=client_id).update(User=next_agent.id, Type='Staff')
            else:
                # Create new link and assign agent
                Agent_Account_Link.objects.create(User=next_agent.id, Client=client_id, Status='Pending', Type='Staff')
                Visa_Info.objects.filter(id=client_id).update(Agent=next_agent.id, Agent_Type='Staff')

            # Update last used agent ID
            last_agent_record.User = next_agent.id
            last_agent_record.save()

            print(f"✅ Agent {next_agent.id} assigned to client {client_id}.")

    except Exception as e:
        print(f"⚠️ Error assigning agent: {e}")


#set_agent(98)


def fix_add_all_cro():
    al = [15,10]
    gp = ['Booked','Unreachable','Briefed']
    x =  Visa_Info.objects.filter(Agent__in=al,Group__in=gp).order_by('id')
  #  if not agents.exists():)
    for i in x:
        set_agent(i.id)
        print(f'Sent--------------------{i.id}--------------')
#thread = threading.Thread(target=fix_add_all_cro)
#thread.start()

def add_all_cro():
    al = [15,10]
    gp = ['Booked','Unreachable','Briefed']
    x =  Visa_Info.objects.filter(Agent__in=al,Group__in=gp).order_by('id')
  #  if not agents.exists():)
    for i in x:
      try:

               try:
                a = int(x.Call)
                Agent_Account_Link.objects.create(User=a,Client=i.id,Status='Pending',Type='Staff')
                Visa_Info.objects.filter(id=i.id).update(Agent=a,Agent_Type='Staff')
                st = 'Assigned 1'
               except:
                set_agent(i.id)

                st = 'Called 1'

               print(f'------------------------------------  {i.Agent} ---------------------------------------')
      except:

       try:
        a = int(x.Call)
        Agent_Account_Link.objects.create(User=a,Client=i.id,Status='Pending',Type='Staff')
        Visa_Info.objects.filter(id=i.id).update(Agent=a,Agent_Type='Staff')
        st = 'Assigned 2'
       except:
        set_agent(i.id)
        st = 'Called 2'

      print(f'Procced id {i.id} and status "{st}"')

#thread = threading.Thread(target=add_all_cro)
#thread.start()







#Agent_Account_Link.objects.filter(Client=9726).update(User=2)
#Visa_Info.objects.filter(id=9726).update(Agent_Type='Staff',Agent=2)
#Agent_Form_Funds.objects.filter(Client=9726).update(User=2)

def fix_agent():
    x = Agent_Account_Link.objects.filter(Type='Staff')
    for i in x:
        a = Visa_Info.objects.get(id=i.Client)
        try:
            if int(a.Call) == int(a.Agent):
                print('The Same')
                a = Visa_Info.objects.get(id=i.Client)
                Agent_Account_Link.objects.filter(Client=i.Client,Type='Staff').update(User=a.Agent)
                Agent_Form_Funds.objects.filter(Client=i.Client).update(User=a.Agent)
                print(f'user {i.Client}  ------ {a} ---------- {a.Agent} ------  {a.Call}')
            else:
              user = Administrator_Info.objects.get(id=a.Call)
              if user.Agent == 'Yes':
               a = Visa_Info.objects.get(id=i.Client)
               print(f'{a.Call}  --- {a.Agent}')
               z = Visa_Info.objects.filter(id=i.Client)
               print(z)
               z.update(Agent=a.Call,Agent_Type='Staff')
               a = Visa_Info.objects.get(id=i.Client)
               print(f'{a.Call}  --- {a.Agent}')

               print('Data Fixed')
               a = Visa_Info.objects.get(id=i.Client)
               Agent_Account_Link.objects.filter(Client=i.Client,Type='Staff').update(User=int(user.id))
               Agent_Form_Funds.objects.filter(Client=i.Client).update(User=a.Agent)
               print(f'user {i.Client}  ------ {a} ---------- {a.Agent} ------  {a.Call}')
              else:
                  print('Staff Not An Agent')
        except:
            print('Not Match')
#thread = threading.Thread(target=fix_agent)
#thread.start()

#s = Agent_Form_Funds.objects.all()
#for ss in s:
 #   uid_val = f'{str(uuid.uuid1())[0:15]}'
   # Agent_Form_Funds.objects.filter(id=ss.id).update(Refrence=uid_val)
  #  print(ss)


def cc():
    for i in range(10702,10709):
     a = Visa_Info.objects.filter(id=i).update(Account_Type='Main')
     print(Visa_Info.objects.get(id=i).Full_Name)
    #Agent_Account_Link.objects.filter(User=,Client=id,Type='Staff').update(User=int(user.id))
#thread = threading.Thread(target=cc)
#thread.start()


def fix_agent1():
    x = Visa_Info.objects.filter(Group='Pending')
    for i in x:

       # try:
            a = Visa_Info.objects.get(id=i.id)
            e =  Agent_Form_Funds.objects.filter(Client=i.id,Status='Recieved')
            if e.count() > 0:
              print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PAID😎<<<<<<<<<<<<<<<<<<<<{i.id} --- {i.Full_Name}')
            else:
                set_agent(i.id)
                print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Done😏<<<<<<<<<<<<<<<<<<<<{i.id} --- {i.Full_Name}')



       # except:
          #  print('Not Match')


#thread = threading.Thread(target=fix_agent1)
#thread.start()








def fix_agent2():
    x = a2= Agent_Form_Funds.objects.all()
    for i in x:
      val = f'{uuid.uuid1()}_{i.id}'
      manager = Agent_Form_Funds.objects.filter(id=i.id).update(Transfared='Pending',Refrence=val)
      print(f'{i.id}-----------------------------')


      #  except:
        #    print('Not Match')


#thread = threading.Thread(target=fix_agent2)
#thread.start()
#==================================== Payment ==========================================

class Confirm_Payment_Form(APIView):
    def post(self , request,pk):
     print(request.data["ResponseCode"])
     print(request.data["Data"]['ClientReference'])
     if request.data["ResponseCode"] == '0000':
         Agent_Form_Funds.objects.filter(id=pk).update(Status="Recieved")
         return Response(200)
     else:
         Funds_info.objects.get(id=pk).delete()
         return Response(200)

class Payment_Form(APIView):

    def post(self , request):
      # dat = Visa_Info.objects.all()
     #    val = f'{uuid.uuid1()}_{i.id}'
   #     Visa_Info.objects.filter(id=i.id).update(Refrene_Code=val)
       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:

           data = Visa_Info.objects.get(id=data_id["Data"])
           try:
               fund = Agent_Form_Funds.objects.get(Client=data.id)
               if fund.Status == 'Pending':
                   pass
               else:
                 return redirect('client_profile')
           except:
            try:
             if int(data.Agent) == 0:
                set_agent(data.id)
                data = Visa_Info.objects.get(id=data_id["Data"])
            except:
                set_agent(data.id)
                data = Visa_Info.objects.get(id=data_id["Data"])
           uid_val = f'{str(uuid.uuid1())[0:15]}'
           fund = Agent_Form_Funds.objects.create(Client=data.id,Amount=150,Transfared="Pending",Status="Pending",Type=data.Agent_Type,User=data.Agent,Completed="Pending",Refrence=uid_val)


           url = "https://payproxyapi.hubtel.com/items/initiate"

           payload = {
    "totalAmount": 150,
    "description": "OTravel Payments.",
    "callbackUrl": f"https://www.sikobs.world/confirm_payment_form/{fund.id}",
    "returnUrl": "https://www.sikobs.world/prompt",
    "cancellationUrl": "https://www.sikobs.world/client_dashboard",
    "merchantAccountNumber": "2017154",
    "clientReference": uid_val
           }
           headers = {
              "accept": "application/json",
              "content-type": "application/json",
              "authorization": "Basic MFlwelFCRzoyZWU3OGU5YWE2ZTM0NDQ0OGFmMzRjNTI1ODcwNTlkYg=="
           }
           response = requests.post(url, json=payload, headers=headers)
           print(response.json())
           return HttpResponseRedirect(response.json()['data']['checkoutUrl'])

       return redirect('client_login')





def update_agent(client_id):
    try:
        # Get or create the record tracking the last agent used
        last_agent, _ = Last_Agent.objects.get_or_create(id=1, defaults={'User': 1})

        next_agent = get_next_agent(last_agent.User)
        if not next_agent:
            print("❌ No agents available.")
            return

        with transaction.atomic():
            # Link agent to client


            # Update Visa_Info with the selected agent
            xp =Agent_Account_Link.objects.filter(Client=client_id)
            if xp.count() > 0 :
                Agent_Account_Link.objects.filter(Client=client_id).update(User=next_agent.id,Type='Staff')
                print(next_agent.id)
                Agent_Form_Funds.objects.filter(Client=client_id).update(User=next_agent.id,Type='Staff')
                print(f"✅ A3333333333333333333333333333333333 ist olient {client_id}.")

            else:
             Agent_Account_Link.objects.create(User=next_agent.id,Client=client_id,Status='Pending',Type='Staff')

            Visa_Info.objects.filter(id=client_id).update(Agent=next_agent.id,Agent_Type='Staff')

            # Save the current agent as the last used
            last_agent.User = next_agent.id
            last_agent.save()






        print(f"✅ Agent olient {client_id}.")

    except Exception as e:
        print(f"⚠️ Error assigning agent: {e}")


def xp():
  x = Agent_Account_Link.objects.filter(User=27)
  print(x)
  for i in x:
     update_agent(i.Client)

#xp()

#set_agent(98)
#s = User_Signed_Document.objects.all()
#for i in s:

 #User_Signed_Document.objects.filter(id=i.id).update(Uid=uuid.uuid1())
 #print('ok')





class Sign_File_View(APIView):
    def get(self , request,pk,pk2):



           rand = random.randint(0,1000)

           #new = Debit_info.objects.filter(User=data.id)

           ad = Administrator_Info.objects.all().last()

           try:
               ea = User_Signed_Document.objects.get(Uid=pk)
               e =ea.id
               dt = ea.date
               day =dt.day
               month = dt.strftime('%B')
               year = dt.strftime('%y')
               stat = ea.Status
               uid = ea.Uid


           except:
               e = 0
               dt = strftime("%Y-%m-%d")
               day =strftime("%d")
               month = strftime("%B")
               year = strftime("%y")
               stat = 'Pending'
               uid = 0

           try:
               e1 = Withness_Signed_Document.objects.get(Document=ea.id)

           except:
               e1 = {'id':0}


           context={"Rand":rand,"Date":dt,'Admin':ad,'Main':pk2,'Image':e,'Witness':e1,'Day':day,"Month":month,"Year":year,'Status':stat,'Uid':uid,'Type':'OFF'}
           return render(request , f"Signature/{pk2}.html",context)



'''

import os
import django
import threading
from django.core.management import call_command
from django.db import transaction
from django.apps import apps
from collections import defaultdict

# Load Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Change to your project
django.setup()


def get_model_dependencies():
    """Return models in dependency order based on foreign keys."""
    graph = defaultdict(set)
    all_models = list(apps.get_models(include_auto_created=False))

    # Build dependency graph
    for model in all_models:
        for field in model._meta.get_fields():
            if field.is_relation and field.many_to_one and field.remote_field:
                parent = field.remote_field.model
                if parent != model:  # avoid self-references
                    graph[model].add(parent)

    # Topological sort
    result = []
    visited = set()

    def visit(m):
        if m in visited:
            return
        for dep in graph[m]:
            visit(dep)
        visited.add(m)
        result.append(m)

    for model in all_models:
        visit(model)

    return result


def migrate_model_data(model_class, source_alias='default', target_alias='dbmain', batch_size=500):
    """Copy data from source DB to target DB preserving PKs, skipping existing ones."""
    pk_name = model_class._meta.pk.name  # Get actual PK field name

    try:
        existing_ids = set(
            model_class.objects.using(target_alias).values_list(pk_name, flat=True)
        )
    except Exception as e:
        print(f"⚠ Could not check existing IDs for {model_class.__name__}: {e}")
        return

    try:
        qs = model_class.objects.using(source_alias).exclude(**{f"{pk_name}__in": existing_ids})
    except Exception as e:
        print(f"⚠ Could not fetch source data for {model_class.__name__}: {e}")
        return

    total = qs.count()
    if total == 0:
        print(f"⏩ No new records for {model_class.__name__}")
        return

    print(f"📦 Migrating {total} records for {model_class.__name__}...")

    start = 0
    while start < total:
        batch = list(qs.order_by(pk_name)[start:start + batch_size])
        if not batch:
            break

        with transaction.atomic(using=target_alias):
            for obj in batch:
                try:
                    data = {f.name: getattr(obj, f.name) for f in obj._meta.fields}
                    model_class.objects.using(target_alias).create(**data)
                except Exception as e:
                    print(f"⚠ Skipped {model_class.__name__} {pk_name}={getattr(obj, pk_name, None)}: {e}")

        start += batch_size
        print(f"  ✅ {min(start, total)}/{total} done")

    print(f"✔ Done {model_class.__name__}\n")


def spo():
    # Step 1 — Create tables in PostgreSQL
    print("🔨 Creating tables in PostgreSQL...")
    call_command("migrate", database="dbmain")

    # Step 2 — Get models Sn FK dependency order
    print("🚀 Copying data from SQLite to PostgreSQL...\n")
    models_in_order = get_model_dependencies()

    for model in models_in_order:
        migrate_model_data(model)

    print("🎉 All data copied successfully!")


# Run in separate thread
#thread = threading.Thread(target=spo)
#thread.start()
'''