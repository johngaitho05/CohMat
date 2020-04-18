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

function submit_question(){
    let content = document.getElementById('question-text');
    let group = document.getElementById('question-group');
    let error_bar = document.getElementById('quiz-error');
    if (content.value !== '' && group.value !== '0' ){
        document.getElementById('question-form').submit();
    }
    else if(content.value === ''){
        error_bar.innerHTML = "Content can't be empty";
    }else{
        error_bar.innerHTML = "Please select the target group";
    }
}

function openAnswerInput(id){
    let answer_input = document.getElementById('answer-input'.concat(id));
    let send_button = document.getElementById('send-answer'.concat(id));
    answer_input.style.width = '80%';
    answer_input.style.height = '50px';
    answer_input.focus();
    answer_input.placeholder = 'Type your answer here';
    send_button.style.opacity = 'unset';
    send_button.style.left = '0';
}

function styleactivelink(link_id) {
    let navlinks = document.getElementsByClassName('nav-link');
    for (let i = 0; i < navlinks.length; i++) {
        navlinks[i].classList.remove('active');
        let to_style = document.getElementById(link_id);
        to_style.classList.add('active');
    }
}

function allow_profile_editing(){
    // find all inputs in the page
    to_edit = document.getElementsByTagName("input");
    // make all the inputs editable by removing the readonly attribute
    for (let i = 0; i< to_edit.length; i++){
        to_edit[i].removeAttribute('readonly');
    }
}

function edit_profile(){

}