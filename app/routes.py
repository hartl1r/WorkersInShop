# routes.py

from flask import session, render_template, flash, redirect, url_for, request, jsonify, json, make_response
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
# @app.before_first_request
# def before_request_func():
#     shopID = request.cookies.get('SHOPID')
#     print("shopID - " + str(shopID))
#     print("Request.path - " + request.path)
#     #if request.path != "/setCookie" and shopID == None:
#     if shopID == None:
#         return render_template('shopLocation.html')
#     else:
#     #if request.path == "/setCookie" and shopID == None:
#         resp = make_response('Setting cookie for current shop.')
#         resp.set_cookie('SHOPID', shopID, max_age=60*60*24*365*2)
#         return redirect (url_for('workersInShop'))
#         #return redirect(url_for(setCookie))

@app.route("/")
@app.route("/setCookie", methods = ['POST'])
def setCookie():
    if request.method == 'POST':
        shopIDentered = request.form['shopList']
        # CREATE A COOKIE NAMED 'SHOPID'
        resp = make_response('Setting cookie for current shop.')
        resp.set_cookie('SHOPID', shopIDentered, max_age=60*60*24*365*2)
        return resp
        #return redirect (url_for('workersInShop'))
    
    # IS THERE A COOKIE NAMED 'SHOPID'?
    shopID = request.cookies.get('SHOPID')
    if shopID is None:
        return render_template("shopLocation.html")
    else:
        return redirect (url_for('workersInShop'))
    #else:
    #    resp = make_response("Value of cookie SHOPID is {}".format(request.cookies.get('SHOPID')))
    #return resp
        #return('Session cookie set to -' + shopID)d
        
    #return redirect (url_for('workersInShop'))
    #return render_template("shopLocation.html")
@app.route("/test")
def test():
    #print(Member.join(MemberActivity))
    #records = db.session.query(MemberActivity.Member_ID,MemberActivity.Check_In_Date_Time,MemberActivity.Check_Out_Date_Time,MemberActivity.Type_Of_Work).filter(MemberActivity.Member_ID=='604875').all()
    #records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).filter(MemberActivity.Member_ID == '604875')
    #records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).all()
    records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).filter(MemberActivity.Member_ID == '604875').all()

    for r in records:
        #for a in r.MemberActivity:
        print (r.Member_ID, r.Last_Name)
        # recordObject = {'name': record.memberName,
        #     'checkIn': record.Check_In_Date_Time,
        #     'checkOut': record.Check_Out_Date_Time}
        # print(recordObject)
    return redirect(url_for('workersInShop'))
@app.route("/workersInShop",methods=['GET','POST'])
def workersInShop():
    todaysDate = datetime.date(2019,3,22)
    # PROCESS POST REQUEST
    if request.method == 'POST':
        displayOptions = request.get_json(force=True)
        print (type(displayOptions))
        #displayOptions = request.json
        shopChoice = displayOptions[0]
        inShop = displayOptions[1]
        orderBy = displayOptions[2]
        filterOption = displayOptions[3]
        print(str(displayOptions))
        #return 'OK', 200
        # BUILD WHERE CLAUSE
        whereClause = "Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and"

        if shopChoice == 'RA':
            shopID = 1
            whereClause += ' Shop_Number = 1 and'
        if shopChoice == 'BW':
            shopID = 2
            whereClause += ' Shop_Number = 2 and'
        
        if inShop == 'InShopNow':
            whereClause += ' Check_out_Date_Time is null and'


        
        if filterOption == 'Defibrillator':
            whereClause += 'Definrillator_Trained'

        if filterOption == 'President':
            whereClause += 'President_VP'

        #right3 = slice(-3)
        if whereClause[-3:] == 'and':
            #lengthOfWhere = len(whereClause)
            #slce = slice(0,lengthOfWhere-3)
        #    remove last 3 characters
            whereClause = whereClause[0:-4]

        print (whereClause)

        sortOrderClause = ''
        if orderBy == 'OrderByName':
            sortOrderClause = 'order by last_name, first_name'

        if orderBy == 'OrderByCheckInTime':
            sortOrderClause = 'order by Check_In_Date_Time'
        
        print (sortOrderClause)
        # optionArray = request.data
        # print ("Options received - " + str(optionArray))

        # # BUILD FILTER

        # BUILD QUERY
        sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
        format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
                FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID
                ORDER BY Last_Name, First_Name""" 
                
        #sqlCheckInRecord += " where " + whereClause 
        #sqlCheckInRecord += " " + sortOrderClause
                
                #WHERE Check_Out_Date_Time Is Null 
                #AND Cast(Check_In_Date_Time as DATE) >= '""" + str(todaysDate) + """'"""
        print(sqlCheckInRecord)
        ##f.write(sqlCheckInRecord)
        #print (sqlCheckInRecord,f)
        #f.close

        workersInShop = db.engine.execute(sqlCheckInRecord)

        #for w in workersInShop:
        #    print (w.memberName, w.CheckInTime, w.CheckOutTime)           
            

        return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopID)




    # NOT A POST REQUEST        
    shopIDcookieValue = ""
    shopIDcookieValue =  request.cookies.get('SHOPID')
    if shopIDcookieValue is None:
        print ("The SHOPID cookie is missing; RA assumed")
        shopIDcookieValue = 'RA'
    else:
        print ("Current shop is " + shopIDcookieValue)

    
    #print ("Date to use - " + str(todaysDate))
    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
     format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
            FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID 
            WHERE Check_Out_Date_Time Is Null 
            AND Cast(Check_In_Date_Time as DATE) >= '""" + str(todaysDate) + """' 
            ORDER BY Last_Name, First_Name"""
    #print(sqlCheckInRecord)
    workersInShop = db.engine.execute(sqlCheckInRecord)
    # print (type(workersInShop))
    # x = workersInShop.filter(Shop_Number = 2)
    # print (type(x))

    # for w in workersInShop:
    #     #recordID = w.ID
    #     typeOfWorkAtCheckIn = w.Type_Of_Work
    #     checkInTime = w.CheckInTime
    #     memberCheckedIn = True
    #     print (w.memberName, w.CheckInTime, w.CheckOutTime)           
        
    return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
