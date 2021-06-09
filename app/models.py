# models.py 

from datetime import datetime 
from time import time
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, func, Column, extract, ForeignKey
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app import app
     

class ControlVariables(db.Model):
    __tablename__ = 'tblControl_Variables'
    __table_args__ = {"schema": "dbo"}
    Shop_Number = db.Column(db.Integer, primary_key=True)
    Current_Dues_Year = db.Column(db.String(4))
    Current_Dues_Amount = db.Column(db.Numeric)
    Current_Initiation_Fee = db.Column(db.Numeric)
    Date_To_Begin_New_Dues_Collection = db.Column(db.Date)
    Date_To_Accept_New_Members = db.Column(db.Date)
    Last_Acceptable_Monitor_Training_Date = db.Column(db.Date)
    AcceptingNewMembers = db.Column(db.Boolean)
    Dues_Account = db.Column(db.String(10))
    Initiation_Fee_Account = db.Column(db.String(10))
    WaitingListApplicantNote = db.Column(db.String(255))
    Message_Board = db.Column(db.String(max))

class Member(db.Model):
    __tablename__ = 'tblMember_Data'
    __table_args__ = {"schema": "dbo"}
    id = db.Column(db.Integer, primary_key=True)
    Member_ID = db.Column(db.String(6),
         index=True,
         unique=True)
    Last_Name = db.Column(db.String(30))
    First_Name = db.Column(db.String(30))
    #NickName = db.Column(db.String(30))
    Date_Joined = db.Column(db.DateTime)
    #monthJoined = db.Column(db.Integer)
    #yearJoined=db.Column(db.String(4))
    Certified = db.Column(db.Boolean)
    Certification_Training_Date = db.Column(db.DateTime)
    Certified_2 = db.Column(db.Boolean)
    Certification_Training_Date_2 = db.Column(db.DateTime)
    Home_Phone = db.Column(db.String(14))
    Cell_Phone = db.Column(db.String(14))
    eMail = db.Column('E-Mail',db.String(255))
    Dues_Paid=db.Column(db.Boolean)
    NonMember_Volunteer=db.Column(db.Boolean)
    Restricted_From_Shop = db.Column(db.Boolean)
    Reason_For_Restricted_From_Shop = db.Column(db.String(255))
    Last_Monitor_Training = db.Column(db.DateTime)
    Last_Monitor_Training_Shop_2 = db.Column(db.DateTime)

    fullName = column_property(First_Name + " " + Last_Name)
    # Relationships
    #activities = db.relationship('MemberActivity', backref='member')
    def wholeName(self):
        return self.lastName + ", " + self.firstName 
  
class ShopName(db.Model):
    __tablename__ = 'tblShop_Names'
    __table_args__ = {"schema": "dbo"}
    Shop_Number = db.Column(db.Integer, primary_key=True)
    Shop_Name = db.Column(db.String(30))

class MemberActivity(db.Model):
    __tablename__ = 'tblMember_Activity'
    __table_args__ = {"schema": "dbo"}
    ID = db.Column(db.Integer, primary_key=True)
    Member_ID = db.Column(db.String(6))
    Check_In_Date_Time = db.Column(db.DateTime)
    Check_Out_Date_Time = db.Column(db.DateTime)
    Type_Of_Work = db.Column(db.String(20))
    Shop_Number = db.Column(db.Integer)
    Door_Used = db.Column(db.String(5))

class MonitorSchedule(db.Model):
    __tablename__ = 'tblMonitor_Schedule'
    __table_args__ = {"schema": "dbo"}
    ID = db.Column(db.Integer,autoincrement=True)
    Member_ID = db.Column(db.String(6), primary_key=True)
    Date_Scheduled = db.Column(db.DateTime, primary_key=True)
    AM_PM = db.Column(db.String(2), primary_key=True)
    Shop_Number = db.Column(db.Integer, primary_key=True)
    Monitor_Notes = db.Column(db.String(255))
    Duty = db.Column(db.String(20))
    No_Show = db.Column(db.Boolean)
    Optional = db.Column(db.Boolean)
    
class CoordinatorsSchedule(db.Model):
	__tablename__ = 'coordinatorsSchedule'
	__table_args__ = {"schema":"dbo"}
	ID = db.Column(db.Integer)
	Shop_Number = db.Column(db.Integer, primary_key=True)
	Start_Date = db.Column(db.DateTime, primary_key=True)
	End_Date = db.Column(db.DateTime)
	Coordinator_ID = db.Column(db.String(6))

