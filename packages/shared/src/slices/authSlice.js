import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    user: null, // Poderia guardar informações do usuário (id, role)
    token: localStorage.getItem('authToken') || null, // Pega o token do localStorage se já existir
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        // Ação para ser chamada após um login bem-sucedido
        setCredentials: (state, action) => {
            const { user, token } = action.payload;
            state.user = user;
            state.token = token;
            // Salva o token no localStorage para persistir a sessão
            localStorage.setItem('authToken', token);
        },
        // Ação para limpar as credenciais no logout
        logOut: (state) => {
            state.user = null;
            state.token = null;
            localStorage.removeItem('authToken');
        },
    },
});

export const { setCredentials, logOut } = authSlice.actions;

export default authSlice.reducer;

// Seletor para pegar o token atual facilmente em qualquer componente
export const selectCurrentToken = (state) => state.auth.token;