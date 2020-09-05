$(document).ready(function() {
  // document.getElementById('todaysMonitorsID').style.display='block'
  //$('#todaysMonitorsID').modal('show')
  var currentShopChoice = 'BOTH'
  // DO WE HAVE A COOKIE
  // IF sessionStorage FOR shopID DOES NOT EXIST, USE clientLocation
  // IF clientLocation DOES NOT EXIST USE 'BOTH'
  if (sessionStorage.getItem('shopChoice')) {
    currentShopChoice = sessionStorage.getItem('shopChoice')
  }
  else {
    if (localStorage.getItem('clientLocation')) {
      currentShopChoice = 'show' + localStorage.getItem('clientLocation')
    }
    else {
      currentShopChoice = 'showBOTH'
    }
    
  }
  //alert('currentShopChoice - ' + currentShopChoice)
  var shopChoiceOPT = document.getElementById('shopChoiceOPT')
  shopChoiceOPT.value = currentShopChoice

  // $('.shopToShowClass').click(function(){
  //   alert('jquery shopToShow clicked\nvalue - ',shopToShowChoiceOPT.value)
  //   currentShopChoice = shopChoiceOPT.value
  //   sessionStorage.setItem('shopChoice',shopChoiceOPT.value)
  // })
  
  //var shopIDcookieValue = checkCookie()
  //var currentShopChoice = shopIDcookieValue
  
  // SET OPTIONS BASED ON ROUTE VALUES PASSED IN
  //var shopChoiceOPT = document.getElementById('shopChoiceOPT')  
  if (shopChoiceOPT.value == 'showRA')
    document.getElementById('showRA').checked = true
  
  if (shopChoiceOPT.value =='showBW')  
    document.getElementById('showBW').checked = true
    
  if (shopChoiceOPT.value == 'showBoth')  
    document.getElementById('showBoth').checked = true
    
  var inShopOPT = document.getElementById('inShopOPT')
  if (inShopOPT.value == 'inShopNow')
    document.getElementById('inShopNow').checked = true

  if (inShopOPT.value == 'inShopToday')
    document.getElementById('inShopToday').checked = true

  var orderByOPT = document.getElementById('orderByOPT')  
  if (orderByOPT.value == 'orderByName')
    document.getElementById('orderByName').checked = true
  if (orderByOPT.value == 'orderByTimeIn')
    document.getElementById('orderByTimeIn').checked = true
  
  var filterOptionOPT = document.getElementById('filterOptionOPT')
  if (filterOptionOPT.value == 'Defibrillator')
    document.getElementById('Defibrillator').checked = true
  if (filterOptionOPT.value == 'President')
    document.getElementById('President').checked = true
  if (filterOptionOPT.value == 'Lumber')
    document.getElementById('Lumber').checked = true
  if (filterOptionOPT.value == 'Maintenance')
    document.getElementById('Maintenance').checked = true
  if (filterOptionOPT.value == 'Merchandise')
    document.getElementById('Merchandise').checked = true
  if (filterOptionOPT.value == 'BOD')
    document.getElementById('BOD').checked = true
  if (filterOptionOPT.value == 'Safety')
    document.getElementById('Safety').checked = true
  if (filterOptionOPT.value == 'SpecProj')
    document.getElementById('SpecProj').checked = true
  if (filterOptionOPT.value == 'AskMe')
    document.getElementById('AskMe').checked = true
  if (filterOptionOPT.value == 'Mentors')
    document.getElementById('Mentors').checked = true
  if (filterOptionOPT.value == 'Everyone')
    document.getElementById('Everyone').checked = true
   
  

  
  // FORCE A 'POST' PAGE BY CLICKING THE 'REFRESH LIST' BUTTON
  // DOES THE SESSION STORAGE VARIABLE 'timesLoaded' EXIST?
  // DEFINE pageLoadCount AS INTEGER WITH VALUE OF ZERO
  var pageLoadCount = 0
  // IF timesLoaded EXISTS ADD 1 TO IT
  if (sessionStorage.getItem('timesLoaded')) {
    pageLoadCount = parseInt(sessionStorage.getItem('timesLoaded'),10)
    pageLoadCount += 1
    sessionStorage.setItem('timesLoaded',pageLoadCount)
  }
  else {
    // CREATE SESSION VARIABLE; INITIALIZE AT 1
    pageLoadCount = 1
    sessionStorage.setItem('timesLoaded',pageLoadCount)
  }
  var getRequestMethod = document.getElementById('requestMethod');
  
  // REQUEST 'POST' PAGE
  if (getRequestMethod.value == 'GET' && pageLoadCount == 1)
    document.getElementById('btnRefresh').click()
    
  // AT PAGE 'UNLOAD' CLEAR THE sessionStorage VARIABLE
  window.addEventListener('unload', function (e) {
    sessionStorage.removeItem('timesLoaded')
  })

 

  // USER CLICKED REFRESH BUTTON
  //$('#btnRefreshx').on('click',function(){
    
  // CLICK ON TABLE ROW EVENT  (NO LOGIC REQUEST YET)
  $(document).on('click','#myTable td', function(e) {
    if ($(this).is('td')) {
      $(this).closest('tr').toggleClass('highlighted');
    } else {
      $('#myTable tr').toggleClass('highlighted');
    }
  });

  // CLICK ON ONE OF THREE SHOP CHOICE BUTTONS
  $('.shopToShowClass input[type=radio]').click(function(){
      currentShopChoice = this.value
      shopChoiceOPT.value = this.id
      if (shopChoiceOPT.value != 'showBoth'){
        // CHANGE THE COOKIE SETTING
        sessionStorage.setItem('shopChoice',this.id)
        //alert('shop choice - '+this.value)
        setCookie("SHOPID", shopChoiceOPT.value, 365);
      }
      //setLocationMsg(currentShopChoice)
  })

  $('.inShopClass input[type=radio]').click(function(){
      inShopOPT.value = this.id
  })

  $('.orderByClass input[type=radio]').click(function(){
    orderByOPT.value = this.id
  })

  $('.filterByClass input[type=radio]').click(function(){
    filterOptionOPT.value = this.id
  })

  // SEARCH FOR A MATCHING NAME
  $(document).on('keyup','#myInput', function (e) {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  })


  // var clickedId;
  //   $(function(){
  //        // When any link is clicked
  //        $('a').click(function(){
  //             // Set your variable
  //             clickedId = this.id; // or clickedId = $(this).attr('id');
  //        });
  //   });



  // GENERAL FUNCTIONS
  

  // function setCookie(cname,cvalue,exdays) {
  //   var d = new Date();
  //   d.setTime(d.getTime() + (exdays*24*60*60*1000));
  //   var expires = "expires=" + d.toGMTString();
  //   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  // }

  // function getCookie(cname) {
  //   var name = cname + "=";
  //   var decodedCookie = decodeURIComponent(document.cookie);
  //   var ca = decodedCookie.split(';');
  //   for(var i = 0; i < ca.length; i++) {
  //     var c = ca[i];
  //     while (c.charAt(0) == ' ') {
  //       c = c.substring(1);
  //     }
  //     if (c.indexOf(name) == 0) {
  //       return c.substring(name.length, c.length);
  //     }
  //   }
  //   return "";
  // }

  // function checkCookie() {
  //   var shopID=getCookie("SHOPID");
  //   if (shopID != "") {
  //     return shopID
  //   }
  //   else {
  //       shopID = prompt("Please enter your shopID ('RA' or 'BW'):","");
  //       if (shopID != "" && shopID != null) {
  //         setCookie("SHOPID", shopID, 365);
  //         return shopID
  //       }
  //   }
  // }
})

// // MODAL PROCESSING
// $('#showTodaysMonitorsID').click(function(){
//   var shopChoiceOPT = document.getElementById('shopChoiceOPT').value
//   // GET MEMBERS SCHEDULED FOR MONITOR DUTY TODAY
//   $.ajax({
//     url : "/getTodaysMonitors",
//     type: "GET",
//     data:{
//       shopChoice:shopChoiceOPT},
//     success: function(data, textStatus, jqXHR)
//     {
//       todaysMonitors = data.todaysMonitorsArray
      
//       msg = ''
//       for (i=0; i<todaysMonitors.length; i++) {
//         msg +=todaysMonitors[i]['name'] +' '+ todaysMonitors[i]['shift']+' '+todaysMonitors[i]['duty']+' '+todaysMonitors[i]['noShow']+'\n'
//         }
//       alert('Monitors: ' + msg)
//       // POPULATE MODAL FORM

//       // SHOW MODAL FORM
//       //document.getElementById('todaysMonitorsModal').style.display='flex'
//       //document.querySelector('.bg-modal-monitors').style.display='flex';
//       //$('#todaysMonitors').modal('show');
//     },
//       error: function (jqXHR, textStatus, errorThrown)
//       {
//         alert('No monitors scheduled')
//       }
//     });
//   })

  $('#todaysMonitorsID').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
    var shopChoiceOPT = document.getElementById('shopChoiceOPT').value
    // GET MEMBERS SCHEDULED FOR MONITOR DUTY TODAY
    $.ajax({
      url : "/getTodaysMonitors",
      type: "GET",
      data:{
        shopChoice:shopChoiceOPT},
      success: function(data, textStatus, jqXHR)
      {
        todaysMonitors = data.todaysMonitorsArray
        detailParent = document.getElementById('detailID')
        
        // ADD DETAIL LINES
        for (i=0; i<todaysMonitors.length; i++) {
          rowID = 'row'+i

          var spanShop = document.createElement('span')
          spanShop.id=rowID+'Shop'
          spanShop.classList.add('Shop')
          spanShop.innerHTML = todaysMonitors[i]['shopInitials']
          detailParent.appendChild(spanShop)

          var spanShift = document.createElement('span')
          spanShift.id=rowID+'Shift'
          spanShift.classList.add('Shift')
          spanShift.innerHTML = todaysMonitors[i]['shift']
          detailParent.appendChild(spanShift)
  
          var spanDuty = document.createElement('span')
          spanDuty.id=rowID+'Duty'
          spanDuty.classList.add('Duty')
          spanDuty.innerHTML = todaysMonitors[i]['duty']
          detailParent.appendChild(spanDuty)
  
          var spanName = document.createElement('span')
          spanName.id=rowID+'Name'
          spanName.classList.add('Name')
          spanName.innerHTML = todaysMonitors[i]['name']
          detailParent.appendChild(spanName)
        
          var spanCheckIn = document.createElement('span')
          spanCheckIn.id=rowID+'CheckIn'
          spanCheckIn.classList.add('CheckIn')
          spanCheckIn.innerHTML = todaysMonitors[i]['checkIn']
          detailParent.appendChild(spanCheckIn)
  
          var spanCheckOut = document.createElement('span')
          spanCheckOut.id=rowID+'CheckOut'
          spanCheckOut.classList.add('CheckOut')
          spanCheckOut.innerHTML = todaysMonitors[i]['checkOut']
          detailParent.appendChild(spanCheckOut)
  
          var spanHomePhone = document.createElement('span')
          spanHomePhone.id=rowID+'HomePhone'
          spanHomePhone.classList.add('HomePhone')
          spanHomePhone.innerHTML = todaysMonitors[i]['homePhone']
          detailParent.appendChild(spanHomePhone)
  
          var spanCellPhone = document.createElement('span')
          spanCellPhone.id=rowID+'CellPhone'
          spanCellPhone.classList.add('CellPhone')
          spanCellPhone.innerHTML = todaysMonitors[i]['cellPhone']
          detailParent.appendChild(spanCellPhone)
  
          var spanLastTraining = document.createElement('span')
          spanLastTraining.id=rowID+'LastTraining'
          spanLastTraining.classList.add('LastTraining')
          spanLastTraining.innerHTML = todaysMonitors[i]['lastTrainingDate']
          if (todaysMonitors[i]['trainingNeeded'] == 'Training needed.') {
            spanLastTraining.style.color = 'Red'
          }
          else {
            spanLastTraining.style.color = 'Black'
          }
          detailParent.appendChild(spanLastTraining)
  
          var spanTrainingNeeded = document.createElement('span')
          spanTrainingNeeded.id=rowID+'TrainingNeeded'
          spanTrainingNeeded.classList.add('TrainingNeeded')
          spanTrainingNeeded.innerHTML = todaysMonitors[i]['trainingNeeded']
          detailParent.appendChild(spanTrainingNeeded)
  
          var inputNoShow = document.createElement('input')
          inputNoShow.id=rowID+'NoShow'
          inputNoShow.classList.add('NoShow')
          inputNoShow.type='checkbox'
          if (todaysMonitors[i]['noShow'] == true) {
            inputNoShow.checked = true
          }
          else {
            inputNoShow.checked = false
          }
          detailParent.appendChild(inputNoShow)
          

          var inputRecordID = document.createElement('input')
          inputRecordID.id=rowID+'RecordID'
          inputRecordID.classList.add('RecordID')
          inputRecordID.type='hidden'
          inputRecordID.value = todaysMonitors[i]['recordID']
          inputRecordID.innerHTML= todaysMonitors[i]['recordID']
          detailParent.appendChild(inputRecordID)
          
          }
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
          alert('No monitors scheduled')
        }
      
   });
      
  });
  

