const chatInput = document.querySelector(".chat-input textarea");
const sendLetter = document.querySelector(".letter");
const sendMicrophone = document.querySelector(".microphone");
const chatbox = document.querySelector(".chatbox");

let UserMessage = "";
const myURL = "https://924a-158-46-32-12.ngrok-free.app"; // http://127.0.0.1:8000/
const inputInitHight = chatInput.scrollHeight;

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

const MakeRequest = (incomingChatLi, IsHandle) => {
  const csrftoken = getCookie("csrftoken");
  const requestURL = myURL;
  const messageElement = incomingChatLi.querySelector("p");
  
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({
      message: {role: "Vasya", content: UserMessage}
    })
  }

  fetch(requestURL, options).then(res => res.json()).then(data => {
    if (!IsHandle)
      GetVoice(data.message["content"]);
    messageElement.textContent = data.message["content"];
  }).catch((error) => {
    messageElement.classList.add("error")
    if (!IsHandle)
      GetVoice("Упс! Что-то пошло не так. Попробуй ещё раз.");
    messageElement.textContent = "Упс! Что-то пошло не так. Попробуй ещё раз.";
  }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent = className === "outgoing" ?  `<p></p>` : `<span class="hedgehog"><img src="static/images/hedgehog.png", alt="img-hedgehog"/></span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
}

const ProcessingMessage = (IsHandle="") => {
  chatInput.value = "";
  chatInput.style.height = `${inputInitHight}px`;

  chatbox.appendChild(createChatLi(UserMessage, "outgoing"));
  const incomingChatLi = createChatLi("Думает...", "incoming")
  chatbox.appendChild(incomingChatLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    MakeRequest(incomingChatLi, IsHandle);
  }, 600);
}

window.speechSynthesis.onvoiceschanged = function() {
  window.speechSynthesis.getVoices();
};

const GetVoice = (text) => {
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  let lst = window.speechSynthesis.getVoices();
  utterance.voice = lst[lst.length - 1];
  window.speechSynthesis.speak(utterance);
}

const Recognizer = () => {
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const Recognizer = new SpeechRecognition();
  Recognizer.interimResults = true;
  Recognizer.lang = "ru-RU";
  
  Recognizer.start();

  Recognizer.onresult = (e) => {
    var result = e.results[e.resultIndex];
    if (!result.isFinal)
      chatInput.value = result[0].transcript;
  };

  Recognizer.onend = () => {
    UserMessage = chatInput.value.trim();
    if (!UserMessage) return;
    ProcessingMessage();
  };
}

const handleChat = () => {
  UserMessage = chatInput.value.trim();
  if (!UserMessage) return;
  ProcessingMessage("handle");
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
sendMicrophone.addEventListener("click", Recognizer);
