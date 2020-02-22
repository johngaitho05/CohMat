/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// $(document).on('click', '.fas-icon', function() {
//     $(this).toggleClass('fa-plus fa-minus');
// });

/* Set the width of the side navigation to 30% */
function openNav() {
    document.getElementById("mySidenav").style.width = "30%";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("profilenav").style.width = "0";
    document.getElementById("passnav").style.width = "0";
    document.getElementById("reservationnav").style.width = "0";
}

function styleJoinButton(){
    let checked_boxes = 0;
    let checkboxes = document.getElementsByClassName('coh-checker');
    let button = document.getElementById('join-recommended');
    let container = document.getElementById('recommended-groups');
    for(let i=0; i< checkboxes.length; i++) {
        if (checkboxes[i].checked === true){
            checked_boxes += 1
        }
    }
    if (checked_boxes === 0){
        document.getElementById('join-help').innerHTML = "Select a group to join";
        $("#join-recommended").css({"opacity":"0","margin-top":"30px"});
        $("#recommended-groups").css({"margin-top":"0"});
    }
    else if(checked_boxes === 1){
        document.getElementById('join-help').innerHTML = "";
       $("#join-recommended").css({"opacity":"1","margin-top":"160px"});
        $("#recommended-groups").css({"margin-top":"50px"});
    }
}

