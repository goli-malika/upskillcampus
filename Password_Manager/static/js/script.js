function copyToClipboard(elementId) {
  const text = document.getElementById(elementId).innerText;
  navigator.clipboard.writeText(text).then(() => {
    const button = event.target;
    const original = button.innerText;
    button.innerText = 'Copied';
    setTimeout(() => {
      button.innerText = original;
    }, 1500);
  });
}
