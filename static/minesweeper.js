document.addEventListener('DOMContentLoaded', function() {
    
    // Keep track if game has started for timer
    hasStarted = false;
    gameOver = false;

    // Adjust size of grid based on board vars
    // document.documentElement.style.setProperty('--grid-size', gridSize);
    
    // Insert to board-container: panel, board
    document.getElementById('board-container-small').appendChild(createPanel(serverBoard));
    document.getElementById('board-container-small').appendChild(createBoard(serverBoard));
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


// Create panel for mines remaining, reset, timer
function createPanel(serverBoard) {

    let panel = document.createElement('div');
    panel.className = 'panel';
    panel.id = 'panel';
 
    // Create panel
    // Mines Remaining
    const mines = document.createElement('span');
    mines.className = 'minesRemaining panel-span';
    mines.id = 'minesRemaining';
    mines.innerText = padNumber(serverBoard.num_mines);
    
    // Reset button
    const reset = document.createElement('button');
    reset.className = 'btn btn-outline-danger btn-block panel-button';
    reset.id = 'reset';
    reset.innerText = 'Reset';
    
    // Add event listener; setting 'onclick' was activating click on page load
    reset.addEventListener('mouseup', (event) => {
        if (event.button === 0) {  

            // Quick way to reset - literally refresh the page
            window.location.reload();
        }
    });
    
    // Timer
    const timer = document.createElement('span');
    timer.className = 'timer panel-span';
    timer.id = 'timer';
    timer.innerText = '000'

    // Add all elements to panel
    panel.appendChild(mines);
    panel.appendChild(reset);
    panel.appendChild(timer);

    return panel;
}


function createBoard(serverBoard) {

    // Create div element for board
    const board = document.createElement('div');
    board.className = 'board';
    board.id = 'board';

    for (let y = 0; y < serverBoard.height; y++) {

        // Create board row
        const row = document.createElement('div');
        row.className = 'board-row';

        // Create table data cells
        for (let x = 0; x < serverBoard.width; x++) {

            // Calculate index from (x, y) coordinates
            let index = y * serverBoard.height + x;

            // Create div for button
            let square = document.createElement('span');
            square.className = 'square';
            square.index = index;

            // Create button
            let b = document.createElement('button');
            
            // Assign attributes to button
            b.className = 'square-button';
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

                        document.getElementById('timer').innerHTML = padNumber(count);

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
                    let minesRemaining = serverBoard.num_mines - document.querySelectorAll('.square[data-flagged]').length;

                    // Set to 0 if below 0
                    if (0 > minesRemaining) {
                        minesRemaining = 0;
                    }
                    
                    // Add to panel; padded by 0s
                    document.getElementById('minesRemaining').innerText = padNumber(minesRemaining);
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
                    let minesRemaining = serverBoard.num_mines - document.querySelectorAll('.square[data-flagged]').length;
                    
                    // Set to 0 if below 0
                    if (0 > minesRemaining) {
                        minesRemaining = 0;
                    }
                    
                    // Add to panel; padded by 0s
                    document.getElementById('minesRemaining').innerText = padNumber(minesRemaining);
                }
            });

            square.appendChild(b);
            row.appendChild(square);
        }

        board.appendChild(row);
    }

    return board;
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
    
    // Game over; win
    if (response.win) {
        
        // Change reset text
        document.querySelector('#reset').textContent = 'WIN!'
    }

    // Game over; lose
    else if (response.mines.length > 0) {
        
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
}


// Pad minesRemaining and timer with 0s
function padNumber(num) {
    return num.toString().padStart(3, '0');
}
