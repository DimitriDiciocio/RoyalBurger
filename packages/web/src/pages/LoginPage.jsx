import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import { useLoginUserMutation, setCredentials } from '@royalburger/shared';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const dispatch = useDispatch();

    // O hook do RTK Query nos dá a função para chamar a API e o estado da chamada
    const [loginUser, { isLoading, error }] = useLoginUserMutation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Chama a API. O 'unwrap()' é para tratar o sucesso/erro com try/catch
            const { access_token } = await loginUser({ email, password }).unwrap();

            // Se o login deu certo, despacha a ação para salvar o token na store do Redux
            dispatch(setCredentials({ token: access_token, user: { email } }));

            // Redireciona o usuário para a página inicial
            navigate('/');
        } catch (err) {
            console.error('Falha ao fazer login:', err);
        }
    };

    return (
        <div>
            <h1>Login (Painel Administrativo)</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Senha:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Entrando...' : 'Entrar'}
                </button>
                {error && <p style={{ color: 'red' }}>Erro: {error.data?.msg || 'Credenciais inválidas'}</p>}
            </form>
        </div>
    );
};

export default LoginPage;