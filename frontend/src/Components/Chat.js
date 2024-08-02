import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

const Chat = () => {
  const location = useLocation();
  console.log("a");
  console.log(location.state);
  console.log("a");
  const { token, username } = location.state;

  const [message, setMessage] = useState('');
  const [receiver, setReceiver] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (token && username) {
      getMessages(username, token);
    } else {
      console.error('No token or username found in navigation state');
    }
  }, [token, username]);

  const getMessages = async (username, token) => {
    try {
      const response = await axios.get(`${API_URL}/messages/${username}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (!token || !username) {
      console.error('No token or sender found in navigation state');
      return;
    }

    try {
      await axios.post(
        `${API_URL}/messages/`,
        {
          sender: username,
          receiver,
          content: message,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessage('');
      setReceiver('');
      getMessages(username, token); // Refresh messages after sending
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div>
      <h1>Chat</h1>
      <div>
        <input
          type="text"
          placeholder="Receiver"
          value={receiver}
          onChange={(e) => setReceiver(e.target.value)}
        />
        <textarea
          placeholder="Type your message here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send Message</button>
      </div>
      <div>
        <h2>Received Messages</h2>
        <ul>
          {messages.map((msg) => (
            <li key={msg[0]}>
              <p>Sender : {msg[1]}</p>
              <p>Message : {msg[3]}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Chat;
