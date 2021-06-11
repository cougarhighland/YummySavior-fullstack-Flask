order = []

foodList = document.getElementById('food-list');
orderTable = document.getElementById('order-table');
confirmBtn = document.getElementById('confirm-btn');
orderTableBody = document.getElementById('order-content');

foodList.addEventListener('click', (e) => {
    if (e.target.classList.contains('addItem')) {
        const column = e.target.parentElement.parentElement.children;
        const id = column[0].innerText;
        const name = column[1].innerText;
        const info = column[2].innerText;
        const business = column[3].innerText;
        const location = column[4].innerText;
        const quantity = column[5];
        const orderQuantity = column[6].firstElementChild;

        if (orderQuantity.value < 1){
            return
        }

        if (quantity.innerText - Math.abs(orderQuantity.value) >= 0){
            // Update the quantity
            quantity.innerText = quantity.innerText - orderQuantity.value;
            // Create a row in the order table
            orderTableBody.innerHTML += `
            <tr>
                <th scope='row'>${id}</th>
                <td>${name}</td>
                <td>${info}</td>
                <td>${business}</td>
                <td>${location}</td>
                <td>${orderQuantity.value}</td>
                <td><button class='btn btn-danger btn-sm remove-btn'>X</button></td>
            </tr>
            `
            order.push({"id":id,"quantity": orderQuantity.value});
            orderQuantity.value = '';
        }
    }
});

orderTableBody.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-btn')) {

        // Add the quantity back to the list
        quantityOrdered = e.target.parentElement.previousElementSibling.innerText;
        orderFoodId = e.target.parentElement.parentElement.firstElementChild.innerText;
        listFoodItem = document.getElementById(orderFoodId);
        listFoodQty = listFoodItem.children[5];
        listFoodQty.innerText = parseInt(listFoodQty.innerText) + parseInt(quantityOrdered);

        // remove the item from the dom
        row = e.target.parentElement.parentElement;
        row.parentElement.removeChild(row);

        // remove the item from the order object
        for(i=0; i < order.length; i++){
            if(order[i].id == orderFoodId){
                order.splice(i, i+1)
            }
        }
    }
})

confirmBtn.addEventListener('click', (e) =>{

    if (order.length < 1){
        return
    }

    fetch('/order', {
        method: 'POST',
        body: JSON.stringify(order),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(
        response => {
            if(response.status == 200){
                window.location = '/';
            }
        }
    )
})

