const net = require('net');

const LISTEN_PORT = 9223;
const TARGET_PORT = 9222;
const TARGET_HOST = '127.0.0.1';

const server = net.createServer((localSocket) => {
  const remoteSocket = net.createConnection({
    port: TARGET_PORT,
    host: TARGET_HOST
  });

  localSocket.pipe(remoteSocket).pipe(localSocket);

  localSocket.on('error', (err) => {
    // Ignore common connection reset errors
  });

  remoteSocket.on('error', (err) => {
    // Ignore common connection reset errors
  });
});

server.listen(LISTEN_PORT, '0.0.0.0', () => {
  console.log(`Windows port forwarder listening on 0.0.0.0:${LISTEN_PORT} -> ${TARGET_HOST}:${TARGET_PORT}`);
});
