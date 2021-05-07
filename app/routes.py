# routes.py

from flask import session, render_template, flash, redirect, url_for, request, jsonify, json, make_response
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import ControlVariables, ShopName, Member , MemberActivity, MonitorSchedule, CoordinatorsSchedule
from app import app
from app import db

from sqlalchemy import func, case, desc, extract, select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError
from sqlalchemy.sql import text as SQLQuery

import datetime
from datetime import date, timedelta
from pytz import timezone

@app.route("/")
@app.route('/index')
@app.route('/index/')
@app.route("/workersInShop",methods=['GET','POST'])
def workersInShop():
    # GET STAFF ID
    staffID = getStaffID()

    # GET DEFAULT SHOP ID
    shopID = getShopID()
    
    #print('shopID - ',shopID)

    # USING CURRENT DATE FOR PRODUCTION
    todaysDate = date.today()
    displayDate = todaysDate.strftime('%-b %-d, %Y')
    tomorrow = todaysDate + timedelta(days=1)
    
    # PROCESS POST REQUEST
    if request.method == 'POST':
        # RETRIEVE OPTIONS SELECTED BY USER
        # NAMES OF OPTIONS
        shopChoiceSelected = request.form['shopChoiceOPT']
        inShopSelected=request.form['inShopOPT'] 
        orderBySelected=request.form['orderByOPT'] 
        filterOptionSelected=request.form['filterOptionOPT']

        # print('shopChoiceSelected - ',shopChoiceSelected)
        # print('inShopSelected - ',inShopSelected)
        # print('orderBySelected - ',orderBySelected)
        # print('filterOptionSelected - ',filterOptionSelected)

        # SELECT STATEMENT PHRASES, E.G., 'order by Last_Name, First_Name'
        if (shopChoiceSelected == 'RA'):
            shopChoice = ' Shop_Number = 1'
        else:
            if (shopChoiceSelected == 'BW'):
                shopChoice = ' Shop_Number = 2'
            else:
                shopChoice = ''

        inShop=request.form['inShopItem'] #'InShopToday'
        orderBy=request.form['orderByItem'] #'OrderByCheckInTime'
        filterOption=request.form['filterItem'] #'All'

        # print('inShop - ',inShop)
        # print('orderBy - ',orderBy)
        # print('filterOption - ',filterOption)
        
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
        sqlCheckInRecord =  "SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID as memberID, "
        sqlCheckInRecord += "format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, "
        sqlCheckInRecord += "Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime, "
        sqlCheckInRecord += "Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor, Defibrillator_Trained, "
        sqlCheckInRecord += "isPresident, isVP, canSellLumber, canSellMdse, Maintenance, isBODmember, isSafetyCommittee, "
        sqlCheckInRecord += "isSpecialProjects, isAskMe, tblMember_Activity.ID as recordID "
        sqlCheckInRecord += "FROM tblMember_Activity "
        sqlCheckInRecord += "left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 

        
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
            if (w.CheckOutTime == None or w.CheckOutTime == ''):
                checkOutTime = '_______'
            else:
                checkOutTime = w.CheckOutTime
            
            workersInShopItem = {
                'recordID':w.recordID,
                'memberID':w.memberID,
                'name':w.memberName,
                'checkIn':w.CheckInTime,
                'checkOut':checkOutTime,
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

        inShopNowCount = countMembersInShopNow(shopChoiceSelected)
        inShopTodayCount = countMembersInShopToday(shopChoiceSelected)
        
        return render_template("workersInShop.html",workersInShopArray=workersInShopArray,shopChoice=shopChoiceSelected,\
        inShop=inShopSelected,orderBy=orderBySelected,filterOption=filterOptionSelected,displayDate=displayDate,\
        inShopNowCount=inShopNowCount,inShopTodayCount=inShopTodayCount,\
        requestMethod='POST')
        
        # END OF POST REQUEST



    # GET REQUEST (NOT A POST REQUEST)        
    inShop="inShopNow"
    orderBy="orderByName"
    filterOption = "Everyone"

    sqlCheckInRecord = """SELECT (Last_Name + ', ' +  First_Name) as memberName, tblMember_Activity.Member_ID,
    format(Check_In_Date_Time,'hh:mm tt') as CheckInTime, Format(Check_Out_Date_Time,'hh:mm tt') as CheckOutTime,
    Type_Of_Work, Emerg_Name, Emerg_Phone, Shop_Number, Door_Used, Mentor, Defibrillator_Trained, 
    isPresident, isVP, canSellLumber, canSellMdse, Maintenance, isBODmember, isSafetyCommittee,
    isSpecialProjects, isAskMe, tblMember_Activity.ID as recordID 
    FROM tblMember_Activity left join tblMember_Data on tblMember_Activity.Member_ID = tblMember_Data.Member_ID""" 
    
    whereClause = " WHERE Cast(Check_In_Date_Time as DATE) >= '" + str(todaysDate) + "' and Cast(Check_In_Date_Time as DATE) < '" + str(tomorrow) + "'"
    whereClause += " and Check_Out_Date_Time is null"
    if (shopID == 'RA'):
        whereClause += " and Shop_Number = 1"
    if (shopID == 'BW'):
        whereClause += " and Shop_Number = 2"
    sqlCheckInRecord += whereClause
    
    #print(sqlCheckInRecord)


    workersInShop = None
    workersInShop = db.engine.execute(sqlCheckInRecord)
    workersInShopArray = []
    workersInShopItem=''

    for w in workersInShop:
        if (w.CheckOutTime == None or w.CheckOutTime == ''):
            checkOutTime = '-------'
        else:
            checkOutTime = w.CheckOutTime
            
        workersInShopItem = {'name':w.memberName,
            'recordID':w.recordID,
            'checkIn':w.CheckInTime,
            'checkOut':checkOutTime,
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
    
    # COUNT MEMBERS IN SHOP
    NowCount = countMembersInShopNow(shopID)
    TodayCount = countMembersInShopToday(shopID)
    
    return render_template("workersInShop.html",workersInShopArray=workersInShopArray,shopChoice=shopID,defaultShopID=shopID,\
    inShop=inShop,orderBy=orderBy,filterOption=filterOption,displayDate=displayDate,inShopNowCount=NowCount,inShopTodayCount=TodayCount)
    

@app.route("/getTodaysMonitors/")
def getTodaysMonitors():
    #print('/getTodaysMonitors')
    shopChoice=request.args.get('shopChoice')
    shopNumber = 'BOTH'
    shopName = 'Both Locations'
    if (shopChoice == 'RA'):
        shopNumber = '1'
        shopName = 'Rolling Acres'
    if (shopChoice == 'BW'):
        shopNumber = '2'
        shopName = 'Brownwood'

    # GET TODAYS DATE IN EST    
    est = timezone('US/Eastern')
    
    todaysDate = date.today()
    todays_dateSTR = todaysDate.strftime('%-m-%-d-%Y')

    # GET LAST ACCEPTABLE TRAINING DATE
    lastAcceptableTrainingDate = db.session.query(ControlVariables.Last_Acceptable_Monitor_Training_Date).filter(ControlVariables.Shop_Number == '1').scalar()

    # lastAcceptableTrainingDate = db.session.query(ControlVariables.Last_Acceptable_Monitor_Training_Date).first().scalar()
    if lastAcceptableTrainingDate == None:
        flash ('Missing Last Acceptable Training Date in Control Variables table','danger')
        return redirect(url_for('workersInShop.html'))
   
    # BUILD WHERE CLAUSE
    whereClause = " WHERE Date_Scheduled = '" + todays_dateSTR + "'"
    if (shopNumber == '1' or shopNumber == '2'):
        whereClause += " and Shop_Number = " + shopNumber
    
    sqlSelect = "SELECT tblMonitor_Schedule.ID as recordID, tblMonitor_Schedule.Member_ID as memberID, (Last_Name + ', ' +  First_Name) as memberName, "
    sqlSelect += " Home_Phone, Cell_Phone, "
    sqlSelect += "format(Last_Monitor_Training,'MM-dd-yy') as lastTrainingDateRA, cast(Last_Monitor_Training as DATE) as LastMonitorTrainingRA, "
    sqlSelect += "format(Last_Monitor_Training_Shop_2,'MM-dd-yy') as lastTrainingDateBW, cast(Last_Monitor_Training_Shop_2 as DATE) as LastMonitorTrainingBW, "
    sqlSelect += " DATEPART(year,Last_Monitor_Training) as trainingYearRA, DATEPART(year,Last_Monitor_Training_Shop_2) as trainingYearBW, "
    sqlSelect += " Date_Scheduled, AM_PM, Duty, No_Show, Shop_Number, "
    sqlSelect += " DATEPART(year,Date_Scheduled) as scheduleYear "
    sqlSelect += " FROM tblMonitor_Schedule LEFT JOIN tblMember_Data ON tblMonitor_Schedule.Member_ID = tblMember_Data.member_ID "
    sqlSelect += whereClause    
    sqlSelect += " ORDER BY Shop_Number, AM_PM, Duty,Last_Name,First_Name"
    
    todaysMonitors = db.engine.execute(sqlSelect)
    todaysMonitorsArray=[]
    todaysMonitor=''

    for m in todaysMonitors:
        
        #print(m.memberName, m.memberID, m.Shop_Number)

        # IS MONITOR CHECKED IN?  GET THE CHECK IN/OUT TIMES FOR THIS MONITOR 
        if (shopNumber == '1' or shopNumber == '2'):
            activity = db.session.query(MemberActivity)\
                .filter(MemberActivity.Member_ID == m.memberID)\
                .filter(MemberActivity.Shop_Number == shopNumber)\
                .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
                .first()
        else:
           activity = db.session.query(MemberActivity)\
                .filter(MemberActivity.Member_ID == m.memberID)\
                .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
                .first()
        if (activity == None) :
            checkInTime='--------'
            checkOutTime='--------'
        else:
            format = '%I:%M %p'
            checkInTime = activity.Check_In_Date_Time.strftime(format)
            if (activity.Check_Out_Date_Time != None and activity.Check_Out_Date_Time != ''):
                checkOutTime = activity.Check_Out_Date_Time.strftime(format)
            else:
                checkOutTime = '--------'
                
        # REFORMAT DATA AS NEEDED
        if m.Shop_Number == 1:
            shopInitials = 'RA'
        else:
            if m.Shop_Number == 2:
                shopInitials = 'BW'
            else:
                shopInitials = '--'
        
        # IS TRAINING NEEDED?
        LastMonitorTrainingDisplay=''
        trainingMsg = ''
       
        if m.Shop_Number == 1:
            if m.LastMonitorTrainingRA == None or m.LastMonitorTrainingRA == '':
                trainingMsg = 'Training Needed'
            else:
                LastMonitorTrainingDisplay = m.LastMonitorTrainingRA.strftime('%b %Y')
                if m.LastMonitorTrainingRA < lastAcceptableTrainingDate:
                    trainingMsg = 'Training Needed'
        else:
            if m.LastMonitorTrainingBW == None or m.LastMonitorTrainingBW == '':
                trainingMsg = 'Training Needed'
            else:
                LastMonitorTrainingDisplay = m.LastMonitorTrainingBW.strftime('%b %Y')
                if m.LastMonitorTrainingBW < lastAcceptableTrainingDate:
                    trainingMsg = 'Training Needed' 
        
        todaysMonitor = {'name':m.memberName + ' (' + m.memberID + ')',
            'shopInitials':shopInitials,
            'shift':m.AM_PM,
            'duty':m.Duty,
            'checkIn':checkInTime,
            'checkOut':checkOutTime,
            'noShow':m.No_Show,
            'homePhone':m.Home_Phone,
            'cellPhone':m.Cell_Phone,
            'lastTrainingDate':LastMonitorTrainingDisplay,
            'trainingNeeded':trainingMsg,
            'recordID':m.recordID}
        todaysMonitorsArray.append(todaysMonitor)
        
    # GET COORDINATOR DATA FOR BOTH SHOPS
    return jsonify(todaysMonitorsArray=todaysMonitorsArray,shopName=shopName)


@app.route('/printTodaysMonitors/<shopChoice>')
def printTodaysMonitors(shopChoice):
    shopNumber = 'BOTH'
    shopName = 'Both Locations'
    if (shopChoice == 'RA'):
        shopNumber = '1'
        shopName = 'Rolling Acres'
    if (shopChoice == 'BW'):
        shopNumber = '2'
        shopName = 'Brownwood'
    
    todaysDate = date.today()

    todays_dateSTR = todaysDate.strftime('%-m-%-d-%Y')
    hdgDate = todaysDate.strftime('%-b %-d, %Y')
   
    whereClause = " WHERE Date_Scheduled = '" + todays_dateSTR + "'"
    if (shopNumber == '1' or shopNumber == '2'):
        whereClause += " AND Shop_Number = " + shopNumber
    
    sqlSelect = "SELECT tblMonitor_Schedule.ID as recordID, tblMonitor_Schedule.Member_ID as memberID, (Last_Name + ', ' +  First_Name) as memberName, "
    sqlSelect += " Home_Phone, Cell_Phone, format(Last_Monitor_Training,'MMM yyyy') as lastTrainingDate, Last_Monitor_Training, "
    sqlSelect += " DATEPART(year,Last_Monitor_Training) as trainingYear, Date_Scheduled, AM_PM, Duty, No_Show, Shop_Number, "
    sqlSelect += " DATEPART(year,Date_Scheduled) as scheduleYear "
    sqlSelect += " FROM tblMonitor_Schedule LEFT JOIN tblMember_Data ON tblMonitor_Schedule.Member_ID = tblMember_Data.member_ID "
    sqlSelect += whereClause    
    sqlSelect += " ORDER BY Shop_Number, AM_PM, Duty,Last_Name,First_Name"
    
    todaysMonitors = db.engine.execute(sqlSelect)
    todaysMonitorsArray=[]
    todaysMonitor=''
    for m in todaysMonitors:
        # IS MONITOR CHECKED IN?  GET THE CHECK IN/OUT TIMES FOR THIS MONITOR 
        if (shopNumber == '1' or shopNumber == '2'):
            activity = db.session.query(MemberActivity)\
                .filter(MemberActivity.Member_ID == m.memberID)\
                .filter(MemberActivity.Shop_Number == shopNumber)\
                .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
                .first()
        else:
           activity = db.session.query(MemberActivity)\
                .filter(MemberActivity.Member_ID == m.memberID)\
                .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
                .first()
        if (activity == None) :
            checkInTime='--------'
            checkOutTime='--------'
        else:
            format = '%I:%M %p'
            checkInTime = activity.Check_In_Date_Time.strftime(format)
            if activity.Check_Out_Date_Time != None and activity.Check_Out_Date_Time != '':
                checkOutTime = activity.Check_Out_Date_Time.strftime(format)
            else:
                checkOutTime = '-------'
                
        # REFORMAT DATA AS NEEDED
        if m.Shop_Number == 1:
            shopInitials = 'RA'
        else:
            if m.Shop_Number == 2:
                shopInitials = 'BW'
            else:
                shopInitials = '--'
        
        # IS TRAINING NEEDED?
        if (m.trainingYear == None): # if last training year is blank
            trainingMsg = 'Training needed'
        else:
            intTrainingYear = int(m.trainingYear) +2 # int of last training year
            intScheduleYear = int(m.scheduleYear) # int of schedule year
            if (intTrainingYear <= intScheduleYear):
                trainingMsg = 'Training needed'
            else:
                trainingMsg = ''

        if (m.Last_Monitor_Training != None and m.Last_Monitor_Training != ''):
            lastTrainingDate = m.Last_Monitor_Training.strftime('%b %Y')
        else:
            lastTrainingDate = ''

        if m.No_Show == True:
            noShow = 'No Show'
        else:
            noShow = ''

        if m.Home_Phone == None:
            homePhone = ''
        else:
            homePhone = m.Home_Phone

        if m.Cell_Phone == None:
            cellPhone = ''
        else:
            cellPhone = m.Cell_Phone
    
        todaysMonitor = {'name':m.memberName,
            'memberID':m.memberID,
            'shopInitials':shopInitials,
            'shift':m.AM_PM,
            'duty':m.Duty,
            'checkIn':checkInTime,
            'checkOut':checkOutTime,
            'noShow':noShow,
            'homePhone':homePhone,
            'cellPhone':cellPhone,
            'lastTrainingDate':lastTrainingDate,
            'trainingNeeded':trainingMsg,
            'recordID':m.recordID}
        todaysMonitorsArray.append(todaysMonitor)
    
    # GET COORDINATOR DATA FOR BOTH SHOPS
    coordinatorArray=[]
    coordinator=[]
    coordinators = db.session.query(CoordinatorsSchedule)\
        .filter(CoordinatorsSchedule.Start_Date <= todaysDate)\
        .filter(CoordinatorsSchedule.End_Date >= todaysDate)
    if coordinators:
        for c in coordinators:
            shopLocation=''
            if c.Shop_Number == 1:
                shopLocation = 'Rolling Acres'
            else:
                if c.Shop_Number == 2:
                    shopLocation = 'Brownwood'
                else:
                    shopLocation = '???'
            # GET COORDINATORS NAME, PHONES, EMAIL FROM MEMBER TABLE
            coordData = db.session.query(Member).filter(Member.Member_ID==c.Coordinator_ID).first()
            if coordData:
                coordinator = {'name':coordData.fullName,
                    'cellPhone':coordData.Cell_Phone,
                    'homePhone':coordData.Home_Phone,
                    'email':coordData.eMail,
                    'shop':shopLocation}
                coordinatorArray.append(coordinator)
            else:
                flash('Missing member data for '+c.Coordinator_ID,'danger')
    else:
        coordinatorArray = []

    return render_template("rptMonitors.html",shopName=shopName,hdgDate=hdgDate,todaysMonitors=todaysMonitorsArray,coordinators=coordinatorArray)


@app.route('/checkOutMember')
def checkOutMember():
    print('/checkOutMember')
    activityID = request.args.get('recordID')
    est = timezone('US/Eastern')
    checkOutDateTime = datetime.datetime.now(est)
    
    try:
        activity = db.session.query(MemberActivity)\
            .filter(MemberActivity.ID == activityID).first()
        activity.Check_Out_Date_Time = checkOutDateTime
        db.session.commit()
        msg = "SUCCESS - member checked out."
        return jsonify(msg=msg)  
    except Exception as e:
        msg="ERROR - member NOT checked out."
        print(msg)
        return jsonify(msg=msg)
   
def countMembersInShopNow(shopID):
    todaysDate = date.today()
    # SHOP COUNTS
    if shopID == 'RA':
        # COUNT THOSE IN SHOP NOW
        inShopNowCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
            .filter(MemberActivity.Check_Out_Date_Time == None)\
            .filter(MemberActivity.Shop_Number == 1).scalar()
    elif shopID == 'BW':
        # COUNT THOSE IN SHOP NOW
        inShopNowCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
            .filter(MemberActivity.Check_Out_Date_Time == None)\
            .filter(MemberActivity.Shop_Number == 2).scalar()
    else:
        # COUNTS FOR BOTH SHOPS
        inShopNowCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
            .filter(MemberActivity.Check_Out_Date_Time == None).scalar()
    return inShopNowCount            

def countMembersInShopToday(shopID):
    todaysDate = date.today()
    if shopID == 'RA':
        # COUNT THOSE IN SHOP TODAY
        inShopTodayCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
            .filter(MemberActivity.Shop_Number == 1).scalar()
    elif shopID == 'BW':
        # COUNT THOSE IN SHOP TODAY
        inShopTodayCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate)\
            .filter(MemberActivity.Shop_Number == 2).scalar()
    else:
        # COUNTS FOR BOTH SHOPS
        inShopTodayCount = db.session.query(func.count(MemberActivity.Member_ID))\
            .filter(MemberActivity.Check_In_Date_Time >= todaysDate).scalar()
    return inShopTodayCount



@app.route('/updateNoShow')
def updateNoShow():
    recordID=request.args.get('recordID')
    noShow = request.args.get('noShow')
    # change the following to ... setNoShow_SP,  ... setNoShow_RAW,  ... setNoShow_SQLALCHEMY
    msg = setNoShow_RAW(recordID,noShow)
    return jsonify(msg=msg)
    
    
def setNoShow_RAW(recordID,noShow):
    # RAW SQL APPROACH
    memberID = db.session.query(MonitorSchedule.Member_ID).filter(MonitorSchedule.ID == recordID).scalar()
    msg = ''
    # SET 'NO SHOW' FLAG IN tblMonitor_Schedule
    try:
        if (noShow == 'True'):
            sqlUpdate = "UPDATE tblMonitor_Schedule SET No_Show = 1 WHERE ID = " + recordID
            db.engine.execute(sqlUpdate)
        else:
            sqlUpdate = "UPDATE tblMonitor_Schedule SET No_Show = 0 WHERE ID = " + recordID
            db.engine.execute(sqlUpdate)
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        error = str(e.__dict__['orig'])
        print('error - ',error)
        return error
    
    # SET RESTRICTED_FROM_SHOP FLAG IN tblMember_Data
    try:
        if (noShow == 'True'):
            sqlUpdateRestricted = "UPDATE tblMember_Data SET Restricted_From_Shop = 1 "
            sqlUpdateRestricted += "WHERE Member_ID = '" + memberID + "'"
            print(sqlUpdateRestricted)
            db.engine.execute(sqlUpdateRestricted)
            msg = "Monitor 'No Show' updated. \ńShift Opened to Add Sub."
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print('error - ',error)
        return error

    # SET RESTRICTED_FROM_SHOP_REASON IN tblMember_Data
    try:
        if (noShow == 'True'):
            # BUILD MESSAGE
            todaysDate = date.today()
            todays_dateSTR = todaysDate.strftime('%-m-%-d-%Y')
            # RETRIEVE CURRENT RESTRICTED REASONS, IF ANY
            noShowReason = "No show on " + todays_dateSTR
            reason = db.session.query(Member.Reason_For_Restricted_From_Shop).filter(Member.Member_ID == memberID).scalar()
            # EITHER INSERT OR APPEND THE NO SHOW REASON TO ANY EXISTING REASON
            if (reason == None or reason == ''):
                reason = noShowReason
            else:
                reason += noShowReason

            sqlUpdateRestrictedReason = "UPDATE tblMember_Data SET "
            sqlUpdateRestrictedReason += "Reason_For_Restricted_From_Shop = '" + reason
            sqlUpdateRestrictedReason += "' WHERE Member_ID = '" + memberID + "'"
            print(sqlUpdateRestrictedReason)
            db.engine.execute(sqlUpdateRestrictedReason)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print('error - ',error)
        return error
    
    return msg

def setNoShow_SQLALCHEMY(recordID,noShow):
    #SQLALCHEMY APPROACH
    print('SQLALCHEMY APPROACH test')
    try:
        schedule = db.session.query(MonitorSchedule)\
                    .filter(MonitorSchedule.ID == recordID).first()
        if (schedule == None):
            msg = 'ERROR - Schedule record not found.'
            return (msg)
        
        if (noShow == 'True'):  
            schedule.No_Show = True
            db.session.commit
            msg="No show updated to true."
        else:
            if (noShow == 'False'): 
                schedule.No_Show = False 
                db.session.commit
                msg = "No show set to off" 
        return (msg)
    except Exception as e:
        db.session.rollback()
        msg = "ERROR - Could not update."
        return (msg)
    


def setNoShow_SP(recordID,noShow):
    # STORED PROCEDURE APPROACH
    print('STORED PROCEDURE APPROACH test')
    if (noShow == 'True'):
        noShowValue = 1
    else:
        noShowValue = 0
    sp = "EXEC setNoShow " + str(recordID) + "," + str(noShowValue)
    print('sp - ',sp)
    sql = SQLQuery(sp)
    result = db.engine.execute(sql)
    print('result - ',result)
    msg = 'No_Show updated'
    return (msg)


def updateRestricted(memberID):
    print('updateRestricted for ',memberID)
    member = db.session.query(Member).filter(Member.Member_ID == memberID).first()
    if member:
        try:
            print('updating restricted')
            member.Restricted_From_Shop = True
            todaysDate = date.today()
            todays_dateSTR = todaysDate.strftime('%-m-%-d-%Y')
            msg = 'No Show for Monitor Duty on ' + todays_dateSTR
            member.Reason_For_Restricted_From_Shop += msg
            db.session.commit
            print('update successful')
        except Exception as e:
            db.session.rollback
            flash('Could not update restricted for No Show.','danger')
    return 

def getStaffID():
	if 'staffID' in session:
		staffID = session['staffID']
	else:
		flash('Login ID is missing, will use 604875','danger')
		staffID = '757856'
	return staffID

def getShopID():
	if 'shopID' in session:
		shopID = session['shopID']
	else:
		# SET RA FOR TESTING; SEND FLASH ERROR MESSAGE FOR PRODUCTION
		shopID = 'RA'
		msg = "Missing location information; Rolling Acres assumed."
		flash(msg,"danger")
	return shopID 

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html', error=e),500
