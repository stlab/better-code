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
