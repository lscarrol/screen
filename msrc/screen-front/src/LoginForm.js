import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LoginForm = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [requires2FA, setRequires2FA] = useState(false);
  const [code, setCode] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', { username, password });

      if (response.data.requires_2fa) {
        setRequires2FA(true);
      } else {
        navigate('/main');
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLoginWithSession = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login_with_session', { username });

      if (response.data.success) {
        navigate('/main');
      } else {
        console.error('Login with session failed:', response.data.message);
      }
    } catch (error) {
      console.error('Login with session failed:', error);
    }
  };

  const handleValidate2FA = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/validate_2fa', { username, password, code });

      if (response.data.success) {
        navigate('/main');
      } else {
        console.error('2FA validation failed:', response.data.message);
      }
    } catch (error) {
      console.error('2FA validation failed:', error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>

      <h2>Login with Session</h2>
      <form onSubmit={handleLoginWithSession}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button type="submit">Login with Session</button>
      </form>

      {requires2FA && (
        <div>
          <h2>2FA Validation</h2>
          <form onSubmit={handleValidate2FA}>
            <input
              type="text"
              placeholder="2FA Code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
            <button type="submit">Validate</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default LoginForm;