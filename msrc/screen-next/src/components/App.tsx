import React, { useState, useRef } from 'react';
import LoginForm from './LoginForm';
import CategoriesList from './CategoriesList';
import { CSSTransition } from 'react-transition-group';

function App() {
  const [username, setUsername] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const loginFormRef = useRef(null);
  const categoriesListRef = useRef(null);

  const handleLogin = (username: string) => {
    setUsername(username);
    setIsLoggedIn(true);
  };

  return (
    <div className="container mx-auto">
      <CSSTransition
        in={!isLoggedIn}
        timeout={300}
        classNames="fade"
        unmountOnExit
        nodeRef={loginFormRef}
      >
        <div ref={loginFormRef}>
          <LoginForm onLogin={handleLogin} />
        </div>
      </CSSTransition>
      <CSSTransition
        in={isLoggedIn}
        timeout={300}
        classNames="fade"
        unmountOnExit
        nodeRef={categoriesListRef}
      >
        <div ref={categoriesListRef}>
          <CategoriesList username={username} />
        </div>
      </CSSTransition>
    </div>
  );
}

export default App;