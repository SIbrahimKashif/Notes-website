function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function closeAlerts() {
  let alertElements = document.querySelectorAll('.alert');

  alertElements.forEach(function (alertElement) {
    setTimeout(function () {
      alertElement.classList.add('hide'); // Add a hide class to start fading out
      setTimeout(function () {
        alertElement.remove(); // Remove the alert from the DOM
      }, 1000); // Remove after fade out animation (1 second)
    }, 5000); // 5 seconds timeout before starting the fade out
  });
}

document.addEventListener('DOMContentLoaded', function () {
  closeAlerts(); // Call the function to close alerts after 5 seconds
});
