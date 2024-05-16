document.addEventListener("DOMContentLoaded", function() {
    var acc = document.getElementsByClassName("accordion");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
});

function copyEmail() {
    const email = 'support@survey.com';
    navigator.clipboard.writeText(email).then(() => {
        alert('Email successfully copied');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}
