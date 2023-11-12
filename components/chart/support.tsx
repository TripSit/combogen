import React from 'react';
import styles from '@/styles/chart.module.css';
import Image from 'next/image';

export interface Support {
    text: string;
}

const Support: React.FC<Support>  = ( {text} ) => {
    return (
        <div className={styles.qr}>
            <div className={styles.qrImage}>
                <Image
                    src="/support_qr.svg"
                    alt="support"
                    layout="fill"
                    objectFit="contain"
                    quality={100}
                />
            </div>
        <h3 className={styles.qrH3}>{text}</h3>
        </div>
    )
};

export default Support;