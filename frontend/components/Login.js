import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const Login = ({ setToken }) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/login`, data);
      setToken(response.data.token);
      navigate('/wallets');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username')} placeholder="Username" />
      <input {...register('password')} type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;