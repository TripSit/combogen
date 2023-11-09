import React from 'react';

const ComboTable = ({ db, cfg }) => {
  const { t } = useTranslation('common'); // Replace 'common' with your actual namespace if different

  // Function to create the horizontal table header
  const horizontalTableHeader = () => (
    <tr>
      <td></td>
      {db.drugs.map((drug) => (
        <td key={drug.name} className={`${drug.group.name} label`}>
          <span>{t(drug.name)}</span>
        </td>
      ))}
      <td></td>
    </tr>
  );

  return (
    <table id="chart">
      {horizontalTableHeader()}
      {db.drugs.map((drugA) => (
        <tr key={drugA.name}>
          <td className={`${drugA.group.name} label`}>
            <span>{t(drugA.name)}</span>
          </td>
          {db.drugs.map((drugB) => {
            const interaction = drugA === drugB ? '' : db.interaction(drugA, drugB);
            const className = drugA === drugB ? `${drugA.group.name} label` : cfg.interaction_to_class(interaction);
            const content = drugA === drugB ? <span>{t(drugA.name)}</span> : (className === 'unknown' ? <span>{interaction}</span> : <i className={`fa ${cfg.interaction_icon(interaction)}`}></i>);

            return (
              <td key={`${drugA.name}-${drugB.name}`} className={className}>
                {content}
              </td>
            );
          })}
          <td className={`${drugA.group.name} label`}>
            <span>{t(drugA.name)}</span>
          </td>
        </tr>
      ))}
      {horizontalTableHeader()}
    </table>
  );
};

export default ComboTable;
