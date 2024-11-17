import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OrderBook = ({ token }) => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrderBook = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_API_URL}/order_book`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setOrders(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchOrderBook();
    }, [token]);

    return (
        <div>
            <h2>Order Book</h2>
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>User ID</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map((order, index) => (
                        <tr key={index}>
                            <td>{order.type}</td>
                            <td>{order.price}</td>
                            <td>{order.quantity}</td>
                            <td>{order.user_id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OrderBook;