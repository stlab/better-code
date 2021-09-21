---
regenerate: true
include_in_navigation: false
layout:
---
{% assign slide_decks = site.pages
   | where_exp: "p", "p.dir == '/slides/'"
   | where_exp: "p", "p.include_in_navigation != false"
  | sort: "path"
%}
<ul class="navigation">
  {% for p in slide_decks %}
  <li>
      <a href="{{ p.url | relative_url }}">{{p.title}}</a>
  </li>
  {% endfor %}
</ul>
