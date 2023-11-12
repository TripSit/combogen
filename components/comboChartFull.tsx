import React from 'react';
import Table from '@/components/chart/table'; // Your converted combo-table component
import Disclaimer from '@/components/chart/disclaimer'; // Your converted disclaimer component, which should handle the different languages based on the current locale
import Legend from '@/components/chart/legend'; // Your converted legend component
import Support from '@/components/chart/support';
import Header from '@/components/chart/header';

import styles from '@/styles/chart.module.css';
// Define a type for the interactions with flexible keys
export type SubstancesInteractions = {
  [key: string]: string;
};

// Define the type for the data structure with flexible substance interactions
export interface Data {
  [key: string]: SubstancesInteractions;
}

export interface Config {
    url: string;
    local_file: string;
    github_url: string;
    version: string;
    languages: string[];
    current_language: string;
    tableOrder: string[][];
    groupNames: string[];
    rewriteInteraction: { [key: string]: string };
    interactionClass: {
      [key: string]: [string, string];
    };
    chart: {
      width: number;
      height: number;
      htmlRelativeResources: string;
    };
  }

export interface Translations {
  title: string;
  app: string;
  support: string;
  drugs: Record<string, string>; // Flexible keys for drug names
  interactions: Record<string, string>; // Flexible keys for interaction descriptions
}

interface ComboChartFullProps {
    data: Data;
    config: Config;
    translation: Translations;
  }

const ComboChartFull: React.FC<ComboChartFullProps> = ({ data, config, translation }) => {

  return (
    <div className={styles.container}>
      <Header text={translation.title} config={config} translation={translation} />
      <Table data={data} translations={translation} config={config} />
      <div className={styles.footer}>
        <Disclaimer language={config.current_language} />
        <Support text={translation.support}/>
      </div>
    </div>
  );
};

export default ComboChartFull;
