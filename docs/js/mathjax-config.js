window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.startup.promise
    .then(() => {
      MathJax.startup.output.clearCache();
      MathJax.typesetClear();
      MathJax.texReset();
      return MathJax.typesetPromise();
    })
    .catch((err) => {
      console.warn("MathJax typeset failed:", err);
    });
});