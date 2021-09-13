Fis = function() {};
Fis.Wizard = function () { };

Fis.Wizard.Preamble = '<div class="modal fade" id="wizardModal" tabindex="-1" role="dialog" aria-labelledby="wizardTitle" aria-hidden="true"> \
						<div class="modal-dialog" role="document"> \
							<div class="modal-content"> \
								<div class="modal-header"> \
									<h5 id="wizardTitle">Wizard</h5> \
									<button type="button" class="close" data-dismiss="modal" aria-label="Close"> \
										<span aria-hidden="true">&times;</span> \
									</button> \
								</div> \
								<div class="modal-body">';

Fis.Wizard.Postamble = '</div><div class="modal-footer"> \
							<div class="container">\
								<div id="buttonrow" class="row"> \
                                    <div class="col-lg col-sm w-100"> \
										<button id="modalSubmit" type="button" class="btn btn-primary w-100">Continue</button> \
									</div> \
									<div class="col-lg col-sm w-100"> \
										<button id="modalCancel" type="button" class="btn btn-secondary w-100" data-dismiss="modal">Close</button> \
									</div> \
								</div>\
                                <div id="progressbar" class="col-sm w100" style="display:none; text-align: center;"><img src="/eam/styles/images/page-loader.gif" alt="loading" /></div>\
                                <hr />\
								<div class="row">\
									<div id="actionHtml" class="col-lg col-sm w-100"></div> \
								</div>\
							</div>\
                            </div>\
						</div></div>';

// A function to set the button text of the wizard, checks
// for the attributes on the first element of the returned HTML.
Fis.Wizard.SetHooksAndText = function () {
	var e = $('[data-wizard-title]');

	// Set the title and button text
	var title = e.attr('data-wizard-title');
	var action_href = e.attr('data-wizard-action-href');
	var action_text = e.attr('data-wizard-action-text');

	var submit_text = e.attr('data-wizard-submit');
	var cancel_text = e.attr('data-wizard-cancel');
	
	if (title)
		$('#wizardTitle').html(title);

	if (submit_text)
		$('#modalSubmit').html(submit_text);
	else
		$('#modalSubmit').hide();

	if (cancel_text)
		$('#modalCancel').html(cancel_text);
	else
		$('#modalCancel').hide();

	// This is for the dumb links that are given by the view but displayed somewhere else is the dialog
	if (action_href && action_text)
		$('#actionHtml').html($('<a id="actionLink"></a>').attr('href', action_href).append(action_text));
	else
		$('#actionHtml').html('');

	$('#actionLink').click(function (event) {
		event.preventDefault();

		$.ajax({
			url: $(this).attr('href'),
            type: 'GET',
            cache: false
		}).done(function (data) {
			Fis.Wizard.ReplaceContent($('#wizardModal'), data);
		});
	});

	$('*[data-wizard-content-transfer]').click(function (event) {
		event.preventDefault();

		$.ajax({
			url: $(this).attr('data-wizard-content-transfer'),
            type: 'GET',
            cache: false
		}).done(function (data) {
			Fis.Wizard.ReplaceContent($('#wizardModal'), data);
		});
    });

    $("[type='tel']").keypress(function (event) {
        return Fis.Telephone.Keypress(event);
    });
};

Fis.Wizard.ReplaceContent = function (modal, data) {
	// Update the data container
	$('.modal-body').html(data);

	// Self-posting form?
	var new_form = $('form[data-auto-submit]');

    if (new_form.length > 0) {
        modal.hide();
        $('body').append(new_form);
        new_form.submit();
        return;
    }

    // Check to see if we are done
	var new_html = $('*[data-dismiss-redirect]');
	var redirect = new_html.attr('data-dismiss-redirect');

	if (new_html.length > 0) {
		modal.modal('hide');

		if (redirect)
			window.location.href = redirect;
	} else {
		// The modal lives, update button text
		Fis.Wizard.SetHooksAndText();
	}
};

Fis.SmartBanner = function () { };
Fis.SmartBanner.Initialize = function () {
    var stored_opts = sessionStorage.getItem("smartBanner");
    var options = null;

    if (typeof (stored_opts) === "string")
        options = JSON.parse(stored_opts);

    if (options) {
        $.smartbanner(options);
        return;
    }

    // Not local, call the server
    $.ajax('https://cibng.ibanking-services.com/eam/Branding/SmartBanner', {
        data: { appId: $('meta[data-appid]').attr('data-appid') },
        success: function (data) {
            sessionStorage.setItem('smartBanner', JSON.stringify(data));
            $.smartbanner(data);
        }
    });
};

Fis.Telephone = function () { };
Fis.Telephone.Keypress = function (event) {
    var charCode = (event.which) ? event.which : event.keyCode;

    if (charCode != 0 && (charCode > 31 && (charCode < 48 || charCode > 57))) {
        return false;
    }

    return true;
};

(function ($) {
	$(document).ajaxStop(function (event, request, settings) {
	});

	$(document).ajaxSuccess(function (event, jqXHR, ajaxOptions, data) {
	});

	$(document).ajaxError(function (event, request, settings) {
	});

    $(document).ready(function () {
        // Perform the action on any self-posting form
        if ($('#autoPost').length)
            setTimeout(function () { $('#autoPost').submit(); }, 250);

        // Set the timeout
        window.setTimeout(function () { window.location.href = 'https://cibng.ibanking-services.com/eam/credential/timeout'; }, 1200000);

        Fis.SmartBanner.Initialize();

        $("[type='tel']").keypress(function (event) {
            return Fis.Telephone.Keypress(event);
        });

		// Hook any modal activators that have dynamic content
		$('[data-modal-content-url]').click(function (event) {
			event.preventDefault();

			// Attribute data-modal-content-url will contain the endpoint
			$.ajax($(this).attr('data-modal-content-url'), {
                type: 'GET',
                cache: false,
				success: function (modalContent) {
					// Append the modal content to the body and activate the modal
					var modal_html = Fis.Wizard.Preamble + modalContent + Fis.Wizard.Postamble;
					$('body').append(modal_html);

					// Always remove the modal from the DOM after it's hidden
                    $('#wizardModal').off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
						$('#wizardModal').remove();
					});

                    // If the first dialog is a redirect, redirect without display the dialog.
					var new_html = $('*[data-dismiss-redirect]');
					var redirect = new_html.attr('data-dismiss-redirect');

					if (redirect) {
                        window.location.href = redirect;
                        return;
					}

                    // First time through make sure the button text is set correctly
					Fis.Wizard.SetHooksAndText(modalContent);
					
				    // bootstrap bug. when user presses enter while in an input box, 
				    //  the form submits as a standard POST and the modal dialog disappears.
                    //  <<Hook and Prevent>>

				    // Hook the form submit button
                    $('#modalSubmit').off('click').on('click', function () {
					    $('#wizardModal').submit();
					});

                    // Prevent form from performing a non-ajax post.
                    $('#wizardModal').off('submit').on('submit', function (e) {
					    e.preventDefault();

					    var modal = $('#wizardModal');
					    var form = $('form', modal);
					    var action = form.attr('action');

                        $('#buttonrow').hide();
                        $('#actionHtml').hide();
					    $('#progressbar').show();
                        
					    $.ajax({
					        url: action,
					        type: $(form).attr('method'),
					        data: $(form).serialize()
					    }).done(function (data) {
					            Fis.Wizard.ReplaceContent(modal, data);
					    }).fail(function () {
					    }).always(function () {
					        $('.modal-body').addClass('modal-body-shim');
					        $('#progressbar').hide();
					        $('#buttonrow').show();
					        $('#actionHtml').show();
					        $('.modal-body').removeClass('modal-body-shim');
					    });
					});




					// Activate the modal preventing modal dismissal from an outside click
					$('#wizardModal').modal({
						backdrop: 'static'
					});
				}
			});
		});
    });
}(jQuery));
