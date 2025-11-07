def post(self , request):
       
              
       if 'cookie_session_id' in request.COOKIES:
        user_check = request.COOKIES['cookie_session_id']
        try:
          find = Cookie_Handler.objects.get(Cookie=user_check)
          data = SignUp_info.objects.get(id=find.User)
          current_date = strftime("%Y-%m-%d")
          if data.Verify == "Yes":
           try:    
            ref = Delivery_Request.objects.get(Main=request.data["id"])
            if ref.Status == "Yes":
               Delivery_Request.objects.filter(Main=request.data["id"]).update(Status="No")
               return render(request, 'go/prompt2.html')
            else:
               Delivery_Request.objects.filter(Main=request.data["id"]).update(Status="Yes")
               return render(request, 'go/prompt1.html')
           except:
              Delivery_Request.objects.create(User=data.id,Main=request.data["id"],Status="Yes")
              return render(request, 'go/prompt1.html')
          else:
             return redirect('verify')
        except:    
            return redirect('login')
       return redirect('login')