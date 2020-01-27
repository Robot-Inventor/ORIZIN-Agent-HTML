jQuery(function() {
    jQuery("header").load("basic.html");
    jQuery.ripple(".ripple_effect", {
        debug: false,
        on: 'mousedown',
        opacity: 0.4,
        color: "auto",
        multi: false,
        duration: 0.7,
        rate: function(pxPerSecond) {
            return pxPerSecond;
        },
        easing: 'linear'
    });
});
