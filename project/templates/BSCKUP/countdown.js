// Get the countdown element from the DOM
var countdownEl = document.getElementById("countdown");

// Get the countdown container element from the DOM
var countdownContainerEl = document.getElementById("countdown-container");

// Get the start button from the DOM
var startBtn = document.getElementById("startBtn");

// When the start button is clicked, start the countdown
startBtn.addEventListener("click", function() {
  // Set the initial countdown value to 5 seconds
  var count = 5;

  // Update the countdown element with the initial value
  countdownEl.innerHTML = count;

  // Start the countdown timer
  var countdownTimer = setInterval(function() {
    // Decrement the countdown value
    count--;

    // Update the countdown element with the new value
    countdownEl.innerHTML = count;

    // If the countdown is finished, clear the interval and remove the countdown element
    if (count == 0) {
      clearInterval(countdownTimer);
      countdownContainerEl.remove();
    }
  }, 1000);
});
