import React from 'react';
import { useTranslation } from 'next-i18next';

const Disclaimer = () => {
  const { t } = useTranslation('disclaimer'); // Assuming disclaimer-related translations are in a 'disclaimer' namespace

  return (
    <div>
      <h4>{t('chatSupport')} <a href="https://www.tripsit.me">www.TripSit.Me</a></h4>
      <p>{t('compilationNote')}</p>
      <p>{t('substanceTesting')} <strong>{t('testYourSubstances')}</strong></p>
      <p>{t('missingWarnings')} <strong>{t('researchYourSubstances')}</strong></p>
      <p>{t('doNotRely')} <strong>{t('medicationInteractions')}</strong></p>
      <p>{t('findInteractions')}</p>
      <p>{t('beResponsible')}</p>
    </div>
  );
};

export default Disclaimer;
