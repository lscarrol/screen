import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { motion } from 'framer-motion';
import { ChevronRightIcon } from '@heroicons/react/solid';

interface LoginFormProps {
  onLogin: (username: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [code, setCode] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [requires2FA, setRequires2FA] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login', {
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

  const handleValidate2FA = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/validate_2fa', {
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
    <div className="bg-white min-h-screen flex">
      <div className="w-1/2 flex justify-center items-center p-8">
        <motion.div
          className="max-w-md w-full shadow-lg rounded-lg p-8"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-4xl font-bold mb-4">Welcome to screen</h1>
          <p className="text-lg">
            Screen is a cutting-edge tool designed to revolutionize the way you capture, organize, and share your screenshots. With its intuitive interface and powerful features, Screen streamlines your workflow and enhances productivity.
          </p>
          <p className="text-lg mt-4">
            Whether you&apos;re a designer, developer, or content creator, Screen provides a seamless experience for managing your visual assets. Say goodbye to the hassle of scattered screenshots and hello to a centralized hub that keeps your images organized and easily accessible.
          </p>
        </motion.div>
      </div>
      <div className="w-1/2 flex justify-center items-center">
        <motion.div
          className="max-w-md w-full"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          <Card className="rounded-lg shadow-lg">
            <CardHeader>
              <CardTitle>Sign in with iCloud</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLogin}>
                <div className="mb-4 relative">
                  <Input
                    type="text"
                    placeholder="Email"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="pr-10"
                  />
                  <button type="submit" className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <ChevronRightIcon className="w-5 h-5 text-gray-400" />
                  </button>
                </div>
                {showPassword && (
                  <motion.div
                    className="mb-4"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4 }}
                  >
                    <Input
                      type="password"
                      placeholder="Password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </motion.div>
                )}
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default LoginForm;