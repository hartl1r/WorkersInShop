$(document).ready(function() {
  // INITIATE TOOLTIPS
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  
  })
  
 
  window.addEventListener('focus', refresh);
    
    
  var currentShopChoice = 'BOTH'
  
  // SET SHOP LOCATION
  defaultShopID = document.getElementById('defaultShopID').value
  
  var shopChoiceOPT = document.getElementById('shopChoiceOPT')
  
  currentShopChoice = shopChoiceOPT

  if (shopChoiceOPT.value == 'RA')
    document.getElementById('showRA').checked = true
  else
    if (shopChoiceOPT.value =='BW')  
      document.getElementById('showBW').checked = true
    else
      document.getElementById('showBoth').checked = true
    

  // SET 'IN SHOP NOW' OR 'IN SHOP SOMETIME TODAY'
  var inShopOPT = document.getElementById('inShopOPT')
  if (inShopOPT.value == 'inShopNow')
    document.getElementById('inShopNow').checked = true

  if (inShopOPT.value == 'inShopToday')
    document.getElementById('inShopToday').checked = true

  // SET SORT ORDER FOR LIST
  var orderByOPT = document.getElementById('orderByOPT')  
  if (orderByOPT.value == 'orderByName')
    document.getElementById('orderByName').checked = true
  if (orderByOPT.value == 'orderByTimeIn')
    document.getElementById('orderByTimeIn').checked = true
  

  // SET FILTERS
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
  
  refreshBtn = document.getElementById('btnRefresh')
  function refresh(){
    refreshBtn.click()
  }
  
  // CLICK ON ONE OF THREE SHOP CHOICE BUTTONS
  $('.shopToShowClass input[type=radio]').click(function(){
      currentShopChoice = this.value
      shopChoiceOPT.value = this.value
      sessionStorage.setItem('shopChoice',this.id)
      refresh()
  })
     
  $('.inShopClass input[type=radio]').click(function(){
      inShopOPT.value = this.id
      refresh()
  })

  $('.orderByClass input[type=radio]').click(function(){
    orderByOPT.value = this.id
    refresh()
  })

  $('.filterByClass input[type=radio]').click(function(){
    filterOptionOPT.value = this.id
    refresh()
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
      td = tr[i].getElementsByTagName("td")[1];
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
        // REMOVE ANY EXISTING DETAIL LINES
        // REMOVE CURRENT DAY ASSIGNMENTS FOR SELECTED SCHEDULE DAY
        while (detailParent.firstChild) {
          detailParent.removeChild(detailParent.lastChild);
        }
        
        // ADD DETAIL LINES
        for (i=0; i<todaysMonitors.length; i++) {

          var spanShop = document.createElement('span')
          spanShop.classList.add('Shop')
          spanShop.innerHTML = todaysMonitors[i]['shopInitials']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanShop.style.color = 'Green'
          }
          else {
            spanShop.style.color = 'Brown'
          }
          detailParent.appendChild(spanShop)

          var spanShift = document.createElement('span')          
          spanShift.classList.add('Shift')
          spanShift.innerHTML = todaysMonitors[i]['shift']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanShift.style.color = 'Green'
          }
          else {
            spanShift.style.color = 'Brown'
          }
          detailParent.appendChild(spanShift)

          var spanDuty = document.createElement('span')
          spanDuty.classList.add('Duty')
          spanDuty.innerHTML = todaysMonitors[i]['duty']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanDuty.style.color = 'Green'
          }
          else {
            spanDuty.style.color = 'Brown'
          }
          detailParent.appendChild(spanDuty)

          var spanName = document.createElement('span')
          spanName.classList.add('Name')
          spanName.innerHTML = todaysMonitors[i]['name']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanName.style.color = 'Green'
          }
          else {
            spanName.style.color = 'Brown'
          }
          detailParent.appendChild(spanName)
        
          var spanCheckIn = document.createElement('span')
          spanCheckIn.classList.add('CheckIn')
          spanCheckIn.innerHTML = todaysMonitors[i]['checkIn']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanCheckIn.style.color = 'Green'
          }
          else {
            spanCheckIn.style.color = 'Brown'
          }
          detailParent.appendChild(spanCheckIn)

          var spanCheckOut = document.createElement('span')
          spanCheckOut.classList.add('CheckOut')
          spanCheckOut.innerHTML = todaysMonitors[i]['checkOut']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanCheckOut.style.color = 'Green'
          }
          else {
            spanCheckOut.style.color = 'Brown'
          }
          detailParent.appendChild(spanCheckOut)

          var spanHomePhone = document.createElement('span')
          spanHomePhone.classList.add('HomePhone')
          spanHomePhone.innerHTML = todaysMonitors[i]['homePhone']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanHomePhone.style.color = 'Green'
          }
          else {
            spanHomePhone.style.color = 'Brown'
          }
          detailParent.appendChild(spanHomePhone)

          var spanCellPhone = document.createElement('span')
          spanCellPhone.classList.add('CellPhone')
          spanCellPhone.innerHTML = todaysMonitors[i]['cellPhone']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanCellPhone.style.color = 'Green'
          }
          else {
            spanCellPhone.style.color = 'Brown'
          }
          detailParent.appendChild(spanCellPhone)

          var spanLastTraining = document.createElement('span')
          spanLastTraining.classList.add('LastTraining')
          spanLastTraining.innerHTML = todaysMonitors[i]['lastTrainingDate']
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            spanLastTraining.style.color = 'Green'
          }
          else {
            spanLastTraining.style.color = 'Brown'
          }
          if (todaysMonitors[i]['trainingNeeded'] != '') {
            spanLastTraining.style.color = 'Red'
          }
          
          detailParent.appendChild(spanLastTraining)

          var spanTrainingNeeded = document.createElement('span')
          spanTrainingNeeded.classList.add('TrainingNeeded')
          spanTrainingNeeded.innerHTML = todaysMonitors[i]['trainingNeeded']
          detailParent.appendChild(spanTrainingNeeded)

          // checkbox within span; span has border
          var spanNoShow = document.createElement('span')
          spanNoShow.classList.add('spanNoShow')
          detailParent.appendChild(spanNoShow)

          // checkbox child of spanNoShow
          var inputNoShow = document.createElement('input')
          inputNoShow.id='R'+todaysMonitors[i]['recordID']
          inputNoShow.classList.add('NoShow')
          inputNoShow.type='checkbox'
          if (todaysMonitors[i]['noShow'] == true) {
            inputNoShow.checked = true
            inputNoShow.value = 'True'
          }
          else {
            inputNoShow.checked = false
            inputNoShow.value = 'False'
          }
          inputNoShow.onclick = function() {
            NoShowRtn(this.id);
          }
          if (todaysMonitors[i]['shopInitials'] == 'RA') {
            inputNoShow.style.color = 'Green'
          }
          else {
            inputNoShow.style.color = 'Brown'
          }
          spanNoShow.appendChild(inputNoShow)
          
          }
          
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
          alert('No monitors scheduled')
        }
      
    });

  function NoShowRtn(clicked_id) {
    recordID = clicked_id.slice(1)
    $.ajax({
      url : "/updateNoShow",
      type: "GET",
      data:{
        recordID:recordID},
      success: function(data, textStatus, jqXHR)
      {
        // alert('No Show updated.' + scheduleRecordID)
      },
      error: function (jqXHR, textStatus, errorThrown)
        {
          alert('Could not update No Show. \n errorThrown - '+errorThrown)
        }
    })  
  }
});  

$(".checkOut").click(function() {
  checkOutCell = this
  parentTR = checkOutCell.parentElement

  tds = parentTR.getElementsByTagName('td')
  recordID = this.id
  response = confirm('Confirm check out?')
  if (response != true){
    return
  }
  
  // SEND REQUEST TO SERVER
  $.ajax({
    url: "/checkOutMember",
    type: "GET",
    data:{
      recordID:recordID},
    success: function(data, textStatus, jqXHR)
    {
      //refresh()
      location.reload()  
    },
    error: function (jqXHR, textStatus,errorThrown)
        {
          // alert(jqXHR.status);
          // alert(textStatus);
          // alert(errorThrown);
          // alert('ERROR - Could not check out member.');
          location.reload()
        }
  })

})


  $(".memberID").click(function() {
    memberID = this.id.slice(0,6)
    if (memberID != '') {
      link = "https://fd.thevwc.org:42734/?villageID=" + memberID
    }
    else {
      link = "https://fd.thevwc.org:42734/"
    }
    window.location.href = link
    
  })
})