const puppeteer = require('puppeteer');
const path = require('path');

// Parse arguments...
const currentDir = path.dirname(process.argv[1]);
const target = process.argv[2];
const width = parseInt(process.argv[3]) || 3800;
const height = parseInt(process.argv[4]) || 1600;

const outFilename = path.basename(target, '.html') + '.png';
const outFilePath = path.join(currentDir, '..', 'output', 'png', outFilename);

console.log('Rendering...');
console.log('argv:', process.argv);
console.log('target:', target);
console.log('out:', outFilePath);

// Render assets...
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(`file://${target}`);
  await page.setViewport({
    width: width,
    height: height,
  });
  await page.screenshot({
    path: outFilePath
  });
  await browser.close();
})();