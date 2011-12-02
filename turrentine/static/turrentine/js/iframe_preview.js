(function(window, $) {
    var document = window.document;

    var iframe_name = 'live_preview';   // Name (and id) to give to the preview iframe
    var preview_url = 'preview';        // Relative url to send the POST data to
    var keypress_delay = 400;           // Number of milliseconds to wait before acting on keypress
    var latest_keypress = new Date();
    var latest_contents = '';

    $(document).ready(function() {
        var initial_url = $('.viewsitelink').attr('href');
        var preview = '<div id="preview_container"><iframe src="' + initial_url +
                      '" id="' + iframe_name + '" name="' + iframe_name + '"></iframe></div>';
        var form = $('#cmspage_form');
        var textarea = $('#id_content');

        // Insert the iframe into the document:
        textarea.after(preview);

        // Set the main form's target to the preview iframe, and POST to our
        // preview url to update the iframe's content.
        textarea.keyup(function(e) {
            var timestamp = new Date();
            latest_keypress = timestamp;

            setTimeout(function() {
                // If no keypresses have occurred since this one, and the
                // content field has changed, refresh the iframe with the main form's data:
                var another_key_was_pressed = (latest_keypress > timestamp);
                var was_changed = (textarea.val() !== latest_contents);

                if (!another_key_was_pressed && was_changed) {
                    latest_contents = textarea.val();
                    // Change the form's target to point to the iframe, and
                    // POST to it by submitting the form:
                    form.attr('target', iframe_name)
                        .attr('action', preview_url)
                        .submit()
                        .attr('target', '')     // Reset form target and action after submitting
                        .attr('action', '');
                }
            }, keypress_delay);
        });
    })
}(window, django.jQuery));
