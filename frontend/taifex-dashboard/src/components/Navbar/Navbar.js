import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/cryptocurrencies">Cryptocurrencies</Link></li>
                <li><Link to="/exchanges">Exchanges</Link></li>
                {/* 可以繼續添加其他導航項目 */}
            </ul>
        </nav>
    );
};

export default Navbar;
