function addQuestion() {
    var questionId = $('#questionsContainer .question').length + 1;
    $('#questionsContainer').append(`
        <div class="question" id="question${questionId}">
            <div class="card mt-2">
                <div class="card-body">
                    <label class="form-label" for="question${questionId}"><strong>Question${questionId}</strong></label>
                    <input class="form-control" type="text" name="question${questionId}" placeholder="Enter your question">
                    <div class="optionsContainer" id="optionsContainer${questionId}"></div>
                    <div class="btn-group mt-3">
                        <button class="btn btn-success" type="button" onclick="addOption(${questionId})">Add Option</button>
                        <button class="btn btn-danger" type="button" id="removeLastOption${questionId}" onclick="removeLastOption(${questionId})" disabled>Remove Last Option</button>
                        <button class="btn btn-danger" type="button" onclick="removeQuestion(${questionId})">Remove Question</button>
                    </div>
                    
                </div>
            </div>
        </div>
    `);
    addOption(questionId); // Add first default option
    addOption(questionId); // Add second default option
    updateRemoveButtonState(questionId);
}

function addOption(questionId) {
    var optionId = $(`#optionsContainer${questionId} .option`).length + 1;
    $(`#optionsContainer${questionId}`).append(`
        <div class="option" id="option${questionId}_${optionId}">
            <div class = "container mt-3">
                <label class="form-label" for="option${questionId}_${optionId}">Option ${optionId}</label>
                <input class="form-control" type="text" name="option${questionId}_${optionId}" placeholder="Enter option text">
            </div>
        </div>
    `);
    updateRemoveButtonState(questionId);
}

function removeLastOption(questionId) {
    var lastOptionId = $(`#optionsContainer${questionId} .option`).length;
    if (lastOptionId > 2) {
        $(`#option${questionId}_${lastOptionId}`).remove();
        updateRemoveButtonState(questionId);
    }
}

function removeQuestion(questionId) {
    $(`#question${questionId}`).remove();
    updateQuestionIDs();
}

function updateQuestionIDs() {
    $('#questionsContainer .question').each(function(index) {
        var newQuestionId = index + 1;
        var oldQuestionId = $(this).attr('id').replace('question', '');
        $(this).attr('id', `question${newQuestionId}`);
        $(this).find('label').first().text(`Question ${newQuestionId}`);
        $(this).find('input').first().attr('name', `question${newQuestionId}`);
        $(this).find('.optionsContainer').each(function() {
            $(this).attr('id', `optionsContainer${newQuestionId}`);
        });
        $(this).find('[onclick^="addOption"]').attr('onclick', `addOption(${newQuestionId})`);
        $(this).find('[onclick^="removeLastOption"]').attr('onclick', `removeLastOption(${newQuestionId})`);
        $(this).find('[onclick^="removeQuestion"]').attr('onclick', `removeQuestion(${newQuestionId})`);
    });
}

function updateRemoveButtonState(questionId) {
    var optionsCount = $(`#optionsContainer${questionId} .option`).length;
    var removeButton = $(`#removeLastOption${questionId}`);
    if (optionsCount > 2) {
        removeButton.prop('disabled', false);
    } else {
        removeButton.prop('disabled', true);
    }
}

$(document).ready(function() {
    $('#survey-form').submit(function(event) {
        // Check if there are any questions added
        if (!hasQuestions()) {
            event.preventDefault(); // Prevent form submission
            alert('Please add at least one question to the survey.');
            return;
        }

        // Validate all fields
        var allFieldsValid = validateFields();
        if (!allFieldsValid) {
            event.preventDefault(); // Prevent form submission
            alert('Please fill in all required fields.');
        }
    });

    function hasQuestions() {
        return $('#questionsContainer .question').length > 0;
    }

    function validateFields() {
        let isValid = true;
        // Check each question input
        $('.question input[type="text"]').each(function() {
            if ($(this).val().trim() === '') {
                $(this).css('border', '2px solid red'); // Highlight empty fields
                isValid = false;
            } else {
                $(this).css('border', ''); // Reset border if corrected
            }
        });

        // Check each option input
        $('.option input[type="text"]').each(function() {
            if ($(this).val().trim() === '') {
                $(this).css('border', '2px solid red'); // Highlight empty fields
                isValid = false;
            } else {
                $(this).css('border', ''); // Reset border if corrected
            }
        });

        return isValid;
    }
});
    