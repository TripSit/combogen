import React from 'react';
import styles from '@/styles/chart.module.css';
import Image from 'next/image';

export interface Header {
    text: string;
}

const Header: React.FC<Header>  = ( {text} ) => {

    return (
    <div className={styles.header}>
        <Image className={styles.logo} src="/logo.svg" alt="logo" width={100} height={100} />
        <h1 className={styles.title}>{text}</h1>
    </div>
    )
};

export default Header;