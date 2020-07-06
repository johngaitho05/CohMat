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
$('#question-form').submit(function(e){
    e.preventDefault();
    let target_group = $(this).find('#question-group').val();
    let content = $(this).find('#question-text').val();
    let image = $(this).find('#question-image').val();
    let quizData = new FormData(this);
    if(target_group){
        if(content || image){
            $.ajax({
                method: "POST",
                url: "/new-post/",
                data: quizData,
                success: function(data) {
                    let message = data['message'];
                    let code = data['code'];
                    if(code === 0){
                        window.location = '/'
                    }else{
                        $('#quiz-error').text(message)
                    }
                },
                processData: false,
                contentType: false,
            });
        }else{
            $('#quiz-error').text('Content or Image is required');
        }
    }else{
        $('#quiz-error').text('Please select the target group');
    }
});

// Opening an input when the user clicks on 'give your answer' button
function showAnswerInput(id){
    let ansForms = $('.answer-form');
    ansForms.each(function() {
        $(this).css({height:0,opacity:0,overflow:"hidden",pointerEvents:'none'})
    });
    let activeForm = $('#'+"answer-form-"+id);
    const input = activeForm.find('textarea');
    input.val("");
    activeForm.css({height:"auto",opacity:1,overflow:"visible",pointerEvents:'all'});
    input.focus()

}
const hideAnswerInput=(id)=>{
    let activeForm = $('#'+"answer-form-"+id);
    activeForm.css({height:0,opacity:0,overflow:"hidden",pointerEvents:'none'})
};

function allow_profile_editing(){
// find all inputs in the page
    let to_edit = document.querySelectorAll("input");
// make all the inputs editable by removing the readonly attribute
    for (let i = 0; i< to_edit.length; i++){
        if(to_edit[i].name !== 'email'){
            to_edit[i].removeAttribute('readonly');
        }
    }
}

// Submitting the edited profile details using ajax
$('#update-profile-form').submit(function(e){
    e.preventDefault();
    let form = document.getElementById('update-profile-form');
    let updatedData = new FormData(form);
    $.ajax({
        method: "POST",
        url: "update",
        data: updatedData,
        success: function(data) {
            let message = data['message'];
            let code = data['code'];
            show_alert(message, code)
        },
        cache: false,
        contentType: false,
        processData: false
    });
});



// Show alert based on the message received from the server after ajax form submission
function show_alert(message, alert_code=1,delay=5000){
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
// Close the alert after 5 seconds (5000 milliseconds)
    container.innerHTML += content;
    setTimeout(function(){
        $(".alert").alert('close');
    },delay);
}


function get_alert_class(alert_code) {
    if (alert_code === 0){
        return "alert-success";
    }else{
        return "alert-danger";
    }

}

function updateMinutesTime(){
    let new_posts = $(".timer:contains('now')");
    let other_posts = $(".timer:contains('minute')");
    new_posts.each(function() {
        $(this).html('<span>'+ 1 + '&nbsp;</span>minute ago')
    });
    other_posts.each(function() {
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

function HandleAnswerNotification(data, currentUsername){
    let username =  data['notifierUsername'];
    let counter = $('#notification-count');
    if(username !== currentUsername) {
        if (counter.length) {
            counter.text(parseInt(counter.text()) + 1)
        } else {
            $('#notifications-badge').html("<sup id='notification-count'>1</sup>");
        }
    }else{
        show_alert('Comment added', 0,3000)
    }
    let quiz = $('#'+'quiz_' + data['quizId']);
    let counter2 = quiz.find($('.ans-counter'));
    counter2.text(parseInt(counter2.text())+1);
    let content = `<div class="answer-item">
            <img src="${data['notifierPhoto']}" class="img-fluid profile-image float-left" />
            <h5><b>${data['reportingName']}</b></h5>
                <p class="float-right time-element answer-time  timer">
                        <span>Just now</span>
                </p>
            <p class="answer-content ">${data['content']}</p>
            <p class="reply-trigger">Reply</p>
        </div>`;
    let container = $('#'+ 'ansHolder_'+data['quizId']);
    container.prepend(content)
}

function HandleMessageNotification(data, currentUsername){
    let username = data['notifierUsername'];
    let counter = $('#messages-count');
    if(username !== currentUsername) {
        if (counter.length) {
            counter.text(parseInt(counter.text()) + 1)
        } else {
            $('#messages-badge').html("<sup id='messages-count'>1</sup>");
        }
    }
}