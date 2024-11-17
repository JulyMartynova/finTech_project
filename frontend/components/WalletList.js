import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const WalletList = ({ token }) => {
  const [wallets, setWallets] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWallets = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/wallets`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setWallets(response.data);
      } catch (error) {
        setError(error.response.data.message);
      }
    };
    fetchWallets();
  }, [token]);

  return (
    <div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <h2>Your Wallets</h2>
      <ul>
        {wallets.map(wallet => (
          <li key={wallet.id}>
            {wallet.address} ({wallet.is_cold ? 'Cold' : 'Hot'})
          </li>
        ))}
      </ul>
      <Link to="/wallets/create">Create New Wallet</Link>
    </div>
  );
};

export default WalletList;