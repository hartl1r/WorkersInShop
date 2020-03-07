# routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify, json, make_response
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import ShopName, Member , MemberActivity
from app import app
from app import db
from sqlalchemy import func, case, desc, extract, select, update
from sqlalchemy.exc import SQLAlchemyError 
import datetime
from datetime import date

@app.route('/')
@app.route('/index')
def index():
    return render_template("checkin.html")

@app.route('/checkIn', methods=["GET","POST"])
def checkIn():
    shopNumber = "1"

    if request.method != 'POST':
        return
    requestData = request.get_json()
    villageID = requestData.get("memberID")
    typeOfWorkOverride = requestData.get("typeOfWork")
    
    # Look up member ID
    sqlSelect = """ SELECT Member_ID, First_Name, Last_Name, NonMember_Volunteer, Certified, Certified_2,Default_Type_Of_Work, Restricted_From_Shop, Reason_For_Restricted_From_Shop, noteToMember
        FROM tblMember_Data LEFT JOIN notesToMembers ON tblMember_Data.Member_ID = notesToMembers.memberID
        WHERE tblMember_Data.Member_ID='""" + villageID + """'"""
    
    member = db.engine.execute(sqlSelect)
    row = 0
    for m in member:
        row += 1
        villageID = m.Member_ID
        memberName = m.First_Name + " " + m.Last_Name
        typeOfWorkToUse = "General"
        if (m.Default_Type_Of_Work != None):
            typeOfWorkToUse = m.Default_Type_Of_Work
        
        if (typeOfWorkOverride != "General"):
            typeOfWorkToUse = typeOfWorkOverride

        certified1 = m.Certified
        certified2 = m.Certified_2
        restricted = m.Restricted_From_Shop
        reasonRestricted = m.Reason_For_Restricted_From_Shop
        volunteer = m.NonMember_Volunteer

    # Were any records found?
    if row == 0:
        response_body = {
        "status" :"Not Found"
        }
        res = make_response(jsonify(response_body),200)
        return(res)
        
    # Member record was found    
    
    # Is member restricted?
    if restricted:
        response_body = {
            "status": "Restricted",
            "memberName": memberName,
            "reason": reasonRestricted
        }
        res = make_response(jsonify(response_body),200) 
        return(res)

    # Is member certified?
    if shopNumber == '1' and not certified1 :
        response_body = {
        "status" :"Not Certified",
        "msg": "Not certified for ROLLING ACRES"
        }
        res = make_response(jsonify(response_body),200)
        return(res)
           
    if shopNumber == '2' and not certified2 :
        response_body = {
        "status" :"Not Certified",
        "msg": "Not certified for BROWNWOOD"
        }
        res = make_response(jsonify(response_body),200)
        return(res)
    
    # Member, or volunteer is not restricted so may be checked in/out
    if not restricted:
        # Retrieve today's check in record for this member
        #sqlActivity = """SELECT Type_Of_Work FROM tblMember_Activity WHERE memberID = '"" + villageID + '''"""
        sqlCheckInRecord = """SELECT ID, Member_ID, Check_In_Date_Time, Check_Out_Date_Time, Type_Of_Work
            FROM tblMember_Activity 
            WHERE Member_ID = '""" + villageID + """' AND Check_Out_Date_Time Is Null 
            AND Check_In_Date_Time >= CAST (GETDATE() as DATE) """
            #AND Format(Check_In_Date_Time,'mm/dd/yyyy') >= Format(CAST (GETDATE() as DATE),'mm/dd/yyyy') """  

       # Look for current checkin in the table tblMember_Activity
        memberCheckedIn = False 
        typeOfWorkAtCheckIn=""
        activity = db.engine.execute(sqlCheckInRecord)
        for a in activity:
            recordID = a.ID
            typeOfWorkAtCheckIn = a.Type_Of_Work
            checkInTime = a.Check_In_Date_Time
            memberCheckedIn = True

        #Is member checked in?
        if not memberCheckedIn:
            processCheckIn(villageID,typeOfWorkToUse,shopNumber)
            response_body = {
                "status": "Check In",
                "memberName": memberName,
                "checkInTime":datetime.datetime.now().strftime('%I:%M %p'),
                "typeOfWork": typeOfWorkToUse
            }
            res = make_response(jsonify(response_body),200)
            return(res)
        else:
            processCheckOut(recordID)
            response_body = {
                "status": "Check Out",
                "memberName": memberName,
                "checkInTime": checkInTime.strftime('%I:%M %p'),
                "checkOutTime":datetime.datetime.now().strftime('%I:%M %p'),
                "typeOfWork": typeOfWorkAtCheckIn
            }
            res = make_response(jsonify(response_body),200)
            return(res)

    # If no condition is met return the following -
    response_body = {
        "status" :"Error"
    }
    res = make_response(jsonify(response_body),200)
    return(res)

def processCheckIn(villageID,typeOfWork,shopNumber):
    checkInDateTime = datetime.datetime.now().strftime("%d/%m/%y %I:%M %p")
    #sqlInsert = """INSERT INTO tblMember_Activity (Member_ID,Check_In_Date_Time,Type_Of_Work,Door_Used,Shop_Number) VALUES ('"""
    #+ villageID + """', '""" + checkInDateTime + """', '""" + typeOfWork + """','FRONT', """ + str(shopNumber) + """)"""
    #print (sqlInsert)   
    try:
        activity = MemberActivity(Member_ID=villageID,Check_In_Date_Time=checkInDateTime,Type_Of_Work=typeOfWork,Shop_Number=int(shopNumber),Door_Used='Front')
        db.session.add(activity)
        db.session.commit()
        flash("Check in added successfully.","success")
        return 
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        db.session.rollback()
        return 
    return

def processCheckOut(recordID):
    checkOutDateTime = date.today().strftime("%d/%m/%y %I:%M %p")
    try:
        activity = db.session.query(MemberActivity).filter(MemberActivity.ID == recordID).one()
        activity.Check_Out_Date_Time = checkOutDateTime
        db.session.commit()
        return
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        db.session.rollback()
        flash("Check out could not be completed.\n"+error,"danger")
        return