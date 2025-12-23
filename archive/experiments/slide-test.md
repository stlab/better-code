---
layout: slideshow
---
{% include slideshow.liquid %}

## First Slide

Some text with **bold** styling.

{{ __ }}

## Second Slide

> blockquote
with more text

{{ __ }}

## Third Slide
{% comment %}
Using jekyll's highlighter works, but we don't currently have a stylesheet that
makes the resulting HTML apparent to the viewer.  Should we care?
{% endcomment %}

```cpp
auto some_cplusplus_code() -> int {
  return 3;
}
```

```swift
var x = 10
```
{{ __ }}

## Fourth Slide

{% comment %}
Using reveal's highlighter doesn't seem to work.  Should we care?
That's ostensibly needed for line-by-line highlight animations.
{% endcomment %}

<pre><code data-line-numbers>
auto some_cplusplus_code() -> int {
  return 3;
}
</code></pre>

{{ endslide }}

<section>
<h2>Fifth Slide</h2>
<pre><code data-line-numbers>
auto some_cplusplus_code() -> int {
  return 3;
}
</code></pre>
</section>

<section data-auto-animate>
<h2>Diagram</h2>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://web.resource.org/cc/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" version="1.1" baseProfile="full" width="480px" height="360px" viewBox="0 0 480 360" preserveAspectRatio="xMidYMid meet" id="svg_document" style="zoom: 1;"><!-- Created with macSVG - https://macsvg.org/ - https://github.com/dsward2/macsvg/ --><title id="svg_document_title">Untitled.svg</title><defs id="svg_document_defs" d=""><path stroke="#000000" id="path1" stroke-width="3px" d="M133,325 C147,308 170,303 194,295 C218,287 86,328 134,328 C182,328 119,342 133,325 " fill="none" transform=""></path><path stroke="#000000" id="path2" stroke-width="3px" d="M39,328 C59,300 72,294 119,286 C166,278 226,250 255,264 C284,278 186,282 285,282 c99,0 -265,-65 -265,-65 " fill="none" transform=""></path></defs><g id="main_group"><rect height="360px" x="3px" y="23px" id="background_rect" width="480px" fill="#90ee90"></rect><text id="sample_text_element" x="240px" y="180px" font-family="Helvetica" font-size="30px" fill="black" xml:space="preserve" text-anchor="middle" text-rendering="geometricPrecision" transform="" style="outline-style:none;">Sample Text Element</text></g><polyline points="111,61 326,66 410,127 379,282 122,227 72,97 111,62 112,62 112,62 100,24 100,24" stroke="#000000" id="Quack" stroke-width="3px" d="" fill="none" transform=""></polyline><polygon points="99,275 94,314 225,312 160,262 77,208" stroke="#000000" id="polygon1" stroke-width="3px" fill="#ffffff" transform=""></polygon><rect stroke="#000000" x="347px" height="38px" y="217px" id="rect1" stroke-width="3px" width="78px" fill="#ffffff" transform=""></rect><rect stroke="#000000" height="50px" x="345px" y="271px" id="rect2" stroke-width="3px" width="69px" fill="#efad" transform=""></rect></svg>
</section>

<section data-auto-animate>
<h2>Diagram</h2>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://web.resource.org/cc/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" version="1.1" baseProfile="full" width="480px" height="360px" viewBox="0 0 480 360" preserveAspectRatio="xMidYMid meet" id="svg_document" style="zoom: 1;"><!-- Created with macSVG - https://macsvg.org/ - https://github.com/dsward2/macsvg/ --><title id="svg_document_title">Untitled.svg</title><defs id="svg_document_defs" d=""><path stroke="#000000" id="path1" stroke-width="3px" d="M133,325 C147,308 170,303 194,295 C218,287 86,328 134,328 C182,328 119,342 133,325 " fill="none" transform=""></path><path stroke="#000000" id="path2" stroke-width="3px" d="M39,328 C59,300 72,294 119,286 C166,278 226,250 255,264 C284,278 186,282 285,282 c99,0 -265,-65 -265,-65 " fill="none" transform=""></path></defs><g id="main_group"><rect x="3px" height="360px" y="23px" id="background_rect" width="480px" fill="#90ee90"></rect><text id="sample_text_element" x="240px" y="180px" font-family="Helvetica" font-size="30px" fill="black" xml:space="preserve" text-anchor="middle" text-rendering="geometricPrecision" transform="" style="outline-style:none;">Sample Text Element</text></g><polyline points="111,61 200,75 410,127 440,360 122,227 72,97 111,62 112,62 112,62 100,24 100,24" stroke="#000000" id="Quack" stroke-width="3px" d="" fill="none" transform=""></polyline><polygon points="99,275 94,314 225,312 160,262 77,208" stroke="#000000" id="polygon1" stroke-width="3px" fill="#ffffff" transform=""></polygon><rect stroke="#000000" x="347px" height="38px" y="217px" id="rect1" stroke-width="3px" width="78px" fill="#ffffff" transform=""></rect><rect stroke="#000000" height="50px" x="345px" y="271px" id="rect2" stroke-width="3px" width="69px" fill="#efad" transform=""></rect></svg>
</section>
