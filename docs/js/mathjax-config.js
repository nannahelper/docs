window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)'], ['$', '$']],
    displayMath: [['\\[', '\\]'], ['$$', '$$']],
    processEscapes: true,
    packages: {'[+]': ['mhchem']}
  },
  svg: {
    fontCache: 'global'
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  },
  startup: {
    ready: () => {
      MathJax.startup.defaultReady();
      
      // 页面加载完成后立即渲染
      const renderMath = () => {
        try {
          MathJax.typeset();
        } catch (e) {
          console.warn('MathJax typeset error:', e);
        }
      };
      
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderMath);
      } else {
        renderMath();
      }
      
      // 监听页面内容变化，自动重新渲染
      const observer = new MutationObserver((mutations) => {
        let shouldRender = false;
        mutations.forEach((mutation) => {
          if (mutation.addedNodes.length > 0) {
            shouldRender = true;
          }
        });
        if (shouldRender) {
          requestAnimationFrame(() => {
            MathJax.typeset();
          });
        }
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  }
};
