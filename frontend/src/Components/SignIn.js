// SignIn.js

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignIn.css'

const SignIn = () => {
  const navigate = useNavigate();
  const [grant_type, setGrantType]= useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [client_id, setClientID]= useState('');
  const [client_secret, setClientSecret]= useState('');
  const [scope, setScope]= useState('');


  const handleLogin = async () => {
    const formData = new FormData();
    formData.append('grant_type', grant_type);
    formData.append('username', username);
    formData.append('password', password);
    formData.append('scope', scope);
    formData.append('client_id', client_id);
    formData.append('client_secret', client_secret);
    
    try {
      const response = await axios.post('http://localhost:8000/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      });
      console.log(response.data);
      const token = response.data.access_token;
      navigate('/chat',{ state: { token,username } });

    } catch (error) {
      alert('Incorrect username or password');
      console.error('Error during login:', error);
      console.log('Response from server:', error.response.data)
    }
  };

  return (
    <div className="login-form-container">
      <h2>SignIn</h2>
      <div className="input-container">
        <label>UserName:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div className="input-container">
        <label>Password:</label>
        <input type="text" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      
      <button onClick={handleLogin}>SignIn</button>
    </div>
  );
};

export default SignIn;