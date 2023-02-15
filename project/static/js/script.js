// Script For Close alert
var alert_del = document.querySelectorAll('.alert-del');
alert_del.forEach((x) =>
    x.addEventListener('click', function () {
        x.parentElement.classList.add('hidden');
    })
);

// Record Audio
