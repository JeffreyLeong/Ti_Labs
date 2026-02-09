// 1. Get references to elements on the page
const billInput = document.getElementById("bill");
const tipInput = document.getElementById("tip");
const calculateBtn = document.getElementById("calculate");
const tipAmountDisplay = document.getElementById("tip-amount");
const totalAmountDisplay = document.getElementById("total-amount");
const presetButtons = document.querySelectorAll(".preset");

// Shared calculate function
function calculateTip(bill, percent) {
    if (isNaN(bill) || isNaN(percent)) {
        tipAmountDisplay.textContent = "$0.00";
        totalAmountDisplay.textContent = "$0.00";
        return;
    }

    const tip = bill * (percent / 100);
    const total = bill + tip;

    tipAmountDisplay.textContent = `$${tip.toFixed(2)}`;
    totalAmountDisplay.textContent = `$${total.toFixed(2)}`;
}

// 2. When user clicks the Calculate button
calculateBtn.addEventListener("click", function(event) {
    event.preventDefault();
    const bill = parseFloat(billInput.value);
    const tipPercent = parseFloat(tipInput.value);
    calculateTip(bill, tipPercent);
});

// 3. When user clicks a preset (auto calculate)
presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        const presetValue = parseFloat(btn.dataset.tip);
        const bill = parseFloat(billInput.value);

        // Fill input box
        tipInput.value = presetValue;

        // Auto-calc
        calculateTip(bill, presetValue);

        // Highlight active button
        presetButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
    });
});
