window.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("editor-container");

  // Function to add a new page to the editor
  window.addPage = function () {
    const newPage = document.createElement("div");
    newPage.className = "page";
    newPage.contentEditable = "true";
    container.appendChild(newPage);
    newPage.focus(); // Automatically focus on the new page
  };

  // Function to check for text overflow in pages
  function handleOverflow() {
    const pages = document.querySelectorAll(".page");
    pages.forEach((page, index) => {
      if (page.scrollHeight > page.clientHeight) {
        // Create a new page if the current page overflows
        const nextPage = pages[index + 1] || document.createElement("div");
        if (!nextPage.classList.contains("page")) {
          nextPage.className = "page";
          nextPage.contentEditable = "true";
          container.appendChild(nextPage);
        }

        // Move overflowing text to the next page
        const range = document.createRange();
        range.selectNodeContents(page);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        const overflowingContent = document.createDocumentFragment();
        while (page.scrollHeight > page.clientHeight && page.lastChild) {
          overflowingContent.insertBefore(page.lastChild, overflowingContent.firstChild);
        }

        nextPage.insertBefore(overflowingContent, nextPage.firstChild);
        nextPage.focus();
      }
    });
  }

  // Listen for input events to handle overflow
  container.addEventListener("input", handleOverflow);
});
