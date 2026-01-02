/**
 * Order Service - Manages customer orders
 */
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const orders = {};
const PORT = process.env.PORT || 3000;
const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://user-service:5000';
const INVENTORY_SERVICE_URL = process.env.INVENTORY_SERVICE_URL || 'http://inventory-service:8080';

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'order-service' });
});

app.get('/api/v1/orders', (req, res) => {
    res.json({ orders: Object.values(orders) });
});

app.get('/api/v1/orders/:id', (req, res) => {
    const order = orders[req.params.id];
    if (order) {
        res.json(order);
    } else {
        res.status(404).json({ error: 'Order not found' });
    }
});

app.post('/api/v1/orders', async (req, res) => {
    try {
        const { userId, items } = req.body;

        // Verify user exists
        await axios.get(`${USER_SERVICE_URL}/api/v1/users/${userId}`);

        // Check inventory
        for (const item of items) {
            await axios.get(`${INVENTORY_SERVICE_URL}/api/v1/inventory/${item.productId}`);
        }

        const orderId = Date.now().toString();
        const order = { id: orderId, userId, items, status: 'pending' };
        orders[orderId] = order;

        res.status(201).json(order);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Order service listening on port ${PORT}`);
});

module.exports = app;