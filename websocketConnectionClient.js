var ws = new WebSocket("ws://192.168.1.2:8765/"),
messages = document.createElement('ul');
ws.onmessage = function (event) {
var messages = document.getElementsByTagName('ul')[0],
    message = document.createElement('li'),
    content = document.createTextNode(event.data);
message.appendChild(content);
messages.appendChild(message);
};
document.body.appendChild(messages);

audioObj = new Audio("guitar.mp3");
audioObj.addEventListener("canplaythrough", event => {
    audioObj.play();
})
