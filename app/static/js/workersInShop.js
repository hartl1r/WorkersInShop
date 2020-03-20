$(document).ready(function() {
  // SET ROLLING ACRES TO CHECKED
  if (document.getElementById("shopID").val = 'RA')
    document.getElementById("showRA").checked = true

  if (document.getElementById("shopID").val = 'BW')
    document.getElementById("showRA").checked = true

  //var shopLocation =$('button[#myShopChoice]:checked').val()
  var shopLocation=$('input[name=shopChoice]:checked').val()
  msg = "Shop location selection is " + shopLocation 

  var inShop=$('input[name=inShop]:checked').val()
  msg = msg + "\nIn Shop option selection is " + inShop 

  var orderByItem = $('input[name=orderByItem]:checked').val()
  msg = msg + "\nOrder By option selection is " + orderByItem

  var filterBy=$('input[name=filterItem]:checked').val()
  msg = msg + "\nFilter By option selection is " + filterBy;

  alert(msg)

  $('#myShopChoice button').click(function() {
    //alert($(this).val())
    var buttonValue = "No value yet"
    buttonValue = $(this).val()
    console.log("myShopChoice value -" + buttonValue  )
   // $(this).addClass('active').siblings().removeClass('active');
  })
    /*
$("#myShopChoice :input").change(function() {
      console.log(this); // points to the clicked input button
  });

  $('input[name="myShopChoice"]').change( function() {
    alert($(this).val())
  })
    /*
    document.getElementById("btnRefresh").addEventListener("click", refreshList);
  document.getElementById('BW').checked = true;
*/
  /*
    function refreshList() {
     
      var ele = document.getElementsByName('shopChoice');        
      for(i = 0; i < ele.length; i++) { 
        if(ele[i].checked) 
        shopSelected = ele[i].value; 
      } 
      console.log (shopSelected)

      if (document.getElementById('RA').checked = true) 
        shopNumberSelected = '1'
      else if (document.getElementById('BW').checked = true) 
        shopNumberSelected = '2'
      else if (document.getElementById('BOTH').checked = true) 
        shopNumberSelected = '3'
      else shopNumberSelected = '0'

      console.log (shopNumberSelected)

      shopOptionSelected = $('button[name=shopChoice]:checked').val()
      console.log (shopOptionSelected)
      inShopOptionSelected = $('button[name=inShop]:checked').val()
      orderByOptionSelected = $('button[name=orderBy]:checked').val()
      filterOptionSelected = $('button[name=filter]:checked').val()
      
      msg = shopOptionSelected + inShopOptionSelected + orderByOptionSelected + filterOptionSelected
      alert(msg)
    )}
*/
})
