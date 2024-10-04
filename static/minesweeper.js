document.addEventListener('DOMContentLoaded', function() {

    // Insert the table into the DOM
    n = document.querySelector('.t');
    console.log(n);
    document.getElementById('table-container').appendChild(createTable(10, 10));

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



function createTable(rows, cols) {
    // Create table element
    const table = document.createElement('table');
    
    // Create thead and add header row
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    // First header cell (Row\Col)
    const firstHeaderCell = document.createElement('th');
    firstHeaderCell.textContent = 'Row\\Col';
    headerRow.appendChild(firstHeaderCell);

    // Generate column headers
    for (let col = 1; col <= cols; col++) {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create tbody and generate table rows
    const tbody = document.createElement('tbody');
    for (let row = 1; row <= rows; row++) {
        const tr = document.createElement('tr');
        
        // Create the first column (row header)
        const rowHeader = document.createElement('th');
        rowHeader.textContent = row;
        tr.appendChild(rowHeader);

        // Create table data cells for each column in this row
        for (let col = 1; col <= cols; col++) {
            const td = document.createElement('td');
            td.textContent = `${row},${col}`;
            tr.appendChild(td);
        }

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}