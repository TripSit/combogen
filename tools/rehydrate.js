var fs = require('fs'),
    _ = require('underscore')._;

/**
 * Rehydrate dehydrated combo.json into multiple dimensions for practical use
 */

var flat_combos = JSON.parse(fs.readFileSync('flat_combos.json', 'utf-8')),
    combos = {};

_.each(flat_combos, function(i, k) {
  var drugs = k.split('&');
  console.log(drugs);
  _.each(drugs, function(d) {
    if(!_.has(combos, d)) {
      combos[d] = {};
    }
  });
  combos[drugs[0]][drugs[1]] = i;
  combos[drugs[1]][drugs[0]] = i;
});

fs.writeFileSync('combo_beta_beta.json', JSON.stringify(combos, null, '    '));
