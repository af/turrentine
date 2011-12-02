(function(window, $) {
    var document = window.document;

    var iframe_name = 'live_preview';   // Name (and id) to give to the preview iframe
    var preview_url = 'preview';        // Relative url to send the POST data to
    var keypress_delay = 400;           // Number of milliseconds to wait before acting on keypress
    var latest_change = new Date();
    var latest_contents = '';

    var form, textarea;

    // Set the main form's target to the preview iframe, and POST to our
    // preview url to update the iframe's content.
    function update_preview(e) {
        var timestamp = new Date();
        latest_change = timestamp;

        setTimeout(function() {
            // If no changes/keypresses have occurred since this one, and the
            // form data has changed, refresh the iframe with the main form's data:
            var more_recent_change_occurred = (latest_change > timestamp);
            var state_has_changed = (e.target.id !== textarea.attr('id')) || (textarea.val() !== latest_contents);

            if (!more_recent_change_occurred && state_has_changed) {
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
    }

    $(document).ready(function() {
        var initial_url = $('.viewsitelink').attr('href');
        var preview = '<div id="preview_container"><iframe src="' + initial_url +
                      '" id="' + iframe_name + '" name="' + iframe_name + '"></iframe></div>';

        form = $('#cmspage_form');
        textarea = $('#id_content');

        if (initial_url) {
            // Insert the iframe into the document and update iframe on keyup events:
            textarea.after(preview).keyup(update_preview);

            // Update iframe when the title or template fields change as well:
            $('#id_title, #id_template_name').change(update_preview);
        }
    });
}(window, django.jQuery));
