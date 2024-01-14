document.querySelector('#dataForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let itemName = document.querySelector('#itemName').value;
    let itemQuantity = document.querySelector('#itemQuantity').value;
    let data = {itemName: itemName, itemQuantity: itemQuantity};

    // Save data to the database
    fetch('http://localhost:5000/save-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Fetch updated data from the database
        fetchData();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function fetchData() {
    fetch('http://localhost:5000/get-data')
        .then(response => response.json())
        .then(data => {
            let dataDisplay = document.querySelector('#dataDisplay');
            dataDisplay.innerHTML = '';
            data.forEach(item => {
                let itemDiv = document.createElement('div');
                itemDiv.textContent = `Item Name: ${item.itemName}, Item Quantity: ${item.itemQuantity}`;

                let deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.addEventListener('click', function() {
                    // Check if item.id is defined
                    if (item.id) {
                        // Delete data from the database
                        fetch(`http://localhost:5000/delete-data/${item.id}`, {
                            method: 'DELETE'
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);

                            // Fetch updated data from the database
                            fetchData();
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                    } else {
                        console.error('Error: item.id is undefined');
                    }
                });

                itemDiv.appendChild(deleteButton);
                dataDisplay.appendChild(itemDiv);
            });
        });
}

// Fetch initial data
fetchData();