import { grabDisclaimer } from '@/lib/grabDisclaimer'; // adjust the path as needed
import styles from '@/styles/chart.module.css';

interface DisclaimerProps {
    language: string;
}

export default async function Disclaimer(language: DisclaimerProps ) {
  
    const disclaimerHtml = await grabDisclaimer(language.language);

    return (
        <div className={styles.disclaimer} dangerouslySetInnerHTML={{ __html: disclaimerHtml }} />
    );
};
