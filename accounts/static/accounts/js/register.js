//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent().parent();
    next_fs = $(this).parent().parent().next();

    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    if (next_fs.hasClass("cohort_list")){
        let mydiv = document.getElementById("page_wrapper");
        mydiv.classList.add('col-lg-12');
        mydiv.classList.remove('offset-md-2');
        mydiv.classList.remove('col-md-8');
        display_cohorts_for_first_time(); // display groups that the user can join
    }
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
});

$(".previous").click(function(){
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent().parent();
    previous_fs = $(this).parent().parent().prev();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    mydiv = document.getElementById("page_wrapper");
    mydiv.classList.remove('col-lg-12');
    mydiv.classList.add('offset-md-2');
    mydiv.classList.add('col-md-8');
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

$(".submit").click(function(){
    return false;
});


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
$("#imageUpload").change(function() {
    readURL(this);
});

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

function submitRegForm() {
    let first_name, last_name, username, email, password1, password2, study_field, school;
    first_name = document.getElementById('first_name').value;
    last_name = document.getElementById('last_name').value;
    username = document.getElementById('username').value;
    email = document.getElementById('email').value;
    password1 = document.getElementById('password1').value;
    password2 = document.getElementById('password2').value;
    study_field = document.getElementById('study_field').value;
    school = document.getElementById('school').value;
    let selected = get_selected().length;
    if (first_name !== '' && last_name !== '' && username !== ''
        && email !== '' && password1 !== '' && password2 !== ''
        && study_field !== '' && school !== '') {
        if (password1 === password2) {
            if (selected === 0){
                alert('You must select at least one cohort');
            }else{
                document.getElementById('msform').submit();
                return false;
            }
        }else{
            alert('Passwords do not match');
        }
    } else {
        alert('Blank fields detected. Please fill in all required fields');
    }
}

function display_cohorts_for_first_time(){
    $.ajax({
        method: "POST",
        url: "to_join",
        data: {'coh_id':document.getElementById('study_field').value},
        success: function(data) {

            let loader_left = document.getElementById('load_previous');
            let loader_right = document.getElementById('load_next');
            let data_length = data.length;
            if(data_length<4) {
                changeCohortsContent(data, 0, data_length);
                document.getElementById('right-count').value= data_length-1;
                loader_left.style.color = '#F0F8FF';
                loader_right.style.color = '#F0F8FF';
            }else{
                changeCohortsContent(data, 0,3);
                loader_left.style.color = '#F0F8FF';
                loader_right.style.color = 'rgb(32, 207, 255)';
                document.getElementById('right-count').value= 2;
            }
            document.getElementById('left-count').value=0
            if(get_selected().length !==0){
                style_previously_selected_cards(data);
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
                                <img src="${data[i].logo}" alt="Group logo"/>
                                <div class="group-info">
                                    <h4>${ data[i].title }</h4>
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

function load_cohorts(direction){
    $.ajax({
        method: "POST",
        url: "to_join",
        data: {'coh_id':document.getElementById('study_field').value},
        success: function(data) {
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

    });

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