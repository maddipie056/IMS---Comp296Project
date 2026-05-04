console.log("empdashboard.js loaded");
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
    console.log("submitAdjustment fired:", action);
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
        return;
    }
    document.getElementById(`quantity-${selectedItemId}`).innerText = data.item.quantity;
    closeAdjustmentModal();
}
