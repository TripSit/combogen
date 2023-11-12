export function parseInteractionsGithub(data: any): Record<string, any> {
  const filteredData = Object.entries(data).filter(([key, value]) => {
    // Check if value is an object and has the 'combos' key
    return typeof value === 'object' && value !== null && 'combos' in value;
  });

  return Object.fromEntries(filteredData);
}
