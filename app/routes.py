# routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify, json, make_response, session
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import ShopName, Member , MemberActivity
from app import app
from app import db
from sqlalchemy import func, case, desc, extract, select, update
from sqlalchemy.exc import SQLAlchemyError 
import datetime
from datetime import date

# MUST HAVE A SHOP ID IN A SESSION COOKIE NAMED SHOPID
@app.before_request
def before_request_func():
    shopID = request.cookies.get('SHOPID')
    if request.path != "/setCookie" and shopID == None:
        return render_template('shopLocation.html')

    if request.path == "/setCookie" and shopID == None:
        return redirect(url_for(setCookie))


@app.route("/setCookie", methods = ['POST'])
def setCookie():
    if request.method == 'POST':
        shopID = request.form['shopList']
        #session['SHOPID'] = shopID
        resp = make_response('Setting cookie for current shop.')
        resp.set_cookie('SHOPID', shopID, max_age=60*60*24*365*2)
        return redirect (url_for('workersInShop'))
    else:
        res = make_response("Value of cookie SHOPID is {}".format(request.cookies.get('SHOPID')))
    return resp
        #return('Session cookie set to -' + shopID)
    #return redirect (url_for('workersInShop'))

@app.route("/")
@app.route("/workersInShop",methods=['GET','POST'])
def workersInShop():
    shopID = request.cookies.get('SHOPID')
    print ("Current shop location is - " + shopID)
   #if shopID = None
   #     return render_template("shopLocation.html")

    todaysDate = date.today()

    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
     format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
            FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID 
            WHERE Check_Out_Date_Time Is Null 
            AND Cast(Check_In_Date_Time as DATE) >= '""" + str(todaysDate) + """'"""
    print(sqlCheckInRecord)
    workersInShop = db.engine.execute(sqlCheckInRecord)
    
#     for w in workersInShop:
#         #recordID = w.ID
#         typeOfWorkAtCheckIn = w.Type_Of_Work
#         checkInTime = w.Check_In_Date_Time
#         memberCheckedIn = True
#         print (w.memberName, w.Check_In_Date_Time, w.Check_Out_Date_Time, w.Emergency_Contact)            
        
    return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopID)
