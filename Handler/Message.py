from django.shortcuts import render,redirect
from django.urls import reverse
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
from PIL import Image
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent

#--------------------- Extra ----------------------
from . Extra import get
from django.shortcuts import render, redirect
from django.db.models import Count
from time import strftime
from django.core.paginator import Paginator


from .noti import *
#--------------------- Extra ----------------------

def count_dict_occurrences(dict_list):
    occurrence_counts = {}  # Dictionary to store occurrence counts
    new_list = []           # List to store dictionaries with occurrence counts

    for d in dict_list:
        # Convert dictionary to a hashable representation (tuples of key-value pairs)
        dict_tuple = tuple(sorted(d.items()))

        # Count occurrences of the dictionary
        if dict_tuple in occurrence_counts:
            occurrence_counts[dict_tuple] += 1
        else:
            occurrence_counts[dict_tuple] = 1

    for dict_tuple, count in occurrence_counts.items():
        # Convert back to dictionary and add the count
        dict_with_count = dict(dict_tuple)
        dict_with_count['occurrences'] = count
        new_list.append(dict_with_count)

    return new_list

def Check2(id):
   #---------------------------------------- Subscription ---------------------------------------------
           data= Message.objects.get(id=id)

           current_date = strftime("%Y-%m-%d")
           #------------------------------------------- Online Status --------------------------------------------------

           years = (int(str(current_date).split("-")[0]) - int(str(data.date).split("-")[0]))*356
           months = (int(str(current_date).split("-")[1]) - int(str(data.date).split("-")[1]))*30
           days = (int(str(current_date).split("-")[2]) - int(str(data.date).split("-")[2]))
           result = years+months+days
           if result > 0 :
             print(result)
             if result == 1:
               return(str(result)+" Day Ago")
             elif result < 7:
               return(str(result)+" Days Ago")
             else:
               return("On "+str(data.date))
           else:
            hour = (int(strftime("%H")) - float(str(data.time).split(":")[0]))*3600
            minute = (int(strftime("%M")) - float(str(data.time).split(":")[1]))*60
            second = (int(strftime("%S")) - float(str(data.time).split(":")[2]))
            result2 = round(hour +second+minute)
            if result2 < 60:
             return(str(result2)+" Seconds ago")
            elif result2/60 < 60:

             return(str(round(result2/60))+" Minutes ago")
            else:
             return(str(round((result2/60)/60))+" Hours ago")




class My_Messages(APIView):
    def get(self, request):
        data_id = get(request)
        if data_id["Stat"] != "Ok":
            return redirect('login')

        try:
            data = Visa_Info.objects.get(id=data_id["Data"])
            if data.Blocked == "Yes":
                return render(request, 'Administrator/pages/samples/error-600.html')

            # Fetch all messages related to the user in one query
            messages = Message.objects.filter(Reciever=data.id)
            unseen_messages = messages.filter(Status='Unseen')

            # Count occurrences of messages per sender
            sender_counts = unseen_messages.values('Sender').annotate(count=Count('Sender'))

            listed = []
            sender_info_map = {info.id: info for info in Visa_Info.objects.filter(id__in=[s['Sender'] for s in sender_counts])}

            for sender_data in sender_counts:
                sender_id = sender_data['Sender']
                last_msg = unseen_messages.filter(Sender=sender_id).last()
                if sender_id in sender_info_map:
                    sender_info = sender_info_map[sender_id]
                    listed.append({
                        "id": sender_info.id,
                        "Name": sender_info.Full_Name,
                        "Time": Check2(last_msg.id),
                        "Message": last_msg.Info,
                        "Status": last_msg.Status,
                        "Count": sender_data['count']
                        ,'Reply_Id':last_msg.Reply_Id,
                        'Reply':last_msg.Reply
                    })

            # Fetch message list in one query
            clients = Message_List.objects.filter(User=data.id)
            client_ids = clients.values_list('Client', flat=True)

            # Pre-fetch client info
            client_info_map = {info.id: info for info in Visa_Info.objects.filter(id__in=client_ids)}

            for client in clients:
                if client.Client not in sender_info_map:  # Avoid duplicates from unseen messages
                    last_msg = Message.objects.filter(Chat=client.Link).last()
                    if last_msg:
                        client_info = client_info_map.get(client.Client)
                        if client_info:
                            listed.append({
                                "id": client_info.id,
                                "Name": client_info.Full_Name,
                                "Time": Check2(last_msg.id),
                                "Message": last_msg.Info,
                                "Status": last_msg.Status,
                                "Count": "Null",
                                'Reply_Id':last_msg.Reply_Id,
                               'Reply':last_msg.Reply
                            })

            # Apply pagination
            page_number = request.GET.get('page', 1)
            paginator = Paginator(listed, 20)  # Load 10 messages per page
            paginated_listed = paginator.get_page(page_number)

            # Notifications count
            noted = Notifications.objects.filter(User=data.id).count()

            # Contact list
            contact_list = [
                {"id": client_info.id, "Name": client_info.Full_Name}
                for client_id, client_info in client_info_map.items()
            ]

            # All staff list (excluding current user)
            all_staff = [{"id": i.id, "Full_Name": i.Full_Name} for i in Visa_Info.objects.exclude(id=data.id)]
            recent = Visa_Info.objects.order_by('-id')[:10]
            context = {
                "Note": noted,
                "User": data,
                "Data": data,

                "Contact": contact_list,
                "All_Staff": all_staff,
                'page_obj':paginated_listed,
                'Recent':recent
            }

            return render(request, 'Chat/home.html', context)
        except Visa_Info.DoesNotExist:
            return redirect('login')




class Client_Message(APIView):
    def get(self , request,pk):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
       # try:
           data = Visa_Info.objects.get(id=data_id["Data"])
           current_date = strftime("%Y-%m-%d")
           if data.Blocked == "Yes":
            return render(request, 'Administrator/pages/samples/error-600.html')


           rand = random.randint(0,1000)
           Client= Visa_Info.objects.get(id=pk)
           try:
            chat = Message_List.objects.get(User=data.id,Client=pk)

            Message.objects.filter(Chat=chat.Link,Reciever = data.id).update(Status="Seen")

            messages = Message.objects.filter(Chat=chat.Link).order_by('id').reverse()[:10:-1]

           except:
             messages = []
             chat = "null"
           send_out =[]
           for i in messages:
              send_out.append({
                 "id":i.id,"Type":i.Type,"Info":i.Info,"Time":f'{str(i.time).split(":")[0]}:{str(i.time).split(":")[1]}',"Sender":i.Sender,"Reciever":i.Reciever,"Status":i.Status,'Reply_Id':i.Reply_Id,'Reply':i.Reply
              })

           noted = Notifications.objects.filter(User=data.id).count()
           context = {"Note":noted,"User_Data":data,"Data":data,"Client":Client,"Rand":rand,"Messages":send_out ,"Chat":chat}
           return render(request, 'Chat/private-chat.html', context)




       # except:
        #   return Response('No')
      return redirect('login')

#Visa_Info.objects.filter(id=6251).update(Account_Type="Main",Password='pass2')
#Visa_Info.objects.filter(id=6252).update(Account_Type="Main",Password='pass3')
#Visa_Info.objects.filter(id=6253).update(Account_Type="Main",Password='pass4')
#Visa_Info.objects.filter(id=6254).update(Account_Type="Main",Password='pass5')
#Visa_Info.objects.filter(id=6255).update(Account_Type="Main",Password='pass6')

class Client_Message_All(APIView):
    def get(self , request,pk):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
        try:
           data = Visa_Info.objects.get(id=data_id["Data"])

           current_date = strftime("%Y-%m-%d")
           if data.Blocked == "Yes":
            return render(request, 'Administrator/pages/samples/error-600.html')


           rand = random.randint(0,1000)
           Client= Visa_Info.objects.get(id=pk)
           try:
            chat = Message_List.objects.get(User=data.id,Client=pk)

            Message.objects.filter(Chat=chat.Link,Reciever = data.id).update(Status="Seen")

            messages = Message.objects.filter(Chat=chat.Link)

           except:
             messages = []
             chat = "null"
           send_out =[]
           for i in messages:
              send_out.append({
                 "id":i.id,"Type":i.Type,"Info":i.Info,"Time":f'{str(i.time).split(":")[0]}:{str(i.time).split(":")[1]}',"Sender":i.Sender,"Reciever":i.Reciever,"Status":i.Status,'Reply_Id':i.Reply_Id,'Reply':i.Reply
              })

           noted = Notifications.objects.filter(User=data.id).count()
           context = {"Note":noted,"User_Data":data,"Data":data,"Client":Client,"Rand":rand,"Messages":send_out ,"Chat":chat}
           return render(request, 'Chat/private-chat.html', context)




        except:
           return Response('No')
      return redirect('login')

#======================================================== Sending Message ===============================================

class Send_Message(APIView):
    def post(self , request):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
        try:
           data = Visa_Info.objects.get(id=data_id["Data"])

           current_date = strftime("%Y-%m-%d")


           try:
             chat =  Message_List.objects.get(User=data.id,Client=request.data["Reciever"])
             uid = chat.Link
           except:
             uid = f'{str(uuid.uuid1())}-{str(uuid.uuid4())}-{str(uuid.uuid1())}'
             chat =  Message_List.objects.create(User=data.id,Client=request.data["Reciever"],Link=uid)
             Message_List.objects.create(Client=data.id,User=request.data["Reciever"],Link=uid)

           message = Message.objects.create(
              Sender = data.id,Reciever=request.data["Reciever"],Type=request.data["Type"],Info=request.data["Info"],Status="Unseen",Chat=uid,Alert="Unseen",
              Reply_Id=request.data["R_ID"],Reply=request.data["R_Value"],
           )
           Type = "Text"
           if request.data["Type"] == "Image":
              uploading_file = request.FILES['New_Img']
              fs = FileSystemStorage()
              fs.save("Messages//Temp//"+str(message.id)+".jpg",uploading_file)
              foo = Image.open(f'{BASE_DIR}/media/Messages/Temp/{str(message.id)}.jpg')  # My image is a 200x374 jpeg that is 102kb large
              foo.size  # (200, 374)
            #  foo = foo.resize(Image.ANTIALIAS)
             # foo.save('path/to/save/image_scaled.jpg', quality=95)  # The saved downsized image size is 24.8kb
              try:
                 foo.save(f'{BASE_DIR}/media/Messages/Images/{str(message.id)}.jpg', optimize=True, quality=50)
              except:
                 rgb_im = foo.convert('RGB')
                 rgb_im.save(f'{BASE_DIR}/media/Messages/Images/{str(message.id)}.jpg')
              Type = "Image"
              os.remove(f'{BASE_DIR}/media/Messages/Temp/{str(message.id)}.jpg')

           elif request.data["Type"] == "Video":
              uploading_file = request.FILES['New_Video']
              fs = FileSystemStorage()
              fs.save("Messages//Videos//"+str(message.id)+".mp4",uploading_file)
              Type = "Video"
           elif request.data["Type"] == "File":
              uploading_file = request.FILES['New_File']
              fs = FileSystemStorage()
              fs.save("Messages//Files//"+str(message.id)+".pdf",uploading_file)
              Type = "File"
           try:
            send_push_notification(request.data["Reciever"], f'Message from {data.Full_Name}', request.data["Info"])
           except:
            pass
           return Response({"id":message.id,"Type":Type,"Time":f'{str(message.time).split(":")[0]}:{str(message.time).split(":")[1]}',"Date":message.date,'Reply_Id':message.Reply_Id,'Reply':message.Reply})



        except:
           return Response('No')
      return redirect('login')


class Get_Message(APIView):
    def post(self , request):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
        try:
             data = Visa_Info.objects.get(id=data_id["Data"])
             current_date = strftime("%Y-%m-%d")



             print(request.data["id"])
             messages = Message.objects.filter(Status="Unseen",Reciever=data.id,Chat=request.data["id"])
             send_out = []
             for message in messages:
                send_out.append(
                   {"id":message.id,"Info":message.Info,"Type":message.Type,"Time":f'{str(message.time).split(":")[0]}:{str(message.time).split(":")[1]}',"Date":message.date,'Reply_Id':message.Reply_Id,'Reply':message.Reply}
                )

             Message.objects.filter(Chat=request.data["id"],Reciever = data.id).update(Status="Seen")

             return Response(send_out)


        except:
           return Response('No')
      return redirect('login')



class Get_Message_all(APIView):
    def post(self , request):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
        try:
             data = Visa_Info.objects.get(id=data_id["Data"])
             current_date = strftime("%Y-%m-%d")




             messages = Message.objects.filter(Alert="Unseen",Reciever=data.id)
             send_out = []
             for message in messages:
               try:
                s = Visa_Info.objects.get(id = message.Sender)
                send_out.append(
                   {"id":message.id,"User":message.Sender,"Name":s.Full_Name,"Info":message.Info,"Type":message.Type,"Time":f'{str(message.time).split(":")[0]}:{str(message.time).split(":")[1]}'
                   ,"Date":message.date,'Reply_Id':message.Reply_Id,'Reply':message.Reply}
                )
               except:
                  pass

               Message.objects.filter(id=message.id).update(Alert="Seen")

             return Response(send_out)


        except:
           return Response('No')
      return redirect('login')


class Load_Message(APIView):
    def post(self , request):
      data_id = get(request)
      if data_id["Stat"] ==  "Ok":
        try:
             data = Visa_Info.objects.get(id=data_id["Data"])

             current_date = strftime("%Y-%m-%d")

             print(request.data["id"])
             messages = Message.objects.filter(Status="Unseen",Reciever=data.id)
             return Response(messages.count())

        except:
           return Response('No')
      return Response(0)


class Find_User(APIView):
    def post(self , request):
       client_list1 = Visa_Info.objects.filter(Full_Name__icontains=request.data["Key"]) | Visa_Info.objects.filter(Email__icontains=request.data["Key"])


       data_id = get(request)
       if data_id["Stat"] ==  "Ok":
      #  try:
           data = Visa_Info.objects.get(id=data_id["Data"])

           listed = []
           for i in client_list1:
            if data.id == i.id:
              pass
            else:
              info = Visa_Info.objects.get(id=i.id)

              listed.append({
                 "id":info.id,"Name":f'{info.Full_Name}',"Email":info.Email
              })


           context= {
              "Data":data,
              "Listed":listed,
              "Key":request.data["Key"],
              }

           return render(request , "Chat/invite-friend.html",context)

        #except:

         #  return redirect('login')
       return redirect('login')

