(function(window, $) {
    var document = window.document;

    $(document).ready(function() {
        var url = $('.viewsitelink').attr('href');
        var preview = '<div id="preview_container"><iframe src="' + url + '" id="live_preview"></iframe></div>';
        $('#id_content').after(preview);
    })
}(window, django.jQuery));
