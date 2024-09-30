import './jquery.js';

$(document).ready(function() {

    // Loop through button class 'correct'
    $('.correct').each(function() {

        // Add event listener for 'click'
        $(this).on('click', function() {

            // Set background color to green
            $(this).css('background-color', 'green')

            // Find paragraph in same div as button and write 'Correct!'
            $("p.result", $(this).parent()).html('Correct!');
        });
    });

    // Loop through button class 'incorrect'
    $('.incorrect').each(function() {

        // Add event listener for 'click'
        $(this).on('click', function() {

            // Set background color to red
            $(this).css('background-color', 'red')

            // Find paragraph in same div as button and write 'Incorrect'
            $("p.result", $(this).parent()).html('Incorrect');
        });
    });

// answer key array
let answer_key = ['0', '2061'];

// Keep track of index to check answer key
$('.free_button').each(function(index) {

    $(this).on('click', function() {

        let response = $("input.response", $(this).parent());

            // Compare value of input to the key
            if (response.val() === answer_key[index]) {

                // Set input box to green
                response.css('background-color', 'green');

                // Set p.result to 'Correct!'
                $("p.result", response.parent()).html('Correct!');

            // NO semi-colon after the 'if' statement since it is continued with 'else'
            } else {

                // Set input box to red
                response.css('background-color', 'red');

                // Set p.result to 'Incorrect'
                $("p.result", response.parent()).html('Incorrect');
            };
        });
    });
});
