from django.shortcuts import render,redirect
#from . serializers import  Client_Serializer,User_Serializer
import requests
from django.http import HttpResponseRedirect

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
import threading
import qrcode
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent

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



def Send_email(id):

          print(id)

          complete = Visa_Info.objects.get(id=int(id))

          sender_email = "omallophlink@gmail.com"
          receiver_email = complete.Email
          password = "hlyhpoojrlnirhxl"
          message = MIMEMultipart("alternative")
          message["Subject"] = "Info From Kingdom Dynasty"
          message["From"] = sender_email
          message["To"] = receiver_email

# Create the plain-text and HTML version of your message
          text = """\
          Hi,
          How are you?
          You are to verify this account:
          www.dalabcloud.pythonanywhere.com"""
          html = """\

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>New email template 2023-02-07</title><!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--><!--[if !mso]><!-- -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet"><!--<![endif]-->
  <style type="text/css">
#outlook a {
	padding:0;
}
.es-button {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors] {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.es-desk-hidden {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
[data-ogsb] .es-button {
	border-width:0!important;
	padding:10px 40px 10px 40px!important;
}
[data-ogsb] .es-button.es-button-1 {
	padding:15px 5px!important;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:36px!important; text-align:left } h2 { font-size:28px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:36px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:28px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:18px!important; display:block!important; border-right-width:0px!important; border-left-width:0px!important; border-top-width:15px!important; border-bottom-width:15px!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0!important } .es-m-p0r { padding-right:0!important } .es-m-p0l { padding-left:0!important } .es-m-p0t { padding-top:0!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } .es-m-p5 { padding:5px!important } .es-m-p5t { padding-top:5px!important } .es-m-p5b { padding-bottom:5px!important } .es-m-p5r { padding-right:5px!important } .es-m-p5l { padding-left:5px!important } .es-m-p10 { padding:10px!important } .es-m-p10t { padding-top:10px!important } .es-m-p10b { padding-bottom:10px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p15 { padding:15px!important } .es-m-p15t { padding-top:15px!important } .es-m-p15b { padding-bottom:15px!important } .es-m-p15r { padding-right:15px!important } .es-m-p15l { padding-left:15px!important } .es-m-p20 { padding:20px!important } .es-m-p20t { padding-top:20px!important } .es-m-p20r { padding-right:20px!important } .es-m-p20l { padding-left:20px!important } .es-m-p25 { padding:25px!important } .es-m-p25t { padding-top:25px!important } .es-m-p25b { padding-bottom:25px!important } .es-m-p25r { padding-right:25px!important } .es-m-p25l { padding-left:25px!important } .es-m-p30 { padding:30px!important } .es-m-p30t { padding-top:30px!important } .es-m-p30b { padding-bottom:30px!important } .es-m-p30r { padding-right:30px!important } .es-m-p30l { padding-left:30px!important } .es-m-p35 { padding:35px!important } .es-m-p35t { padding-top:35px!important } .es-m-p35b { padding-bottom:35px!important } .es-m-p35r { padding-right:35px!important } .es-m-p35l { padding-left:35px!important } .es-m-p40 { padding:40px!important } .es-m-p40t { padding-top:40px!important } .es-m-p40b { padding-bottom:40px!important } .es-m-p40r { padding-right:40px!important } .es-m-p40l { padding-left:40px!important } }
</style>
 </head>
 <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#F9F4FF"><!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" color="#F9F4FF" origin="0.5, 0" position="0.5, 0"></v:fill>
			</v:background>
		<![endif]-->
   <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png);background-repeat:repeat;background-position:center top;background-color:#F9F4FF">
     <tr>
      <td valign="top" style="padding:0;Margin:0">
       <table cellpadding="0" cellspacing="0" class="es-header" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-header-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#666666;font-size:14px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/group.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="40"></a></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:30px;padding-bottom:30px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank"  style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/25469811_developer_male_ICK.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="280" class="adapt-img"></a></td>
                     </tr>
                     <tr>
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><h1 style="Margin:0;line-height:60px;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;font-size:40px;font-style:normal;font-weight:bold;color:#E9E9E9">Kingdom Dynasty Travels</h1></td>
                     </tr>
                   </table></td>
                 </tr>
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-width:2px;border-style:solid;border-color:#4ca2f8;border-radius:20px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png);background-repeat:no-repeat;background-position:left center" background="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png" role="presentation">
                     <tr>
                      <td align="left" class="es-m-p20r es-m-p20l" style="padding:40px;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Hi <strong>"""+complete.Full_Name+"""</strong>,<br><br>We wanted to let you know your application has been recieved!<br>Thank you.<br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#ff0000;font-size:16px;text-align:center"><span style="font-size:22px"></span>&nbsp;</p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;padding-bottom:20px"><!--[if mso]><a href="https://dalabcloud.pythonanywhere.com/Manager" target="_blank" hidden>
	<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="https://dalabcloud.pythonanywhere.com/Manager"
                style="height:51px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#4ca2f8">
		<w:anchorlock></w:anchorlock>
		<center style='color:#ffffff; font-family:Poppins, sans-serif; font-size:18px; font-weight:400; line-height:18px;  mso-text-raise:1px'>Goto Login</center>
	</v:roundrect></a>
<![endif]--><!--[if !mso]><!-- --><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#4CA2F8;border-width:0px;display:block;border-radius:30px;width:auto;mso-hide:all"><a href="http://otravel.pythonanywhere.com/"  class="es-button msohide es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:18px;border-style:solid;border-color:#4CA2F8;border-width:15px 5px;display:block;background:#4CA2F8;border-radius:30px;font-family:Poppins, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;mso-hide:all">I Understand</a></span><!--<![endif]--></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png);background-repeat:no-repeat;background-position:right top">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="left" class="es-m-p0r es-m-p0l" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Thanks,<br><strong>Dalabcloud Assistance</strong></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td class="es-m-p40l" align="left" style="padding:0;Margin:0;padding-left:20px;padding-bottom:40px;padding-right:40px"><!--[if mso]><table style="width:540px" cellpadding="0" cellspacing="0"><tr><td style="width:46px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                 <tr class="es-mobile-hidden">
                  <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:46px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" height="40" style="padding:0;Margin:0"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td><td style="width:10px"></td><td style="width:484px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:484px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:10px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="tel:+(000)123456789" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope_1.png" alt="+ (253) 771 465 09" title="+ (253) 771 465 09" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">+ (253) 771 465 09</a></td>
                         </tr>
                       </table></td>
                     </tr>
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:0px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope.png" alt="dalab@email.com" title="dalab@email.com" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">dalab@email.com</a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td></tr></table><![endif]--></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" bgcolor="#77c82a" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px;background-color:#77c82a">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0">
                       <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Facebook" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/facebook-circle-white.png" alt="Fb" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Twitter" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/twitter-circle-white.png" alt="Tw" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Instagram" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/instagram-circle-white.png" alt="Inst" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Youtube" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/youtube-circle-white.png" alt="Yt" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" bgcolor="#FFFFFF">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table></td>
     </tr>
   </table>
  </div>
 </body>
</html>


          """
          part1 = MIMEText(text, "plain")
          part2 = MIMEText(html, "html")
          message.attach(part1)
          message.attach(part2)
          context = ssl.create_default_context()
          with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(
              sender_email, receiver_email, message.as_string()
              )




def Lottery_email(id):

          print(id)

          complete = Lottery_Info.objects.get(id=int(id))

          sender_email = "omallophlink@gmail.com"
          receiver_email = complete.Email
          password = "hlyhpoojrlnirhxl"
          message = MIMEMultipart("alternative")
          message["Subject"] = "Info From Kingdom Dynasty"
          message["From"] = sender_email
          message["To"] = receiver_email

# Create the plain-text and HTML version of your message
          text = """\
          Hi,
          How are you?
          You are to verify this account:
          www.dalabcloud.pythonanywhere.com"""
          html = """\

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>New email template 2023-02-07</title><!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--><!--[if !mso]><!-- -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet"><!--<![endif]-->
  <style type="text/css">
#outlook a {
	padding:0;
}
.es-button {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors] {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.es-desk-hidden {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
[data-ogsb] .es-button {
	border-width:0!important;
	padding:10px 40px 10px 40px!important;
}
[data-ogsb] .es-button.es-button-1 {
	padding:15px 5px!important;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:36px!important; text-align:left } h2 { font-size:28px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:36px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:28px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:18px!important; display:block!important; border-right-width:0px!important; border-left-width:0px!important; border-top-width:15px!important; border-bottom-width:15px!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0!important } .es-m-p0r { padding-right:0!important } .es-m-p0l { padding-left:0!important } .es-m-p0t { padding-top:0!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } .es-m-p5 { padding:5px!important } .es-m-p5t { padding-top:5px!important } .es-m-p5b { padding-bottom:5px!important } .es-m-p5r { padding-right:5px!important } .es-m-p5l { padding-left:5px!important } .es-m-p10 { padding:10px!important } .es-m-p10t { padding-top:10px!important } .es-m-p10b { padding-bottom:10px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p15 { padding:15px!important } .es-m-p15t { padding-top:15px!important } .es-m-p15b { padding-bottom:15px!important } .es-m-p15r { padding-right:15px!important } .es-m-p15l { padding-left:15px!important } .es-m-p20 { padding:20px!important } .es-m-p20t { padding-top:20px!important } .es-m-p20r { padding-right:20px!important } .es-m-p20l { padding-left:20px!important } .es-m-p25 { padding:25px!important } .es-m-p25t { padding-top:25px!important } .es-m-p25b { padding-bottom:25px!important } .es-m-p25r { padding-right:25px!important } .es-m-p25l { padding-left:25px!important } .es-m-p30 { padding:30px!important } .es-m-p30t { padding-top:30px!important } .es-m-p30b { padding-bottom:30px!important } .es-m-p30r { padding-right:30px!important } .es-m-p30l { padding-left:30px!important } .es-m-p35 { padding:35px!important } .es-m-p35t { padding-top:35px!important } .es-m-p35b { padding-bottom:35px!important } .es-m-p35r { padding-right:35px!important } .es-m-p35l { padding-left:35px!important } .es-m-p40 { padding:40px!important } .es-m-p40t { padding-top:40px!important } .es-m-p40b { padding-bottom:40px!important } .es-m-p40r { padding-right:40px!important } .es-m-p40l { padding-left:40px!important } }
</style>
 </head>
 <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#F9F4FF"><!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" color="#F9F4FF" origin="0.5, 0" position="0.5, 0"></v:fill>
			</v:background>
		<![endif]-->
   <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png);background-repeat:repeat;background-position:center top;background-color:#F9F4FF">
     <tr>
      <td valign="top" style="padding:0;Margin:0">
       <table cellpadding="0" cellspacing="0" class="es-header" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-header-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#666666;font-size:14px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/group.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="40"></a></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:30px;padding-bottom:30px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank"  style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/25469811_developer_male_ICK.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="280" class="adapt-img"></a></td>
                     </tr>
                     <tr>
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><h1 style="Margin:0;line-height:60px;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;font-size:40px;font-style:normal;font-weight:bold;color:#E9E9E9">Kingdom Dynasty Travels</h1></td>
                     </tr>
                   </table></td>
                 </tr>
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-width:2px;border-style:solid;border-color:#4ca2f8;border-radius:20px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png);background-repeat:no-repeat;background-position:left center" background="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png" role="presentation">
                     <tr>
                      <td align="left" class="es-m-p20r es-m-p20l" style="padding:40px;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Hi <strong>"""+complete.Full_Name+"""</strong>,<br><br>We wanted to let you know your lottery application has been recieved! 😉. You will be updated with the results soon. <br>Thank you.<br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#ff0000;font-size:16px;text-align:center"><span style="font-size:22px"></span>&nbsp;</p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;padding-bottom:20px"><!--[if mso]><a href="https://dalabcloud.pythonanywhere.com/Manager" target="_blank" hidden>
	<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="https://dalabcloud.pythonanywhere.com/Manager"
                style="height:51px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#4ca2f8">
		<w:anchorlock></w:anchorlock>
		<center style='color:#ffffff; font-family:Poppins, sans-serif; font-size:18px; font-weight:400; line-height:18px;  mso-text-raise:1px'>🎊🎊 Congratulations 🎊🎊</center>
	</v:roundrect></a>
<![endif]--><!--[if !mso]><!-- --><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#4CA2F8;border-width:0px;display:block;border-radius:30px;width:auto;mso-hide:all"><a href="http://otravel.pythonanywhere.com/"  class="es-button msohide es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:18px;border-style:solid;border-color:#4CA2F8;border-width:15px 5px;display:block;background:#4CA2F8;border-radius:30px;font-family:Poppins, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;mso-hide:all">I Understand</a></span><!--<![endif]--></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png);background-repeat:no-repeat;background-position:right top">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="left" class="es-m-p0r es-m-p0l" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Thanks,<br><strong>Sikobs Assistance</strong></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td class="es-m-p40l" align="left" style="padding:0;Margin:0;padding-left:20px;padding-bottom:40px;padding-right:40px"><!--[if mso]><table style="width:540px" cellpadding="0" cellspacing="0"><tr><td style="width:46px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                 <tr class="es-mobile-hidden">
                  <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:46px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" height="40" style="padding:0;Margin:0"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td><td style="width:10px"></td><td style="width:484px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:484px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:10px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="tel:+(000)123456789" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope_1.png" alt="+ (253) 771 465 09" title="+ (253) 771 465 09" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">+ (253) 771 465 09</a></td>
                         </tr>
                       </table></td>
                     </tr>
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:0px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope.png" alt="dalab@email.com" title="dalab@email.com" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">dalab@email.com</a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td></tr></table><![endif]--></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" bgcolor="#77c82a" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px;background-color:#77c82a">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0">
                       <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Facebook" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/facebook-circle-white.png" alt="Fb" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Twitter" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/twitter-circle-white.png" alt="Tw" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Instagram" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/instagram-circle-white.png" alt="Inst" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Youtube" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/youtube-circle-white.png" alt="Yt" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" bgcolor="#FFFFFF">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table></td>
     </tr>
   </table>
  </div>
 </body>
</html>


          """
          part1 = MIMEText(text, "plain")
          part2 = MIMEText(html, "html")
          message.attach(part1)
          message.attach(part2)
          context = ssl.create_default_context()
          with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(
              sender_email, receiver_email, message.as_string()
              )





#========================================================================================================================
class Job_Visa_Share(APIView):
    def get(self , request,pk):
      sh = Share_Link.objects.get(Link=pk)
      job = Job.objects.get(id=sh.Job)

      role = Job_Role.objects.filter(Job=job.id)
      skill = Job_Skills.objects.filter(Job=job.id)
      benefit = Job_Benefits.objects.filter(Job=job.id)
      user= SignUp_info.objects.get(id=job.User)
      context = {"User":user,"Job":job,"Role":role,"Skill":skill,"Benefit":benefit}
      return render(request , "Home/job-visa.html", context=context)
    def post(self , request,pk):
           sh = Share_Link.objects.get(Link=pk)
           job = Job.objects.get(id=sh.Job)
           check = Visa_Info.objects.filter(Email=request.data["Email"])
           if check.count() > 0:
             return render(request,'Home/error.html')

           data = Visa_Info.objects.create(
              Admin=sh.User,
              Call=sh.User,


              Full_Name=request.data["Name"],
              Gender=request.data["Gender"],
              Birth=request.data["Birth"],
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Skill=request.data["Skill"],
              Experience=request.data["Experience"],
              Education=request.data["Education"],
              Skill_Level=request.data["Skill_Level"],
              Passport=request.data["Passport"],
              Birth_Cert=request.data["Birth_Cert"],
              Link=job.id,
              Group='New Applicant'





           )
           set_id(data.id)
           set_agent(data.id)
           val = f'{uuid.uuid1()}_{data.id}'
           Visa_Info.objects.filter(id=data.id).update(Refrene_Code=val)
           qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=10,
           border=4,
           )
           qr.add_data(val)
           img = qr.make_image(fill_color="green", back_color="white")
           img.save(f'{BASE_DIR}/media/QR/{data.id}.jpg')
           x = threading.Thread(args={data.id,}, target=Send_email)
           x.start()




      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------

           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Profiles//"+str(data.id)+".jpg",uploading_file)
           uploading_file = request.FILES['ID']
           fs = FileSystemStorage()
           fs.save("Ids//"+str(data.id)+".jpg",uploading_file)




           return render(request,'Home/error.html')
#======================================================== Home ===========================================================
#======================================================== Home ===========================================================
class Home(APIView):
    def get(self , request):
      job= Job.objects.all().order_by('id')[0:6]

      context = {"Jobs":job}
      return render(request , "Home/index.html",context)



class Travel_Packages(APIView):
    def get(self , request ,pk):

      job= Job.objects.filter(Group=pk).order_by('id')

      context = {"Jobs":job,"pk":pk}
      return render(request , "Home/job_post.html",context)


#======================================================== Home ===========================================================
def Check():
   #---------------------------------------- Subscription ---------------------------------------------
           data= Date_Info.objects.last()

           current_date = strftime("%Y-%m-%d")
           #------------------------------------------- Online Status --------------------------------------------------

           years = (int(str(current_date).split("-")[0]) - int(str(data.Dated).split("-")[0]))*356
           months = (int(str(current_date).split("-")[1]) - int(str(data.Dated).split("-")[1]))*30
           days = (int(str(current_date).split("-")[2]) - int(str(data.Dated).split("-")[2]))
           result = abs(years+months+days)
           return({'yeah':years,'month':months,'day':days,'result':result})

#======================================================== Home ===========================================================


class Job_Visa(APIView):
    def get(self , request,pk):
      job = Job.objects.get(Link=pk)
      role = Job_Role.objects.filter(Job=job.id)
      skill = Job_Skills.objects.filter(Job=job.id)
      benefit = Job_Benefits.objects.filter(Job=job.id)
      user= SignUp_info.objects.get(id=job.User)
      context = {"User":user,"Job":job,"Role":role,"Skill":skill,"Benefit":benefit}
      return render(request , "Home/job-visa.html", context=context)
    def post(self , request,pk):
           job = Job.objects.get(Link=pk)
           check = Visa_Info.objects.filter(Email=request.data["Email"])
           if check.count() > 0:
             return render(request,'Home/error.html')

           data = Visa_Info.objects.create(
              Admin=0,
              Full_Name=request.data["Name"],
              Gender=request.data["Gender"],
              Birth=request.data["Birth"],
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Skill=request.data["Skill"],
              Experience=request.data["Experience"],
              Education=request.data["Education"],
              Skill_Level=request.data["Skill_Level"],
              Passport=request.data["Passport"],
              Birth_Cert=request.data["Birth_Cert"],
              Link=job.id,
              Group='New Applicant'





           )
           set_id(data.id)
           set_agent(data.id)
           val = f'{uuid.uuid1()}_{data.id}'
           Visa_Info.objects.filter(id=data.id).update(Refrene_Code=val)
           qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=10,
           border=4,
           )
           qr.add_data(val)
           img = qr.make_image(fill_color="green", back_color="white")
           img.save(f'{BASE_DIR}/media/QR/{data.id}.jpg')
           x = threading.Thread(args={data.id,}, target=Send_email)
           x.start()


      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------

           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Profiles//"+str(data.id)+".jpg",uploading_file)
           uploading_file = request.FILES['ID']
           fs = FileSystemStorage()
           fs.save("Ids//"+str(data.id)+".jpg",uploading_file)




           return render(request,'Home/error.html')

#======================================================== Home ===========================================================

#======================================================== Home ===========================================================
class Student_Visa(APIView):
    def get(self , request):
      return render(request , "Home/s-visa.html",)


#======================================================== Home ===========================================================


class Manager_Login(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = Administrator_Info.objects.get(id=int(find.User))
          return redirect('dashboard')
         except:
           return render(request , "Home/signup.html")
      else:
         return render(request , "Home/signup.html")

    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try:
          data = Administrator_Info.objects.get(Email=request.data['Email'], Password=request.data['Password'])
          response =  redirect('dashboard')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Manager")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Manager")
          response.set_cookie('csrf-session-xdii-token',generated_uuid)
          #Notifications.objects.create(Status = "New",Uid = data.id, Type="Manager", Info=f"You have successfully logged in on {current_time}.")
          return response
       except:
         return render (request, 'Home/error2.html' )


class Manager_Logout(APIView):
    def get(self , request):
      response = redirect("home")
      response.delete_cookie('csrf-session-xdii-token')

      return response



class Dashboard(APIView):
    def get(self , request):
      if 'csrf-admin-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = Administrator_Info.objects.get(id=int(find.User))
          books = Visa_Info.objects.all()
          accounts = SignUp_info.objects.all().count()
          all = Visa_Info.objects.all()
          trends = Visa_Info.objects.all().count()

          context = {"Data":User_data,"Books":books,"My_Books":books.count,"Trends":trends,"Accounts":accounts,"All":all.count()}
          return render(request, "Manager/index.html",context)
         except:
          return redirect("login")
      else:
        return redirect("login")


class Cards(APIView):
    def get(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = Administrator_Info.objects.get(id=int(find.User))


          User_data = Visa_Info.objects.get(id=int(pk))

          context = {"Data":User_data}
          return render(request, "Id/IDCard.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")

class Cv_Profile(APIView):
    def get(self , request,pk):
      if 'csrf-admin-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-admin-token']
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = Administrator_Info.objects.get(id=int(find.User))

          edu = Extra_Info.objects.filter(Profile=pk,Type="School")
          work = Extra_Info.objects.filter(Profile=pk,Type="Work")
          User_data = Visa_Info.objects.get(id=int(pk))

          context = {"Data":User_data,"Education":edu,"Work":work}
          return render(request, "Cv/one-page.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")



class Lottery_Profile(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = Administrator_Info.objects.get(id=int(find.User))


          User_data = Lottery_Info.objects.get(id=int(pk))

          context = {"Data":User_data}
          return render(request, "Cv/lottery_cv.html",context)
         #except:
         # return redirect("login")
      else:
        return redirect("login")


class Lottery(APIView):
    def get(self , request):
      val = Check()
      context = {"Time":val}
      return render(request , "Home/sat-coaching.html",context)

class Lottery_Add(APIView):
    def get(self , request):

      return render(request , "Home/lottery.html",)
    def post(self , request):

           data = Lottery_Info.objects.create(
              Full_Name=request.data["Name"],
              Gender=request.data["Gender"],
              Birth=request.data["Birth"],
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Skill=request.data["Skill"],
              Experience=request.data["Experience"],
              Education=request.data["Education"],
              Skill_Level=request.data["Skill_Level"],
              Passport=request.data["Passport"],
              Birth_Cert=request.data["Birth_Cert"],

              Weight = request.data['Weight'],
              Card_Id = request.data['Card_Id'],
              Height = request.data['Height'],
              Hair = request.data['Hair'],
              Eye = request.data['Eye'],
              Country_Recidence = request.data['Country_Recidence'],
              Postal_Code_Recidence = request.data['Postal_Code_Recidence'],
              Marital=request.data['Marital'],
           )
           val = f'{uuid.uuid1()}_{data.id}'
           Lottery_Info.objects.filter(id=data.id).update(Refrene_Code=val)

           x = threading.Thread(args={data.id,}, target=Lottery_email)
           x.start()

      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------

           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Lottery_Profiles//"+str(data.id)+".jpg",uploading_file)
           uploading_file = request.FILES['ID']
           fs = FileSystemStorage()
           fs.save("Lottery_Ids//"+str(data.id)+".jpg",uploading_file)

           uid_val = f'{str(uuid.uuid1())[0:15]}-{data.id}'
           url = "https://payproxyapi.hubtel.com/items/initiate"

           payload = {
    "totalAmount": 800,
    "description": "OTravel Lottery Raffel.",
    "callbackUrl": f"https://www.sikobs.world/confirm_ticket/{data.id}",
    "returnUrl": "https://www.sikobs.world/lottery_prompt",
    "cancellationUrl": "https://www.sikobs.world/",
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

class Lottery_Prompt(APIView):
    def get(self , request):
     return render(request,'Home/success.html')

class Confirm_Ticket(APIView):
    def post(self , request,pk):
     print(request.data["ResponseCode"])
     print(request.data["Data"]['ClientReference'])
     if request.data["ResponseCode"] == '0000':
         Lottery_Info.objects.filter(id=pk).update(Validate="Validated")
         return Response(200)
     else:
         Lottery_Info.objects.get(id=pk).delete()
         return Response(200)

#======================================================== Home ===========================================================
class Reciept(APIView):
    def get(self , request,pk):
      pay =Funds_info.objects.get(id=pk)
      client = Visa_Info.objects.get(id=pay.User)

      context = {'Funds':pay,"Client":client}
      return render(request , "Cv/recept.html",context)



def set_agent1(id):
 try:
  l = Last_Agent.objects.last()
 except:
    l = Last_Agent.objects.create(User=0)
 lst = []
 a = Agent_Account.objects.all()
 if a.count() > 1 :
  for i in a:
     if int(i.User) == l.User:
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


#






















from django.db import transaction

def get_next_agent(last_user_id):
    """Returns the next agent (different from the last one), or None if none found."""
    agents = Administrator_Info.objects.filter(Agent='Yes').exclude(id=last_user_id)
    if not agents.exists():
        return Administrator_Info.objects.last()  # fallback to any agent
    return random.choice(agents)


def set_agent(client_id):
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
            else:
             Agent_Account_Link.objects.create(User=next_agent.id,Client=client_id,Status='Pending',Type='Staff')
            Visa_Info.objects.filter(id=client_id).update(Agent=next_agent.id,Agent_Type='Staff')

            # Save the current agent as the last used
            last_agent.User = next_agent.id
            last_agent.save()

        print(f"✅ Agent olient {client_id}.")

    except Exception as e:
        print(f"⚠️ Error assigning agent: {e}")

#set_agent(9726)


#---------------------------------------- Quick -------------------------------------------

class Quick_Visa_Share(APIView):
    def get(self , request):

      return render(request , "Home/quick.html")

    def post(self , request):
           check = Visa_Info.objects.filter(Email=request.data["Email"])
           if check.count() > 0:
             return render(request,'Home/error.html')

           data = Visa_Info.objects.create(
              Full_Name=request.data["Name"],
              Gender='Null',
              Birth='Null',
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Experience='Null',
              Education='Null',
              Skill_Level='Null',
              Passport='Null',
              Birth_Cert='Null',
              Group='Leads',
              Skill=request.data["Skill"],
               Seen=request.data["Seen"],



           )
           set_id(data.id)
           set_agent(data.id)
           val = f'{uuid.uuid1()}_{data.id}'
           Visa_Info.objects.filter(id=data.id).update(Refrene_Code=val)
           qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=10,
           border=4,
           )
           qr.add_data(val)
           img = qr.make_image(fill_color="green", back_color="white")
           img.save(f'{BASE_DIR}/media/QR/{data.id}.jpg')
           x = threading.Thread(args={data.id,}, target=Send_email)
           x.start()




      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------
           try:
            uploading_file = request.FILES['New_Img']
            fs = FileSystemStorage()
            fs.save("Profiles//"+str(data.id)+".jpg",uploading_file)
           except:
               shutil.copyfile(f"{BASE_DIR}/static/OIP.jpg",f"{BASE_DIR}/media/Profiles/{str(data.id)}.jpg" )




           return render(request,'Home/error.html')


#------------------------------------------------------------------------------------------

class Plane_Home(APIView):
    def get(self , request):

      return render(request , "Plane/index.html")


class Plane_Contact(APIView):
    def get(self , request):

      return render(request , "Plane/contact.html")


class Plane_About(APIView):
    def get(self , request):

      return render(request , "Plane/about.html")

class Plane_Blog(APIView):
    def get(self , request):

      return render(request , "Plane/blog.html")








class Quick_Visa_Share_With(APIView):
    def get(self , request,pk):
      context = {'Name':pk}
      return render(request , "Home/quick.html",context )

    def post(self , request,pk):
           check = Visa_Info.objects.filter(Email=request.data["Email"])
           if check.count() > 0:
             return render(request,'Home/error.html')

           data = Visa_Info.objects.create(
              Full_Name=request.data["Name"],
              Gender='Null',
              Birth='Null',
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Experience='Null',
              Education='Null',
              Skill_Level='Null',
              Passport='Null',
              Birth_Cert='Null',
              Group='Leads',
              SEP=pk,
              Skill=request.data["Skill"],
               Seen=request.data["Seen"],



           )
           set_id(data.id)
           set_agent(data.id)
           val = f'{uuid.uuid1()}_{data.id}'
           Visa_Info.objects.filter(id=data.id).update(Refrene_Code=val)
           qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=10,
           border=4,
           )
           qr.add_data(val)
           img = qr.make_image(fill_color="green", back_color="white")
           img.save(f'{BASE_DIR}/media/QR/{data.id}.jpg')
           x = threading.Thread(args={data.id,}, target=Send_email)
           x.start()



      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------
           try:
            uploading_file = request.FILES['New_Img']
            fs = FileSystemStorage()
            fs.save("Profiles//"+str(data.id)+".jpg",uploading_file)
           except:
               shutil.copyfile(f"{BASE_DIR}/static/OIP.jpg",f"{BASE_DIR}/media/Profiles/{str(data.id)}.jpg" )




           return render(request,'Home/error.html')







#agents = Agent_Account.objects.all()
#for o in agents:

#  uid = f'{uuid.uuid1()}{str(strftime("%H-%M-%S"))}'
#   Agent_Account.objects.filter(id=o.id).update(Link=uid)
#   print('ok')




class Quick_Visa_Share_With_Agent(APIView):
    def get(self , request,pk,pk2):
      context = {'Name':pk}
      return render(request , "Home/quick.html",context )

    def post(self , request,pk,pk2):
           check = Visa_Info.objects.filter(Email=request.data["Email"])
           if check.count() > 0:
             return render(request,'Home/error.html')
           if pk == 'General':
               pk = None
           agent = Agent_Account.objects.get(Link=pk2)
           data = Visa_Info.objects.create(
              Full_Name=request.data["Name"],
              Gender='Null',
              Birth='Null',
              Address=request.data["Address"],
              City=request.data["City"],
              Email=request.data["Email"],
              Contact=request.data["Contact"],
              Experience='Null',
              Education='Null',
              Skill_Level='Null',
              Passport='Null',
              Birth_Cert='Null',
              Group='Leads',
              SEP=pk,
              Skill=request.data["Skill"],
               Seen=request.data["Seen"],
              Agent=agent.id,
              Agent_Type='Agent',



           )
           Agent_Account_Link.objects.create(User=agent.id,Client=data.id,Status='Pending',Type='Agent')
           set_id(data.id)
           val = f'{uuid.uuid1()}_{data.id}'
           Visa_Info.objects.filter(id=data.id).update(Refrene_Code=val)
           qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=10,
           border=4,
           )
           qr.add_data(val)
           img = qr.make_image(fill_color="green", back_color="white")
           img.save(f'{BASE_DIR}/media/QR/{data.id}.jpg')
           x = threading.Thread(args={data.id,}, target=Send_email)
           x.start()




      #-----------------------------------------------------------------------------------

      #-----------------------------------------------------------------------------------
           try:
            uploading_file = request.FILES['New_Img']
            fs = FileSystemStorage()
            fs.save("Profiles//"+str(data.id)+".jpg",uploading_file)
           except:
               shutil.copyfile(f"{BASE_DIR}/static/OIP.jpg",f"{BASE_DIR}/media/Profiles/{str(data.id)}.jpg" )




           return render(request,'Home/error.html')

