import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Home from './components/Pages/Home';
import Cryptocurrencies from './components/Pages/Cryptocurrencies';

function App() {
    return (
        <Router>
            <div>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/cryptocurrencies" element={<Cryptocurrencies />} /> {/* 添加新的路由 */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
