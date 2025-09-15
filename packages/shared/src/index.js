// Exporta a store do Redux
export { store } from './store';

// Exporta os hooks da nossa API de autenticação
export {
    useRegisterCustomerMutation,
    useLoginUserMutation,
} from './api/authApi';

// Exporta as ações e seletores do nosso slice de autenticação
export {
    setCredentials,
    logOut,
    selectCurrentToken,
} from './slices/authSlice';