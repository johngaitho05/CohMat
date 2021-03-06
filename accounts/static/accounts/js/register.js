let current_fs, next_fs, previous_fs; //fieldsets
let left, opacity, scale; //fieldset properties which we will animate
let animating; //flag to prevent quick multi-click glitches
let cohorts =null;

$(".next").click(function(){
    if(animating) return false;
    // define current and next slides
    current_fs = $(this).parent().parent();
    next_fs = $(this).parent().parent().next();

    // prevent loading of the next slide if there are blank fields in the current slide
    let field = $('#study_field').val();
    if (missingFields(current_fs)){
        show_alert('Please fill in all the required fields')
    }else{
        animating = true;
        //activate next step on progressbar using the index of next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        if (next_fs.hasClass("cohort_list")) {
            let mydiv = $("#page_wrapper");
            mydiv.removeClass('col-md-6');
            mydiv.removeClass('offset-md-3');
            mydiv.addClass('col-md-10');
            mydiv.addClass('offset-md-1');
            displayCohortsFirstTime(field); // display groups that the user can join
        }
        //show the next fieldset
        next_fs.show();

        //	hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50)+"%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale('+scale+')',
                    'position': 'absolute'
                });
                next_fs.css({'left': left, 'opacity': opacity});
            },
            duration: 800,
            complete: function(){
                current_fs.hide();
                animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    }
});

$(".previous").click(function(){
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent().parent();
    previous_fs = $(this).parent().parent().prev();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    let mydiv = $("#page_wrapper");
    mydiv.removeClass('col-md-10');
    mydiv.removeClass('offset-md-1');
    mydiv.addClass('offset-md-3');
    mydiv.addClass('col-md-6');
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1-now) * 50)+"%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
        },
        duration: 800,
        complete: function(){
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
$("#profile_photo").change(function() {
    readURL(this);
});

/**
 * @return {boolean}
 */
function missingFields(container){
    let missing = false;
    container.find('input[type=text],input[type=password],select').each(function() {
        if (!$(this).val()){
            missing = true;
            return false
        }
    });
    return missing
}

function selectCard(id) {
    let cohort = document.getElementById(id);
    let to_check = document.getElementById('check-'.concat(id));
    let selected = document.getElementById('selected_cohorts');
    let selected_list = get_selected();
    if (cohort.style.border === "thick solid green") {
        cohort.style.border = "1px solid rgba(0,0,0,.125)";
        to_check.checked = false;
        let to_delete = selected_list.indexOf(id);
        selected_list.splice(to_delete,1);
        let new_string = '';
        for(let i=0;i<selected_list.length;i++){
            new_string = new_string.concat(selected_list[i].concat(','))
        }
        selected.value = new_string;
    } else {
        cohort.style.border = "thick solid green";
        to_check.checked = true;
        let was_selected = false;
        for(let i=0;i<selected_list.length;i++){
            if (selected_list[i] === id){
                was_selected = true;
                break;
            }
        }
        if (was_selected === false){
            selected.value =  selected.value.concat(id.concat(','));
        }
    }
}

function displayCohortsFirstTime(studyField){
    let loader_left = document.getElementById('load_previous');
    let loader_right = document.getElementById('load_next');
    $.ajax({
        method: "POST",
        url: "to_join",
        data: {'coh_id':studyField},
        success: function(data) {
            cohorts = data;
            let data_length = cohorts.length;
            if(data_length<4) {
                changeCohortsContent(cohorts, 0, data_length);
                document.getElementById('right-count').value= data_length-1;
                loader_left.style.color = '#F0F8FF';
                loader_right.style.color = '#F0F8FF';
            }else{
                changeCohortsContent(cohorts, 0,3);
                loader_left.style.color = '#F0F8FF';
                loader_right.style.color = 'rgb(32, 207, 255)';
                document.getElementById('right-count').value= 2;
            }
            document.getElementById('left-count').value=0;
            if(get_selected().length !==0){
                style_previously_selected_cards(cohorts);
            }
        }
    });
}

function changeCohortsContent(data, index1, index2){
    let container = document.getElementById('to_join_container');
    container.innerHTML = '';
    for(let i=index1;i<index2;i++){
        let content = ` 
                        <div class="col-md-4 col-sm-6">
                            <div class="card cohort-item" id="${data[i].id}" onclick="selectCard('${data[i].id}')">
                                <img src="${data[i].logo}" alt="" style="background: ${data[i].background_color}"/>
                                <h4 class="cohort-title ">${ data[i].title }</h4>
                                <div class="group-info">
<!--                                    <h4>${ data[i].title }</h4>-->
                                    <div class="row">
                                        <div class="col-sm-6 sub-column">
                                            <p><i class="fas fa-calendar"></i><span> Date Created</span><br/>
                                                <span class="group_data">${ data[i].date_created }</span></p>
                                        </div>
                                        <div class="col-sm-6 sub-column">
                                            <p><i class="fas fa-users"></i><span> Members</span><br/>
                                                <span class="group_data">${data[i].no_of_members }</span></p>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-12 text-center">
                                        <p><i class="far fa-address-book"></i><span> Total posts</span>
                                            <br/><span class="group_data">${data[i].total_posts }</span></p>
                                    </div>
                                    <input class="card-selector"  type="checkbox" id="check-${data[i].id}" name="to_join"  value="${data[i].id}"/>
                                </div>
                            </div>
                     </div>`;
        container.innerHTML += content;
    }
}

// load groups every time the user clicks on next/previous button
function load_cohorts(direction){
    let data = cohorts;
    let left_input = document.getElementById('left-count');
    let right_input = document.getElementById('right-count');
    let left_value = parseInt(left_input.value);
    let right_value = parseInt(right_input.value);

    if (direction === 'left' && left_value !== 0) {
        changeCohortsContent(data, left_value - 3, left_value);
        left_input.value = left_value-3;
        right_input.value = left_value-1;
        design_controls(data.length);
        style_previously_selected_cards(data);
    } else if (direction === 'right' && (right_value + 1) % 3 === 0 && data.length > right_value+1) {
        if (data.length < right_value + 4) {
            changeCohortsContent(data, right_value + 1, data.length);
            right_input.value = data.length - 1;
            left_input.value = left_value+3
        } else {
            changeCohortsContent(data, right_value + 1, right_value + 4);
            right_input.value = right_value + 3;
            left_input.value = left_value + 3;
        }
        design_controls(data.length);
        style_previously_selected_cards(data);
    }
}

function design_controls(data_length){
    let left_value = parseInt(document.getElementById('left-count').value);
    let right_value = parseInt(document.getElementById('right-count').value);
    let previous = document.getElementById('load_previous');
    let next = document.getElementById('load_next');
    if (left_value === 0){
        previous.style.color = '#F0F8FF';
    }else{
        previous.style.color = 'rgb(32, 207, 255)';
    }
    if(right_value === data_length-1){
        next.style.color = '#F0F8FF';
    }else{
        next.style.color = 'rgb(32, 207, 255)';
    }
}




function get_selected(){
    let selected =  document.getElementById('selected_cohorts').value;
    let selected_list= selected.split(",");
    selected_list.splice(selected_list.indexOf(""),1);
    return selected_list
}


function style_previously_selected_cards(data){
    let left_value = parseInt(document.getElementById('left-count').value);
    let right_value = parseInt(document.getElementById('right-count').value);
    let selected = get_selected();
    for(let i=left_value;i<=right_value;i++){
        for(let j=0;j<selected.length;j++){
            if(data[i].id.toString() === selected[j]){
                selectCard(data[i].id.toString());
            }
        }
    }
}

function submitRegForm(){
    let form = document.querySelector('#msform');
    let formData = new FormData(form);
    $.ajax({
        url: "",
        type: 'POST',
        data: formData,
        success: function (data) {
            let message = data['message'];
            let code = data['code'];
            if (code === 0){
                $('body').addClass("loading");
                let form = $('#email-confirmation-form');
                form.find('input[name=email]').val(data['email']);
                form.submit();
            }else{
                show_alert(message)
            }
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

const show_alert = (message) => {
    let element = $('#alert-message');
    element.text(message);
    $('#alert-modal').modal('show');

};

function showResendForm(){
    let form = $('#resend-link-form');
    form.removeAttr('hidden')
}

$('#resend-link-form').submit(function(e){
    e.preventDefault();
    resendLink();
});

function resendLink() {
    let old_email = $('#old-email').val();
    let new_email = $('#new-email').val();
    if (old_email  && new_email) {
        $.ajax({
            method: "POST",
            url: '/accounts/register/resend-link',
            data: {'old-email': old_email, 'new-email': new_email},
            success: function (data) {
                let code = data['code'];
                let message = data['message'];
                show_alert(message, code);
                if (code === 0)
                    $('#old-email').val(new_email)
            }
        });
    }else{
        show_alert("The email field cannot not be empty")
    }
}

