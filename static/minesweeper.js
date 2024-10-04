document.addEventListener('DOMContentLoaded', function() {

    // Insert the table into the DOM
    document.getElementById('board-container').appendChild(createBoard(serverBoard));

    // Render board

})


function checkServer(index) {
    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: 'minesweeper',
        data: {'square': index},
        success: success
    })    
}


function success(){
    console.log("Completed POST request")
}


function createBoard(serverBoard) {
    
    // Initialize array of flags - bools
    flags = Array(serverBoard.width * serverBoard.height);
    
    // Initialize array of squares - <td><button>
    squares = Array(serverBoard.width * serverBoard.height);
    
    // Create table element for board
    const table = document.createElement('table');

    // Create table body
    const tbody = document.createElement('tbody');

    for (let y = 0; y < serverBoard.height; y++) {

        // Create table row
        const tr = document.createElement('tr');

        // Create table data cells
        for (let x = 0; x < serverBoard.width; x++) {
            const td = document.createElement('td');
            let index = y * serverBoard.height + x;
            
            // Set flag initial value to false
            flags[index] = false

            let b = document.createElement('button')
            squares[index] = b
            
            b.className = 'square';
            b.name = index;
            b.id = index;

            // Add EventListener to button
            b.addEventListener("mouseup", (event) => {
                
                // Left mouse click
                if (event.button === 0) {
                    
                    // Send button id to server if not flag
                    if (!(flags[b.id])) {
                        checkServer(b.id);
                    }
                }
                
                // Right mouse click
                else if (event.button === 2) {

                    // SUPPOSED TO PREVENT CONTEXT MENU APPEARING; NOT WORKING
                    event.preventDefault();
                    
                    // Toggle flag on/off
                    if (flags[index]) {
                        b.textContent = '0';
                        flags[index] = false;
                    }
                    else {
                        flags[index] = true;
                        b.textContent = 'f';
                    }
                }
            });
            
            // Grab focus on hover
            b.addEventListener("mousemove", (event) => {
                b.focus();
            });

            // TEMP FIX FOR RIGHT CLICK ISSUE - USE KEY 'F' INSTEAD
            b.addEventListener("keydown", (event) => {
                
                // Press 'F' for right click
                if (event.code === "KeyF") {

                    // Toggle flag on/off
                    if (flags[index]) {
                        flags[index] = false;
                        b.textContent = '';
                    }
                    else {
                        flags[index] = true;
                        b.textContent = 'f';
                    }
                }
            });

            // // Set 'onclick' -- this may be redundant due to 'addEventListener' above
            // button.setAttribute("onclick", `checkServer(${button.id})`);
            

            // SPLIT INTO RENDER BOARD
            // If square has been clicked
            if (serverBoard.visible[index]) {
                
                // Darken square
                b.style.backgroundColor = 'gray';

                // Display adj number if > 0
                if (serverBoard.adj[index] > 0) {
                    b.textContent = serverBoard.adj[index];
                }
            }

            if (flags[index] === true) {
                b.textContent = 'f';
            }
            
            td.appendChild(b);
            tr.appendChild(td);
        }

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}