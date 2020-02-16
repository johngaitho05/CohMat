//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
    if(animating) return false;
    animating = true;
	
    current_fs = $(this).parent();
    next_fs = $(this).parent().next();
	
    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
    //show the next fieldset
    next_fs.show(); 
    if (next_fs.hasClass("cohort_list")){
        mydiv = document.getElementById("page_wrapper");
        mydiv.classList.add('col-lg-12');
        mydiv.classList.remove('offset-md-2');
        mydiv.classList.remove('col-md-8');   
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
	
    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();
	
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
    if (cohort.style.border === "thick solid green") {
        cohort.style.border = "1px solid rgba(0,0,0,.125)";
        to_check.checked = false;
    } else {
        cohort.style.border = "thick solid green";
        to_check.checked = true;
    }
}

function submitRegForm() {
    let first_name, last_name, username, email, password1, password2, study_field, cohorts;
    first_name = document.getElementById('first_name').value;
    last_name = document.getElementById('last_name').value;
    username = document.getElementById('username').value;
    email = document.getElementById('email').value;
    password1 = document.getElementById('password1').value;
    password2 = document.getElementById('password2').value;
    study_field = document.getElementById('study_field').value;
    cohorts = document.getElementsByClassName('cohort-item');
    let count = 0;
    console.log(cohorts.length);
    for (let i=0; i<cohorts.length;i++){
        let cohort_id = cohorts[i].id.toString();
        let checkbox_id = 'check-'.concat(cohort_id);
        let checkbox = document.getElementById(checkbox_id);
        if (checkbox.checked === true){
            count += 1;
            break;
        }
    }
    let selected = count;
    if (first_name !== '' && last_name !== '' && username !== ''
        && email !== '' && password1 !== '' && password2 !== ''
        && study_field !== '') {
        if (password1 === password2) {
            if (selected === 0){
                alert('You must select at least one cohort');
                // document.getElementById('banner').innerHTML = 'You must select at least one cohort';
            }else{
                 document.getElementById('msform').submit();
            }
        }else{
            alert('Passwords do not match');
            // document.getElementById('banner').innerHTML = 'Passwords do not match';
        }
    } else {
        alert('Blank fields detected. Please fill in all required fields');
        // document.getElementById('banner').innerHTML = 'Blank fields detected!';
        // document.getElementById('banner').style.
    }
}

