$(function(){
  var baseElement = $('.label').first();
  var baseFontSize = parseFloat(baseElement.css('font-size'));
  var baseWidth = parseInt(baseElement.css('width'));

  baseFontSize = Math.round(baseFontSize);
  baseWidth = Math.round(baseWidth * 0.92);

  // maxFontPixels: Make sure labels aren't upsized to fill cell, only downsized so they don't overflow
  // explicitWidth: Add some space so cell isn't 100% filled side-to-side
  $('#chart .label').textfill({
    widthOnly: true,
    /*explicitWidth: baseWidth,*/
    maxFontPixels: baseFontSize
  });
});