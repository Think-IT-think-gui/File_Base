from django.urls import path
from . views import *
from . Client import *
from django.conf.urls.static import static
from django.conf import settings

from .Administrator_view import *

from .Portal import *
from . Message import *
from .Rec import *
from .Interview import *
from . noti import *
from . Agent import *

urlpatterns = [
   # path('duplicate', duplicate_data, name='duplicate_data'),

    path('overview_report', Overview_Report.as_view(), name="overview_report"),

    path('sign_file_view/<str:pk>/<int:pk2>',Sign_File_View.as_view(), name="sign_file_view"),
    path('save-subscription/', save_subscription, name='save_subscription'),

    path('delete_message', Delete_Message.as_view(), name="delete_message"),


    path('staff_agent_client_group_main/<int:pk>',Staff_Agent_Client_Group_Main.as_view(), name="staff_agent_client_group_main"),


    path('find_completed_logs', Find_Completed_Logs.as_view(), name="find_completed_logs"),

    path('interview_page_dashboard_find', Interview_Page_Dashboard_Find.as_view(), name="interview_page_dashboard_find"),
    path('interview_page_filter_list', Interview_Page_Filter_List.as_view(), name="interview_page_filter_list"),

    path('interview_profile_admin_report/<int:pk>',Interview_Profile_Admin_Report.as_view(), name="interview_profile_admin_report"),

    path('interview_page_client/<int:pk>',Interview_Page_Client.as_view(), name="interview_page_client"),
    path('interview_page_client_filter/<int:pk>',Interview_Page_Client_Filter.as_view(), name="interview_page_client_filter"),

    path('site_blog', Site_Blog.as_view(), name="site_blog"),
    path('view_media_posts', View_Media_Posts.as_view(), name="view_media_posts"),
    path('personal_post', Personal_Post.as_view(), name="personal_post"),

    path('manage_files_group_edit/<int:pk>',Manage_Files_Group_Edit.as_view(), name="manage_files_group_edit"),

    path('completed_account_group_filter/<int:pk>',Completed_Account_Group_Filter.as_view(), name="completed_account_group_filter"),
    path('completed_account_group/<int:pk>',Completed_Account_Group.as_view(), name="completed_account_group"),

    path('add_completed_data',Add_Completed_Data.as_view(), name="add_completed_data"),

    path('interview_page_dashboard',Interview_Page_Dashboard.as_view(), name="interview_page_dashboard"),
    path('interview_page_dashboard_filter',Interview_Page_Dashboard_Filter.as_view(), name="interview_page_dashboard_filter"),


    path('proccess_account_filter',Proccess_Account_Filter.as_view(), name="proccess_account_filter"),
    path('proccess_account',Proccess_Account.as_view(), name="proccess_account"),
    path('filter_decition_account',Filter_Decition_Account.as_view(), name="filter_decition_account"),
    path('decition_account',Decition_Account.as_view(), name="decition_account"),

    path('issue_update_status',Issue_Update_Status.as_view(), name="issue_update_status"),
    path('issue_update',Issue_Update.as_view(), name="issue_update"),

    path('manage_issues',Manage_Issues.as_view(), name="manage_issues"),
    path('issues_media_view/<int:pk>',Issues_Media_View.as_view(), name="issues_media_view"),

    path('list_uploaded_files_group_filter',List_Uploaded_Files_Group_Filter.as_view(), name="list_uploaded_files_group_filter"),
    path('create_side_menu',Create_Side_Menu.as_view(), name="create_side_menu"),
    path('list_side_menu',List_Side_Menu.as_view(), name="list_side_menu"),
    path('confirm_booking_filter',Confirm_Booking_Filter.as_view(), name="confirm_booking_filter"),

    path('set_card_point_session',Set_Card_Point_Session.as_view(), name="set_card_point_session"),

    path('create_card_point_message/<int:pk>',Create_Card_Point_Message.as_view(), name="create_card_point_message"),

    path('set_card_point_permission',Set_Card_Point_Permission.as_view(), name="set_card_point_permission"),


    path('create_card_point',Create_Card_Point.as_view(), name="create_card_point"),
    path('list_card_point',List_Card_Point.as_view(), name="list_card_point"),
    path('view_scanned_booking/<int:pk>',View_Scaned_Booking.as_view(), name="view_scanned_booking"),
    path('scan_id_qr',Scan_ID_QR.as_view(), name="scan_id_qr"),
    path('assign_id_cards',Assign_Id_Cards.as_view(), name="assign_id_cards"),
    path('check_assign_id_cards',Check_Assign_Id_Cards.as_view(), name="check_assign_id_cards"),

    path('list_all_cards',List_All_Cards.as_view(), name="list_all_cards"),
    path('generate_id_card/<int:pk>',Generate_ID_Card.as_view(), name="generate_id_card"),
    path('manage_files_group', Manage_Files_Group.as_view(), name="manage_files_group"),
    path('list_uploaded_files_group', List_Uploaded_Files_Group.as_view(), name="list_uploaded_files_group"),
    path('view_uploaded_files_group/<int:pk>', View_Uploaded_Files_Group.as_view(), name="view_uploaded_files_group"),


    path('client_password', Client_Password.as_view(), name="client_password"),
    path('interview_paged/<int:pk>', Interview_Paged.as_view(), name="interview_paged"),

    path('interview_profile_admin/<int:pk>', Interview_Profile_Admin.as_view(), name="interview_profile_admin"),

    path('delete_interview', Delete_Interview.as_view(), name="delete_interview"),

    path('interview_paged_filter/<int:pk>', Interview_Paged_Filter.as_view(), name="interview_paged_filter"),



    path('manage_files/<str:pk>', Manage_Files.as_view(), name="manage_files"),
    path('list_uploaded_files/<int:pk>', List_Uploaded_Files.as_view(), name="list_uploaded_files"),
    path('view_uploaded_files/<int:pk>', View_Uploaded_Files.as_view(), name="view_uploaded_files"),

    path('movement_issued', Movement_Issued.as_view(),name="movement_issued"),
    path('delete_cookies', Delete_Cookies.as_view(),name="delete_cookies"),
    path('manager_staff_account', Manager_Staff_Account.as_view(),name="manager_staff_account"),
    path('add_staff', Add_Staff.as_view(),name="add_staff"),
    path('edit_staff/<int:pk>', Edit_Staff.as_view(),name="edit_staff"),

    path('quick_visa_share_with/<str:pk>', Quick_Visa_Share_With.as_view(),name="quick_visa_share_with"),

    path('view_log/<int:pk>', View_Logs.as_view(), name="view_log"),
    path('add_log_data', Add_Log_Data.as_view(), name="add_log_data"),
    path('update_email_data', Update_Email_Data.as_view(), name="update_email_data"),
    path('status_account/<str:pk>/<str:pk2>', Status_Account_Group.as_view(), name="status_account"),
    path('update_applicant_data', Update_Applicant_Data.as_view(), name="update_applicant_data"),
    path('booking_filter', Booking_Filter.as_view(), name="booking_filter"),
    path('booking_confirm', Confirm_Booking.as_view(), name="booking_confirm"),

    path('booking_confirm_find', Confirm_Booking_Find.as_view(), name="booking_confirm_find"),
    path('booking_find', Booking_Find.as_view(), name="booking_find"),
    path('manage_booking', Add_Booking.as_view(), name="manage_booking"),
    path('view_booking/<int:pk>',View_Booking.as_view(), name="view_booking"),
    path('delete_booking',Delete_Booking.as_view(), name="delete_booking"),
    path('manager_account_group_filter/<str:pk>', Manager_Account_Group_Filter.as_view(), name="manager_account_group_filter"),
    path('manager_account_group_filter_region/<str:pk>', Manager_Account_Group_Filter_Region.as_view(), name="manager_account_group_filter_region"),
    path('manager_account_group_region/<str:pk>', Manager_Account_Group_Region.as_view(), name="manager_account_group_region"),
    path('view_regions', View_Regions.as_view(),name="view_regions"),






 #------------------------------ Messages ---------------------------------------
    path('client_message/<int:pk>', Client_Message.as_view(), name="client_message"),


#---------------------------------------------------------------------------------------
    path('send_message', Send_Message.as_view(), name="send_message"),
    path('get_message', Get_Message.as_view(), name="get_message"),
    path('my_messages', My_Messages.as_view(), name="messages"),
    path('all_chat/<int:pk>', Client_Message_All.as_view(), name="all_chat"),
    path('load_message', Load_Message.as_view(), name="load_message"),
    path('find_user', Find_User.as_view(), name="find_user"),
    path('get_message_all', Get_Message_all.as_view(), name="get_message_all"),



#------------------------------ Messages ---------------------------------------
#-------------------------------------------------------------------------






    path('air', Plane_Home.as_view(),name="air"),

    path('air_contact', Plane_Contact.as_view(),name="air_contact"),
    path('air_about', Plane_About.as_view(),name="air_about"),
    path('air_blog', Plane_Blog.as_view(),name="air_blog"),
#-------------------------------------------------------------------------




    path('client_new_login', Client_New_Login.as_view(),name="client_new_login"),

    path('enquiry', Quick_Visa_Share.as_view(),name="enquiry"),

    path('view_cro_call_logs/<int:pk>', View_Cro_Call_Logs.as_view(),name="view_cro_call_logs"),


    path('cro_call_logs', Cro_Call_Logs.as_view(),name="cro_call_logs"),


    path('get_code', Generate_Code.as_view(),name="get_code"),
    path('job_visa_share/<str:pk>', Job_Visa_Share.as_view(),name="job_visa_share"),



    path('update_call', Update_Call.as_view(),name="update_call"),

    path('manager_find', Manager_Find.as_view(),name="manager_find"),

    path('add_call_logs/<int:pk>', Add_Call_Logs.as_view(),name="add_call_logs"),

    path('portal_dashboard', Portal_Dashboard.as_view(),name="portal_dashboard"),

    path('buy_code', Buy_Code.as_view(),name="buy_code"),


    path('confirm_code/<int:pk>', Confirm_Code.as_view(),name="confirm_code"),

    path('code_prompt', Code_Prompt.as_view(),name="code_prompt"),

    path('apply_passport', Apply_Passport.as_view(),name="apply_passport"),

    path('applying', Applying.as_view(),name="applying"),

    path('portal_login', Portal_Login.as_view(),name="portal_login"),


    path('portal_user', Portal_User.as_view(),name="portal_user"),


    path('portal_user_show/<int:pk>', Portal_User_View.as_view(),name="portal_user_show"),



    path('update_theme', Update_Theme.as_view(),name="update_theme"),


    path('job_pannel', Job_Pannel.as_view(),name="job_pannel"),
    path('job_pannel_manage', Job_Pannel_Manage.as_view(),name="job_pannel_manage"),

    path('job_view/<int:pk>', Job_View.as_view(),name="job_view"),




    path('manager_paid/<int:pk>', Manager_Paid.as_view(),name="manager_paid"),


    path('manager_debit/<int:pk>', Manager_Debit.as_view(),name="manager_debit"),
    path('delete_debit', Delete_Debit.as_view(),name="delete_debit"),



    path('reciept/<int:pk>', Reciept.as_view(),name="reciept"),


    path('lottery_profile/<int:pk>', Lottery_Profile.as_view(),name="lottery_profile"),


    path('lottery_account', Lottery_Account.as_view(),name="lottery_account"),


    path('confirm_ticket/<int:pk>', Confirm_Ticket.as_view(),name="confirm_ticket"),

    path('lottery_prompt', Lottery_Prompt.as_view(),name="lottery_prompt"),

    path('lottery_add', Lottery_Add.as_view(),name="lottery_add"),
    path('lottery', Lottery.as_view(),name="lottery"),




    path('profile_cv/<int:pk>', Cv_Profile.as_view(),name="profile_cv"),



    path('rec_dashboard', Dashboard_Rec.as_view(), name="rec_dashboard"),
    path('rec_login', Rec_Login.as_view(),name="rec_login"),
    path('profile_user_rec/<int:pk>', Profile_User_Rec.as_view(),name="profile_user_rec"),







    path('', Home.as_view(), name="home"),

    path('job_visa/<str:pk>', Job_Visa.as_view(), name="job"),
    path('job_post/<str:pk>', Travel_Packages.as_view(), name="job_post"),


    path('student_visa', Student_Visa.as_view(), name="student"),
    path('logout', Manager_Logout.as_view(),name="logout"),
    path('login', Manager_Login.as_view(),name="login"),
    path('dashboard', Dashboard.as_view(),name="dashboard"),

    path('cards/<int:pk>', Cards.as_view(),name="cards"),


    path('billings', Add_Bill.as_view(), name="billings"),


    #---------------------------------------------------------
    path('client_dashboard', Dashboard_User.as_view(),name="client"),
    path('client_login', Client_New_Login.as_view(),name="client_login"),
    path('client_logout', Client_Logout_Main.as_view(),name="client_logout"),

    path('client_profile', Profile_User.as_view(),name="client_profile"),
    path('client_payment', Payment_User.as_view(),name="client_payment"),
    path('prompt', Prompt.as_view(),name="prompt"),
    path('user_payment_list', Payment_User_List2.as_view(),name="user_payment_list"),

    path('view_client_type/<str:pk>', View_Client_Type.as_view(),name="view_client_type"),


    path('confirm_payment/<int:pk>', Confirm_Payment.as_view(),name="confirm_payment"),


    path('confirm_payment_form/<int:pk>', Confirm_Payment_Form.as_view(),name="confirm_payment_form"),
    path('payment_form', Payment_Form.as_view(),name="payment_form"),



    path('login_authenticate', Login_Authenticate.as_view(),name="login_authenticate"),


#------------------------------------------------ Administrator Urls --------------------------------------------------------------------

    path('admin_dashboard', Administrator_Dashboard.as_view(),name="admin_dashboard"),
    path('admin_login', Administrator_Login.as_view(),name="admin_login"),
    path('admin_logout', Administrator_Logout.as_view(),name="admin_logout"),




    path('payment_issued', Payments_Issued.as_view(), name="payment_issued"),

    path('traffic_table', Traffic_Table.as_view(), name="traffic_table"),
    path('traffic_graph', Traffic_Graph.as_view(), name="traffic_graph"),








    path('manager_account', Manager_Account.as_view(),name="manager_account"),
    path('manager_edit/<int:pk>', Manager_Edit.as_view(),name="manager_edit"),
    path('visitor', Visitors.as_view(), name="visitor"),
    path('update_proccess', Update_Progress.as_view(),name="update_proccess"),
    path('manager_account_group/<str:pk>/<str:pk2>', Manager_Account_Group.as_view(),name="manager_account_group"),







    path('interview_page', Interview_Page.as_view(), name="interview_page"),
    path('interview_login', Interview_Login.as_view(), name="interview_login"),
    path('interview_logout', Interview_Logout.as_view(), name="interview_logout"),
    path('interview_profile/<int:pk>', Interview_Profile.as_view(),name="interview_profile"),
    path('add_interview', Add_Interview.as_view(), name="add_interview"),

    path('interview_page_group/<str:pk>/<str:pk2>', Interview_Page_Group.as_view(), name="interview_page_group"),

    path('interview_page_filter', Interview_Page_Filter.as_view(), name="interview_page_filter"),
    path('interview_page_find', Interview_Page_Find.as_view(), name="interview_page_find"),


    path('add_interviewer', Add_Interviewer.as_view(), name="add_interviewer"),
    path('edit_interviewer/<int:pk>', Edit_Interviewer.as_view(), name="edit_interviewer"),
    path('manager_interview_account', Manager_Interview_Account.as_view(), name="manager_interview_account"),


    path('interview_file/<int:pk>', Interview_File.as_view(), name="interview_file"),

    path('manager_questions', Manager_Questions.as_view(), name="manager_questions"),

    path('manager_questions_view/<int:pk>', Manager_Questions_View.as_view(), name="manager_questions_view"),

    path('manager_edit_update', Manager_Edit_Update.as_view(), name="manager_edit_update"),

    path('client_media/<int:pk>', Client_Media.as_view(), name="client_media"),








#------------------------------------------- Sign ------------------------------------------
    path('sign_file/<int:pk>', Sign_File.as_view(), name="sign_file"),
    path('witness_sign_file/<int:pk>', Witness_Sign_File.as_view(), name="witness_sign_file"),


    path('list_sign_file', List_Sign_File.as_view(), name="list_sign_file"),
#-------------------------------------------Agent --------------------

    path('agent_page', Agent_Page.as_view(), name="agent_page"),
    path('agent_login', Agent_Login.as_view(), name="agent_login"),
    path('agent_logout', Agent_Logout.as_view(), name="agent_logout"),

    path('agent_fill_page', Agent_Fill_Page.as_view(), name="agent_fill_page"),
    path('agent_client_group/<str:pk>', Agent_Client_Group.as_view(), name="agent_client_group"),




    path('add_agent', Add_Agent.as_view(), name="add_agent"),
    path('edit_agent/<int:pk>', Edit_Agent.as_view(), name="edit_agent"),
    path('manager_agent_account', Manager_Agent_Account.as_view(), name="manager_agent_account"),
    path('agent_edit/<int:pk>', Agent_Edit.as_view(), name="agent_edit"),
    path('agent_edit_update', Agent_Edit_Update.as_view(), name="agent_edit_update"),
    path('agent_add_booking', Agent_Add_Booking.as_view(), name="agent_add_booking"),
    path('agent_delete_booking', Agent_Delete_Booking.as_view(), name="agent_delete_booking"),

    path('agent_add_call_logs/<int:pk>', Agent_Add_Call_Logs.as_view(), name="agent_add_call_logs"),

    path('quick_visa_share_with_agent/<str:pk>/<str:pk2>', Quick_Visa_Share_With_Agent.as_view(), name="quick_visa_share_with_agent"),

    path('staff_agent_client_group/<str:pk>', Staff_Agent_Client_Group.as_view(), name="staff_agent_client_group"),


    path('preview_pannel', Preview_Pannel.as_view(), name="preview_pannel"),


    path('confirm_manager_edit/<str:pk>', Confirm_Manager_Edit.as_view(), name="confirm_manager_edit"),

    path('confirm_agent_client_form/<str:pk>', Confirm_Agent_Client_Form.as_view(), name="confirm_agent_client_form"),

    path('confirm_forms', Confirm_Forms.as_view(), name="confirm_forms"),

    path('staff_agent_dash', Staff_Agent_Dash.as_view(), name="staff_agent_dash"),

    path('confirm_documment_list/<int:pk>', Confirm_Documment_List.as_view(), name="confirm_documment_list"),

    path('admin_sign_file/<int:pk>/<int:pk2>', Admin_Sign_File.as_view(), name="admin_sign_file"),

    path('manage_staff_agent_client_group/<str:pk>/<int:pk2>', Manage_Staff_Agent_Client_Group.as_view(), name="manage_staff_agent_client_group"),
    path('manage_staff_agent_client_group_main/<str:pk>/<int:pk2>', Manage_Staff_Agent_Client_Group_Main.as_view(), name="manage_staff_agent_client_group_main"),

    path('find_staff_agent_dash', Find_Staff_Agent_Dash.as_view(), name="find_staff_agent_dash"),

    path('agent_pay_list', Agent_Pay_List.as_view(), name="agent_pay_list"),


    path('confirm_manager_payout/<int:pk>', Confirm_Manager_Payout.as_view(), name="confirm_manager_payout"),

    path('confirm_payout', Confirm_Payout.as_view(), name="confirm_payout"),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)