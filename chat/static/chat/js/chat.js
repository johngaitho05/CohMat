function delete_texts(){
    let inputs1 = document.getElementsByClassName('delete-sent');
    let inputs2 = document.getElementsByClassName('delete-reply');
    let checked = 0;
    for(let i=0;i<inputs1.length;i++){
        if (inputs1[i].checked === true){
            checked += 1;
        }
    }
    for(let i=0;i<inputs2.length;i++){
        if (inputs2[i].checked === true){
            checked += 1;
        }
    }
    if(checked !==0){
        document.getElementById('delete-form').submit();
    }else{
        alert("You have not selected any text");
    }
}
function toggle_delete_view(){
    let button1 = document.getElementById('delete-initiator');
    let button2 = document.getElementById('delete-button');
    let inputs1 = document.getElementsByClassName('delete-sent');
    let inputs2 = document.getElementsByClassName('delete-reply');
    if(button1.innerHTML === 'DeleteView'){
        for(let i=0;i<inputs1.length;i++){
            inputs1[i].style.position = 'relative';
            inputs1[i].style.top = '0';

        }
        for(let i=0;i<inputs2.length;i++){
            inputs2[i].style.position = 'relative';
            inputs2[i].style.top = '0';
        }
        button1.innerHTML = 'Exit DeleteView';
        button2.style.position = 'unset';
    }else{
        for(let i=0;i<inputs1.length;i++){
            inputs1[i].checked = false;
            inputs1[i].style.position = 'absolute';
        }
        for(let i=0;i<inputs2.length;i++){
            inputs2[i].checked = false;
            inputs2[i].style.position = 'absolute';
        }
        button2.style.position = 'absolute';
        button1.innerHTML = 'DeleteView'

    }
}

