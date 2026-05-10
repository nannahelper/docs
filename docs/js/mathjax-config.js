window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true
  },
  chtml: {
    matchFontHeight: false,
    scale: 1.0
  },
  startup: {
    typeset: true,
    ready: () => {
      MathJax.startup.defaultReady();
      
      // 确保页面完全加载后再次渲染
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
          setTimeout(() => {
            MathJax.typeset();
          }, 100);
        });
      } else {
        setTimeout(() => {
          MathJax.typeset();
        }, 100);
      }
    }
  }
};
