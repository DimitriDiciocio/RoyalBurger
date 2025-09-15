import React from 'react';
import AppRouter from './navigation/AppRouter';
import Header from './components/layout/Header'; // 1. Importa o Header
import './assets/styles/global.css';

function App() {
    return (
        <div>
            <Header /> {/* 2. Adiciona o Header aqui */}
            <main>
                <AppRouter /> {/* O conteúdo da página será renderizado aqui */}
            </main>
            {/* O Footer poderia vir aqui */}
        </div>
    );
}

export default App;