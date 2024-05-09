<script>
  const socket = io('http://localhost:5000');  // Update the URL to match your WebSocket server

  socket.on('connect', function() {
    console.log('Connected to server!');
  });

  socket.on('status', function(data) {
    console.log(data);
  });

  socket.on('new_token', function(token) {
    const container = document.querySelector('.right_side_text');
    container.textContent += token;  // Append each token to the text content
  });
</script>
