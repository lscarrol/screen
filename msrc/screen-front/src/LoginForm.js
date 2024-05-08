import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

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
    <Card className="max-w-md mx-auto mt-8">
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <Input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="flex justify-end">
            <Button type="submit">Login</Button>
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <form onSubmit={handleLoginWithSession}>
          <div className="mb-4">
            <Input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="flex justify-end">
            <Button type="submit">Login with Session</Button>
          </div>
        </form>
      </CardFooter>
      {requires2FA && (
        <CardFooter>
          <CardTitle>2FA Validation</CardTitle>
          <form onSubmit={handleValidate2FA}>
            <div className="mb-4">
              <Input
                type="text"
                placeholder="2FA Code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>
            <div className="flex justify-end">
              <Button type="submit">Validate</Button>
            </div>
          </form>
        </CardFooter>
      )}
    </Card>
  );
};

export default LoginForm;