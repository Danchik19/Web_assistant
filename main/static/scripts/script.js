const chatInput = document.querySelector(".chat-input textarea");
const sendLetter = document.querySelector(".letter");
const sendMicrophone = document.querySelector(".microphone");
const chatbox = document.querySelector(".chatbox");

let UserMessage = "";
const triggers = ["еж", "ежик", "ёж", "ёжик"];
const StopWord = "пока";
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

const generateResponse = (incomingChatLi) => {
  const csrftoken = getCookie("csrftoken");
  const requestURL = "https://f749-158-46-32-12.ngrok-free.app"; // http://127.0.0.1:8000/
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
    GetVoice(data.message["content"]);
    messageElement.textContent = data.message["content"];
  }).catch((error) => {
    messageElement.classList.add("error");
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

const ProcessingMessage = () => {
  chatInput.value = "";
  chatInput.style.height = `${inputInitHight}px`;

  chatbox.appendChild(createChatLi(UserMessage, "outgoing"));
  const incomingChatLi = createChatLi("Думает...", "incoming")
  chatbox.appendChild(incomingChatLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    generateResponse(incomingChatLi);
  }, 600);
}

window.speechSynthesis.onvoiceschanged = function() {
  window.speechSynthesis.getVoices();
};

const GetVoice = (text) => {
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.voice = window.speechSynthesis.getVoices()[1];
  window.speechSynthesis.speak(utterance);
}

const InternalRecognizer = () => {
  const InRecognizer = new SpeechRecognition();
  InRecognizer.interimResults = true;
  InRecognizer.lang = "ru-RU";
  var check = false;
  
  InRecognizer.start();

  InRecognizer.onresult = (e) => {
    var result = e.results[e.resultIndex];
    if (!result.isFinal) {
      if (result[0].transcript.toLowerCase() === StopWord) {
        check = true;
        return;
      }
      else chatInput.value = result[0].transcript;
    }
  };

  InRecognizer.onend = () => {
    if (!check) {
      if (chatInput.value) {
        UserMessage = chatInput.value;
        ProcessingMessage();
      }
      InRecognizer.start();
    }
    else GetVoice("Пока, мой друг.");
  };
}

const OuterRecognizer = () => {
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const OutRecognizer = new SpeechRecognition();
  OutRecognizer.interimResults = false;
  OutRecognizer.lang = "ru-RU";
  var TempResult = "";
  
  OutRecognizer.start();

  OutRecognizer.onresult = (e) => {
    var result = e.results[e.resultIndex];
    if (result.isFinal) {
      TempResult = result[0].transcript.toLowerCase().slice(0, -1);
    }
  };

  OutRecognizer.onend = () => {
    if (triggers.includes(TempResult)) {
      GetVoice("Я здесь");
      InternalRecognizer();
    }
    else if (!TempResult) GetVoice("Ты что-то хочешь мне сказать? Не бойся, я никому не расскажу.");
  };
}

const handleChat = () => {
  UserMessage = chatInput.value.trim();
  if (!UserMessage) return;
  ProcessingMessage();
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
sendMicrophone.addEventListener("click", OuterRecognizer);
