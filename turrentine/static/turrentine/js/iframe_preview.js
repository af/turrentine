(function(window, $) {
    var document = window.document;

    var iframe_name = 'live_preview';   // Name (and id) to give to the preview iframe
    var preview_url = 'preview';        // Relative url to send the POST data to
    var keypress_delay = 400;           // Number of milliseconds to wait before acting on keypress
    var latest_keypress = new Date();

    $(document).ready(function() {
        var initial_url = $('.viewsitelink').attr('href');
        var preview = '<div id="preview_container"><iframe src="' + initial_url +
                      '" id="' + iframe_name + '" name="' + iframe_name + '"></iframe></div>';
        var form = $('#cmspage_form');

        // Insert the iframe into the document:
        $('#id_content').after(preview);

        // Set the main form's target to the preview iframe, and POST to our
        // preview url to update the iframe's content.
        $('#id_content').keyup(function(e) {
            var timestamp = new Date();
            latest_keypress = timestamp;

            setTimeout(function() {
                // If no keypresses have occurred since this one, refresh the
                // iframe using the main form's data:
                var another_key_was_pressed = (latest_keypress > timestamp);
                if (!another_key_was_pressed) {
                    form.attr('target', iframe_name)
                        .attr('action', preview_url)
                        .submit()
                        .attr('target', '')     // Reset target and action after submitting
                        .attr('action', '');
                }
            }, keypress_delay);
        });
    })
}(window, django.jQuery));
