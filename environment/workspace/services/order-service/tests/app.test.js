const request = require('supertest');
const axios = require('axios');
const app = require('../index');

jest.mock('axios');

describe('Order Service API', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('GET /health', () => {
        it('should return health status', async () => {
            const response = await request(app).get('/health');

            expect(response.status).toBe(200);
            expect(response.body).toEqual({
                status: 'healthy',
                service: 'order-service'
            });
        });
    });

    describe('GET /api/v1/orders', () => {
        it('should return empty orders list', async () => {
            const response = await request(app).get('/api/v1/orders');

            expect(response.status).toBe(200);
            expect(response.body.orders).toEqual([]);
        });

        it('should return all orders', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1' } });

            await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 2 }]
                });

            const response = await request(app).get('/api/v1/orders');

            expect(response.status).toBe(200);
            expect(response.body.orders).toHaveLength(1);
            expect(response.body.orders[0].userId).toBe('user-1');
        });
    });

    describe('GET /api/v1/orders/:id', () => {
        it('should return order by id', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1' } });

            const createResponse = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            const orderId = createResponse.body.id;
            const response = await request(app).get(`/api/v1/orders/${orderId}`);

            expect(response.status).toBe(200);
            expect(response.body.id).toBe(orderId);
            expect(response.body.userId).toBe('user-1');
        });

        it('should return 404 for non-existent order', async () => {
            const response = await request(app).get('/api/v1/orders/nonexistent');

            expect(response.status).toBe(404);
            expect(response.body.error).toBe('Order not found');
        });
    });

    describe('POST /api/v1/orders', () => {
        it('should create order successfully', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1', name: 'John' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1', name: 'Widget' } });

            const orderData = {
                userId: 'user-1',
                items: [{ productId: 'prod-1', quantity: 2 }]
            };

            const response = await request(app)
                .post('/api/v1/orders')
                .send(orderData);

            expect(response.status).toBe(201);
            expect(response.body.userId).toBe('user-1');
            expect(response.body.items).toEqual(orderData.items);
            expect(response.body.status).toBe('pending');
            expect(response.body.id).toBeDefined();
        });

        it('should verify user exists', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1' } });

            await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            expect(axios.get).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/users/user-1')
            );
        });

        it('should verify inventory exists', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1' } });

            await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            expect(axios.get).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/inventory/prod-1')
            );
        });

        it('should fail when user does not exist', async () => {
            axios.get.mockRejectedValueOnce(new Error('User not found'));

            const response = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'invalid-user',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            expect(response.status).toBe(400);
            expect(response.body.error).toBe('User not found');
        });

        it('should fail when product does not exist', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockRejectedValueOnce(new Error('Product not found'));

            const response = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'invalid-product', quantity: 1 }]
                });

            expect(response.status).toBe(400);
            expect(response.body.error).toBe('Product not found');
        });

        it('should handle multiple items', async () => {
            axios.get.mockResolvedValueOnce({ data: { id: 'user-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-1' } });
            axios.get.mockResolvedValueOnce({ data: { id: 'prod-2' } });

            const response = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [
                        { productId: 'prod-1', quantity: 2 },
                        { productId: 'prod-2', quantity: 1 }
                    ]
                });

            expect(response.status).toBe(201);
            expect(response.body.items).toHaveLength(2);
            expect(axios.get).toHaveBeenCalledTimes(3);
        });

        it('should generate unique order IDs', async () => {
            axios.get.mockResolvedValue({ data: { id: 'user-1' } });

            const response1 = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            const response2 = await request(app)
                .post('/api/v1/orders')
                .send({
                    userId: 'user-1',
                    items: [{ productId: 'prod-1', quantity: 1 }]
                });

            expect(response1.body.id).not.toBe(response2.body.id);
        });
    });

    describe('Content-Type', () => {
        it('should return JSON content type', async () => {
            const response = await request(app).get('/health');

            expect(response.headers['content-type']).toMatch(/json/);
        });
    });
});