interface CategoryMap {
  [drug: string]: string;
}

export function parseDrugCategory(data: any): CategoryMap {
  let categoryMap: CategoryMap = {};

  Object.keys(data).forEach(drug => {
    if (data[drug].categories && data[drug].categories.length > 0) {
      categoryMap[drug] = data[drug].categories[0]; // Get the first category
    } else {
      categoryMap[drug] = 'unknown'; // Default category if none is provided
    }
  });

  return categoryMap;
}
