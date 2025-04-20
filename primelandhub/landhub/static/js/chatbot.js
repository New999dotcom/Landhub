// static/js/chatbot.js
document.addEventListener("DOMContentLoaded", function () {
    const chatbotForm = document.getElementById("chatbot-form");
    const chatbotMessages = document.getElementById("chatbot-messages");

    chatbotForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const userMessage = document.getElementById("chatbot-input").value;
        if (userMessage) {
            const userBubble = `<div class="user-message">${userMessage}</div>`;
            chatbotMessages.innerHTML += userBubble;

            // Simulate bot response
            const botResponse = getBotResponse(userMessage);
            const botBubble = `<div class="bot-message">${botResponse}</div>`;
            chatbotMessages.innerHTML += botBubble;

            document.getElementById("chatbot-input").value = "";
        }
    });

    function getBotResponse(message) {
        // Simple rule-based response
        if (message.toLowerCase().includes("hello")) {
            return "Hi there! How can I assist you today?";
        }
        return "I'm here to help! Please ask a question.";
    }
});
