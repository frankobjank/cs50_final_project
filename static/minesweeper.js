document.addEventListener('DOMContentLoaded', function() {
    console.log("board = " + board.width);
    
    // Insert the table into the DOM
    document.getElementById('table-container').appendChild(createTable(board));

})


function checkSquare() {
    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: "minesweeper",
        data: {"name": 'test'},
        success: success
    })
    
    console.log("first element of square id " + document.querySelector('.square').id[0])
}


function success(){
    console.log("square id " + document.querySelector('.square').id)
}


function createTable(board) {
    // Create table element
    const table = document.createElement('table');

    // Create tbody and generate table rows
    const tbody = document.createElement('tbody');
    for (let y = 0; y < board.height; y++) {
        const tr = document.createElement('tr');

        // Create table data cells for each column in this row
        for (let x = 0; x < board.width; x++) {
            const td = document.createElement('td');
            let index = y * board.height + x;

            let value = board.adj[index];

            td.textContent = value;
            tr.appendChild(td);
        }

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}