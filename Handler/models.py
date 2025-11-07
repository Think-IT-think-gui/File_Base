from email.headerregistry import Address
from django.db import models

#from Handler.views import Categories

class Date_Info(models.Model):
    Dated = models.CharField(max_length=10000, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Dated

class Debit_info(models.Model):
    User = models.IntegerField()
    Amount = models.FloatField()
    Status = models.CharField(max_length=10000)


    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Amount
class Administrator_Info(models.Model):
    User = models.CharField(max_length=10000)
    Password = models.CharField(max_length=10000)
    Full_Name = models.CharField(max_length=200)
    Location = models.CharField(max_length=10000, null=True)
    Email = models.EmailField(max_length=10000)
    Contact = models.CharField(max_length=10000, null=True)
    Account = models.CharField(max_length=10000, null=True)
    Currency = models.CharField(max_length=10000, null=True)



    Birth = models.CharField(max_length=10000)
    Gender = models.CharField(max_length=10000)

    Interview = models.CharField(max_length=10000)
    New_Leads = models.CharField(max_length=10000)
    All_Applications = models.CharField(max_length=10000)
    New_Applications = models.CharField(max_length=10000)
    Pending_Applications = models.CharField(max_length=10000)
    Unreachable_Applicants = models.CharField(max_length=10000)

    Briefed_Applicants = models.CharField(max_length=10000)
    Booked_Applicants = models.CharField(max_length=10000)
    SEP_Applicants = models.CharField(max_length=10000)
    Ready_Applicants = models.CharField(max_length=10000)
    Active_Applicants = models.CharField(max_length=10000)

    Declined_Applicants = models.CharField(max_length=10000)

    Operation_Unit = models.CharField(max_length=10000)
    IELTS = models.CharField(max_length=10000)
    Police_Report = models.CharField(max_length=10000)
    Medicals_Status = models.CharField(max_length=10000)

    Client_Booking = models.CharField(max_length=10000)
    Financials = models.CharField(max_length=10000)
    Bills_Pricing = models.CharField(max_length=10000)
    Call_Overview = models.CharField(max_length=10000)
    Packages = models.CharField(max_length=10000)

    Traffic_Overview = models.CharField(max_length=10000)
    Account_Management = models.CharField(max_length=10000)
    Briefing_Room = models.CharField(max_length=10000)
    Medical = models.CharField(max_length=10000)
    Decision = models.CharField(max_length=10000)

    Archived = models.CharField(max_length=10000)
    Travelled = models.CharField(max_length=10000)
    Exiting = models.CharField(max_length=10000)
    Travelling = models.CharField(max_length=10000)
    Agent = models.CharField(max_length=10000)
    Confirm_Agent = models.CharField(max_length=10000)
    Method = models.CharField(max_length=10000)


    Ashanti = models.CharField(max_length=10000)
    Bono = models.CharField(max_length=10000)
    Bono_East = models.CharField(max_length=10000)
    Central = models.CharField(max_length=10000)
    Eastern = models.CharField(max_length=10000)
    Greater_Accra = models.CharField(max_length=10000)
    Northern = models.CharField(max_length=10000)
    North_East = models.CharField(max_length=10000)

    Oti = models.CharField(max_length=10000)
    Savannah = models.CharField(max_length=10000)
    Upper_East = models.CharField(max_length=10000)

    Upper_West = models.CharField(max_length=10000)
    Volta = models.CharField(max_length=10000)
    Western = models.CharField(max_length=10000)
    Western_North = models.CharField(max_length=10000)
    Ahafo = models.CharField(max_length=10000)


    Regional = models.CharField(max_length=10000)






    Profile_1 = models.CharField(max_length=10000)
    Profile_2 = models.CharField(max_length=10000)
    Profile_3 = models.CharField(max_length=10000)


    Last_Seen = models.CharField(max_length=10000, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Full_Name



class Status_Logs(models.Model):
    User = models.IntegerField()
    Client = models.IntegerField()
    Old = models.CharField(max_length=10000)
    New = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.User



class Applicant_Logs(models.Model):
    User = models.IntegerField()
    Client = models.IntegerField()
    Log = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.User


class Visa_Info(models.Model):
    Admin = models.CharField(max_length=300)
    Agent = models.CharField(max_length=300)

    Agent_Type = models.CharField(max_length=300)
    Contact_Email = models.CharField(max_length=300, null=True)
    Contact_Email_Password = models.CharField(max_length=300, null=True)
    IELTS = models.CharField(max_length=10000)
    Police = models.CharField(max_length=10000)
    Medicals = models.CharField(max_length=10000)
    Full_Name = models.CharField(max_length=300)
    Gender = models.CharField(max_length=10000)
    Birth = models.CharField(max_length=10000)
    Marital = models.CharField(max_length=10000)
    Seen = models.CharField(max_length=10000)
    Password = models.CharField(max_length=10000)
    Address = models.CharField(max_length=10000, null=True)
    City = models.CharField(max_length=10000, null=True)
    Email = models.EmailField(max_length=10000)
    Contact = models.CharField(max_length=10000, null=True)
    Skill = models.CharField(max_length=10000, null=True)
    Skill_Level = models.CharField(max_length=10000, null=True)
    Experience = models.CharField(max_length=10000, null=True)
    Education = models.CharField(max_length=10000, null=True)
    Passport = models.CharField(max_length=10000, null=True)
    Birth_Cert = models.CharField(max_length=10000, null=True)
    Refrene_Code = models.CharField(max_length=300, null=True)

    Garantor_Full_Name = models.CharField(max_length=300 , null=True)
    Garantor_Gender = models.CharField(max_length=10000 , null=True)
    Garantor_Address = models.CharField(max_length=10000, null=True)
    Garantor_City = models.CharField(max_length=10000, null=True)
    Garantor_Email = models.EmailField(max_length=10000 , null=True)
    Garantor_Contact = models.CharField(max_length=10000, null=True)



    Garantor_Birth = models.CharField(max_length=10000, null=True)
    Garantor_ID = models.CharField(max_length=10000, null=True)
    Garantor_Job = models.CharField(max_length=10000, null=True)
    Garantor_Title = models.CharField(max_length=10000, null=True)
    Garantor_Job_Address = models.CharField(max_length=10000, null=True)
    Garantor_Job_Contact = models.CharField(max_length=10000, null=True)
    Garantor_House = models.CharField(max_length=10000, null=True)
    Garantor_Street = models.CharField(max_length=10000, null=True)
    Garantor_Landmark = models.CharField(max_length=10000, null=True)
    Garantor_Gps = models.CharField(max_length=10000, null=True)


    #----------------------------------------------------------
    Father_Full_Name = models.CharField(max_length=300 , null=True)
    Father_Address = models.CharField(max_length=10000, null=True)
    Father_Birth = models.CharField(max_length=10000 , null=True)
    Father_Contact = models.CharField(max_length=10000, null=True)
    Father_City = models.CharField(max_length=10000, null=True)


    Mother_Full_Name = models.CharField(max_length=300 , null=True)
    Mother_Address = models.CharField(max_length=10000, null=True)
    Mother_Birth = models.CharField(max_length=10000 , null=True)
    Mother_Contact = models.CharField(max_length=10000, null=True)
    Mother_City = models.CharField(max_length=10000, null=True)
    Link = models.CharField(max_length=10000)
    Group = models.CharField(max_length=10000)

    Main_ID = models.CharField(max_length=900000, null=True)
    #--------------------------------------------------------------------

    Reference1_Full_Name = models.CharField(max_length=300 , null=True)
    Reference1_Address = models.CharField(max_length=10000, null=True)
    Reference1_Job = models.CharField(max_length=10000 , null=True)
    Reference1_Contact = models.CharField(max_length=10000, null=True)

    Reference2_Full_Name = models.CharField(max_length=300 , null=True)
    Reference2_Address = models.CharField(max_length=10000, null=True)
    Reference2_Job = models.CharField(max_length=10000 , null=True)
    Reference2_Contact = models.CharField(max_length=10000, null=True)

    Reference3_Full_Name = models.CharField(max_length=300 , null=True)
    Reference3_Address = models.CharField(max_length=10000, null=True)
    Reference3_Job = models.CharField(max_length=10000 , null=True)
    Reference3_Contact = models.CharField(max_length=10000, null=True)


    Job_Choice1 = models.CharField(max_length=300)
    Country1 = models.CharField(max_length=10000)
    Job_Choice2 = models.CharField(max_length=300)
    Country2 = models.CharField(max_length=10000)
    Job_Choice3 = models.CharField(max_length=300)
    Country3 = models.CharField(max_length=10000)

    #--------------------------------------------------------
    Marital = models.CharField(max_length=10000, null=True)

    Height = models.CharField(max_length=10000, null=True)
    Hair = models.CharField(max_length=10000, null=True)
    Eye = models.CharField(max_length=10000, null=True)

    Birth_City = models.CharField(max_length=10000, null=True)
    Country_Birth = models.CharField(max_length=10000, null=True)
    Postal_Code = models.CharField(max_length=10000, null=True)
    Birth_Address = models.CharField(max_length=10000, null=True)

    Blocked = models.CharField(max_length=300, null=True)
    Account_Type = models.CharField(max_length=300, null=True)
    Country_Recidence = models.CharField(max_length=10000, null=True)

    Postal_Code_Recidence = models.CharField(max_length=10000, null=True)
    Father_Living = models.CharField(max_length=10000, null=True)
    Mother_Living = models.CharField(max_length=10000, null=True)

    Weight = models.CharField(max_length=10000, null=True)
    Card_Id = models.CharField(max_length=10000, null=True)










    Call = models.CharField(max_length=10000,null=True)
    Code = models.CharField(max_length=10000)
    FCM = models.TextField()



    SEP = models.CharField(max_length=10000, null=True)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Email



class Cookie_Handler(models.Model):
    Cookie = models.CharField(max_length=10000)
    User = models.IntegerField()
    Type = models.CharField(max_length=10000)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Cookie

class SignUp_info(models.Model):
    Full_Name = models.CharField(max_length=10000)
    Email = models.EmailField(max_length=10000)
    Password = models.CharField(max_length=10000)
    Contact = models.CharField(max_length=10000)
    Location = models.CharField(max_length=10000)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Email


class Funds_info(models.Model):
    User = models.IntegerField()
    Amount = models.FloatField()
    Status = models.CharField(max_length=10000)

    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Amount

#-------------------------------------------------

class Traffic(models.Model):
    Ip_Address = models.CharField(max_length=10000)
    City = models.CharField(max_length=10000)
    Region = models.CharField(max_length=10000)
    Country = models.CharField(max_length=10000)
    Coordinate = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)

    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.City


class Visit(models.Model):
    Name = models.CharField(max_length=300)
    Contact = models.CharField(max_length=300)
    Email = models.EmailField(max_length=300)
    Location = models.CharField(max_length=300)
    Group = models.CharField(max_length=300)
    Region = models.CharField(max_length=300)
    Confirmation = models.CharField(max_length=10000)
    Attended = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Region

class Extra_Images(models.Model):
    Profile = models.IntegerField()
    Type = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Profile

class Extra_Info(models.Model):
    Profile = models.IntegerField()
    Type = models.CharField(max_length=300)
    Name = models.CharField(max_length=300)
    Start = models.CharField(max_length=300)
    End = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Profile

class Notifications(models.Model):
    Name = models.CharField(max_length=10000)
    User = models.IntegerField()
    Info = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    Link = models.CharField(max_length=200, null=True)
    Type = models.CharField(max_length=10000, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Billings(models.Model):
    Name = models.CharField(max_length=10000)
    Price = models.FloatField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name

class Client_Billing(models.Model):
    Name = models.CharField(max_length=10000)
    Price = models.FloatField()
    User = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name

class Call_Record(models.Model):
    User = models.IntegerField()
    Admin = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.User





class Lottery_Info(models.Model):
    Full_Name = models.CharField(max_length=300)
    Gender = models.CharField(max_length=10000)
    Birth = models.CharField(max_length=10000)
    Marital = models.CharField(max_length=10000)


    Validate = models.CharField(max_length=10000)


    Address = models.CharField(max_length=10000, null=True)
    City = models.CharField(max_length=10000, null=True)
    Email = models.EmailField(max_length=10000)
    Contact = models.CharField(max_length=10000, null=True)
    Skill = models.CharField(max_length=10000, null=True)
    Skill_Level = models.CharField(max_length=10000, null=True)
    Experience = models.CharField(max_length=10000, null=True)
    Education = models.CharField(max_length=10000, null=True)
    Passport = models.CharField(max_length=10000, null=True)
    Birth_Cert = models.CharField(max_length=10000, null=True)
    Refrene_Code = models.CharField(max_length=300, null=True)

    Garantor_Full_Name = models.CharField(max_length=300 , null=True)
    Garantor_Gender = models.CharField(max_length=10000 , null=True)
    Garantor_Address = models.CharField(max_length=10000, null=True)
    Garantor_City = models.CharField(max_length=10000, null=True)
    Garantor_Email = models.EmailField(max_length=10000 , null=True)
    Garantor_Contact = models.CharField(max_length=10000, null=True)


    #----------------------------------------------------------
    Father_Full_Name = models.CharField(max_length=300 , null=True)
    Father_Address = models.CharField(max_length=10000, null=True)
    Father_Birth = models.CharField(max_length=10000 , null=True)
    Father_Contact = models.CharField(max_length=10000, null=True)
    Father_City = models.CharField(max_length=10000, null=True)


    Mother_Full_Name = models.CharField(max_length=300 , null=True)
    Mother_Address = models.CharField(max_length=10000, null=True)
    Mother_Birth = models.CharField(max_length=10000 , null=True)
    Mother_Contact = models.CharField(max_length=10000, null=True)
    Mother_City = models.CharField(max_length=10000, null=True)


    #--------------------------------------------------------------------

    Reference1_Full_Name = models.CharField(max_length=300 , null=True)
    Reference1_Address = models.CharField(max_length=10000, null=True)
    Reference1_Job = models.CharField(max_length=10000 , null=True)
    Reference1_Contact = models.CharField(max_length=10000, null=True)

    Reference2_Full_Name = models.CharField(max_length=300 , null=True)
    Reference2_Address = models.CharField(max_length=10000, null=True)
    Reference2_Job = models.CharField(max_length=10000 , null=True)
    Reference2_Contact = models.CharField(max_length=10000, null=True)

    Reference3_Full_Name = models.CharField(max_length=300 , null=True)
    Reference3_Address = models.CharField(max_length=10000, null=True)
    Reference3_Job = models.CharField(max_length=10000 , null=True)
    Reference3_Contact = models.CharField(max_length=10000, null=True)


    Job_Choice1 = models.CharField(max_length=300)
    Country1 = models.CharField(max_length=10000)
    Job_Choice2 = models.CharField(max_length=300)
    Country2 = models.CharField(max_length=10000)
    Job_Choice3 = models.CharField(max_length=300)
    Country3 = models.CharField(max_length=10000)

    #--------------------------------------------------------
    Marital = models.CharField(max_length=10000, null=True)

    Height = models.CharField(max_length=10000, null=True)
    Hair = models.CharField(max_length=10000, null=True)
    Eye = models.CharField(max_length=10000, null=True)

    Birth_City = models.CharField(max_length=10000, null=True)
    Country_Birth = models.CharField(max_length=10000, null=True)
    Postal_Code = models.CharField(max_length=10000, null=True)
    Birth_Address = models.CharField(max_length=10000, null=True)



    Country_Recidence = models.CharField(max_length=10000, null=True)

    Postal_Code_Recidence = models.CharField(max_length=10000, null=True)
    Father_Living = models.CharField(max_length=10000, null=True)
    Mother_Living = models.CharField(max_length=10000, null=True)

    Weight = models.CharField(max_length=10000, null=True)
    Card_Id = models.CharField(max_length=10000, null=True)




    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Email


class Job(models.Model):
    User = models.IntegerField()
    Link = models.CharField(max_length=10000)
    Title = models.CharField(max_length=10000)
    Experience = models.CharField(max_length=10000)
    Type = models.CharField(max_length=10000)
    Group = models.CharField(max_length=10000)
    Min_Salary = models.FloatField()
    Max_Salary = models.FloatField()
    View_Salary = models.CharField(max_length=10000)
    About = models.CharField(max_length=90000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Title


class Job_Skills(models.Model):
    Job = models.IntegerField()
    About = models.CharField(max_length=9000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.About

class Job_Role(models.Model):
    Job = models.IntegerField()
    About = models.CharField(max_length=9000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.About

class Job_Benefits(models.Model):
    Job = models.IntegerField()
    About = models.CharField(max_length=9000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.About










#-------------------------------------------------------

class Pass_Port(models.Model):
    User = models.IntegerField(blank=True, null=True)

    Last_name = models.CharField(max_length=10000)
    First_name = models.CharField(max_length=10000)
    Other_name = models.CharField(max_length=10000, blank=True, null=True)
    Gender = models.CharField(max_length=10000)
    Date_of_birth = models.CharField(max_length=10000)
    Contact = models.CharField(max_length=10000)
    Email = models.EmailField(max_length=10000)
    City_of_birth = models.CharField(max_length=10000)
    Country_of_birth = models.CharField(max_length=10000)
    Height = models.CharField(max_length=10)
    Colour_of_eyes = models.CharField(max_length=10000)
    Colour_of_hair = models.CharField(max_length=10000)
    Nationality = models.CharField(max_length=10000)
    Marital_status = models.CharField(max_length=200)
    Profession = models.CharField(max_length=10000)
    Previous_profession = models.CharField(max_length=10000, blank=True, null=True)
    National_id = models.CharField(max_length=10000)
    Social_security = models.CharField(max_length=10000,)

    House_number = models.CharField(max_length=10000)
    Street_name = models.CharField(max_length=10000)
    Postal_address = models.CharField(max_length=10000)

    City_of_residence = models.CharField(max_length=10000)
    Country_of_residence = models.CharField(max_length=10000)
    Zip_code = models.CharField(max_length=20)

    Father_full_name = models.CharField(max_length=10000)
    Father_living = models.CharField(max_length=10000)
    Father_contact = models.CharField(max_length=10000)
    Father_email = models.EmailField(blank=True, null=True)
    Father_home_town = models.CharField(max_length=10000)
    Father_residential_address = models.CharField(max_length=10000)
    Father_nationality = models.CharField(max_length=10000)

    Mother_full_name = models.CharField(max_length=10000)
    Mother_living = models.CharField(max_length=10000)
    Mother_contact = models.CharField(max_length=10000)
    Mother_email = models.EmailField(blank=True, null=True)
    Mother_home_town = models.CharField(max_length=10000)
    Mother_residential_address = models.CharField(max_length=10000)
    Mother_nationality = models.CharField(max_length=10000)

    Grandparent_full_name = models.CharField(max_length=10000)
    Grandparent_living = models.CharField(max_length=10000)
    Grandparent_contact = models.CharField(max_length=10000)
    Grandparent_email = models.EmailField(blank=True, null=True)
    Grandparent_home_town = models.CharField(max_length=10000)
    Grandparent_residential_address = models.CharField(max_length=10000)
    Grandparent_nationality = models.CharField(max_length=10000)


    First_guarantor_full_name = models.CharField(max_length=10000)
    First_guarantor_occupation = models.CharField(max_length=10000)
    First_guarantor_contact = models.CharField(max_length=10000)
    First_guarantor_email = models.EmailField(blank=True, null=True)
    First_guarantor_residential_address = models.CharField(max_length=10000)


    Second_guarantor_full_name = models.CharField(max_length=10000)
    Second_guarantor_occupation = models.CharField(max_length=10000)
    Second_guarantor_contact = models.CharField(max_length=10000)
    Second_guarantor_email = models.EmailField(blank=True, null=True)
    Second_guarantor_residential_address = models.CharField(max_length=10000)

    Witness_full_name = models.CharField(max_length=10000)
    Witness_email = models.EmailField(blank=True, null=True)
    Witness_contact = models.CharField(max_length=10000)
    Witness_residential_address = models.CharField(max_length=10000)
    Witness_home_town = models.CharField(max_length=10000)
    Witness_occupation = models.CharField(max_length=10000)


    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.First_name


class Birth_Cert(models.Model):
    User = models.IntegerField()
    First_name = models.CharField(max_length=10000)
    Middle_name = models.CharField(max_length=10000, blank=True, null=True)
    Surname = models.CharField(max_length=10000)
    Date_of_birth = models.DateField()
    Place_of_birth = models.CharField(max_length=10000)

    Father_name = models.CharField(max_length=10000)
    Father_residential_address = models.CharField(max_length=10000)
    Father_town = models.CharField(max_length=10000)
    Father_telephone = models.CharField(max_length=10000)
    Father_occupation = models.CharField(max_length=10000)
    Father_religion = models.CharField(max_length=10000)

    Mother_maiden_name = models.CharField(max_length=10000)
    Mother_residential_address = models.CharField(max_length=10000)
    Mother_town = models.CharField(max_length=10000)
    Mother_telephone = models.CharField(max_length=10000)
    Mother_occupation = models.CharField(max_length=10000)
    Number_of_previous_births = models.PositiveIntegerField()

    Informant_name = models.CharField(max_length=10000)
    Relationship = models.CharField(max_length=10000)
    Informant_residential_address = models.CharField(max_length=10000)
    Informant_town = models.CharField(max_length=10000)
    Informant_telephone = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.First_name











class Code_Info(models.Model):
    Name = models.CharField(max_length=10000)
    User = models.IntegerField(null=True)
    Validate = models.CharField(max_length=50)
    Email =models.EmailField(max_length=700)
    Contact = models.CharField(max_length=10000)
    Used = models.CharField(max_length=10000)
    Type = models.CharField(max_length=10000)

    Refrene_Code = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name

class Education_Info(models.Model):
    Name = models.CharField(max_length=10000)
    User = models.IntegerField()
    Start = models.CharField(max_length=10000)
    End = models.CharField(max_length=10000)
    Location = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name

class Passport_Code_Info(models.Model):
    Name = models.CharField(max_length=10000)
    Price = models.FloatField(max_length=10000)
    Profit= models.FloatField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name








class Portal_Info(models.Model):
    Password = models.CharField(max_length=10000)
    Full_Name = models.CharField(max_length=10000)
    Location = models.CharField(max_length=10000, null=True)
    Email = models.EmailField(max_length=10000)
    Contact = models.CharField(max_length=10000, null=True)
    Account = models.CharField(max_length=10000, null=True)
    Currency = models.CharField(max_length=10000, null=True)
    Last_Seen = models.CharField(max_length=10000, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Email





class Call_Logs(models.Model):
    User = models.IntegerField()
    Agent = models.IntegerField()

    Member = models.IntegerField()

    Name = models.CharField(max_length=300)
    Contact = models.CharField(max_length=10000)
    Location = models.CharField(max_length=10000)
    Gender = models.CharField(max_length=10000)

    Start_Time = models.CharField(max_length=10000)
    End_Time = models.CharField(max_length=10000)

    Status = models.CharField(max_length=10000)
    Type = models.CharField(max_length=10000)
    About = models.CharField(max_length=9000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name



class Share_Link(models.Model):
    User = models.IntegerField()

    Job = models.IntegerField()

    Link = models.CharField(max_length=300)

    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Link


class Booking(models.Model):
    User = models.IntegerField()
    Admin = models.IntegerField()

    Name = models.CharField(max_length=10000)
    Topic = models.CharField(max_length=10000)
    Location = models.CharField(max_length=10000)
    Gender = models.CharField(max_length=10000)
    Contact = models.CharField(max_length=10000)
    About = models.CharField(max_length=100000)
    Remark = models.CharField(max_length=10000)
    Details = models.CharField(max_length=10000)
    Schedule_Date = models.CharField(max_length=10000)
    Schedule_Time = models.CharField(max_length=10000)
    Type = models.CharField(max_length=10000)
    Clock_In = models.TimeField(auto_now_add=True)
    Clock_Out = models.TimeField(auto_now_add=True)


    Status = models.CharField(max_length=10000)
    Agent = models.CharField(max_length=10000)

    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name






















class Uploaded_Files(models.Model):
    User = models.IntegerField()
    Name = models.CharField(max_length=10000)
    About = models.TextField()
    Count = models.CharField(max_length=10000)
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Uploaded_Files_List(models.Model):
    User = models.IntegerField()
    File = models.IntegerField()
    Name = models.CharField(max_length=900)
    Extention = models.CharField(max_length=10000)
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name



class Uploaded_Files_Group(models.Model):
    User = models.IntegerField()
    Name = models.CharField(max_length=10000)
    About = models.TextField()
    Count = models.CharField(max_length=10000)
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.Name} - {self.date}'


class Uploaded_Files_List_Group(models.Model):
    User = models.IntegerField()
    File = models.IntegerField()
    Name = models.CharField(max_length=900)
    Extention = models.CharField(max_length=10000)
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Uploaded_Client_Group(models.Model):
    User = models.IntegerField()
    File = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.File




#--------------------------------------------- Messaging ---------------------------------------------------------


class Message(models.Model):
    Chat =  models.TextField()
    Sender = models.IntegerField()
    Reciever = models.IntegerField()
    Info = models.TextField()
    Reply_Id = models.IntegerField()
    Reply = models.TextField()

    Type = models.CharField(max_length=10000, null=True)
    Status = models.CharField(max_length=10000)
    Alert = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Type

class Message_List(models.Model):
    User= models.IntegerField()
    Client = models.IntegerField()
    Link = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.User

class File_Link(models.Model):
    User = models.IntegerField()
    Post = models.IntegerField()
    Link = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Link

#--------------------------------------------- Messaging ---------------------------------------------------------





class Interview_Account(models.Model):
    Name = models.CharField(max_length=300)
    Contact = models.CharField(max_length=300)
    Password = models.CharField(max_length=300)
    Email = models.EmailField(max_length=300)
    Location = models.CharField(max_length=300)
    Country = models.CharField(max_length=300)

    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Interview_Session(models.Model):
    User = models.IntegerField()
    Client = models.IntegerField()

    Appearance = models.CharField(max_length=300)
    Appearance_Remark = models.TextField()

    Communication = models.CharField(max_length=300)
    Communication_Remark = models.TextField()

    Practical = models.CharField(max_length=300)
    Practical_Remark = models.TextField()

    Commitment = models.CharField(max_length=300)
    Commitment_Remark = models.TextField()

    Medicals = models.CharField(max_length=300)
    Medicals_Remark = models.TextField()

    Confidence = models.CharField(max_length=300)
    Confidence_Remark = models.TextField()

    Knowledge = models.CharField(max_length=300)
    Knowledge_Remark = models.TextField()


    Question = models.CharField(max_length=300)
    Remark = models.TextField()
    Start = models.CharField(max_length=300)
    End = models.CharField(max_length=300)
    Dated = models.CharField(max_length=300)
    Status = models.CharField(max_length=10000)
    Answer = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Client



class Question_Group(models.Model):
    User = models.IntegerField()
    Name = models.CharField(max_length=300)
    About = models.TextField()
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Question(models.Model):
    Group = models.IntegerField()
    Question = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class ID_Card(models.Model):
    Link = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Link

class Card_Point(models.Model):
    Name =  models.CharField(max_length=300)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Card_Session(models.Model):
    Card = models.IntegerField()
    User = models.IntegerField()
    Client = models.IntegerField()
    About = models.TextField()
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Client


class Card_Session_Point(models.Model):
    Name =  models.CharField(max_length=300)
    User = models.IntegerField()
    Client = models.IntegerField()
    Session = models.IntegerField()
    Point = models.IntegerField()
    Status = models.CharField(max_length=10000)
    Set_Time =  models.CharField(max_length=300)
    Set_Date =  models.CharField(max_length=300)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Card_Point_Permission(models.Model):
    User = models.IntegerField()
    Point = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.User


class Card_Point_Message(models.Model):
    User = models.IntegerField()
    Session = models.IntegerField()
    About = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.User


class Side_Menu(models.Model):
    Name = models.CharField(max_length=100000)
    Level = models.IntegerField()
    Status_Change = models.CharField(max_length=10000)
    Call_Log = models.CharField(max_length=10000)
    Book_Client = models.CharField(max_length=10000)
    Interview = models.CharField(max_length=10000)
    Chat_Files = models.CharField(max_length=10000)
    Profile = models.CharField(max_length=10000)
    Cv = models.CharField(max_length=10000)
    Payment = models.CharField(max_length=10000)
    Debit = models.CharField(max_length=10000)
    Id_Card = models.CharField(max_length=10000)
    Upload_Files = models.CharField(max_length=10000)
    View_Files = models.CharField(max_length=10000)
    Delete = models.CharField(max_length=10000)
    Opperation = models.CharField(max_length=10000)
    Sign = models.CharField(max_length=10000)


    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name



class Side_Menu_Permission(models.Model):
    User = models.IntegerField()
    Menu = models.IntegerField()
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Status



class Issue_Logs(models.Model):
    User = models.IntegerField()
    Name =  models.CharField(max_length=3000)
    About = models.TextField()
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name



class Issue_Files_List(models.Model):
    User = models.IntegerField()
    Issue = models.IntegerField()
    Name = models.CharField(max_length=900)
    Extention = models.CharField(max_length=10000)
    Status = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Completed_Logs(models.Model):
    User = models.IntegerField()
    Client = models.IntegerField()
    Type = models.CharField(max_length=10000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.User





#---------------------------------------------------------------------------------------------
class Post_Info(models.Model):
    Context = models.CharField(max_length=100000, null=True)
    User = models.IntegerField()
    Type = models.CharField(max_length=10000)
    Link = models.CharField(max_length=100000, null=True)
   #-------------------------------------------
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Type

class Likes(models.Model):
    Post = models.IntegerField()
    User = models.IntegerField()
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Post

class Comments(models.Model):
    Post = models.IntegerField()
    User = models.IntegerField()
    Comment = models.CharField(max_length=100000, null=True)
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Post


class Extra_Images_Post(models.Model):
    Post = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Post

class Extra_Videos(models.Model):
    Post = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Post



class Remarks(models.Model):
    Remark = models.TextField()
    Mark = models.IntegerField()
    Group = models.CharField(max_length=10000)
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Post

#-----------------------------------------------------------


class Document_Signable(models.Model):
    Name = models.TextField()
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class User_Signed_Document(models.Model):
    Document = models.IntegerField()
    User = models.IntegerField()
    Status = models.CharField(max_length=300)
    Uid = models.CharField(max_length=300)
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Document

class Withness_Signed_Document(models.Model):
    Document = models.IntegerField()
    User = models.IntegerField()
    Name = models.CharField(max_length=10000)
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Document


class Confirm_Signed_Document(models.Model):
    Signed = models.IntegerField()
    User = models.IntegerField()
    Client = models.IntegerField()
    Time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.Signed





class Agent_Account(models.Model):
    Name = models.CharField(max_length=300)
    Contact = models.CharField(max_length=300)
    Method = models.CharField(max_length=100)
    Password = models.CharField(max_length=300)
    Email = models.EmailField(max_length=300)
    Location = models.CharField(max_length=300)
    Country = models.CharField(max_length=300)
    Link = models.CharField(max_length=1000)

    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name


class Agent_Account_Link(models.Model):
    Client = models.IntegerField()
    User = models.IntegerField()
    Status = models.CharField(max_length=300)
    Type = models.CharField(max_length=300)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Status

class Last_Agent(models.Model):
    User = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __int__(self):
        return self.User


class Preview_Board(models.Model):
    User = models.IntegerField()

    Booking = models.IntegerField()
    Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Count = models.CharField(max_length=100)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name





class Agent_Form_Funds(models.Model):
    User = models.IntegerField()
    Client = models.IntegerField()
    Type = models.CharField(max_length=100)
    Amount = models.FloatField()
    Status = models.CharField(max_length=300)
    Transfared = models.CharField(max_length=300)
    Completed = models.CharField(max_length=300)
    Refrence = models.CharField(max_length=1000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Type

