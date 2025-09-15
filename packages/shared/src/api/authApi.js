import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Este arquivo é o "mapa" do frontend que diz como se comunicar com as rotas da API do Python.
export const authApi = createApi({
    reducerPath: 'authApi',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://127.0.0.1:5000/api/', // O endereço do backend
    }),
    endpoints: (builder) => ({
        // Mapeia para a rota POST /api/customers
        registerCustomer: builder.mutation({
            query: (userData) => ({
                url: 'customers',
                method: 'POST',
                body: userData,
            }),
        }),
        // Mapeia para a rota POST /api/users/login
        loginUser: builder.mutation({
            query: (credentials) => ({
                url: 'users/login',
                method: 'POST',
                body: credentials,
            }),
        }),
        // Poderíamos adicionar o login de cliente aqui também
        // loginCustomer: builder.mutation(...)
    }),
});

export const {
    useRegisterCustomerMutation,
    useLoginUserMutation,
} = authApi;