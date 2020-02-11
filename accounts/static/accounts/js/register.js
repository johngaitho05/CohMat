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


// profile picture preview
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
    cohort = document.getElementById(id);
    if (cohort.style.border === "thick solid green"){
        cohort.style.border = "1px solid rgba(0,0,0,.125)";
    }else{
        cohort.style.border = "thick solid green";
    }
}




//$(function () {
//    // Enables popover
//    $("[data-toggle=popover]").popover({
//        
//    });
//
//        // set a flag when you move from button to popover
//        // dirty but only way I could think of to prevent
//        // closing the popover when you are navigate across
//        // the white space between the two
//        $popover.data('popover').tip().mouseenter(function () {
//            overPopup = true;
//        }).mouseleave(function () {
//            overPopup = false;
//            $popover.popover('hide');
//
//    }).mouseout(function (e) {
//        // on mouse out of button, close the related popover
//        // in 200 milliseconds if you're not hovering over the popover
//        var $popover = $(this);
//        setTimeout(function () {
//            if (!overPopup) {
//                $popover.popover('hide');
//            }
//        }, 5000);
//    });
//});

