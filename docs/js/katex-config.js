(function() {
  var attempts = 0;
  
  function renderMath() {
    if (typeof renderMathInElement === 'undefined') {
      attempts++;
      if (attempts < 20) {
        setTimeout(renderMath, 100);
      }
      return;
    }
    
    console.log('KaTeX rendering started...');
    
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$", right: "$", display: false },
        { left: "$$", right: "$$", display: true }
      ],
      throwOnError: false,
      strict: false
    });
    
    console.log('KaTeX rendering completed');
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderMath);
  } else {
    renderMath();
  }
  
  if (typeof document$ !== 'undefined') {
    document$.subscribe(renderMath);
  }
})();