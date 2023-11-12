import React from 'react';
import styles from '@/styles/chart.module.css';
import Image from 'next/image';
import Legend from '@/components/chart/legend';


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

export interface Header {
    text: string;
    config: Config;
    translation: Translations;
}

const Header: React.FC<Header>  = ( {text, config, translation} ) => {

    return (
    <div className={styles.header}>
        <div className={styles.logo}>
          <Image
                src="/logo.svg" // Assuming the logo is stored in the public directory
                alt="logo"
                layout="fill"
                objectFit="contain" // This makes the image scale to fit within the element
                quality={100} // Optionally set the quality of the image
            />
        </div>
        <h1 className={styles.title}>{text}</h1>
        <Legend config={config} translations={translation}/>
    </div>
    )
};

export default Header;