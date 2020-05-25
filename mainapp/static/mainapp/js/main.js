/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// Update posts and notifications time after every minute
setInterval('updateMinutesTime()',60000);

// Update posts and notifications time after every hour
setInterval('updateHourlyTime()',3600000);

/* Set the width of the side navigation to 30% */
function openNav() {
    document.getElementById("mySidenav").style.width = "400px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

// highlight the link of the current page as active
function styleActiveLink(linkId) {
    let nav_links = document.getElementsByClassName('nav-link');
    for (let i = 0; i < nav_links.length; i++) {
        nav_links[i].classList.remove('active');
        let to_style = document.getElementById(linkId);
        to_style.classList.add('active');
    }
}

// dynamically styling the button for joining recommended groups
function styleJoinButton(){
    let checked_boxes = 0;
    let checkboxes = document.getElementsByClassName('coh-checker');
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

// submitting a new post (question)
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

// Opening an input when the user clicks on 'give your answer' button
function openAnswerInput(id){
    let otherForms = $('.answer-form');
    let answer_input = document.getElementById('answer-input'.concat(id));
    let send_button = document.getElementById('send-answer'.concat(id));
    answer_input.style.width = '80%';
    answer_input.style.height = '50px';
    answer_input.focus();
    answer_input.placeholder = 'Type your answer here';
    send_button.style.opacity = 'unset';
    send_button.style.left = '0';
    answer_input.parentElement.setAttribute('id','activeAnsForm')
}


function allow_profile_editing(){
    // find all inputs in the page
    let to_edit = document.querySelectorAll("input")
    // make all the inputs editable by removing the readonly attribute
    for (let i = 0; i< to_edit.length; i++){
        if(to_edit[i].name !== 'email'){
            to_edit[i].removeAttribute('readonly');
        }
    }
}

// Submitting the edited profile details using ajax
function update_profile(){
    let current_interest = document.getElementById('interest-input').value;
    let first_name = document.getElementById('first_name').value;
    let last_name = document.getElementById('last_name').value;
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;

    if (first_name && last_name && username && email){
        $.ajax({
            method: "POST",
            url: "update",
            data: {
                'first_name':first_name,
                'last_name':last_name,
                'username':username,
                'email':email,
                'current_interest':current_interest,
            },
            success: function(data) {
                var message = data['message'];
                var code = data['code'];
                show_alert(message, code)
            }
        });
    }else{
        show_alert("Failed! Please ensure that all fields contain valid values")
    }

}

// Show alert based on the message received from the server after ajax form submission
function show_alert(message, alert_code=1){
    let alert_class = get_alert_class(alert_code);
    let container = document.getElementById('alert-container');
    let content = `
    <div class="alert ${alert_class} text-center alert-dismissible fade show" id="home-alert" role="alert">
    <p id="home-alert-text">${message}</p>
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
    `;
    // Close the alert after 10 seconds (10000 milliseconds)
    container.innerHTML += content;
    setTimeout(function(){
        $(".alert").alert('close');
    },10000);
}


function get_alert_class(alert_code) {
    if (alert_code === 0){
        return "alert-success";
    }else{
        return "alert-danger";
    }

}

function updateMinutesTime(){
    let spans = $(".timer:contains('minute')");
    spans.each(function( index ) {
        let minSpan = $(this).find('span');
        let minutes = parseInt(minSpan.text());
        if(minutes<59){
            let updatedTime = minutes+1;
            $(this).html('<span>'+ updatedTime + '&nbsp;</span>minutes ago')
        }else{
            minSpan.text(1);
            $(this).html('<span>1 &nbsp;</span>hour ago')
        }
    });
}

function updateHourlyTime(){
    let timeHolders = $(".timer:contains('hour')");
    timeHolders.each(function( index ) {
        let minSpan = $(this).find('span');
        let hours = parseInt(minSpan.text());
        if(hours<23){
            let updatedTime = hours+1;
            $(this).html('<span>'+ updatedTime + '&nbsp;</span>hours ago')
        }else{
            minSpan.text(1);
            $(this).html('<span>1 &nbsp;</span>day ago')
        }
    });
}