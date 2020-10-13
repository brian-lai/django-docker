$(document).ready(function() {
	// accordion menu
	$(".accordion .row .title").on("click", function(e) {
		var target = $(e.currentTarget).parent();
        $(target).toggleClass('open');
	});
});
