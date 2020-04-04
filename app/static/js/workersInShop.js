$(document).ready(function() {
  // DO WE HAVE A COOKIE
  var shopIDcookieValue = checkCookie()
  var currentShopChoice = shopIDcookieValue
  
  // SET SELECTED SHOP TO CHECKED
  if (shopIDcookieValue == 'RA')
    document.getElementById("showRA").checked = true
  
  if (shopIDcookieValue == 'BW')
    document.getElementById("showBW").checked = true
  
  setLocationMsg(shopIDcookieValue)

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
    refreshList()
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
  $('#shopChosen input[type=radio]').click(function(){
      currentShopChoice = this.value
      if (currentShopChoice != 'BOTH'){
        // CHANGE THE COOKIE SETTING
        setCookie("SHOPID", currentShopChoice, 365);
        //console.log("Cookie set to " + currentShopChoice)
      }
      setLocationMsg(currentShopChoice)
  })

  // TEXT ENTERED INTO SEARCH BOX
  $("#nameSearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });



  // GENERAL FUNCTIONS
  function setLocationMsg(shopChoice){
    if (shopChoice == "RA"){
      document.getElementById("msg1").innerHTML = "ROLLING ACRES LOCATION"
    }
    else if (shopChoice == "BW") {
      document.getElementById("msg1").innerHTML = "BROWNWOOD LOCATION"
    }
    else {
      document.getElementById("msg1").innerHTML = "SHOWING BOTH LOCATIOS"
    }
  }

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