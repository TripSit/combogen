export function parseInteractionsGithub(lines: string[]) {
 // Join the array of strings into a single string
//  console.log(lines)
 let jsonString = lines.join('')
 // Add double quotes around any word characters that come before a colon to ensure keys are properly quoted
 .replace(/([a-zA-Z0-9-\/\u00C0-\u017F]+)(\s*):/g, '"$1":')
 // Replace single quotes with double quotes
 .replace(/'/g, '"')
 // Remove trailing commas before a closing brace
 .replace(/,\s*}/g, '}')
 // Remove trailing commas before a closing bracket
 .replace(/,\s*]/g, ']');

// Parse the JSON string
try {
 const data = JSON.parse(jsonString);
 return data;
} catch (error) {
 console.error('Failed to parse data', error);
 return null;
}
}