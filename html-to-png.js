var page = require('webpage').create();
page.open('drug-combinations.html', function() {
  page.render('drug-combinations.png');
  phantom.exit();
});