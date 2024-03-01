window.onload = function() {
    var sendButton = document.getElementById("send-btn");
    var messageInput = document.getElementById("message-input");
    var messagesContainer = document.getElementById("messages");
  
    sendButton.addEventListener("click", function() {
      var message = messageInput.value;
      if (message !== "") {
        var newMessage = document.createElement("div");
        newMessage.className = "message sent";
        newMessage.innerHTML = '<span class="username">Me: </span><span class="content">' + message + '</span>';
        messagesContainer.appendChild(newMessage);
        messageInput.value = "";
      }
    });
  };