var Nightmare = require('nightmare');
var nightmare = Nightmare({ show: false });
var path = require('path');

var target = process.argv[2];
var width = parseInt(process.argv[3]) || 3800;
var height = parseInt(process.argv[4]) || 1600;

var currentDir = path.dirname(process.argv[1]);

var outFilename = path.basename(target, '.html') + '.png';
var outFilePath = path.join(currentDir, '..', 'output', 'png',  outFilename);

console.log('Rendering...');
// console.log('argv:', process.argv);
console.log('target:', target);
console.log('out:', outFilePath);

nightmare
  .viewport(width, height)
  .goto(`file://${target}`)
  .wait(250)
  .screenshot(outFilePath)
  .end()
  .catch(function (error) {
    console.error('Error:', error);
  });
