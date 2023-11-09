import React from 'react';
import styles from '@/styles/chart.module.css';
import Image from 'next/image';

export interface Support {
    text: string;
}

const Support: React.FC<Support>  = ( {text} ) => {
    console.log(text)
    return (
        <div className={styles.qr}>
            <Image src="/support_qr.svg" alt="support" width={100} height={100} />
        <h3 className={styles.qrH3}>{text}</h3>
        </div>
    )
};

export default Support;