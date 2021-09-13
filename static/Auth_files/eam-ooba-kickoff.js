(function ($) {
	$(document).ready(function() {
	    if ($("._learnMore") != null) {
	        $("._learnMore").each(function () {
	            if ($(this).text() == "" || $(this).attr("href") == null) { $(this).parent().hide(); }
	            else { if ($(this).attr("href") == "") { $(this).parent().hide(); } else { $(this).attr("target", "_blank"); } }
	        });
	    }
	});
}(jQuery));