// packages/shared/src/api/ordersApi.js

import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const ordersApi = createApi({
    reducerPath: 'ordersApi',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://127.0.0.1:5000/api/',
        // Prepara os headers para incluir o token de autenticação em cada requisição
        prepareHeaders: (headers, { getState }) => {
            const token = getState().auth.token;
            if (token) {
                headers.set('authorization', `Bearer ${token}`);
            }
            return headers;
        },
    }),
    endpoints: (builder) => ({
        createOrder: builder.mutation({
            // A query agora espera receber o objeto completo do pedido do frontend
            query: (fullOrderData) => ({
                url: 'orders',
                method: 'POST',
                // O corpo da requisição agora reflete a estrutura completa que o backend espera
                body: {
                    address_id: fullOrderData.addressId,
                    items: fullOrderData.items, // ex: [{ product_id: 1, quantity: 1, extras: [...] }]
                    notes: fullOrderData.notes,
                    payment_method: fullOrderData.paymentMethod,
                    change_for_amount: fullOrderData.changeForAmount,
                    cpf_on_invoice: fullOrderData.cpfOnInvoice,
                    points_to_redeem: fullOrderData.pointsToRedeem,
                },
            }),
        }),
        // Endpoint para buscar o histórico de pedidos (lista resumida)
        getOrderHistory: builder.query({
            query: () => 'orders',
        }),
        // Endpoint para buscar os detalhes de um pedido específico
        getOrderDetails: builder.query({
            query: (orderId) => `orders/${orderId}`,
        }),
    }),
});

// Exporta os hooks para serem usados nos componentes React
export const {
    useCreateOrderMutation,
    useGetOrderHistoryQuery,
    useGetOrderDetailsQuery,
} = ordersApi;