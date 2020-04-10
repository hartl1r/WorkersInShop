$(document).ready(function() {

  // DO WE HAVE A COOKIE
  var shopIDcookieValue = checkCookie()
  var currentShopChoice = shopIDcookieValue
  
  // SET OPTIONS BASED ON ROUTE VALUES PASSED IN
  var shopChoiceOPT = document.getElementById('shopChoiceOPT')  
  if (shopChoiceOPT.value == 'showRA')
    document.getElementById('showRA').checked = true
  //alert( '2. shopChoiceOPT -'+ shopChoiceOPT.value)
  if (shopChoiceOPT.value =='showBW')  
    document.getElementById('showBW').checked = true
  //alert( '3. shopChoiceOPT -'+ shopChoiceOPT.value)
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
    sessionStorage.clear
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
  // function setLocationMsg(shopChoice){
  //   if (shopChoice == "RA"){
  //     document.getElementById("msg1").innerHTML = "ROLLING ACRES LOCATION"
  //   }
  //   else if (shopChoice == "BW") {
  //     document.getElementById("msg1").innerHTML = "BROWNWOOD LOCATION"
  //   }
  //   else {
  //     document.getElementById("msg1").innerHTML = "SHOWING BOTH LOCATIOS"
  //   }
  // }

  function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function checkCookie() {
    var shopID=getCookie("SHOPID");
    if (shopID != "") {
      return shopID
    }
    else {
        shopID = prompt("Please enter your shopID ('RA' or 'BW'):","");
        if (shopID != "" && shopID != null) {
          setCookie("SHOPID", shopID, 365);
          return shopID
        }
    }
  }

})