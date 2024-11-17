import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ token, setToken }) => {
  const handleLogout = () => {
    setToken(null);
  };

  return (
    <header>
      <nav>
        <Link to="/wallets">Wallets</Link>
        <Link to="/order">Order</Link>
        <Link to="/order-book">Order Book</Link>
        {token ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/">Login</Link>
        )}
      </nav>
    </header>
  );
};

export default Header;