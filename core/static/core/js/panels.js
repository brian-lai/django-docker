$(document)
    .on('click', '.panel-heading span.clickable', function(e){
        $(this).parents('.panel').find('.panel-collapse').collapse('toggle');
    })
    .on('show.bs.collapse', '.panel-collapse', function () {
        var $span = $(this).parents('.panel').find('.panel-heading span.clickable');
        $span.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    })
    .on('hide.bs.collapse', '.panel-collapse', function () {
        var $span = $(this).parents('.panel').find('.panel-heading span.clickable');
        $span.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    });