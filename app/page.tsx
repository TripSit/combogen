import React from 'react';
import { grabInteractionsGithub } from '@/lib/grabInteractionsGithub'
import { parseInteractionsGithub } from '@/lib/parseInteractionsGithub'
import { grabConfig } from '@/lib/grabConfig';
import ComboChartFull from '@/components/comboChartFull'
import { grabTranslation } from '@/lib/grabTranslation'; // Your translation grabbing function
import DownloadFiles from '@/components/downloadFiles'; // Your download files component


export default async function Home() {
  const config = await grabConfig();
  const data = await grabInteractionsGithub(config.github_url);
  const parsed = parseInteractionsGithub(data)
  const translation = await grabTranslation(config.current_language);

  return (
    <main>
      <div id="comboChart">
        <ComboChartFull data={parsed} config={config} translation={translation}/>
      </div>
      <DownloadFiles componentId="comboChart" />

    </main>
  )
}
