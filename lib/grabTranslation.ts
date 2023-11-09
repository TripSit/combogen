import { promises as fs } from 'fs';

export async function grabTranslation(language: string) {
  const path = `./public/translations/${language}.json`;
  const translation = await fs.readFile(path, 'utf-8');
  return JSON.parse(translation);
}