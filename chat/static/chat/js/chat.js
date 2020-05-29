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
    if(button1.innerHTML === 'Delete Texts'){
        for(let i=0;i<inputs1.length;i++){
            inputs1[i].style.position = 'relative';
            inputs1[i].style.top = '0';

        }
        for(let i=0;i<inputs2.length;i++){
            inputs2[i].style.position = 'relative';
            inputs2[i].style.top = '0';
        }
        button1.innerHTML = 'Exit DeleteView';
        button2.style.position = 'fixed';
        button2.style.right = '140px';
        button2.style.top = '30px';

    }else{
        for(let i=0;i<inputs1.length;i++){
            inputs1[i].checked = false;
            inputs1[i].style.position = 'absolute';
            inputs1[i].style.top = '-9999px';
        }
        for(let i=0;i<inputs2.length;i++){
            inputs2[i].checked = false;
            inputs2[i].style.position = 'absolute';
            inputs2[i].style.top = '-9999px';
        }
        button1.innerHTML = 'Delete Texts';
        button2.style.position = 'absolute';
        button2.style.top = '-9999px';

    }
}

function HandleMessage(data, username, activeContactId){
    // console.log(data, username, active_contact)
    let message = data['message'];
    let author = message['authorUsername'];
    let last_text = data['last_text'];
    let content;
    if(author === username){
        content = `<div class="sent">
                                    <p> ${message.content}</p>
                                    <p class ="time">${message.time}</p>
                                    <input class="delete-sent" type="checkbox" name="to_delete" value="${message.id}"/>
                                </div>`
    }else{
        content = `<div class="replies">
                                        <p> ${message.content}</p>
                                        <p class ="time">${message.time}</p>
                                        <input class="delete-reply" type="checkbox" name="to_delete" value="${message.id}"/>
                                    </div>`;
        markAsRead(message['id']);
    }
    let today = $('#today');
    let container = $('#texts-container')
    if (! today.length){
        container.prepend('<p class="text-center date" >Today</p>');
    }
    container.append(content);
    let container2 = $('#recents-container');
    if(container2.length){
        let helper = $('#recents-helper');
        if (helper.length) {
            helper.remove();
            let new_recent = `<a href="javascript:{window.location.pathname = '/messaging/chat/${roomName}';}" id="chat_init">
                            <div class="card contact">
                                <div class="image" style="float:left; height:100%">
                                    <img src="${message['authorImage']}" alt="image" class="dp"/>
                                    <h4>${message['reportingName']}</h4>
                                    <br />
                                        <small class="last-text" id="${activeContactId}">${last_text}</small>
                                </div>
                            </div>
                        </a>`;
            let button = '<p id="delete-initiator" onclick="toggle_delete_view()">Delete Texts</p>';
            container2.append(new_recent);
            $('#chat-panel-heading').append(button);
        }
        else
        {
            let active_contact = $('#'+activeContactId);
            active_contact.text(last_text);
        }
    }
}

function markAsRead(id){
    $.ajax({
        method: "POST",
        url: "/messaging/mark-as-read",
        data: {
            'msgId':id
        },
        success: function(data) {
            console.log('Marked as read')
        }
    });
}