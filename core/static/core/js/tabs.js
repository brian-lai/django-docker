$(document).ready(function() {
	$(".tab-container .tab").on("click", function(e) {
		showTab($(e.currentTarget));
	});
});

function showTab(target) {
	var name = target.attr('anchor');

	if (!target.hasClass("selected")) {
		$(".tab").removeClass("selected");
		target.addClass("selected");
		$('.tab-content').addClass('hidden');
		$(name).removeClass('hidden');
	}
}
