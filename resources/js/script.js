$(function(){
  var baseElement = $('.label').first();
  var baseFontSize = parseFloat(baseElement.css('font-size'));
  var baseWidth = parseInt(baseElement.css('width'));

  baseFontSize = Math.round(baseFontSize);
  baseWidth = Math.round(baseWidth * 0.95);

  // maxFontPixels: Make sure labels aren't upsized to fill cell, only downsized so they don't overflow
  // explicitWidth: Add some space so cell isn't 100% filled side-to-side
  $('#chart .label').textfill({
    widthOnly: true,
    explicitWidth: baseWidth,
    maxFontPixels: baseFontSize
  });

  var SUPER_MAGIC_CONSTANT_THAT_MAKES_IT_LOOK_GOOD = 2;

  $('#legend td').width($('#chart td').eq(10).width() + SUPER_MAGIC_CONSTANT_THAT_MAKES_IT_LOOK_GOOD);
});