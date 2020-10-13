'use strict'

$(document).ready(function() {
    utils();
    dateToday();
    expander();
});

function utils() {
    $.fn.slideFadeToggle  = function(speed, easing, callback) {
        return this.animate({opacity: 'toggle', height: 'toggle'}, speed, easing, callback);
    };
    $.fn.slideFadeOn = function(speed, easing, callback) {
        return this.animate({opacity: 'show', height: 'show'}, speed, easing, callback);
    };
    $.fn.slideFadeOff = function(speed, easing, callback) {
        return this.animate({opacity: 'hide', height: 'hide'}, speed, easing, callback);
    };
}

function dateToday() {
    var date = new Date();
    var day = date.getDate();
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    var monthName = monthNames[date.getMonth()];
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    var dateNumber = month + "/" + day + "/" + year;
    var dateWritten = monthName + ' ' + day + ', ' + year;
    var $dateToday = $('.date-today');
    $dateToday.attr('value', dateWritten);
}

function expander() {
    var $parents = $('[data-expand]');



    $parents.each(function(){
        var $parent = $(this);
        var parentId = $parent.attr('data-expand');
        var $labels = $parent.find('[data-expand-value]');
        var $targets = $('[data-expander]');

        $targets.hide();

        $labels.on('click', function() {
            var $label = $(this);
            var labelValue = $label.attr('data-expand-value');

            var checkbox = $label.has('input[type="checkbox"]');
            var $checkbox = $label.find('input[type="checkbox"]');
            var checked = $checkbox.is(':checked');

            $targets.each(function() {
                var $target = $(this);
                var targetId = $target.attr('data-expander');
                var targetValue = $target.attr('data-expander-value');

                if (parentId == targetId) {
                    // if (typeof targetValue !== typeof undefined && targetValue !== false) {
                    //     $target.slideFadeOn();
                    // }



                    if (labelValue == targetValue) {
                        // if (checkbox) {
                        //     console.log('CHECKBOX!');
                        //     if (checked) {
                        //         console.log('CHECKED!');
                        //         $target.slideFadeOn();
                        //
                        //     } else {
                        //         console.log('NO CHECKED!!!!');
                        //         $target.slideFadeOff();
                        //     }
                        // }
                        $target.slideFadeOn();
                    } else {
                        $target.slideFadeOff();
                    }
                }
            });
        });

        // See if we should activate
        $labels.each(function() {
            if($(this).find('input').attr('checked')) {
                $(this).click();
            }
        });
    });
}

