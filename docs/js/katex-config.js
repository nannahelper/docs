function renderMath() {
  if (typeof renderMathInElement === 'undefined') {
    setTimeout(renderMath, 100);
    return;
  }
  
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$", right: "$", display: false },
      { left: "$$", right: "$$", display: true }
    ],
    throwOnError: false
  });
}

document.addEventListener('DOMContentLoaded', renderMath);

if (typeof document$ !== 'undefined') {
  document$.subscribe(renderMath);
}