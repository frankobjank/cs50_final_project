document.addEventListener('DOMContentLoaded', function() {
    
    // Keep track if game has started for timer
    hasStarted = false;
    gameOver = false;

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

    // Set gameOver to true if mines are included in response
    if (response.mines.length > 0 || response.win) {
        gameOver = true;
    }
}


function createBoard(serverBoard) {

    const numMines = serverBoard.num_mines;

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
    thTimer.colSpan="4"
    
    thTimer.className = 'timer';
    thTimer.id = 'timer';
    thTimer.innerText = '00:00'

    // Add th to thead
    thead.appendChild(thTimer);
    
    // Reset button
    const thReset = document.createElement('th');
    
    // Set items in header to span more than one col
    thReset.colSpan="2"
    
    let b = document.createElement('button');
    b.className = 'btn btn-outline-danger btn-block panel-button';
    b.id = 'reset';
    b.innerText = 'Reset';
    
    // Add event listener; setting 'onclick' was activating on page load
    b.addEventListener('mouseup', (event) => {
        
        if (event.button === 0) {
            
            // Quick way to reset - literally refresh the page
            window.location.reload();
        }
    });

    // Add button to th
    thReset.appendChild(b);

    // Add th to thead
    thead.appendChild(thReset);
    
    // Mines Remaining
    const thMines = document.createElement('th');
    
    // Set items in header to span more than one col
    thMines.colSpan="4"
    
    thMines.className = 'minesRemaining';
    thMines.id = 'minesRemaining';
    thMines.innerText = `Mines left: ${numMines}`

    // Add th to thead
    thead.appendChild(thMines);
    
    // Add thead to table
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
                
                if (!hasStarted) {
                    hasStarted = true;
                    
                    // Start the timer
                    let count = 0;
                    let intervalId = setInterval(() => {
                        count++;
                        
                        // Stop timer if game over and exit early
                        if (gameOver) {
                            clearInterval(intervalId);
                            return;
                        }

                        // Get minutes and seconds
                        let minutes = Math.floor(count / 60);
                        let seconds = count % 60;

                        // Split minutes and seconds into digits to add leading zeroes
                        thTimer.innerHTML = `${Math.floor(minutes / 10)}${minutes % 10}:${Math.floor(seconds / 10)}${seconds % 10}`;

                    }, 1000);
                }

                // Left mouse click
                if (event.button === 0 && !gameOver) {
                    
                    // Send button id to server if not flag
                    if (b.getAttribute('data-flagged') === null) {
                        serverRequest(b.id);
                    }
                }
                
                // Right mouse click
                else if (event.button === 2 && !gameOver) {

                    // SUPPOSED TO PREVENT CONTEXT MENU APPEARING; NOT WORKING
                    event.preventDefault();
                    
                    // Toggle flag true/false
                    b.toggleAttribute('data-flagged');

                    // Calc mines - flags for Remaining Mines value
                    let minesRemaining = numMines - document.querySelectorAll('.square[data-flagged]').length;

                    // Set to 0 if below 0
                    if (0 > minesRemaining) {
                        minesRemaining = 0;
                    }
                    
                    // Add to panel
                    thMines.innerText = `Mines left: ${minesRemaining}`;
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

                    // Toggle flag true/false
                    b.toggleAttribute('data-flagged');

                    // Calc mines - flags for Remaining Mines value
                    let minesRemaining = numMines - document.querySelectorAll('.square[data-flagged]').length;
                    
                    // Set to 0 if below 0
                    if (0 > minesRemaining) {
                        minesRemaining = 0;
                    }
                    
                    // Add to panel
                    thMines.innerText = `Mines left: ${minesRemaining}`;
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
            
            // Pass without revealing if flag
            if (b.getAttribute('data-flagged') !== null) {
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

    // Game over; lose
    if (response.mines.length > 0) {
        
        // List of indices of mines
        for (sqIndex of response.mines) {
            let b = document.getElementById(sqIndex);
            
            // Reveal mine if it was not flagged
            if (b.getAttribute('data-flagged') === null) {
                // Set mine attribute
                b.toggleAttribute('data-mine');
                b.innerText = '*';
            }
        }

        // Check if any squares were wrongly flagged
        document.querySelectorAll('.square[data-flagged]').forEach((b) => {
            
            // b is not a mine
            if (b.getAttribute('data-mine') === null) {
                b.toggleAttribute('data-false-flag');
            }
        });

        // Change reset text
        document.querySelector('#reset').textContent = 'LOSE'
    }
    
    // Game over; win
    else if (response.win) {
        // Change reset text
        document.querySelector('#reset').textContent = 'WIN!'
    }
}
