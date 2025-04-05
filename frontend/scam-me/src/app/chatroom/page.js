"use client";
import React, { useState } from 'react';
import styles from './chatroom.module.css';


const Layout = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleSidebar = () => setIsOpen(!isOpen);

    return (
        <div>
            <div 
                className = {`${styles.sidebar} ${isOpen ? styles.open : ''}`}
            >
                <button className = {styles.closeBtn} onClick={toggleSidebar}>
                    &times;
                </button>
                <ul className={styles.navList}>
                    <li><a href="#">EXPLORE</a></li>
                    <li><a href="#">assume this is a node</a></li>
                    <li><a href="#">assume this is some channel</a></li>
                </ul>
            </div>

            <button className={styles.toggleBtn} onClick={toggleSidebar}>
                {isOpen ? 'Close' : 'Open'} Sidebar
            </button>

            <div style={{ marginLeft: '270px', padding: '20px' }}>
                <h1>Test title</h1>
            </div>
        </div>
    )
}

export default Layout;