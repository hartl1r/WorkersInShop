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
from datetime import date, timedelta
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
    #return render_template(workersInShop.html",workersInShop=workersInShop,shopID=shopIDcookieValue)


#@app.route("/")
# @app.route("/setCookie", methods = ['POST'])
# def setCookie():
#     if request.method == 'POST':
#         shopIDentered = request.form['shopList']
#         # CREATE A COOKIE NAMED 'SHOPID'
#         resp = make_response('Setting cookie for current shop.')
#         resp.set_cookie('SHOPID', shopIDentered, max_age=60*60*24*365*2)
#         return resp
    
    
#     # IS THERE A COOKIE NAMED 'SHOPID'?
#     shopID = request.cookies.get('SHOPID')
#     if shopID is None:
#         return render_template("shopLocation.html")
#     else:
#         return redirect (url_for(':workersInShop'))
    

# ORM APPROACH (FOREIGN KEY NOT WORKING)
# @app.route("/test")
# def test():
#     records = db.session.query(MemberActivity).\
#         join(Member, Member.Member_ID == MemberActivity.Member_ID).all()
#     for r in records:
#         recordObject = {'name': r.Last_Name,
#             'checkInTime': record.Check_In_Date_Time}
#         print(recordObject)
#         #for a in r.MemberActivity:
#         #print (r.Member_ID, r.Last_Name)
#         # recordObject = {'name': record.memberName,
#         #     'checkIn': record.Check_In_Date_Time,
#         #     'checkOut': record.Check_Out_Date_Time}
#         # print(recordObject)
#     return redirect(url_for(':workersInShop'))

@app.route("/")
@app.route("/workersInShop",methods=['GET','POST'])
def workersInShop():
    #print('/workersInShop request method - ', request.method)
    
    # USING A FIXED DATE FOR TESTING
    todaysDate = datetime.date(2019,3,22)

    tomorrow = todaysDate + timedelta(days=1)

    # PROCESS POST REQUEST
    if request.method == 'POST':
        # RETRIEVE OPTIONS SELECTED BY USER
        # NAMES OF OPTIONS
        shopChoiceSelected = request.form['shopChoiceOPT']
        inShopSelected=request.form['inShopOPT'] 
        orderBySelected=request.form['orderByOPT'] 
        filterOptionSelected=request.form['filterOptionOPT']
        
        # SELECT STATEMENT PHRASES, E.G., 'order by Last_Name, First_Name'
        shopChoice = request.form['shopChoiceItem']# SHOP_NUMBER = 1
        inShop=request.form['inShopItem'] #'InShopToday'
        orderBy=request.form['orderByItem'] #'OrderByCheckInTime'
        filterOption=request.form['filterItem'] #'All'

        # BUILD INITIAL WHERE CLAUSE TO SELECT TODAY'S ACTIVITY RECORDS
        whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "' and"
        whereClause += ' ' + shopChoice
        if (len(whereClause) > 6) & (whereClause[-4:] != 'and '):
            whereClause += ' and '

        whereClause += inShop
        
        if whereClause[-4:] != 'and ':
            whereClause += ' and '

        if len(filterOption) > 0:
            whereClause += filterOption
        
        if whereClause[-4:] == 'and ':
            whereClause = whereClause[0:-5]
        
        # BUILD MAIN QUERY
        sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
        format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
                    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor, Defibrillator_Trained, 
                    isPresident, isVP, canSellLumber, canSellMdse, Maintenance, isBODmember, isSafetyCommittee,
                    isSpecialProjects, isAskMe
                FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 

        
        # REMOVE 'AND' IF IT EXISTS
        if whereClause[-4:] == 'and ':
            whereClause = whereClause[0:-5]

        # ADD THE WHERE CLAUSE TO THE MAIN QUERY        
        sqlCheckInRecord += whereClause

        # ADD THE ORDER BY CLAUSE TO THE MAIN QUERY 
        sqlCheckInRecord += ' ' + orderBy        
        
        # EXECUTE THE SQL STATEMENT
        workersInShop = None
        workersInShop = db.engine.execute(sqlCheckInRecord)
        workersInShopArray = []
        workersInShopItem=''

        for w in workersInShop:
            workersInShopItem = {'name':w.memberName,
                'checkIn':w.CheckInTime,
                'checkOut':w.CheckOutTime,
                'typeOfWork':w.Type_Of_Work,
                'emergName':w.Emerg_Name,
                'emergPhone':w.Emerg_Phone,
                'shopNumber':w.Shop_Number,
                'doorUsed':w.Door_Used,
                'mentor':w.Mentor,
                'defibrillatorTrained':w.Defibrillator_Trained,
                'isPresident':w.isPresident,
                'isVP':w.isVP,
                'canSellLumber':w.canSellLumber,
                'canSellMdse':w.canSellMdse,'maintenance':w.Maintenance,'isBODmember':w.isBODmember,'isSafetyCommittee':w.isSafetyCommittee,
                'isSpecialProjects':w.isSpecialProjects,'isAskMe':w.isAskMe}
            workersInShopArray.append(workersInShopItem)
        
        # for w in workersInShop:
        #     print (w.memberName,w.Member_ID,w.CheckInTime,w.CheckOutTime)
        return render_template("workersInShop.html",workersInShopArray=workersInShopArray,shopChoice=shopChoiceSelected,\
        inShop=inShopSelected,orderBy=orderBySelected,filterOption=filterOptionSelected,requestMethod='POST')
        
        # END OF POST REQUEST



    # GET REQUEST (NOT A POST REQUEST)        
    shopChoiceCookie = request.cookies.get('SHOPID')
    shopChoice = 'showBoth'
    if shopChoiceCookie == 'showRA':
        shopChoice='showRA'
    if shopChoiceCookie == 'showBW':
        shopChoice='showBW'
    
    inShop="inShopNow"
    orderBy="orderByName"
    filterOption="Everyone"
    
    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
    format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor, Defibrillator_Trained, 
    isPresident, isVP, canSellLumber, canSellMdse, Maintenance, isBODmember, isSafetyCommittee,
    isSpecialProjects, isAskMe
    FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 
    
    whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "'"
    sqlCheckInRecord += whereClause
    
    print (sqlCheckInRecord)
    
    workersInShop = None
    workersInShop = db.engine.execute(sqlCheckInRecord)
    workersInShopArray = []
    workersInShopItem=''

    for w in workersInShop:
        workersInShopItem = {'name':w.memberName,
            'checkIn':w.CheckInTime,
            'checkOut':w.CheckOutTime,
            'typeOfWork':w.Type_Of_Work,
            'emergName':w.Emerg_Name,
            'emergPhone':w.Emerg_Phone,
            'shopNumber':w.Shop_Number,
            'doorUsed':w.Door_Used,
            'mentor':w.Mentor,
            'defibrillatorTrained':w.Defibrillator_Trained,
            'isPresident':w.isPresident,
            'isVP':w.isVP,
            'canSellLumber':w.canSellLumber,
            'canSellMdse':w.canSellMdse,'maintenance':w.Maintenance,'isBODmember':w.isBODmember,'isSafetyCommittee':w.isSafetyCommittee,
            'isSpecialProjects':w.isSpecialProjects,'isAskMe':w.isAskMe}
        workersInShopArray.append(workersInShopItem)
    
    return render_template("workersInShop.html",workersInShopArray=workersInShopArray,shopChoice=shopChoice,\
    inShop=inShop,orderBy=orderBy,filterOption=filterOption)
    #return render_template(workersInShop.html",shopChoice=shopChoice,inShop=inShop,orderBy=orderBy,filterOption=filterOption,requestMethod='GET')


