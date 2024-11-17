import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Order = ({ token }) => {
    const { register, handleSubmit } = useForm();
    const [wallets, setWallets] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Загрузка списка кошельков
        const fetchWallets = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_API_URL}/wallets`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setWallets(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchWallets();
    }, [token]);

    const onSubmit = async (data) => {
        try {
            const response = await axios.post(`${process.env.REACT_API_URL}/order`, data, {
                headers: { Authorization: `Bearer ${token}` }
            });
            console.log(response.data);
            navigate('/order-book');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('type')} placeholder="Type (buy/sell)" />
            <input {...register('price')} placeholder="Price" />
            <input {...register('quantity')} placeholder="Quantity" />
            <select {...register('wallet_id')}>
                {wallets.map(wallet => (
                    <option key={wallet.id} value={wallet.id}>{wallet.name}</option>
                ))}
            </select>
            <button type="submit">Submit</button>
        </form>
    );
};

export default Order;