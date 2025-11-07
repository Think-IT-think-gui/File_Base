from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.db.models import Q
import shutil
from time import *
import uuid
import requests
import random
from datetime import datetime, timedelta



def weeks_until_7_months(id):
    # Convert the created_date to a datetime object
    user = Visa_Info.objects.get(id=id)
    created_datetime = datetime.combine(user.date, datetime.min.time())

    # Calculate the target date which is 7 months from the creation date
    target_date = created_datetime + timedelta(days=7*30)  # Approximating a month as 30 days

    # Calculate the difference between the current date and the target date
    time_difference = target_date - datetime.now()

    # Calculate the number of weeks left
    weeks_left = time_difference.days // 7

    return weeks_left


def get(request):
      if 'cookie_session_id' in request.COOKIES:
        user_check = request.COOKIES['cookie_session_id']

        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)

          data = Visa_Info.objects.get(id=find.User)

          current_date = strftime("%Y-%m-%d")
          return ({"Stat":"Ok","Data":find.User})
        except:
          return ({"Stat":"No"})
      return ({"Stat":"No"})


def admin_get(request):
      if 'csrf-admin-token' in request.COOKIES:
        user_check = request.COOKIES['csrf-admin-token']

        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)

          data = Administrator_Info.objects.get(id=find.User)
          try:
               theme = request.COOKIES['theme_id']
          except:
              theme = "dark"
          try:
               color = request.COOKIES['theme_color']
          except:
              color = "dark"
          current_date = strftime("%Y-%m-%d")
          return ({"Stat":"Ok","Data":find.User,"Theme":theme,"Color":color})
        except:
          return ({"Stat":"No"})
      return ({"Stat":"No"})


def interview_get(request):
      if 'csrf-interview-token' in request.COOKIES:
        user_check = request.COOKIES['csrf-interview-token']

        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)

          data = Interview_Account.objects.get(id=find.User)
          try:
               theme = request.COOKIES['theme_id']
          except:
              theme = "dark"
          try:
               color = request.COOKIES['theme_color']
          except:
              color = "dark"
          current_date = strftime("%Y-%m-%d")
          return ({"Stat":"Ok","Data":find.User,"Theme":theme,"Color":color})
        except:
          return ({"Stat":"No"})
      return ({"Stat":"No"})



def agent_get(request):
      if 'csrf-agent-token' in request.COOKIES:
        user_check = request.COOKIES['csrf-agent-token']

        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)

          data = Agent_Account.objects.get(id=find.User)
          try:
               theme = request.COOKIES['theme_id']
          except:
              theme = "dark"
          try:
               color = request.COOKIES['theme_color']
          except:
              color = "dark"
          current_date = strftime("%Y-%m-%d")
          return ({"Stat":"Ok","Data":find.User,"Theme":theme,"Color":color})
        except:
          return ({"Stat":"No"})
      return ({"Stat":"No"})

#=================================================== Checker =================================================

def mgr_get(request):
      if 'cookie_session_manager_id' in request.COOKIES:
        user_check = request.COOKIES['cookie_session_manager_id']

        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)

          data = Portal_Info.objects.get(id=find.User)

          current_date = strftime("%Y-%m-%d")
          return ({"Stat":"Ok","Data":find.User})
        except:
          return ({"Stat":"No"})
      return ({"Stat":"No"})