let selectedItemId = null;
let selectedItemName = null;
let selectedItemQuantity = null;

function openAdjustmentModal(itemId, itemName, itemQuantity) {
    selectedItemId = itemId;
    selectedItemName = itemName;
    selectedItemQuantity = itemQuantity;

    document.getElementById('modalItemName').innerText = itemName;
    document.getElementById('modalItemQuantity').innerText = itemQuantity;
    document.getElementById('adjustmentModal').style.display = 'block';

}

function closeAdjustmentModal() {
    document.getElementById('adjustmentModal').style.display = 'none';
    document.getElementById('adjustmentAmount').value = '';
    document.getElementById('adjustmentError').innerText = '';
}
function openAddItemModal() {
    document.getElementById('addItemModal').style.display = 'block';
}
function closeAddItemModal() {
    document.getElementById('addItemModal').style.display = 'none';
    document.getElementById('item_name').value = '';
    document.getElementById('itemCategoryId').value = '';
    document.getElementById('sku').value = '';
    document.getElementById('quantity').value = '';
    document.getElementById('low_stock_threshold').value = '';
}
function submitNewItem() {
    const item_name = document.getElementById('item_name').value.trim();
    const category_id = parseInt(document.getElementById('itemCategoryId').value);
    const sku = document.getElementById('sku').value.trim();
    const quantity = parseInt(document.getElementById('quantity').value);
    const low_stock_threshold = parseInt(document.getElementById('low_stock_threshold').value);
    const errorBox = document.getElementById('newItemError');

    if(!item_name){
        alert('Item name is required');
        return;
    }
    if(isNaN(quantity) || quantity < 0){
        alert('Quantity must be a positive number');
        return;
    }
    if(isNaN(category_id)){
        alert('Please select a category');
        return;
    }
    if(isNaN(low_stock_threshold) || low_stock_threshold < 0){
        alert('Low stock threshold must be a positive number');
        return;
    }
    fetch('/api/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },        body: JSON.stringify({
            item_name,
            sku,
            quantity,
            low_stock_threshold,
            category_id
        })
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(result => {
        if (result.status === 201) {
            alert("Item added successfully");
            closeAddItemModal();
            location.reload();
        }
        else {
            alert(result.body.message || 'Failed to add item');
        }
    }).catch(error => {
        console.error('Error adding item:', error);
        alert('An error occurred while adding the item');
    }
    )
}
async function submitAdjustment(action) {
    const amount = parseInt(document.getElementById('adjustmentAmount').value);
    const errorBox = document.getElementById('adjustmentError');

    if (!amount || amount <= 0) {
        errorBox.innerText = 'Please enter a valid number';
        return;

    }

    const payload = {
        item_id: parseInt(selectedItemId),
        staff_id: parseInt(STAFF_ID),
        change_amount: amount,
        action: action
    };
    console.log("Payload:", payload);
    const response = await fetch('/api/adjustments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    let data;
    try{
        data = await response.json();
    }catch (err) {
        console.error("Non-JSON response (likely a server error):", err);
        errorBox.innerText = 'An unexpected error occurred. Please try again later.';
        return;
    }

    if (!response.ok) {
        errorBox.innerText = data.message || 'An error occurred';
    }
    document.getElementById(`quantity-${selectedItemId}`).innerText = data.item.quantity;
    closeAdjustmentModal();
}

async function updateThreshold() {
    const threshold = parseInt(document.getElementById('thresholdInput').value);
    if (!threshold || threshold < 0) {
        alert('Please enter a valid threshold');
        return;
    }
    try {
        const response = await fetch('/api/update-threshold', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ threshold: threshold })
        });
        let data;
        try{
            data = await response.json();
        }catch (err) {
            console.error("Non-JSON response (likely a server error):", err);
            alert('An unexpected error occurred. Please try again later.');
            return;
        }
        if (!response.ok) {
            alert(data.message || 'Failed to update threshold');
        }
        alert('Threshold updated successfully');
        location.reload();

    } catch (error) {
        console.error('Error updating threshold:', error);
        alert('An error occurred while updating threshold');
    }
}
