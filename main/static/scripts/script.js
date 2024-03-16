const chatInput = document.querySelector(".chat-input textarea");
const sendLetter = document.querySelector(".letter");
const sendMicrophone = document.querySelector(".microphone");
const chatbox = document.querySelector(".chatbox");

let userMessage;
const inputInitHight = chatInput.scrollHeight;


const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent = className === "outgoing" ?  `<p></p>` : `<span class="hedgehog"><img src="static/images/hedgehog.png", alt="img-hedgehog"/></span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
}


function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = jQuery.trim(cookies[i]);
          if (cookie.startsWith(name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }

  return cookieValue;
}


const generateResponse = (incomingChatLi) => {
  const csrftoken = getCookie("csrftoken");
  const requestURL = "http://127.0.0.1:8000/";
  const messageElement = incomingChatLi.querySelector("p");
  
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      messages: [{role: "Vasya", content: userMessage}]
    })
  }

  fetch(requestURL, options).then(res => res.json()).then(data => {
    messageElement.textContent = data.messages[0].content;
  }).catch((error) => {
    messageElement.classList.add("error");
    messageElement.textContent = "Упс! Что-то пошло не так. Попробуй ещё раз.";
  }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}


const microphoneChat = () => {

}


const handleChat = () => {
  userMessage = chatInput.value.trim();
  if (!userMessage) return;
  chatInput.value = "";
  chatInput.style.height = `${inputInitHight}px`;

  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);


  setTimeout(() => {
    const incomingChatLi = createChatLi("Думает...", "incoming")
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 600);
}


chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});


chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});


sendLetter.addEventListener("click", handleChat);
sendMicrophone.addEventListener("click", microphoneChat);
