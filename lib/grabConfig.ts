import { promises as fs } from 'fs';

export async function grabConfig() {
  const config = await fs.readFile('./lib/config.json', 'utf-8');
  return JSON.parse(config);
}