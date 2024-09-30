// Wait for everything on page to load
document.addEventListener('DOMContentLoaded', function() {

    // Keep track of which questions have been answered
    // let answers=[]

    // Create array of correct answer elements before checking for user input
    // '.' used to reference class
    let corrects = document.querySelectorAll('.correct');

    // Add event listeners to each correct button
    for (let i = 0; i < corrects.length; i++) {
        corrects[i].addEventListener('click', function() {

            // Set background color to green
            corrects[i].style.backgroundColor = 'green';

            // go to parent element and add message
            corrects[i].parentElement.querySelector('.result').innerHTML = 'Correct!';
        });
    }

    // Add event listeners to each incorrect button
    let incorrects = document.querySelectorAll('.incorrect');
    for (let i = 0; i < incorrects.length; i++) {
        incorrects[i].addEventListener('click', function() {

            // Set background color to red
            incorrects[i].style.backgroundColor = 'red';

            // go to parent element and add message
            incorrects[i].parentElement.querySelector('.result').innerHTML = 'Incorrect';
        });
    }

    // Answer key array to check free response against
    let answer_key = ['0', '2061'];

    // NodeList of all submit buttons for free responses (selected by class)
    let answer_buttons = document.querySelectorAll('.free_submit');

    // NodeList of all free response answers (selected by class)
    let free_answers = document.querySelectorAll('.response');

    // Add listeners to all submit buttons
    for (let i = 0; i < answer_buttons.length; i++) {
        answer_buttons[i].addEventListener('click', function() {

            // Debug - see contents of answer
            // alert(`answer = ${free_answers[i]}, answer.value = ${free_answers[i].value}`)

            // Compare value of input to the key
            if (free_answers[i].value === answer_key[i]) {

                // Right answer; set to green
                free_answers[i].style.backgroundColor = 'green';

                // Print 'correct'
                free_answers[i].parentElement.querySelector('.result').innerHTML = 'Correct!';
            } else {

                // Wrong answer; set to red
                free_answers[i].style.backgroundColor = 'red';

                // Print 'incorrect'
                free_answers[i].parentElement.querySelector('.result').innerHTML = 'Incorrect';
            }
        });
    }
});
