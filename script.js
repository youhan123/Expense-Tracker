function captureData() {
    // 1. Grab the values the user typed into the boxes
    let date = document.getElementById("dateInput").value;
    let category = document.getElementById("categoryInput").value;
    let description = document.getElementById("descInput").value;
    let amount = document.getElementById("amountInput").value;

    // 2. Package it into an object (this is exactly like a Python dictionary!)
    let newExpense = {
        date: date,
        category: category,
        description: description,
        amount: amount
    };

    // 3. Prove it worked!
    console.log("New Expense Captured:", newExpense);
    alert("Success! Your expense data was captured. Check the developer console.");

    // 4. THE INTERACTION: Force the HTML boxes to clear themselves
    document.getElementById("dateInput").value = "";
    document.getElementById("categoryInput").value = "Food"; // Resets dropdown to the first option
    document.getElementById("descInput").value = "";
    document.getElementById("amountInput").value = "";
}