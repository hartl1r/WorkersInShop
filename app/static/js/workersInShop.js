$(document).ready(function() {
  // INITIATE TOOLTIPS
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  
  })
})  

window.addEventListener('focus', refresh);
  
  
var currentShopChoice = 'BOTH'

// SET SHOP LOCATION
defaultShopID = document.getElementById('defaultShopID').value
//window.addEventListener('load')


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

// function refreshInitialPage() {
//   $.ajax({
//     url : "/workersInShop",
//     type: "GET",
//     data : {
//     },
//     success: function(data, textStatus, jqXHR)
//     {}
    
// }

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
  //alert('Getting monitors for location '+ shopChoiceOPT)
  console.log('shopChoiceOPT - ',shopChoiceOPT)

  // GET MEMBERS SCHEDULED FOR MONITOR DUTY TODAY
  $.ajax({
    url : "/getTodaysMonitors",
    type: "GET",
    data:{
      shopChoice:shopChoiceOPT},
    success: function(data, textStatus, jqXHR)
    {
      todaysMonitors = data.todaysMonitorsArray
      console.log('todaysMonitors - ' + todaysMonitors)
      
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
          spanShop.style.color = 'Black'
        }
        else {
          spanShop.style.color = 'Brown'
        }
        detailParent.appendChild(spanShop)

        var spanShift = document.createElement('span')          
        spanShift.classList.add('Shift')
        spanShift.innerHTML = todaysMonitors[i]['shift']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanShift.style.color = 'Black'
        }
        else {
          spanShift.style.color = 'Brown'
        }
        detailParent.appendChild(spanShift)

        var spanDuty = document.createElement('span')
        spanDuty.classList.add('Duty')
        spanDuty.innerHTML = todaysMonitors[i]['duty']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanDuty.style.color = 'Black'
        }
        else {
          spanDuty.style.color = 'Brown'
        }
        detailParent.appendChild(spanDuty)

        var spanName = document.createElement('span')
        spanName.classList.add('Name')
        spanName.innerHTML = todaysMonitors[i]['name']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanName.style.color = 'Black'
        }
        else {
          spanName.style.color = 'Brown'
        }
        detailParent.appendChild(spanName)
      
        var spanCheckIn = document.createElement('span')
        spanCheckIn.classList.add('CheckIn')
        spanCheckIn.innerHTML = todaysMonitors[i]['checkIn']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanCheckIn.style.color = 'Black'
        }
        else {
          spanCheckIn.style.color = 'Brown'
        }
        detailParent.appendChild(spanCheckIn)

        var spanCheckOut = document.createElement('span')
        spanCheckOut.classList.add('CheckOut')
        spanCheckOut.innerHTML = todaysMonitors[i]['checkOut']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanCheckOut.style.color = 'Black'
        }
        else {
          spanCheckOut.style.color = 'Brown'
        }
        detailParent.appendChild(spanCheckOut)

        var spanHomePhone = document.createElement('span')
        spanHomePhone.classList.add('HomePhone')
        spanHomePhone.innerHTML = todaysMonitors[i]['homePhone']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanHomePhone.style.color = 'Black'
        }
        else {
          spanHomePhone.style.color = 'Brown'
        }
        detailParent.appendChild(spanHomePhone)

        var spanCellPhone = document.createElement('span')
        spanCellPhone.classList.add('CellPhone')
        spanCellPhone.innerHTML = todaysMonitors[i]['cellPhone']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanCellPhone.style.color = 'Black'
        }
        else {
          spanCellPhone.style.color = 'Brown'
        }
        detailParent.appendChild(spanCellPhone)

        var spanLastTraining = document.createElement('span')
        spanLastTraining.classList.add('LastTraining')
        spanLastTraining.innerHTML = todaysMonitors[i]['lastTrainingDate']
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          spanLastTraining.style.color = 'Black'
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
        inputNoShow.onchange = function() {
          //location.href='/updateNoShow/?record=' + this.id + '&noShow='
          NoShowRtn(this.id);
        }
        if (todaysMonitors[i]['shopInitials'] == 'RA') {
          inputNoShow.style.color = 'Black'
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
})

function NoShowRtn(clicked_id) {
  console.log('...........................................')
  console.log("NO SHOW ROUTINE")
  recordID = clicked_id.slice(1)
  console.log('recordID - ' + recordID)
  if (document.getElementById(clicked_id).checked == true){
    console.log('No Show is true')
    noShow = 'True'
  }
  else {
    console.log('No Show is FALSE')
    noShow = 'False'
  }
  $.ajax({
    url : "/updateNoShow",
    type: "GET",
    data:{
      recordID:recordID,noShow:noShow},
    success: function(data, textStatus, jqXHR)
    {
      alert(data.msg)
      // alert('No Show updated.' + scheduleRecordID)
      //window.reload()
      //show showTodaysMonitorsID
    },
    error: function (jqXHR, textStatus, errorThrown)
      {
        alert(data.msg)
        //alert('Could not update No Show. \n errorThrown - '+errorThrown)
      }
  })  
}


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
  currentURL = document.getElementById('currentURL').value 
  if (memberID != '') {
    link = currentURL + ":42734/?villageID=" + memberID
  }
  else {
    link = currentURL + ":42734/"
  }
  var memberWindow = window.open(link,'memberWindow')
  memberWindow.focus
})

$(".photoBtn").click(function() {
  console.log('.photoBtn')
  memberID = this.id.slice(0,6)
  console.log('memberID - ',memberID)
  photoImgModal = document.getElementById('photoImgID')
  // Try to find a .jpg file
  url = "/static/memberPhotos/" + memberID + ".jpg"
  
  try {
    photoImgModal.src = url
  }
  catch {
    console.log('Photo not found for member '+ memberID)
  }
 
  photoImgModal.alt = "No photo available."
  $('#photoModal').modal('show')
  return 
})

function closePhotoModal() {
  $('#photoModal').modal('hide')
}
function doesFileExist(urlToFile) {
  var xhr = new XMLHttpRequest();
  xhr.open('HEAD', urlToFile, false);
  xhr.send();
   
  if (xhr.status == "404") {
      return false;
  } else {
      return true;
  }
}