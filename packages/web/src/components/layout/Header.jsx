import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

// Importando nosso seletor e ação diretamente do pacote shared!
import { selectCurrentToken, logOut } from '@royalburger/shared';

const Header = () => {
    // O hook useSelector "escuta" a store do Redux.
    // Toda vez que o token mudar, este componente será re-renderizado.
    const token = useSelector(selectCurrentToken);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        // Despacha a ação de logout que importamos do shared
        dispatch(logOut());
        // Navega para a página de login após o logout
        navigate('/login');
    };

    return (
        <header style={{
            display: 'flex',
            justifyContent: 'space-between',
            padding: '1rem',
            backgroundColor: '#333',
            color: 'white'
        }}>
            <div className="logo">
                <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5rem' }}>
                    Royal Burger
                </Link>
            </div>
            <nav>
                {token ? (
                    // O que mostrar se o usuário ESTIVER logado
                    <ul style={{ listStyle: 'none', display: 'flex', gap: '1rem', margin: 0 }}>
                        <li><Link to="/" style={{ color: 'white' }}>Cardápio</Link></li>
                        <li><Link to="/my-orders" style={{ color: 'white' }}>Meus Pedidos</Link></li>
                        <li>
                            <button onClick={handleLogout} style={{ background: 'none', border: 'none', color: 'cyan', cursor: 'pointer' }}>
                                Logout
                            </button>
                        </li>
                    </ul>
                ) : (
                    // O que mostrar se o usuário NÃO estiver logado
                    <ul style={{ listStyle: 'none', display: 'flex', gap: '1rem', margin: 0 }}>
                        <li><Link to="/" style={{ color: 'white' }}>Home</Link></li>
                        <li><Link to="/login" style={{ color: 'white' }}>Login</Link></li>
                    </ul>
                )}
            </nav>
        </header>
    );
};

export default Header;