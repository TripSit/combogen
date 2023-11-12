import { promises as fs } from 'fs';
import path from 'path';

export async function grabDisclaimer(lang: string): Promise<string> {
  // Assuming the disclaimers are in the 'public/translations' directory
  const filePath = path.join(process.cwd(), 'public', 'translations', `disclaimer-${lang}.html`);
  try {
    const disclaimerHtml = await fs.readFile(filePath, 'utf-8');
    return disclaimerHtml;
  } catch (error) {
    console.error(`Error reading the disclaimer file for language: ${lang}`, error);
    return ''; // Return an empty string or some default message if the file is not found
  }
}
