import React from 'react';
import { useTranslation } from 'next-i18next';

const LegendItem = ({ interaction, cfg }) => {
  const { t } = useTranslation('common'); // 'common' namespace is assumed, replace if necessary

  const interactionIcon = cfg.interaction_icon(interaction); // Method to get the icon class based on interaction
  const interactionTranslation = t(`interaction.${interaction}`); // Translation key structure is assumed, replace with actual key if different

  return (
    <div className={`legend-card ${interaction.toLowerCase().replace(/\s&\s/g, '-')}`}>
      <div className="legend-icon">
        <i className={`fa ${interactionIcon}`}></i>
      </div>
      <div className="legend-content">
        {interactionTranslation}
      </div>
    </div>
  );
};

const Legend = ({ cfg }) => {
  // List of interaction types
  const interactions = [
    "Caution",
    "Unsafe",
    "Dangerous",
    "Low Risk & Synergy",
    "Low Risk & No Synergy",
    "Low Risk & Decrease",
  ];

  return (
    <>
      <div className="legend">
        {interactions.slice(0, 3).map(interaction => (
          <LegendItem key={interaction} interaction={interaction} cfg={cfg} />
        ))}
      </div>
      <div className="legend">
        {interactions.slice(3).map(interaction => (
          <LegendItem key={interaction} interaction={interaction} cfg={cfg} />
        ))}
      </div>
      <span id="status">{cfg.status}</span> {/* cfg.status is assumed to hold status message */}
    </>
  );
};

export default Legend;
