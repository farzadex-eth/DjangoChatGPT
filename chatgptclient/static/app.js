const promptForm = document.getElementById("prompt-form");
const promptBtn = document.getElementById("prompt-btn");
let chatbox = document.getElementById("chatbox");

var converter = new showdown.Converter();

// get csrf token from cookies
const getCsrf = () => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; csrftoken=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return "";
}

// get last 10 messages in history for the user
const getLastTen = async () => {
    chatbox.innerHTML = "<h5>Loading Your Messages ...</h5>"
    const formData = new FormData();
    formData.append("history", 10);
    formData.append("csrfmiddlewaretoken", getCsrf());
    const formRequest = new URLSearchParams(formData);
    fetch('/', {
        method: 'post',
        body: formRequest,
    })
        .then(resp => resp.json())
        .then(data => {
            if(data.error) {
                chatbox.innerHTML = `<div class="message"><p class="bubble error">🚫: ${data.msg}</p></div>`;
            } else {
                chatbox.innerHTML = "";
                data.history.forEach((msg) => {
                    chatbox.innerHTML += `<div class="message"><div class="bubble ${msg['role'] === 'user' ? 'right' : 'left'}">${msg['role'] === 'user' ? '🙂' : '🤖'}: ${converter.makeHtml(msg['content'])}</div></div>`;
                    chatbox.scrollTop = chatbox.scrollHeight;
                })
            }
        })
}

// submit the prompt and wait for the reply
const submitChat = async (e) => {
    e.preventDefault();
    const formData = new FormData(promptForm);
    console.log(formData)
    const formRequest = new URLSearchParams(formData);
    chatbox.innerHTML += `<div class="message"><div class="bubble right">🙂: ${formData.get("prompt")}</div></div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
    promptForm.reset();
    fetch('/', {
        method: 'post',
        body: formRequest,
    })
        .then(resp => resp.json())
        .then(data => {
            if (data.error) {
                console.log(data.msg);
                chatbox.innerHTML += `<div class="message"><div class="bubble error">🚫: ${data.msg}</div></div>`;
            } else {
                chatbox.innerHTML += `<div class="message"><div class="bubble left">🤖: ${converter.makeHtml(data.response)}</div></div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        })
}

//load the history
document.addEventListener("DOMContentLoaded", getLastTen)

//submit the prompt
promptForm.addEventListener("submit", submitChat);
promptBtn.addEventListener("click", submitChat);