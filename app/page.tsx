import React from 'react';
import { grabInteractionsGithub } from '@/lib/grabInteractionsGithub'
import { parseInteractionsGithub } from '@/lib/parseInteractionsGithub'
import { grabConfig } from '@/lib/grabConfig';
import ComboChartFull from '@/components/comboChartFull'
import { grabTranslation } from '@/lib/grabTranslation'; // Your translation grabbing function


export default async function Home() {
  const config = await grabConfig();
  const data = await grabInteractionsGithub(config.github_url);
  const parsed = parseInteractionsGithub(data.payload.blob.rawLines)
  const translation = await grabTranslation(config.current_language);

  console.log(config)

  return (
    <main style={{width: config.chart.width, height: config.chart.height}}>
      <ComboChartFull data={parsed} config={config} translation={translation}/>
    </main>
  )
}
