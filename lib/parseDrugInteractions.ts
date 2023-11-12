interface DrugData {
    [key: string]: {
      combos?: {
        [key: string]: {
          status: string;
          note?: string;
        }
      },
    };
  }
  
  interface TransformedData {
    [drug: string]: {
      [otherDrug: string]: string; // Here, the string would be the status of the interaction
    };
  }
  
  export function parseDrugInteractions(data: DrugData): TransformedData {
    let transformedData: TransformedData = {};
  
    Object.keys(data).forEach(drug => {
      const combos = data[drug].combos;
      if (combos) {
        transformedData[drug] = {};
        Object.keys(combos).forEach(comboDrug => {
          // Safely access the status of the interaction
          transformedData[drug][comboDrug] = combos[comboDrug].status;
        });
      }
    });
  
    return transformedData;
  }