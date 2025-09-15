import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';
import HomePage from '../pages/HomePage'; // Página principal (ainda vazia)

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/" element={<HomePage />} />
                {/* Outras rotas virão aqui */}
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;