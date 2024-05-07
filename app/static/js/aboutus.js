document.addEventListener("DOMContentLoaded", function() {
    var acc = document.getElementsByClassName("accordion");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            var allPanels = document.getElementsByClassName("panel");
            for (var j = 0; j < allPanels.length; j++) {
                if (allPanels[j] !== this.nextElementSibling) {
                    allPanels[j].style.maxHeight = null;
                    allPanels[j].previousElementSibling.classList.remove("active");
                }
            }
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
  
    var copyButton = document.querySelector('.email-button');
    if (copyButton) {
        copyButton.addEventListener('click', function() {
            var email = 'support@survey.com';
            navigator.clipboard.writeText(email).then(function() {
                alert("Email address copied: " + email);
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    }
  });
  