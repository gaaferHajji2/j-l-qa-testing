const { WebSocketServer } = require('ws');

const PORT = process.env.WS_PORT || 8080;
const wss = new WebSocketServer({ 
  port: PORT,
  // Performance: Disable per-message compression for local/LAN use.
  // Compression adds significant CPU overhead with minimal benefit on fast networks.
  perMessageDeflate: false 
});

console.log(`🚀 WebSocket server running on ws://localhost:${PORT}`);

wss.on('connection', (ws, req) => {
  const clientIp = req.socket.remoteAddress;
  console.log(`⚡ Client connected: ${clientIp}`);

  // Attach metadata to the socket for tracking
  ws.isAlive = true;
  ws.clientId = Math.random().toString(36).substring(7);

  // --- Heartbeat / Ping-Pong ---
  // Prevents stale connections from consuming resources
  ws.on('pong', () => { ws.isAlive = true; });

  // --- Message Handling ---
  ws.on('message', (rawData, isBinary) => {
    try {
      if (isBinary) {
        // Handle binary data (e.g., protobuf, msgpack, images)
        console.log(`📦 Binary message received: ${rawData.length} bytes`);
        // Echo back for testing
        ws.send(rawData); 
      } else {
        // Handle text/JSON messages
        const message = JSON.parse(rawData.toString());
        
        // Example: Simple echo or routing logic
        switch (message.type) {
          case 'ping':
            ws.send(JSON.stringify({ type: 'pong', ts: Date.now() }));
            break;
          case 'broadcast':
            // Efficient broadcast to all other clients
            ws.send(rawData.toString());
            break;
          default:
            ws.send(JSON.stringify({ type: 'echo', data: message }));
        }
      }
    } catch (err) {
      console.error('❌ Message processing error:', err.message);
      ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
    }
  });

  ws.on('close', () => {
    console.log(`🔌 Client disconnected: ${ws.clientId}`);
  });

  ws.on('error', (err) => {
    console.error(`💥 Socket error [${ws.clientId}]:`, err.message);
  });

  // Send initial welcome message
  ws.send(JSON.stringify({ 
    type: 'welcome', 
    clientId: ws.clientId,
    serverTime: Date.now() 
  }));
});

// --- Graceful Shutdown ---
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down gracefully...');
  wss.clients.forEach((ws) => ws.close(1001, 'Server shutting down'));
  wss.close(() => {
    console.log('✅ Server closed.');
    process.exit(0);
  });
});