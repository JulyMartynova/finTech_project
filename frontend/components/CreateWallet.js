import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const CreateWallet = ({ token }) => {
  const { handleSubmit } = useForm();
  const history = useHistory();

  const createHotWallet = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/wallets/create/hot_wallet`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      history.push('/wallets');
    } catch (error) {
      console.error(error);
    }
  };

  const createColdWallet = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/wallets/create/cold_wallet`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      history.push('/wallets');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Create Wallet</h2>
      <button onClick={createHotWallet}>Create Hot Wallet</button>
      <button onClick={createColdWallet}>Create Cold Wallet</button>
    </div>
  );
};

export default CreateWallet;