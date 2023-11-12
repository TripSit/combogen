import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faXmark, faArrowUp, faArrowDown, faQuestion, faBolt, faHeartPulse, faTriangleExclamation, faCircleDot } from '@fortawesome/free-solid-svg-icons';

import styles from '@/styles/chart.module.css';
import { parseDrugInteractions } from '@/lib/parseDrugInteractions';
import { parseDrugCategory } from '@/lib/parseDrugCategory';

interface TableProps {
  data: Record<string, Record<string, string>>;
  translations: {
    drugs: Record<string, string>;
    interactions: Record<string, string>;
  };
  config: {
    interactionClass: Record<string, [string, string]>;
  };
}

// Mapping iconClass strings to FontAwesome icons
const iconMap: Record<string, IconDefinition> = {
  'arrow-up': faArrowUp,
  'circle-dot': faCircleDot,
  'arrow-down': faArrowDown,
  'triangle-exclamation': faTriangleExclamation,
  'heart-pulse': faHeartPulse,
  'xmark': faXmark,
  'question': faQuestion,
  'bolt': faBolt,
};

const Table: React.FC<TableProps> = ({ data, translations, config }) => {
  const transformedData = parseDrugInteractions(data);
  
  const drugs = Object.keys(transformedData);
  const categoryMap = parseDrugCategory(data);
  console.log(drugs)

  const renderHeader = () => (
    <tr>
      <td className={styles.chartTD}></td>
      {drugs.map(drug => (
        <td key={drug} className={`${styles[categoryMap[drug]]} ${styles.chartTD}`}>
          <span className={styles.chartSpan}>{translations.drugs[drug]}</span>
        </td>
      ))}
      <td className={styles.chartTD}></td>
    </tr>
  );

  const renderRow = (drugA: string) => (
    <tr key={drugA}>
      <td className={`${styles[categoryMap[drugA]]} ${styles.chartTD}`}>
        <span className={styles.chartSpan}>{translations.drugs[drugA]}</span>
      </td>
      {drugs.map(drugB => {
        let interaction = drugA === drugB || transformedData[drugA][drugB] === undefined ? 'unknown' : transformedData[drugA][drugB];

        const [interactionClass, iconClass] = config.interactionClass[interaction.toLowerCase()] || config.interactionClass['fallback'];
        const icon = iconMap[iconClass] || faQuestion;
        
        return (
          <td key={drugB} className={`${styles[categoryMap[drugB]]} ${styles[interactionClass]} ${styles.chartTD}`}>
            {drugA === drugB ? (
              <span className={styles.chartSpan}>{translations.drugs[drugB]}</span>
            ) : (
              <div className={styles.table_icon}><FontAwesomeIcon icon={icon} className={styles.fa} /></div>
            )}
          </td>
        );
      })}
      <td className={`${styles[categoryMap[drugA]]} ${styles.chartTD}`}>
        <span className={styles.chartSpan}>{translations.drugs[drugA]}</span>
      </td>
    </tr>
  );

  return (
    <table id="chart" className={styles.chart}>
      <tbody>
        {renderHeader()}
        {drugs.map(renderRow)}
        {renderHeader()}
      </tbody>
    </table>
  );
};

export default Table;
