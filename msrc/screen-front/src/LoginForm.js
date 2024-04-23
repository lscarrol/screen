import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [requires2FA, setRequires2FA] = useState(false);
  const [code, setCode] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username,
        password,
      });
      if (response.data.requires_2fa) {
        setRequires2FA(true);
      } else {
        onLogin(username);
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLoginWithSession = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login_with_session', {
        username,
      });
      if (response.data.success) {
        onLogin(username);
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
      const response = await axios.post('http://127.0.0.1:5000/api/validate_2fa', {
        username,
        password,
        code,
      });
      if (response.data.success) {
        onLogin(username);
      } else {
        console.error('2FA validation failed:', response.data.message);
      }
    } catch (error) {
      console.error('2FA validation failed:', error);
    }
  };

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={handleLogin}>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="mb-4">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="flex items-center justify-between">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Login
          </button>
        </div>
      </form>
      <h2 className="text-2xl font-bold mt-8 mb-4">Login with Session</h2>
      <form onSubmit={handleLoginWithSession}>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="flex items-center justify-between">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Login with Session
          </button>
        </div>
      </form>
      {requires2FA && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">2FA Validation</h2>
          <form onSubmit={handleValidate2FA}>
            <div className="mb-4">
              <input
                type="text"
                placeholder="2FA Code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>
            <div className="flex items-center justify-between">
              <button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Validate
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default LoginForm;