$(document).ready(function() {
    function typewriterEffect(message, container) {
        var index = 0;
      function type() {
        container.append(message[index]);
        index++;

       
  
        if (index < message.length) {
          setTimeout(type, 50);
        }
      }
  
      type();
    }

    // Lắng nghe sự kiện khi form được submit
    $("#messageForm").submit(function(event) {
      event.preventDefault(); // Chặn sự kiện mặc định của form submission
      var formData = $("#messageForm").serialize();

      $.ajax({
        type: "POST",
        url: $("#messageForm").attr("action"),
        data: formData,
        success: function(response) {
          // Xử lý phản hồi từ Flask
          console.log(response);

          // Phân tách giá trị
          var values = response.split("|");
          var user = values[0];
          var chatbot = values[1];

          // Hiển thị tin nhắn người dùng
          if (user) {
            // Tạo phần tử container cho tin nhắn của người dùng
            var userWrapper = $("<div class='message user-message'></div>");
            var username = $("#username_avatar").data("username");
        
            // Tạo phần tử hình ảnh của người dùng
            var userImage = $('<div class="box-avatar"><div class="cricle-avarta"><h5>'+ username.charAt(0)+'</h5></div></div>');
        
            // Thêm hình ảnh vào userWrapper
            userWrapper.append(userImage);
        
            // Tạo phần tử chứa tin nhắn của người dùng
            var userMessage = $("<p>" + user + "</p>");
        
            // Thêm tin nhắn vào userWrapper
            userWrapper.append(userMessage);
        
            // Thêm userWrapper vào #chatbox
            $("#chatbox").append(userWrapper);
        }

          // Hiển thị tin nhắn của chatbot với hiệu ứng gõ chữ
          if (chatbot) {
            // Tạo container mới cho tin nhắn của chatbot
            var chatbotWrapper = $("<div class='message chatbot-message'></div>");
            var chatbotImage = $('<div class="icon-chatbot"><img class="icon-chatbot-img" src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png"></div>');
            var chatbotContainer = $("<p></p>");

            // Thêm hình ảnh và văn bản vào container
            chatbotWrapper.append(chatbotImage);
            chatbotWrapper.append(chatbotContainer);
            $("#chatbox").append(chatbotWrapper);

            // Áp dụng hiệu ứng gõ chữ cho văn bản của chatbot
            typewriterEffect(chatbot, chatbotContainer);
        }

          // Xóa nội dung của ô input sau khi gửi tin nhắn
          $("#text").val("");
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
});

$(document).ready(function () {
    $("#cleanButton").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/clean_messages",
            success: function (response) {
                console.log(response.message);
                $("#chatbox").empty();  
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});

$(document).ready(function() {
    function autoScrollToBottom() {
      var chatbox = $('#chatbox');
      chatbox.scrollTop(chatbox.prop('scrollHeight'));
    }

    // Lắng nghe sự kiện khi nút gửi được nhấn
    $("#sendMessage").on("click", function() {

      autoScrollToBottom();


    });

  

  });