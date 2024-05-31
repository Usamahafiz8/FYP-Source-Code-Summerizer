document.addEventListener("DOMContentLoaded", function() {
    const webSocketURL = 'ws://localhost:8006/chat'; // Adjust this URL as necessary
    let webSocket = new WebSocket(webSocketURL);

    webSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const activeContentDiv = document.querySelector('.content.active .response-output');
        console.log("data: ", data, data.overwrite, data.text)
        if (data.overwrite) {
            console.log('if condition...')
            activeContentDiv.innerHTML = data.text;  // Use innerHTML since content is now HTML
        } else {
            console.log('else condition...')
            activeContentDiv.innerHTML += data.text;
        }
    };
    


    
    webSocket.onopen = function(event) {
        console.log("Connection opened");
    };

    webSocket.onerror = function(event) {
        console.error("WebSocket Error:", event);
    };

    

    document.querySelectorAll('.query-input').forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                const tabId = this.closest('.content').id;
                const message = this.value;
                webSocket.send(JSON.stringify({ tabId, message }));
                this.value = message; // Clear the input field after sending
            }
        });
    });

    webSocket.onclose = function(event) {
        console.log("WebSocket is closed now.");
    };
});



