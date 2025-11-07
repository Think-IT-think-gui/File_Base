'use strict'
/* PWA services worker register */
if ("serviceWorker" in navigator) {
    window.addEventListener("load", function (event) {
        navigator.serviceWorker
            //.register("././serviceWorker.js", {
            .register("https://www.omanager.world/static/sw.js", {
                scope: './'
            })
            .then(reg => console.log("service worker registered"))
            .catch(err => console.log("service worker not registered"));
    });
}

window.addEventListener("appinstalled", function (event) {
    //app.logEvent("a2hs", "Installed");
    document.getElementById('toastinstall').style.display = 'none';
});

if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    navigator.serviceWorker.register('https://www.omanager.world/static/sw.js')
    .then(function(registration) {
        console.log('Service Worker Registered with scope:', registration.scope);
    })
    .catch(function(error) {
        console.error('Service Worker registration failed:', error);
    });
}




if (window.matchMedia('(display-mode: fullscreen)').matches) {
    $('#toastinstall').fadeOut()
} else {
    $('#toastinstall').fadeIn()
}
