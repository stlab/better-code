---
layout: presentation2
---
{% comment %}
DWA In principle it should be possible to lift the textarea tag up into the
presentation2 template, but it doesn't seem to work for reasons I don't yet
understand.  Perhaps it's important that the markdown not be processed by jekyll.
{% endcomment %}

<textarea data-template>
## Slide 1
A paragraph with some text and a [link](http://hakim.se).
---
## Slide 2
---
## Slide 3
</textarea>
