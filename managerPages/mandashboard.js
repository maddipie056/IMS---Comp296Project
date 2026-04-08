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

async function submitAdjustment(action) {
    const amount = parseInt(document.getElementById('adjustmentAmount').value);
    const errorBox = document.getElementById('adjustmentError');

    if (!amount || amount <= 0) {
        errorBox.innerText = 'Please enter a valid number';
        return;

    }

    const payload = {
        item_id: selectedItemId,
        staff_id: STAFF_ID, // Replace with actual staff ID
        amount: amount,
        action: action
    };
    const response = await fetch('/api/stock-adjustment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    const data = await response.json();

    if (!response.ok) {
        errorBox.innerText = data.message || 'An error occurred';
    }
    document.getElementById(`quantity-${selectedItemId}`).innerText = data.new_quantity;
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
        const data = await response.json();
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