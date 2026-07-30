document.querySelectorAll('[data-copy-citation]').forEach((button) => {
  button.addEventListener('click', async () => {
    const panel = button.closest('.citation-panel, [popover]');
    const citation = panel?.querySelector('[data-citation-text]')?.textContent?.trim();
    const status = panel?.querySelector('[data-copy-status]');
    if (!citation || !status) return;

    try {
      await navigator.clipboard.writeText(citation);
      status.textContent = 'BibTeX copied to clipboard.';
      button.textContent = 'Copied';
    } catch {
      status.textContent = 'Select the citation text and copy it manually.';
    }
  });
});
