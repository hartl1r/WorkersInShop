//var processedOnce = false
$(document).ready(function() {
  // DO WE HAVE A COOKIE
  var shopIDcookieValue = checkCookie()
  var currentShopChoice = shopIDcookieValue
  
  // SET OPTIONS BASED ON ROUTE VALUES PASSED IN
  var shopChoiceOPT = document.getElementById('shopChoiceOPT')

  if (shopChoiceOPT.value = 'RA')
    document.getElementById('showRA').checked = true

  if (shopChoiceOPT.value = 'BW')  
    document.getElementById('showBW').checked = true

  if (shopChoiceOPT.value = 'BOTH')  
    document.getElementById('showBoth').checked = true
  
  var inShopOPT = document.getElementById('inShopOPT')
  if (inShopOPT.value = 'inShopNow')
    document.getElementById('inShopNow').checked = true

  if (inShopOPT.value = 'inShopToday')
    document.getElementById('inShopToday').checked = true

//  if (document.getElementById('orderByOPT').val == "orderByName")
  var orderByOPT = document.getElementById('orderByOPT')  
  if (orderByOPT.value = 'orderByName')
    document.getElementById('orderByName').checked = true
  if (orderByOPT.value = 'orderByTimeIn')
    document.getElementById('orderByTimeIn').checked = true
  

  var filterOptionOPT = document.getElementById('filterOptionOPT')
  if (filterOptionOPT.value = 'Defibrillator')
    document.getElementById('Defibrillator').checked = true
  if (filterOptionOPT.value = 'President')
    document.getElementById('President').checked = true
    if (filterOptionOPT.value = 'Lumber')
    document.getElementById('Lumber').checked = true
    if (filterOptionOPT.value = 'Maintenance')
    document.getElementById('Maintenance').checked = true
    if (filterOptionOPT.value = 'Merchandise')
    document.getElementById('Merchandise').checked = true
    if (filterOptionOPT.value = 'BOD')
    document.getElementById('BOD').checked = true
    if (filterOptionOPT.value = 'Safety')
    document.getElementById('Safety').checked = true
    if (filterOptionOPT.value = 'SpecProj')
    document.getElementById('SpecProj').checked = true
    if (filterOptionOPT.value = 'AskMe')
    document.getElementById('AskMe').checked = true
    if (filterOptionOPT.value = 'Mentors')
    document.getElementById('Mentors').checked = true
    if (filterOptionOPT.value = 'Everyone')
    document.getElementById('Everyone').checked = true
   
  msg = shopIDcookieValue + "\n" + shopChoiceOPT.value + "\n" + inShopOPT.value + "\n" + "\n" + filterOptionOPT.value
  alert(orderByOPT.value)

  // var opt = filterOptionOPT.options[filterOptionOPT.selectedIndex];
  // console.log( opt.value );
  // console.log( opt.text );

    // if (document.getElementById(' ').val() == " ")
    // document.getElementById(' ').checked = true
    // if (document.getElementById(' ').val() == " ")
    // document.getElementById(' ').checked = true
    // if (document.getElementById(' ').val() == " ")
    // document.getElementById(' ').checked = true
    // if (document.getElementById(' ').val() == " ")
    // document.getElementById(' ').checked = true
    // if (document.getElementById(' ').val() == " ")
    // document.getElementById(' ').checked = true



  //alert("Processed once sw - " + processedOnce)
  //processedOnce=true
  //alert(processedOnce)
  //if (processedOnce != true)
  // var inShop=$('input[name=inShop]:checked').val()
  // console.log (inShop.length)
  // console.log (inShop)

  // alert(inShop)
  // alert("ALERT")
  // //if (inShop.length == 0)
  // if (document.getElementById("inShopNow").checked != true && document.getElementById("inShopToday").checked != true)
  //   document.getElementById("inShopNow").checked=true
  //   document.getElementById("Everyone").checked=true
  //   document.getElementById("orderByName").checked=true
  // //   processedOnce=true
  //   alert("Processed once switch - " + processedOnce)

  // SET SELECTED SHOP TO CHECKED
  // if (shopIDcookieValue == 'RA')
  //   document.getElementById("showRA").checked = true
  
  // if (shopIDcookieValue == 'BW')
  //   document.getElementById("showBW").checked = true
  
  // setLocationMsg(shopIDcookieValue)

  //BUILD MESSAGE DURING TESTING TO SHOW STATUS OF OPTIONS
  msg = "Shop location selection is " + currentShopChoice
  var inShop=$('input[name=inShop]:checked').val()
  msg = msg + "\nIn Shop option selection is " + inShop 
  var orderByItem = $('input[name=orderByItem]:checked').val()
  msg = msg + "\nOrder By option selection is " + orderByItem
  var filterBy=$('input[name=filterItem]:checked').val()
  msg = msg + "\nFilter By option selection is " + filterBy;
  //alert(msg)
//})


  // USER CLICKED REFRESH BUTTON
  $('#btnRefreshx').on('click',function(){
    
    //refreshList()
    // PUT OPTIONS INTO AN ARRAY
    // var optionArray = []
    // // START ARRAY WITH SHOP LOCATION ('RA', 'BW' OR 'BOTH')
    // optionArray.push(currentShopChoice)
    // // ADD INSHOPNOW OR INSTHOP TODAY OPTION
    // optionArray.push($('input[name=inShop]:checked').val())
    // // ADD ORDER BY PARAMETER
    // optionArray.push($('input[name=orderByItem]:checked').val())
    // // ADD FILTER CHOICE
    // optionArray.push($('input[name=filterItem]:checked').val())
    
    // POST ARRAY TO SERVER
    //$.post("workersInShop",{'options':optionArray})
    //$.post("workersInShop",{'choices[]':["Jon","Susan"]});
  })

  // REFRESH (GET)
  //$('#btnRefreshGET').on('click',function(){
  //  refreshListGET()
  //})

  // CLICK ON TABLE ROW EVENT
  $(document).on('click','#myTable td', function(e) {
    if ($(this).is('td')) {
      $(this).closest('tr').toggleClass('highlighted');
    } else {
      $('#myTable tr').toggleClass('highlighted');
    }
  });

  // CLICK ON ONE OF THREE SHOP CHOICE BUTTONS
  $('.shopToShow input[type=radio]').click(function(){
      currentShopChoice = this.value
      shopChoiceOPT.value = this.id
      //document.getElementById('shopChoiceOPT').innerHTML = this.id 
      if (currentShopChoice != 'BOTH'){
        // CHANGE THE COOKIE SETTING
        setCookie("SHOPID", currentShopChoice, 365);
      }
      //setLocationMsg(currentShopChoice)
  })
  $('.inShop input[type=radio]').click(function(){
      inShopOPT.value = this.id
  })

  $('.orderBy input[type=radio]').click(function(){
    orderByOPT.value = this.id
  })

  $('.filterBy input[type=radio]').click(function(){
    filterOptionOPT.value = this.id
  })

  // $('.shopChoiceItem input[type=radio]').click(function(){
  //   currentShopChoice = this.value
  //   console.log (this.id)
  //   alert (this.id)
  //   document.getElementById("shopChoiceOPT").innerHTML = this.id 
  //   if (currentShopChoice != 'BOTH'){
  //     // CHANGE THE COOKIE SETTING
  //     setCookie("SHOPID", currentShopChoice, 365);
  //     //console.log("Cookie set to " + currentShopChoice)
  //   }
    //setLocationMsg(currentShopChoice)


  var clickedId;
    $(function(){
         // When any link is clicked
         $('a').click(function(){
              // Set your variable
              clickedId = this.id; // or clickedId = $(this).attr('id');
         });
    });


  // TEXT ENTERED INTO SEARCH BOX
  $("#nameSearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });



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

  // function refreshList() { 
  //   // PUT OPTIONS INTO AN ARRAY
  //   var optionArray = []
  //   // START ARRAY WITH SHOP LOCATION ('RA', 'BW' OR 'BOTH')
  //   optionArray.push(currentShopChoice)
  //   // ADD INSHOPNOW OR INSTHOP TODAY OPTION
  //   optionArray.push($('input[name=inShop]:checked').val())
  //   // ADD ORDER BY PARAMETER
  //   optionArray.push($('input[name=orderByItem]:checked').val())
  //   // ADD FILTER CHOICE
  //   optionArray.push($('input[name=filterItem]:checked').val())
  //   //alert (optionArray)

  //   // SEND ARRAY TO WORKERSINSHOP
  //   xhr = new XMLHttpRequest();
  //   var url = "/workersInShopPOST";
  //   //var url = "/workersInShop";
  //   xhr.open("POST", url, true);
  //   xhr.setRequestHeader("Content-type", "application./json");
  //   xhr.onreadystatechabnge = function() {
  //     if (xhr.readyState === 4 && xhr.status === 200) {
  //       console.log("Result - " + this.responseText)
  //     }
  //   }
  //   //console.log("Array - " + optionArray)
  //   var data = JSON.stringify(optionArray);
  //   //console.log("Data - " + data)

  //   xhr.send(data);
  // }  

  // function refreshListGET() { 
  //   // PUT OPTIONS INTO AN ARRAY
  //   var optionArray = []
  //   // START ARRAY WITH SHOP LOCATION ('RA', 'BW' OR 'BOTH')
  //   optionArray.push(currentShopChoice)
  //   // ADD INSHOPNOW OR INSTHOP TODAY OPTION
  //   optionArray.push($('input[name=inShop]:checked').val())
  //   // ADD ORDER BY PARAMETER
  //   optionArray.push($('input[name=orderByItem]:checked').val())
  //   // ADD FILTER CHOICE
  //   optionArray.push($('input[name=filterItem]:checked').val())
  //   //alert (optionArray)

  //   // SEND ARRAY TO WORKERSINSHOP
  //   xhr = new XMLHttpRequest();
  //   var url = "/workersInShopGET";
  //   xhr.open('GET','/workersInShopGET', true);
  //   xhr.setRequestHeader("Content-type", "application./json");
  //   xhr.onreadystatechabnge = function() {
  //     if (xhr.readyState === 4 && xhr.status === 200) {
  //       console.log("Result - " + this.responseText)
  //     }
  //   }
  //   console.log("Array - " + optionArray)
  //   var data = "option=x"  //JSON.stringify(optionArray);
  //   console.log("Data - " + data)

  //   xhr.send('option=x');
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
      //alert("Working at " + shopID);
    } else {
        shopID = prompt("Please enter your shopID ('RA' or 'BW'):","");
        if (shopID != "" && shopID != null) {
          setCookie("SHOPID", shopID, 365);
          return shopID
        }
    }
  }


  // $("button").click(function() {
  //   alert("Button clicked")
  // })

  // $("input").click(function() {
  //   alert("Input clicked")
  // })
})