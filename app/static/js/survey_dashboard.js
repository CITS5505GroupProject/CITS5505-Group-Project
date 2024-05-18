// Example data, replace with actual data passed from the backend
var surveys = {{ surveys|tojson | safe }};
const surveyList = document.getElementById('survey-list');

function displaySurveys() {
    surveyList.innerHTML = ''; // Clear current surveys
    surveys.forEach(survey => {
        if (isActiveSurvey(survey) && matchesSearch(survey)) { // Check if the survey should be shown
            const div = document.createElement('div');
            div.className = 'col-12 col-md-4 survey-item'; // Bootstrap classes for responsiveness
            div.setAttribute('data-type', survey.type);
            div.innerHTML = `
                <div class="card mb-4">
                    <div class="card-header">
                        <div class="d-flex align-items-center">
                            <img src="static/${survey.creator.profilePic}" class="rounded-circle me-2" width="40" height="40" alt="User">
                            <div>
                                <h6 class="mb-0">${survey.creator.username}</h6>
                                <small class="text-muted">Created at: ${survey.created_at}</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <p><strong>${survey.title}</strong></p>
                        <p class="card-text">${survey.description}</p>
                    </div>
                    <div class="card-footer d-flex justify-content-between align-items-center">
                        <a class="btn btn-info" href="/take-survey/${survey.id}">Answer</a> 
                    </div>
                </div>
            `;
            surveyList.appendChild(div);
        }
    });
}

function isActiveSurvey(survey) {
    const checkedTypes = Array.from(document.querySelectorAll('.filter-type:checked')).map(el => el.value);
    return checkedTypes.length === 0 || checkedTypes.includes(survey.type);
}

function matchesSearch(survey) {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    return (
        survey.title.toLowerCase().includes(searchInput) ||
        survey.description.toLowerCase().includes(searchInput) ||
        survey.creator.username.toLowerCase().includes(searchInput)
    );
}

function searchItems() {
    displaySurveys(); // Update display on search input
}

displaySurveys(); // Initial display

document.querySelectorAll('.filter-type').forEach(input => {
    input.addEventListener('change', displaySurveys); // Update display on filter change
});