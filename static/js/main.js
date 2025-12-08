document.addEventListener('DOMContentLoaded', function () {
    // Mood Selection Logic in Dashboard
    const moodBtns = document.querySelectorAll('.mood-btn');
    const moodInput = document.getElementById('mood-score');

    moodBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            moodBtns.forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
            moodInput.value = this.dataset.score;
        });
    });

    // Chat Logic
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        const chatInput = document.getElementById('chat-input');
        const messagesContainer = document.getElementById('chat-messages');

        function appendMessage(text, sender, isCrisis = false) {
            const div = document.createElement('div');
            div.classList.add('message', sender);
            if (isCrisis) div.classList.add('crisis');
            div.textContent = text;
            messagesContainer.appendChild(div);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        chatForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            appendMessage(message, 'user');
            chatInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });

                const data = await response.json();
                appendMessage(data.response, 'ai', data.is_crisis);
            } catch (error) {
                console.error('Error:', error);
                appendMessage("Sorry, I'm having trouble connecting right now.", 'ai');
            }
        });
    }
});
