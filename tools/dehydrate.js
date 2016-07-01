var fs = require('fs'),
    _ = require('underscore')._;

/**
 * Dehydrate combo_beta.json into single dimensions so that it can easily be edited
 */

var combos = JSON.parse(fs.readFileSync('combo_beta.json', 'utf-8')),
    result = {};

_.each(combos, function(k, c) {
  _.each(k, function(m, i) {
    if(!result[c+'&'+i]) {
      result[i+'&'+c] = {
        'status': m.status,
        'note': m.note
      }
    }
  });
});

fs.writeFileSync('coco.json', JSON.stringify(result, null, '    '));
