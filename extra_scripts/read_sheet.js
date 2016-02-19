var cheerio = require('cheerio'),
    fs = require('fs'),
    _ = require('underscore')._;

/**
 * Steal the legacy .html export of sheet from google spreadsheets into a combo.json
 */

fs.readFile('sheet.html', 'utf8', function(err, data) {
    console.log('--> Loaded sheet');

    $ = cheerio.load(data, {'normalizeWhitespace': true });
    
    var chemicals = [],
        results = {};

    $('tr').eq(7).find('td').each(function(index) {
        $this = $(this);
        var name = $this.text().toLowerCase();
        if(name === 'nitrous oxide') name = 'nitrous';
        if(!_.include(chemicals, name) && name !== '.' && name !== '') {
          chemicals.push(name);
          results[name] = {}; 
        }
    });
    console.log(results);

    $('tr').slice(8).each(function(index) {
        $this = $(this);
        var name = $this.find('td').eq(1).text().toLowerCase();
        /*if(name == '') {
          name = $this.find('td').eq(3).text().toLowerCase();
        }*/
        console.log('index: ' + index + ' name: ' + name);
        if(!_.include(chemicals, name)) return;
        if(name === 'nitrous oxide') name = 'nitrous';
        $this.find('td').slice(3).each(function(index) {
            $this = $(this);
            var attr = $this.attr('class');
            console.log('comparing ' + name + ' and ' + chemicals[index] + ' with attr ' + attr);

            if(attr === 's26' || attr === 's12') {
                results[name][chemicals[index]] = 'Low Risk & Synergy';
            } else if(attr === 's27') {
                results[name][chemicals[index]] = 'Caution';
            } else if(attr === 's39') {
                results[name][chemicals[index]] = 'Low Risk & No Synergy';
            } else if(attr === 's31') {
                results[name][chemicals[index]] = 'Serotonin Syndrome';
            } else if(attr === 's29') {
                results[name][chemicals[index]] = 'Unsafe';
            } else if(attr === 's30') {
                results[name][chemicals[index]] = 'Deadly';
            } else if(attr === 's28') {
                results[name][chemicals[index]] = 'Low Risk & Decrease';
            }
        });
    });  
    console.log(results);
    fs.writeFileSync('combo.json', JSON.stringify(results, null, '    '));
});
