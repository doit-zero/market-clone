function displayMsg(msg) {
    const ul = document.querySelector("#msg-ul");
    const li = document.createElement("li")
    li.innerText = msg.content;
    ul.appendChild(li);
}


async function readMsg() {
    const res = await fetch("/msg");
    const jsonRes = await res.json();
    const ul = document.querySelector("#msg-ul");
    ul.innerHTML = " ";
    jsonRes.forEach(displayMsg);
}


async function createMsg (value){
    const res = await fetch("/msg",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            id : new Date().getTime(),
            content : value,
        }),
    });
}

function handleMsg(event) {
    event.preventDefault();
    const input = document.querySelector("#msg-input");
    createMsg(input.value);
    input.value = " ";
}


const form = document.querySelector("#msg-form");
form.addEventListener("submit",handleMsg)


readMsg();