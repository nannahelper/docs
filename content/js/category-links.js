/*
 * Material 的导航链接通常使用相对路径。
 * GitHub Pages 在访问没有结尾斜杠的目录地址时，会把这类链接解析到错误层级。
 * 根据站点配置计算前缀，统一修正分类概览入口。
 */
(function () {
  const categorySlugs = new Set([
    "cyber-literacy",
    "programming-languages",
    "data-and-computing",
    "web-and-data",
    "ai-and-ml",
    "systems-and-platforms",
    "networks-and-security",
    "embedded-and-hardware",
    "software-quality",
    "tools-and-productivity",
    "learning-map",
    "basic-skills",
    "technical-domains",
    "engineering-practice",
  ]);

  function getSitePrefix() {
    const header = document.querySelector("[data-site-url]");
    if (header) {
      return new URL(header.dataset.siteUrl, window.location.href).pathname.replace(/\/$/, "");
    }

    const canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) return "";

    const pathname = new URL(canonical.href, window.location.href).pathname;
    const marker = "/categories/";
    const markerIndex = pathname.indexOf(marker);
    return markerIndex >= 0 ? pathname.slice(0, markerIndex).replace(/\/$/, "") : "";
  }

  function normalizeCategoryLinks() {
    const sitePrefix = getSitePrefix();
    if (!sitePrefix) return;

    document.querySelectorAll("a[href]").forEach((link) => {
      const href = link.getAttribute("href");
      const match = href && href.match(/^(?:\.\.\/)+(?:categories\/)?([^/]+)\/$/);
      if (!match || !categorySlugs.has(match[1])) return;

      link.setAttribute("href", `${sitePrefix}/categories/${match[1]}/`);
    });
  }

  if (window.document$) {
    document$.subscribe(normalizeCategoryLinks);
  } else {
    document.addEventListener("DOMContentLoaded", normalizeCategoryLinks);
  }
})();
