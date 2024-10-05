document.addEventListener('DOMContentLoaded', function() {

    // Insert the table into the DOM
    document.getElementById('board-container').appendChild(createBoard(serverBoard));
});


function serverRequest(input) {

    // Initialize data with nulls
    let data = {'square': null, 'reset': null};

    // If input is 'reset'
    if (input === 'reset') {
        data.reset = true;
    }

    // If input is a number
    else if (!isNaN(input)) {
        data.square = input;
    }

    // Send data via jQuery ajax function
    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: 'minesweeper',
        data: data,
        success: success
    });
}


// Handle the success response from Flask
function success(response) {

    // Catch if response is undefined
    if (response === undefined) {
        return;
    }

    // Updates board if there is there is visible or mines data
    if (response.visible || response.mines) {
        updateBoard(response);
    }
}


function createBoard(serverBoard) {
    
    // Create table element for board
    const table = document.createElement('table');
    table.className = 'board-table';

    // Create table head for timer, mines remaining, controls
    const thead = document.createElement('thead');
    thead.className = 'panel-container';
    
    // Create panel
    
    // Timer
    
    const thTimer = document.createElement('th');
    
    // Set items in header to span more than one col
    thTimer.colSpan="3"
    
    thTimer.className = 'timer';
    thTimer.id, thTimer.name = 'timer';
    thTimer.innerHTML = 'timer';
    
    thead.appendChild(thTimer);
    
    // Reset button
    const thReset = document.createElement('th');
    
    // Set items in header to span more than one col
    thReset.colSpan="3"
    
    let b = document.createElement('button');
    b.className = 'btn btn-outline-danger btn-block panel-button';
    b.id, b.name = 'reset';
    b.innerHTML = '<h2>Reset</h2>';

    // Add event listener; setting 'onclick' was activating on page load
    b.addEventListener('mouseup', (event) => {

        if (event.button === 0) {

            // Quick way to reset - literally refresh the page
            window.location.reload();
        }
    });
    
    // Add child elements to th, thead, table
    thReset.appendChild(b);
    thead.appendChild(thReset);
    table.appendChild(thead);
    
    // Create table body for buttons
    const tbody = document.createElement('tbody');

    for (let y = 0; y < serverBoard.height; y++) {

        // Create table row
        const tr = document.createElement('tr');

        // Create table data cells
        for (let x = 0; x < serverBoard.width; x++) {
            const td = document.createElement('td');

            // Calculate index from of (x, y) coordinates
            let index = y * serverBoard.height + x;

            // Create button
            let b = document.createElement('button')
            
            // Assign attributes to button
            b.className = 'square';
            b.name = index;
            b.id = index;

            // Add EventListeners to button
            b.addEventListener("mousedown", (event) => {
                if (isGameOver()) {
                    alert('game is over');
                }
                // Left mouse click
                if (event.button === 0) {
                    
                    // Send button id to server if not flag
                    if ((b.getAttribute('data-flag')) === null) {
                        serverRequest(b.id);
                    }
                }
                
                // Right mouse click
                else if (event.button === 2) {

                    // SUPPOSED TO PREVENT CONTEXT MENU APPEARING; NOT WORKING
                    event.preventDefault();
                    
                    // Toggle flag on/off
                    b.toggleAttribute('data-flag')
                }
            });
            
            // Grab focus on hover - BUG: this keeps focus even after mouse leaves square
            b.addEventListener("mousemove", (event) => {
                b.focus();
            });

            // TEMP FIX FOR RIGHT CLICK ISSUE - USE KEY 'F' INSTEAD
            b.addEventListener("keydown", (event) => {

                // Press 'F' for right click
                if (event.code === "KeyF") {

                    // Toggle flag on/off
                    b.toggleAttribute('data-flag')
                }
            });

            /* Set 'onclick' -- this is redundant due to 'addEventListener' above */
            // button.setAttribute('onclick', `serverRequest(${button.id})`);
            
            td.appendChild(b);
            tr.appendChild(td);
        }

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}


function updateBoard(response) {

    // Reveal if visible is not empty
    if (response.visible.length > 0) {

        // List of indices of visible squares
        for (let i = 0; i < response.visible.length; i++) {

            let b = document.getElementById(response.visible[i]);
            
            // Continue if flag
            if (b.getAttribute('data-flag') !== null) {
                continue;
            }

            // Square should be visible; disable the button
            b.disabled = true;

            // Display number in square
            let adj = response.adj[i];

            if (adj > 0) {
                b.textContent = adj;
            }
        }
    }

    if (response.mines.length > 0) {

        // List of indices of mines
        for (sq_index of response.mines) {
            let b = document.getElementById(sq_index);
            
            b.setAttribute('data-mine', true);
        }
    }
}


function isGameOver() {
    return document.querySelector('data-mine')
}