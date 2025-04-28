// This script enables copying text from a textarea to the clipboard

document.addEventListener('DOMContentLoaded', () => {
    // any button with data-target="#textareaId" will copy that textarea
    document.querySelectorAll('[data-copy-target]').forEach(btn => {
      btn.addEventListener('click', () => {
        const ta = document.querySelector(btn.getAttribute('data-copy-target'));
        const text = ta.value.trim();
        if (!text) return;
        navigator.clipboard.writeText(text)
          .then(() => {
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy to clipboard', 2000);
          })
          .catch(() => { btn.textContent = 'Error'; });
      });
    });
  });
  