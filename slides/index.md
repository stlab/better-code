---
regenerate: true
include_in_navigation: false
show_navigation: false
---
## Slide Chapter Index

{% assign slide_decks = site.pages | where_exp: "p", "p.dir == '/slides/'" %}
{% include navigation.html chapters=slide_decks %}
