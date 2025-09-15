import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { store } from '@royalburger/shared';
import { Provider } from 'react-redux'; // Importa o Provider

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Provider store={store}>
            <App />
        </Provider>
    </React.StrictMode>,
);