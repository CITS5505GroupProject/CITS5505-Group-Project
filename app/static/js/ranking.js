document.addEventListener('DOMContentLoaded', function () {
    const accordion = document.querySelector('.accordion');
    const panel = document.querySelector('.panel');

    if (accordion) {
        accordion.addEventListener('click', function () {
            this.classList.toggle('active');
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }

    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');

    // 保证在悬停时保持下拉框显示
    dropdown.addEventListener('mouseenter', function () {
        dropdownContent.style.display = 'block';
    });

    dropdownContent.addEventListener('mouseenter', function () {
        dropdownContent.style.display = 'block';
    });

    dropdown.addEventListener('mouseleave', function () {
        setTimeout(() => {
            if (!dropdownContent.matches(':hover')) {
                dropdownContent.style.display = 'none';
            }
        }, 100);
    });

    dropdownContent.addEventListener('mouseleave', function () {
        setTimeout(() => {
            if (!dropdown.matches(':hover')) {
                dropdownContent.style.display = 'none';
            }
        }, 100);
    });

    // Load more rows
    const loadMoreButton = document.querySelector('.load-more');
    const extraRows = document.querySelectorAll('.extra-row');
    let isExpanded = false;

    loadMoreButton.addEventListener('click', function () {
        isExpanded = !isExpanded;
        extraRows.forEach(row => {
            row.style.display = isExpanded ? 'table-row' : 'none';
        });
        loadMoreButton.textContent = isExpanded ? 'Show Less' : 'Load More';
    });
});
