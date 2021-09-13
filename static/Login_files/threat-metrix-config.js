$(function () {
    window.setTimeout(function () { window.location.href = window.location.href; }, 1200000);
    window.setTimeout(function () { TM.Process(); }, Number($('#tm_config').attr('data-waitTimeout')) * 1000);

    if ($($('#tm_config').attr('data-submit')).length > 0) { 
        $($('#tm_config').attr('data-submit')).click(function (event) {
            if (!TM.Processed) {
                TM.TriggerEvent = true;
                if ($($('#tm_config').attr('data-submit')).length > 0) {
                    $($('#tm_config').attr('data-submit')).prop('disabled', true);
                }
                event.preventDefault();
                return false;
            }
        });
    }

});

TM = function () { };
TM.Process = function () {
    TM.Processed = true;
    if ($($('#tm_config').attr('data-submit')).length > 0) {
        $($('#tm_config').attr('data-submit')).prop('disabled', false);
    }
    if ($('#tm_config').attr('data-selfpostingform') != '0') { TM.Submit(); }
    if (TM.TriggerEvent) { TM.Submit(); }
};
TM.Submit = function () {
    if ($($('#tm_config').attr('data-form')).length > 0) {
        $($('#tm_config').attr('data-form')).submit();
    }
};
TM.Processed = false;
TM.TriggerEvent = false;