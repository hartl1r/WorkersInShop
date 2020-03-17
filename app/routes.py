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
    shop = request.cookies.get('shopAbbr')
    # IF NO COOKIE IS FOUND, PROMPT FOR SHOP ABBREVIATION
    if shop == None:
        return render_template("index.html")
        #return render_template("index.html")
    # IF A COOKIE IS FOUND, SAVE THE SHOP ABBR AND OPEN THE WORKERSINSHOP PAGE
    if shop == 'RA':
        shopName = 'Rolling Acres'
    elif shop == 'BW':
        shopName = 'Brownwood'
    
    # SAVE SHOP ABBREVIATION IN A SESSION VARIABLE ???
    return redirect (url_for('workersInShop',shop=shop))
  #  return redirect(url_for('trainingClass',id=trainingClassID))

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        shopAbbrInput = request.form['shopAbbr']
        resp = make_response('Setting cookie for current shop.')
        resp.set_cookie('shopAbbr', shopAbbrInput)
        # SAVE SHOP ABBREVIATION IN A SESSION VARIABLE ???
        return redirect (url_for('workersInShop',shop=shop))


@app.route('/getcookie')
def getcookie():
    shop = request.cookies.get('shopAbbr')
    if shop == 'RA':
        shopName = 'Rolling Acres'
    elif shop == 'BW':
        shopName = 'Brownwood'
    else:
        shopName = 'Not specified'
        
    return '<h1>Welcome to ' +shopName+'</h1>'      

@app.route("/workersInShop/<string:shop>/",methods=['GET','POST'])
def workersInShop(shop):
    todaysDate = date.today()

    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
     format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, isMentor
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
        
    return render_template("workersInShop.html",workersInShop=workersInShop,shop=shop)
