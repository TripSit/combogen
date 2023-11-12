import React from 'react';
import styles from '@/styles/chart.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faXmark, faArrowUp, faArrowDown, faQuestion, faBolt, faHeartPulse, faTriangleExclamation, faCircleDot } from '@fortawesome/free-solid-svg-icons';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

// Define a type for the iconMap with an index signature
type IconMapType = {
  [key: string]: IconDefinition;
};

interface LegendProps {
  config: {
    interactionClass: {
      [key: string]: [string, string];
    };
  };
  translations: {
    interactions: Record<string, string>;
  };
}

// Mapping iconClass strings to FontAwesome icons

// Now declare iconMap using the defined type
const iconMap: IconMapType = {
  'arrow-up': faArrowUp,
  'circle-dot': faCircleDot,
  'arrow-down': faArrowDown,
  'triangle-exclamation': faTriangleExclamation,
  'heart-pulse': faHeartPulse,
  'xmark': faXmark,
  'question': faQuestion,
  'bolt': faBolt, // Assuming you have a 'bolt' icon class as well
};


const InteractionLabel: React.FC<{ interactionKey: string; config: LegendProps['config']; translations: LegendProps['translations'] }> = ({
  interactionKey,
  config,
  translations,
}) => {
  const [interactionClass, iconClass] = config.interactionClass[interactionKey];
  const interactionText = translations.interactions[interactionKey];
  const icon = iconMap[iconClass] || faQuestion; // Default to faQuestion if no matching icon

  return (
    <>
      <div className={`${styles.legend_icon} ${styles[interactionClass]}`}>
        <FontAwesomeIcon className={styles.fa} icon={icon} />
      </div>
      <div className={styles.legend_content}>{interactionText}</div>
    </>
  );
};

const Legend: React.FC<LegendProps> = ({ config, translations }) => {
  const interactionKeys = Object.keys(translations.interactions);

  return (
    <div className={styles.legend}>
      {interactionKeys.map((interactionKey) => (
        <div key={interactionKey} className={`${styles.legend_card} ${styles[config.interactionClass[interactionKey][0]]}`}>
          <InteractionLabel interactionKey={interactionKey} config={config} translations={translations} />
        </div>
      ))}
    </div>
  );
};

export default Legend;
