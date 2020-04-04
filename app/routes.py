# routes.py

from flask import session, render_template, flash, redirect, url_for, request, jsonify, json, make_response
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import ShopName, Member , MemberActivity
from app import app
from app import db
from app import ma
from sqlalchemy import func, case, desc, extract, select, update
from sqlalchemy.exc import SQLAlchemyError
#from datatables import ColumnDT
from flask_marshmallow import Marshmallow
import datetime
from datetime import date, timedelta

#ma = Marshmallow(app)

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

# @app.before_request
# def before_request():
#     # When you import jinja2 macros, they get cached which is annoying for local
#     # development, so wipe the cache every request.
#     if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
#         app.jinja_env.cache = {}
#@app.route("/")
@app.route('/index')
def index():
    data = {
        "data": [
            {
                "name": "Abbot, Jim",
                "checkInTime": "08:30 am"
            },
            {
                "name": "Smith, Sara",
                "checkInTime": "08:00 am"
            }]
    }
    print(type(data))
    member = Member.query.limit(5).all()
    for m in member:
        print(m.fullName, m.Member_ID)
    return m.fullName
    #jsonStr = json.dumps(member.__dict__)
    #print(jsonStr)
    #return jsonStr
    #member_schema = MemberSchema(many=true)
    #output = member_schema.dump(member).data
    #return jsonify({'member' : output})

    #return render_template('index.html')

@app.route('/index_get_data')
def stuff():
    # NOT A POST REQUEST        
    shopIDcookieValue = ""
    shopIDcookieValue =  request.cookies.get('SHOPID')
    todaysDate = datetime.date(2019,3,22)
    tomorrow = todaysDate + timedelta(days=1)
    # BUILD DEFAULT SQL STATEMENT USED ON FIRST DISPLAY OF THE PAGE
    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
     format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
            Check_In_Date_Time, Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
            FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID """
            #WHERE Cast(Check_In_Date_Time as DATE) >= '""" + str(todaysDate) + """' and Cast(Check_In_Date_Time as DATE) < '""" + str(tomorrow) + "'"""
            #+ """' AND Check_Out_Date_Time Is Null ORDER BY Last_Name, First_Name"""
    
    whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' AND Check_Out_Date_Time Is Null"
    sqlCheckInRecord += whereClause

    sortOrderClause = ' order by last_name, first_name'
    sqlCheckInRecord += sortOrderClause

    #print (sqlCheckInRecord)

    # EXECUTE THE SQL STATEMENT
    workersInShop = db.engine.execute(sqlCheckInRecord)

    # print(type(workersInShop))
    # shopArray=[]
    # shopArray=workersInShop
    # print(shopArray)
    # print(workersInShop)
    # #data = workersInShop
    data = {
        "data": [
            {
                "name": "Abbot, Jim",
                "checkInTime": "08:30 am"
            },
            {
                "name": "Smith, Sara",
                "checkInTime": "08:00 am"
            }]
    }
    print (type(data))
    #columns=[
    #     ColumnDT(Member.Last_Name),
    #     ColumnDT(MemberActivity.Check_In_Date_Time)
    # ]

    #query = db.session.query().\
    #   select(Member).\
    #       join(MemberActivity)

    #rowTable = datatables(request.GET, workersInShop, columns)
    #return rowTable.output_result()

    #print ("Data - " + data)
    #return jsonify(data)
    #return jsonify(workersInShop)
    #return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)


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
    

@app.route("/test")
def test():
    #print(Member.join(MemberActivity))
    #records = db.session.query(MemberActivity.Member_ID,MemberActivity.Check_In_Date_Time,MemberActivity.Check_Out_Date_Time,MemberActivity.Type_Of_Work).filter(MemberActivity.Member_ID=='604875').all()
    #records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).filter(MemberActivity.Member_ID == '604875')
    #records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).all()
    #records = db.session.query(Member).join(MemberActivity, Member.Member_ID == MemberActivity.Member_ID).filter(MemberActivity.Member_ID == '604875').all()
    records = db.session.query(MemberActivity).\
        join(Member, Member.Member_ID == MemberActivity.Member_ID).all()
    for r in records:
        recordObject = {'name': r.Last_Name,
            'checkInTime': record.Check_In_Date_Time}
        print(recordObject)
        #for a in r.MemberActivity:
        #print (r.Member_ID, r.Last_Name)
        # recordObject = {'name': record.memberName,
        #     'checkIn': record.Check_In_Date_Time,
        #     'checkOut': record.Check_Out_Date_Time}
        # print(recordObject)
    return redirect(url_for('workersInShop'))


@app.route("/workersInShop",methods=['GET','POST'])
def workersInShop():
    # USING A FIXED DATE FOR TESTING
    todaysDate = datetime.date(2019,3,22)
    tomorrow = todaysDate + timedelta(days=1)
    #print (tomorrow)

    # PROCESS POST REQUEST
    if request.method == 'POST':
        # RETRIEVE OPTIONS SELECTED BY USER
        #displayOptions = request.get_json(force=True)
        # shopChoice = displayOptions[0]
        # inShop = displayOptions[1]
        # orderBy = displayOptions[2]
        # filterOption = displayOptions[3]
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print (key,":",value)
        
        #shopChoice = request.form['shopChoice']
        shopChoice='RA'
        inShop='InShopToday'
        orderBy='OrderByCheckInTime'
        filterOption='All'
        # BUILD INITIAL WHERE CLAUSE TO SELECT TODAY'S ACTIVITY RECORDS
        whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' and"
        # ADD OPTIONS TO WHERE CLAUSE
        if shopChoice == 'RA':
            shopID = 1
            whereClause += ' Shop_Number = 1 and'
        if shopChoice == 'BW':
            shopID = 2
            whereClause += ' Shop_Number = 2 and'
        
        if inShop == 'InShopNow':
            whereClause += ' Check_out_Date_Time is null and'
        
        if filterOption == 'Defibrillator':
            whereClause += ' Definrillator_Trained'

        if filterOption == 'President':
            whereClause += ' President_VP'

        # IF WHERE CLAUSE ENDS WITH 'AND' REMOVE THE 'AND'
        if whereClause[-3:] == 'and':
            whereClause = whereClause[0:-4]

        # BUILD THE ORDER BY CLAUSE
        if orderBy == 'OrderByCheckInTime':
            sortOrderClause = ' order by Check_In_Date_Time'
        else:
            sortOrderClause = ' order by last_name, first_name'

        # BUILD MAIN QUERY
        sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
        format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
                FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 
        # ADD THE WHERE CLAUSE TO THE MAIN QUERY        
        sqlCheckInRecord += whereClause
        # ADD THE ORDER BY CLAUSE TO THE MAIN QUERY 
        sqlCheckInRecord += sortOrderClause
                
        #print (sqlCheckInRecord)
        # EXECUTE THE SQL STATEMENT
        workersInShop = None
        workersInShop = db.engine.execute(sqlCheckInRecord)

        # GET THE SHOP ID COOKIE
        shopIDcookieValue = ""
        shopIDcookieValue =  request.cookies.get('SHOPID')
        # for w in workersInShop:
        #     print (w.memberName, w.CheckInTime)
        return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
        #return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
        # END OF POST REQUEST



    # NOT A POST REQUEST        
    shopIDcookieValue = ""
    shopIDcookieValue =  request.cookies.get('SHOPID')
    
    # BUILD DEFAULT SQL STATEMENT USED ON FIRST DISPLAY OF THE PAGE
    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
     format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
            Check_In_Date_Time, Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
            FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID """
            #WHERE Cast(Check_In_Date_Time as DATE) >= '""" + str(todaysDate) + """' and Cast(Check_In_Date_Time as DATE) < '""" + str(tomorrow) + "'"""
            #+ """' AND Check_Out_Date_Time Is Null ORDER BY Last_Name, First_Name"""
    
    whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' AND Check_Out_Date_Time Is Null"
    sqlCheckInRecord += whereClause

    sortOrderClause = ' order by last_name, first_name'
    sqlCheckInRecord += sortOrderClause

    #print (sqlCheckInRecord)

    # EXECUTE THE SQL STATEMENT
    workersInShop = db.engine.execute(sqlCheckInRecord)
      
    #return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
    return render_template("workersInShop.html")



@app.route("/workersInShopPOST",methods=['GET','POST'])
def workersInShopPOST():
    # USING A FIXED DATE FOR TESTING
    todaysDate = datetime.date(2019,3,22)
    tomorrow = todaysDate + timedelta(days=1)
    #print (tomorrow)

    # PROCESS POST REQUEST
    if request.method == 'POST':
        # RETRIEVE OPTIONS SELECTED BY USER
        # displayOptions = request.get_json(force=True)
        # shopChoice = displayOptions[0]
        # inShop = displayOptions[1]
        # orderBy = displayOptions[2]
        # filterOption = displayOptions[3]
        shopChoice='RA'
        inShop='InShopToday'
        orderBY='OrderByCheckInTime'
        # BUILD INITIAL WHERE CLAUSE TO SELECT TODAY'S ACTIVITY RECORDS
        whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' and"
        # ADD OPTIONS TO WHERE CLAUSE
        if shopChoice == 'RA':
            shopID = 1
            whereClause += ' Shop_Number = 1 and'
        if shopChoice == 'BW':
            shopID = 2
            whereClause += ' Shop_Number = 2 and'
        
        if inShop == 'InShopNow':
            whereClause += ' Check_out_Date_Time is null and'
        
        if filterOption == 'Defibrillator':
            whereClause += ' efinrillator_Trained'

        if filterOption == 'President':
            whereClause += ' President_VP'

        # IF WHERE CLAUSE ENDS WITH 'AND' REMOVE THE 'AND'
        if whereClause[-3:] == 'and':
            whereClause = whereClause[0:-4]

        # BUILD THE ORDER BY CLAUSE
        if orderBy == 'OrderByCheckInTime':
            sortOrderClause = ' order by Check_In_Date_Time'
        else:
            sortOrderClause = ' order by last_name, first_name'

        # BUILD MAIN QUERY
        sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
        format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
                FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 
        # ADD THE WHERE CLAUSE TO THE MAIN QUERY        
        sqlCheckInRecord += whereClause
        # ADD THE ORDER BY CLAUSE TO THE MAIN QUERY 
        sqlCheckInRecord += sortOrderClause
                
        #print (sqlCheckInRecord)
        # EXECUTE THE SQL STATEMENT
        workersInShop = None
        workersInShop = db.engine.execute(sqlCheckInRecord)

        # GET THE SHOP ID COOKIE
        shopIDcookieValue = ""
        shopIDcookieValue =  request.cookies.get('SHOPID')
        #for w in workersInShop:
        #   print (w.memberName, w.CheckInTime)
        return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
        #return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
        # END OF POST REQUEST




#--------------------------------------------------------------------------------------------------------------------
#@app.route("/workersInShopGET/<string:options>/",methods=['GET'])
@app.route("/workersInShopGET",methods=['GET'])
def workersInShopGET(options):
    print (options)

    # USING A FIXED DATE FOR TESTING
    todaysDate = datetime.date(2019,3,22)
    tomorrow = todaysDate + timedelta(days=1)
    #print (tomorrow)

    # PROCESS POST REQUEST
    #if request.method == 'POST':
    # RETRIEVE OPTIONS SELECTED BY USER
    #displayOptions = request.get_json(force=True)
    shopChoice = displayOptions[0]
    inShop = displayOptions[1]
    orderBy = displayOptions[2]
    filterOption = displayOptions[3]
    
    # BUILD INITIAL WHERE CLAUSE TO SELECT TODAY'S ACTIVITY RECORDS
    whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' and"
    # ADD OPTIONS TO WHERE CLAUSE
    if shopChoice == 'RA':
        shopID = 1
        whereClause += ' Shop_Number = 1 and'
    if shopChoice == 'BW':
        shopID = 2
        whereClause += ' Shop_Number = 2 and'
    
    if inShop == 'InShopNow':
        whereClause += ' Check_out_Date_Time is null and'
    
    if filterOption == 'Defibrillator':
        whereClause += ' efinrillator_Trained'

    if filterOption == 'President':
        whereClause += ' President_VP'

    # IF WHERE CLAUSE ENDS WITH 'AND' REMOVE THE 'AND'
    if whereClause[-3:] == 'and':
        whereClause = whereClause[0:-4]

    # BUILD THE ORDER BY CLAUSE
    if orderBy == 'OrderByCheckInTime':
        sortOrderClause = ' order by Check_In_Date_Time'
    else:
        sortOrderClause = ' order by last_name, first_name'

    # BUILD MAIN QUERY
    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
    format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor
            FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 
    # ADD THE WHERE CLAUSE TO THE MAIN QUERY        
    sqlCheckInRecord += whereClause
    # ADD THE ORDER BY CLAUSE TO THE MAIN QUERY 
    sqlCheckInRecord += sortOrderClause
            
    #print (sqlCheckInRecord)
    # EXECUTE THE SQL STATEMENT
    workersInShop = None
    workersInShop = db.engine.execute(sqlCheckInRecord)

    # GET THE SHOP ID COOKIE
    shopIDcookieValue = ""
    shopIDcookieValue =  request.cookies.get('SHOPID')
    # for w in workersInShop:
    #     print (w.memberName, w.CheckInTime)
    return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
    #return render_template("workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)
    # END OF POST REQUEST


