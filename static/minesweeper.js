document.addEventListener('DOMContentLoaded', function() {
    console.log(squares)
    let board = {
        'adj': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1, 1, 1, 0, 0, 1, 2, 1, 1, 0, 1, 0, 2, 1, 0, 0, 1, 1, 1, 1, 1, 3, 0, 2, 0, 2, 3, 2, 0, 1, 0, 2, 0, 2, 0, 0, 2, 0, 2, 1, 0, 1, 1, 1, 0, 1, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], 
        'flags': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'visible': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    // Insert the table into the DOM
    document.getElementById('table-container').appendChild(createTable(10, 10, board));

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


function createTable(width, height, squares) {
    // Create table element
    const table = document.createElement('table');

    // Create tbody and generate table rows
    const tbody = document.createElement('tbody');
    for (let y = 0; y < height; y++) {
        const tr = document.createElement('tr');

        // Create table data cells for each column in this row
        for (let x = 0; x < width; x++) {
            const td = document.createElement('td');
            let index = y * height + x;

            let value = squares.adj[index];

            td.textContent = value;
            tr.appendChild(td);
        }

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}