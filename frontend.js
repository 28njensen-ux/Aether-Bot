// --- DOM Elements ---
const sendBtn = document.getElementById('send-btn');
const messageInput = document.getElementById('message-input');
const messageContainer = document.querySelector('#right .messages');

// --- Rate-limiting ---
let canSend = true; // user can send a message

// --- Function to append a message ---
function appendMessage(content, sender = 'user') {
    const prefix = sender === 'user' ? "You: " : "AI: ";
    const msg = document.createElement('p');
    msg.textContent = `${prefix}${content}`;
    
    messageContainer.prepend(msg); // prepend because flex-direction: column-reverse
    
    // Scroll to bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// --- Send message function ---
function sendMessage() {
    if (!canSend) return; // prevent spamming
    const userMessage = messageInput.value.trim();
    if (!userMessage) return;

    appendMessage(userMessage, 'user'); // show user message
    messageInput.value = ''; // clear input

    canSend = false;          // block further sends
    sendBtn.disabled = true;  // visually disable button

    // Mock AI response (replace this with real backend later)
    setTimeout(() => {
        const aiReply = `AI says: ${userMessage.split('').reverse().join('')}`; // demo response
        appendMessage(aiReply, 'bot');

        // Re-enable sending after cooldown
        canSend = true;
        sendBtn.disabled = false;
    }, 500); // 500ms delay to simulate AI thinking
}

// --- Event Listeners ---
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});
