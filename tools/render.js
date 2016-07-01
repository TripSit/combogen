var Nightmare = require('nightmare');
var nightmare = Nightmare({ show: false });
var path = require('path');

var target = process.argv[2];
var width = process.argv[3] || 3800;
var height = process.argv[4] || 1600;

var currentDir = path.dirname(process.argv[1]);
var targetPath = 'file://' + path.join(currentDir, '..', target + '.html');

nightmare
  .viewport(width, height)
  .goto(targetPath)
  .screenshot(path.join(currentDir, '..', 'output', 'png', target + '.png'))
  .end()
  .catch(function (error) {
    console.error('error:', error);
  });
