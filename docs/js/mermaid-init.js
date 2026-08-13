document.addEventListener('DOMContentLoaded', function () {
  if (typeof mermaid === 'undefined') return;
  mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'strict' });
  mermaid.run({ querySelector: '.mermaid' });
});

if (typeof document$ !== 'undefined') {
  document$.subscribe(function () {
    if (typeof mermaid !== 'undefined') mermaid.run({ querySelector: '.mermaid' });
  });
}
