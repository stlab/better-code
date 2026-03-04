/* Must load before MathJax runs */
if (window.MathJax && window.MathJax.Hub) {
  MathJax.Hub.Config({
    "HTML-CSS": {
      availableFonts: [],   // do not try local STIX
      webFont: "TeX",       // download TeX webfonts
      imageFont: null
    }
  });
}
