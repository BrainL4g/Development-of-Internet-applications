import React, { useState, useEffect } from 'react';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/chat/ws');

    socket.onopen = () => {
      console.log('WebSocket подключён');
    };

    socket.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };

    socket.onclose = () => {
      console.log('WebSocket отключён');
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  const sendMessage = (e) => {
    e.preventDefault();
    if (ws && message.trim()) {
      ws.send(message);
      setMessage('');
    }
  };

  return (
    <div className="chat-section">
      <h2>Чат поддержки</h2>
      <div className="messages">
        {messages.length === 0 ? (
          <p>Сообщений пока нет. Напишите первым!</p>
        ) : (
          messages.map((msg, idx) => <p key={idx}><strong>{msg}</strong></p>)
        )}
      </div>
      <form onSubmit={sendMessage} className="chat-form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Введите сообщение..."
          required
        />
        <button type="submit">Отправить</button>
      </form>
    </div>
  );
}

export default Chat;