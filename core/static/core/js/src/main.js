'use strict'

utils();
bootstrapPlugins();
dateToday();
expander();
subMenus();
mainMenuMobileToggle();
customerMenu();
header();
flowNav();
forms();
Checked();
playClick();
videoModal();
getStartedSelector();
infoExpand();
delayInfoExpand();
infoExpand2();
mainAccordion();
variantSelector();
disableAnchor();
leaderBio();


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

function bootstrapPlugins() {
    // popover
    $('[data-toggle="popover"]').popover({
        trigger: 'hover',
        container: 'body',
        placement: 'bottom'
    });
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
    /* Provides a way to have elements dynamically toggle being shown and hidden based on input selection.

    Dynamically determines the number of toggles to bind, and allows multiple cases to trigger the same element.
    */
    function get_expander_parents() {
        /* Returns a list of objects with the following format:

        {
            'name': {
                'value': Currently selected option for the `data-expand`,
                'choices: List of potential values for this `data-expand`,
                'element': JQuery HTML DOM element
            }
        }
        */
        // Get a list of the `data-expand` parents which trigger toggles
        var parents = {};
        // Iterate over the parents and append a data structure about it
        $('[data-expand]').each(function(idx, dataExpand) {
            var $dataExpand = $(dataExpand);

            // What is the name of the toggle we are defining?
            var parent = {
                'element': $dataExpand,
                'choices': []
            };

            // Select all of the inputs defined to toggle this `data-expand`
            var $dataExpandOptions = $dataExpand.find('[data-expand-value]');
            $dataExpandOptions.each(function(idx, dataExpandOption){
                var $dataExpandOption = $(dataExpandOption);
                var dataExpandValue = $dataExpandOption.attr('data-expand-value');

                // Find all of the inputs designated to toggle for this value
                var input = $dataExpandOption.find('input[type="radio"], input[type="checkbox"]');
                if(input.attr('checked'))
                    parent['value'] = dataExpandValue;
                parent['choices'].push({
                    'element': $dataExpandOption,
                    'value': dataExpandValue
                });
            });
            parents[$dataExpand.attr('data-expand')] = parent;
        });
        return parents;
    }

    function get_expander_targets() {
        /* Returns a list of the targets for all `data-expand` elements with the following format:

        {
            'element': JQuery HTML DOM element,
            'expanders': List of objects with `name` and `value` defined
        }
        */
        var $targets = $('[data-expander]');
        var targetId = 2;
        while(true) {
            var extraTargets = $('[data-expander-' + targetId + ']');
            if(extraTargets.length == 0)
                break;
            // If we found more elements for `data-expander-(n+1)`, add to the running list and try to find more
            $.merge($targets, extraTargets);
            targetId++;
        }

        var targets = [];
        // Create an easier to use format for the target elements
        $.each($.unique($targets), function(idx, target) {
            var $target = $(target);
            var target = {
                'element': $target,
                'expanders': {}
            };
            target['expanders'][$target.attr('data-expander')] = [$target.attr('data-expander-value')];

            var targetId = 2;
            while(true) {
                var extraExpander = $target.attr('data-expander-' + targetId);
                if(extraExpander === undefined)
                    break;
                // If we found more elements for `data-expander-(n+1)`, add to the running list and try to find more
                if(target['expanders'][extraExpander] === undefined)
                    target['expanders'][extraExpander] = [];
                target['expanders'][extraExpander].push($target.attr('data-expander-value-' + targetId));
                targetId++;
            }

            targets.push(target);
        });

        return targets;
    }

    function toggle_elements_by_parent(parent) {
        /* Toggles the appropriate values based on the updated parent element.
        */
        // For each element we identified could be toggled before, determine what state it should be set to
        $.each(targets, function(idx, target) {
            var $target = target['element'];
            if(!setup)
                $target.stop().slideFadeOff();
            else
                $target.hide();

            // Determine if the target is a <label> element
            var targetIsLabel = $target.is('label');

            // Working from the highest 'order' toggle, determine what the state of the element should be
            $.each(target['expanders'], function(key, targetExpanders) {
                if(targetExpanders.indexOf(parents[key]['value']) >= 0)
                    if(!setup) {
                        $target.stop().slideFadeOn();
                    } else {
                        $target.show();
                    }
            });
        });
    }

    var setup = true;
    var parents = get_expander_parents();
    var targets = get_expander_targets();

    // Bind all of the click events to toggle appropriate elements
    $.each(parents, function(idx, parent) {
        var $parent = parent['element'];

        // Find all the toggles
        var $toggles = $parent.find('[data-expand-value]');
        $toggles.on('click', function() {
            parent['value'] = $(this).attr('data-expand-value');
            // Custom code to handle checkbox toggles
            if($(this).find('input[type="checkbox"]') && $(this).hasClass('checked'))
                parent['value'] = '';
            toggle_elements_by_parent(parent);
        });
    });
    toggle_elements_by_parent();
    setup = false;
}




function flowNav() {
    var $nav = $('.user-flow-nav');

    function flowNavScroll() {
        $(window).on("scroll", function(){
            var scrollPos = $(window).scrollTop();
            if(scrollPos > 250){
                $nav.addClass('scroll');
            } else {
                $nav.removeClass('scroll');
            }
        });
    }
    flowNavScroll();
}

/* mainMenuMobileToggle  controls sliding the mobile menu in and out ****************
**************************************************************************************/

function mainMenuMobileToggle() {
    var $body = $('body');
    var $nav = $('.main-menu');
    var $overlay =  $('<div class="main-menu-overlay"></div>');
    // var $siteConstraint = $('.site-constraint');
    var $header = $('.header');
    var $openToggle = $('.mobile-menu-toggle');
    var $closeToggle = $('.mobile-menu-toggle-2');

    //function used to close mobile nav
    function closeMenu(time){
        setTimeout(function(){
            $openToggle.removeClass('toggle-on');
        },time);
        $body.removeClass('mobile-nav-open');
        setTimeout(function(){
            $overlay.remove();
        },time);

        //closes sub menus
        $('.sub-open').children('.submenu-wrap').slideUp(300);
        $('.sub-open').removeClass('sub-open');
        //closes customer menu
        $('.customer-menu').slideUp(300);
        $('.customer-menu-open').removeClass('customer-menu-open');
    }

    //function used to open mobile nav
    $openToggle.on('click', function(){
        $header.append($overlay);
        $openToggle.toggleClass('toggle-on');
        setTimeout(function(){
            $body.toggleClass('mobile-nav-open');
        },100);
        $('.main-menu-overlay').on('swiperight', function(){
            closeMenu(500);
        });
    });

    $closeToggle.on('click', function(){
        closeMenu(500);
    });
    $($nav).on('swiperight', function(){
        closeMenu(500);
    });
    $(document).on('click touchstart', '.main-menu-overlay', function(){
        closeMenu(500);
    });
    $(window).resize(function(){
        closeMenu(500);
    });
}


/* subMenus controls toggling of the sub menus within the main menu ******************
 **************************************************************************************/

function subMenus() {
    var $toggle = $('.main-menu-list-item');
    var $clickToggle = $('.menu-toggle');
    var sm = 768;
    var md = 992;

    $toggle.hover(function(){
        var $this = $(this);
        if($(window).width() > md ){
            $this.children('.submenu-wrap').stop().slideDown(300);
        }
    }, function () {
        var $this = $(this);
        if($(window).width() > md ) {
            $this.children('.submenu-wrap').stop().slideUp(300);
            $('.customer-menu-open').removeClass('customer-menu-open');
            $('.sub-open').removeClass('sub-open');
        }
    });

    $clickToggle.on('click', function(){
        var $this = $(this);
        var $thisSub = $this.siblings('.submenu-wrap');
        var $thisParent = $this.parent('li');


        if(!$thisParent.hasClass('sub-open')){
            $('.sub-open').children('.submenu-wrap').stop().slideUp(300);
            $('.sub-open').removeClass('sub-open');
            $thisSub.slideDown(300);
            $thisParent.addClass("sub-open");
        } else if($thisParent.hasClass('sub-open')) {
            $thisSub.slideUp(300);
            $thisParent.removeClass("sub-open");
        }
    });
    $(window).resize(function(){
        $('.sub-open').children('.submenu-wrap').stop().slideUp(300);
        $('.sub-open').removeClass('sub-open');
    });
}


/* customer menu controls toggling of the  customer menus within the header ***********
 **************************************************************************************/

function customerMenu() {
    var $toggle = $('.customer-title');
    var $toggle2 = $('.customer-title span');
    var $toggle3 = $('.customer-sub-icon');
    var icon = $('.customer-sub-icon');
    var $menu = $('.customer-menu');
    var md = 992;

    $toggle.hover(function(){
        if($(window).width() > md && !$('.customer-nav').hasClass('logged-out')) {
            $(this).children('.customer-menu').stop().slideDown(300);
        }
    },function(){
        if($(window).width() > md && !$('.customer-nav').hasClass('logged-out')) {
            $(this).children('.customer-menu').stop().slideUp(300);
            $('.customer-menu-open').removeClass('customer-menu-open');
        }
    });

    $toggle2.on('click', function(){
        var $this = $(this);
        $this.parent('.customer-title').toggleClass('customer-menu-open');
        $menu.stop().slideToggle(300);
    });
    $toggle3.on('click', function(){
        var $this = $(this);
        $this.stop().parent('.customer-title').toggleClass('customer-menu-open');
        $menu.slideToggle(300);
    });
    $(window).resize(function(){
        $('.customer-menu-open').removeClass('customer-menu-open');
        $menu.stop().slideUp(300);
    });
}

/*  Scroll event for header ***********************************************************
 **************************************************************************************/

function header() {
    var $header = $('.header');

    headerScroll();
    barHover();

    function headerScroll() {
        $(window).on("scroll", function(){
            var scrollPos = $(window).scrollTop();
            if(scrollPos > 40){
                $header.addClass('header-top');
            }else {
                $header.removeClass('header-top');
            }
        });
    }

/*  hover event on the scroll bar *****************************************************
 **************************************************************************************/

    function barHover() {
        var $bar = $('.header .health-professionals-info');
        var $link = $bar.find('a');
        $link.each(function() {
            var $link = $(this);
            $link.on('mouseenter', function() {
                $bar.addClass('active');
            }).on('mouseleave', function() {
                $bar.removeClass('active');
            });
        });
    }
}

/*  forms *****************************************************************************
 **************************************************************************************/

function forms() {
    select();
    function select() {
        var $select = $('select');
        $select.each(function(){
            var $select =  $(this);
            $select.change(function(){
               $select.addClass('checked');
            });
        });
    }
}


/*  radio and checkbox *****************************************************************
 **************************************************************************************/

function Checked() {

    $('input[type="radio"]').parents('label').on('click', function(){
        typeCheck("radio");
    });

    $('input[type="checkbox"]').parents('label').on('click', function(){
        typeCheck("checkbox");
    });

    function typeCheck(type){
        $('input[type="' + type + '"]').each(function(){
            var $this2 = $(this);
            if($this2.prop("checked") == true){
                $this2.parents('label').addClass('checked');
            } else {
                $this2.parents('label').removeClass('checked');
            }
        });
    }
    typeCheck("radio");
    typeCheck("checkbox");
}

/*  play click ***********************************************************************
 **************************************************************************************/

function playClick() {
    $('.btn-play').on('click', function(){
        var $this = $(this);
        $this.addClass('play-click');
        setTimeout(function(){
            $this.removeClass('play-click');
        },500);
    });
}


/*  video modal ***********************************************************************
 **************************************************************************************/


function videoModal() {
    var $siteConstraint = $('.site-constraint');
    var $body = $('body');

    $('[data-video]').on('click', function(){
        var videoAttr = $(this).attr('data-video');
        var videoModal = $('<div class="video-modal"><span class="video-close"></span><div class="video-wrapper"><div class="video-container"><iframe ' + videoAttr + '></iframe></div></div></div>');
        $siteConstraint.append(videoModal);
        setTimeout(function(){
            $body.addClass('video-modal-active');
        }, 200);
    });
    $(document).on('click', '.video-modal', function(){
        var $this = $(this);
        $body.removeClass('video-modal-active');
        setTimeout(function(){
            $this.remove();
        }, 500);

    });
    $(document).on('click', '.video-close', function(){
        $body.removeClass('video-modal-active');
        setTimeout(function(){
            $('.video-modal').remove();
        }, 500);

    });
}


/*  leaderBio ***********************************************************************
 **************************************************************************************/


function leaderBio() {
    var $siteConstraint = $('.site-constraint');
    var $body = $('body');

    $('[data-modal]').on('click', function(){
        var modalAttr = $(this).attr('data-modal');
        var content = $('[data-modal-value="' + modalAttr + '"]').html();
        var baseModal = $('<div class="base-modal"><span class="modal-close"></span><div class="base-content-wrapper">' + content + '</div></div>');
        $siteConstraint.append(baseModal);
        setTimeout(function(){
            $body.addClass('base-modal-active');
        }, 200);
    });
    $(document).on('click', '.base-modal', function(){
        var $this = $(this);
        $body.removeClass('base-modal-active');
        setTimeout(function(){
            $this.remove();
        }, 500);

    });
    $(document).on('click', '.modal-close', function(e){
        $body.removeClass('base-modal-active');
        setTimeout(function(){
            $('.base-modal').remove();
        }, 500);

    });
}

/*  Get started Selector **************************************************************
 **************************************************************************************/

function getStartedSelector() {
    getstartedselect($('#get-started-select-1'),$('#get-started-1-content'));
    getstartedselect($('#get-started-select-2'),$('#get-started-2-content'));
    getstartedselect($('#get-started-select-3'),$('#get-started-3-content'));


    function getstartedselect(select, content){
            select.on('click', function() {
                $('.get-started-select-toggle').removeClass('select-active');
                $(this).addClass('select-active');
            $('.get-started-content').removeClass('active-content');
                $('.get-started-content').stop().slideUp(400);
                content.stop().slideDown(400);
        });
    }

}

/*  Info expand **********************************************************************
 **************************************************************************************/

function infoExpand() {
    $('[data-reveal="toggle"]').on('click', function(){
        var $this = $(this);
        if($this.hasClass('expanded')){
            $this.removeClass('expanded');
            $this.children('[data-reveal="target"]').stop().slideUp(400);
        } else {
            $this.addClass('expanded');
            $this.children('[data-reveal="target"]').stop().slideDown(400);
        }
    });
    $('[data-reveal-hover="true"]').hover(function(){
            $(this).children('[data-reveal="target"]').stop().slideDown(400);
    }, function(){
            $(this).removeClass('expanded');
            $(this).children('[data-reveal="target"]').stop().slideUp(400);
    });
    $('[data-reveal="toggle-inset"]').on('click', function(){
        var $this = $(this);
            $this.parent().toggleClass('expanded');
            $this.parent().children('[data-reveal="target"]').stop().slideToggle(400);
    });
}


/* delay Info expand **********************************************************************
 **************************************************************************************/

function delayInfoExpand() {
    $('[data-delay-reveal="toggle"]').on('click', function(){
        var $this = $(this).parent();
        if (!$this.hasClass('animating')) {
            if($this.hasClass('expanded')){
                $this.children('[data-delay-reveal="target"]').stop().slideUp(400, function () {
                    $this.removeClass('expanded');
                });
            } else {
                $this.addClass('expanded');
                $this.addClass('animating');
                setTimeout(function () {
                    $this.children('[data-delay-reveal="target"]').stop().slideDown(400, function(){
                        $this.removeClass('animating');
                    });
                }, 400)
            }
        }
    });
}

/*  Info expand 2 -- for the my_genepeeks page  ***************************************
 **************************************************************************************/

function infoExpand2() {
    $('[data-reveal="toggle-inset-2"]').on('click', function(){
        var $parent = $(this).parent();
        $parent.toggleClass('expanded');
        if(!$parent.hasClass('expanded')){
            $parent.toggleClass('show');
            setTimeout(function(){
                $parent.children('[data-reveal="target"]').stop().slideToggle(400);
            }, 400);
        } else {
            $parent.children('[data-reveal="target"]').stop().slideToggle(500,function () {
                    $parent.toggleClass('show');
            });
        }

    });
}

/*  main accordion ********************************************************************
 **************************************************************************************/

function mainAccordion() {
    $('[data-accordion="toggle"]').on('click', function(){
        var $this = $(this);

        if(!$this.parent().hasClass('section-open')){
            $this.parent().parent('[data-accordion="container"]').children('.section-open').children('[data-accordion="target"]').stop().slideUp(400);
            $this.parent().parent('[data-accordion="container"]').children('.section-open').removeClass('section-open');
            $this.siblings('[data-accordion="target"]').stop().slideToggle(400);
            $this.parent().addClass('section-open');
        } else {
            $this.parent().parent('[data-accordion="container"]').children('.section-open').children('[data-accordion="target"]').stop().slideUp(400);
            $this.parent().parent('[data-accordion="container"]').children('.section-open').removeClass('section-open');
        }

    });
}

/*  variant selector ******************************************************************
 **************************************************************************************/

function variantSelector() {
    $("[data-variant^='toggle-']").each(function(i, e) {
      variantSelect($('[data-variant="toggle-'+(i+1)+'"]'),'[data-variant="variant-'+(i+1)+'"]');
    });

    function variantSelect(toggle, variant){
        toggle.on('click', function(){
            var $this = $(this);
            if($this.hasClass('active')){
                $this.parent().siblings('.variant-open').stop().slideUp(400,function () {
                    $(this).removeClass('variant-open');
                });
                $this.removeClass('active');
            } else {
                $this.parent().siblings('.variant-open').stop().slideUp(400, function() {
                    $(this).removeClass('variant-open');
                });
                $this.parent().children('.active').removeClass('active');
                $this.addClass('active');
                $this.parent().siblings(variant).stop().slideDown(400, function(){
                    $(this).addClass('variant-open');
                });
            }

        });
    }

}

/*  smooth scrolling  ******************************************************************
 **************************************************************************************/

$(function() {
    $('a[href*="#"]:not([href="#"])').click(function() {
        var $this = $(this);
        $('.active').removeClass('active');
        $this.addClass('active');
        setTimeout(function(){
            $('.active').removeClass('active');
            $this.addClass('active');
        },1100);
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});

/*  set active nav item  ******************************************************************
**************************************************************************************/

function activeItem() {
        $('.list-group-item').each(function(){
            var $this = $(this);
            var href = $this.attr('href');
            // Ensure the href is an anchor in the page
            if(href !== undefined && href.startsWith('#')) {
                var id = $(href);
                if(id.position() !== undefined){
                    $(window).on('scroll', function(){
                        var scrollP = $(document).scrollTop();
                        if(id.position().top <= scrollP  && id.position().top + id.height() > scrollP){
                            $('a[href="' + href + '"]').addClass('active');
                        } else {
                            $('a[href="' + href + '"]').removeClass('active');
                        }

                    });
                }
            }
        });
    $(window).on('scroll', function(){
        var scrollP = $(document).scrollTop() + $(window).height() + 50;
        if (scrollP >= $(document).height()){
            $('.active').removeClass('active');
            $('.list-group-item').last().addClass('active');
        }
    });


}

/*  disable anchor element  ***********************************************************
 **************************************************************************************/

function disableAnchor(){
    $('.disable-anchor').on('click', function(e){
        e.preventDefault();
    });
}


/*  Autotabbing functionality, will jump to next input  upon completion of the first  *
***************************************************************************************/
function bindAutoTab(class_identifier) {
    $(class_identifier).on('keyup', function(event) {
        if(event.keyCode != 9) {
            var $this = $(this);
            if($this.val().length == $this.attr('maxlength')) {
                $this.blur();
                var inputs = $(this).parent().siblings().eq($this.parents().index()).children('input');
                if(inputs.length)
                    inputs.focus();
            }
        }
    });
}


