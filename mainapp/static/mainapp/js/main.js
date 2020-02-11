/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).on('click', '.fas-icon', function() {
    $(this).toggleClass('fa-plus fa-minus');
});

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


function styleactivelink(link_id) {
    let navlinks = document.getElementsByClassName('nav-link');
    for(let i=0; i< navlinks.length; i++) {
        navlinks[i].classList.remove('active');
    }
    let to_style = document.getElementById(link_id);
    to_style.classList.add('active');
}

