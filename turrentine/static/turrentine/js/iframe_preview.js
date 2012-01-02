(function(window, $) {
    var document = window.document;

    var iframe_name = 'live_preview';   // Name (and id) to give to the preview iframe
    var preview_url = 'preview';        // Relative url to send the POST data to
    var keypress_delay = 800;           // Number of milliseconds to wait before acting on keypress

    var latest_change = new Date();
    var latest_contents = '';
    var form_has_changed = false;

    var form, textarea;

    // Load the preview page into our iframe element.
    function load_iframe() {
        latest_contents = textarea.val();
        // Change the form's target to point to the iframe, and
        // POST to it by submitting the form:
        form.attr('target', iframe_name)
            .attr('action', preview_url)
            .submit()
            .attr('target', '')     // Reset form target and action after submitting
            .attr('action', '');
    }

    // Check the state of our data, and if something has changed, load our
    // preview after our throttling interval.
    function handle_updates(e) {
        var timestamp = new Date();
        latest_change = timestamp;
        form_has_changed = true;

        setTimeout(function() {
            // If no changes/keypresses have occurred since this one, and the
            // form data has changed, refresh the iframe with the main form's data:
            var more_recent_change_occurred = (latest_change > timestamp);
            var state_has_changed = (e.target.id !== textarea.attr('id')) || (textarea.val() !== latest_contents);

            if (!more_recent_change_occurred && state_has_changed) {
                load_iframe();
            }
        }, keypress_delay);
    }

    $(document).ready(function() {
        var preview = '<div id="preview_container"><iframe src="" ' +
                      'id="' + iframe_name + '" name="' + iframe_name + '"></iframe></div>';

        form = $('#cmspage_form');
        textarea = $('#id_content');

        // Insert the iframe into the document and update iframe on keyup events:
        textarea.after(preview).keyup(handle_updates);
        load_iframe();

        // Update iframe when the title or template fields change as well:
        $('#id_title, #id_template_name').change(handle_updates);

        // If submitting the form normally (Save button), prevent beforeunlod event:
        form.bind('submit', function(e) {
            var is_regular_submission = !e.target.target;
            if (is_regular_submission) {
                form_has_changed = false;
            }
        });
        $(window).bind('beforeunload', function(e) {
            if (form_has_changed) { return 'You have unsaved changes!'; }
        });
    });
}(window, django.jQuery));
