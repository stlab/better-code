---
title: Introduction
---

{% include slideshow.liquid %}

## Welcome

This is the introduction

```c++
int x = 3;
auto y = &x;
automobile = 4; // Here's a comment.
```

{{ note }}
This is a speaker note.  In theory it is supposed to

- Recognize markdown
- Truly
{{ endnote }}

{{ __ }}

### Stick around

```c++
template <class Container>
struct transcribe_iterator {
    using iterator_category = std::output_iterator_tag;
    using value_type = void;
    using difference_type = void;
    using pointer = void;
    using reference = void;
    using container_type = Container;

    transcribe_iterator(Container& c, typename Container::iterator i) : _c{&c}, _i{std::move(i)} {}

    constexpr auto& operator*() { return *this; }
    constexpr auto& operator++() {
        ++_i;
        return *this;
    }
```

<script>
// Create an instance of mark.js and pass an argument containing
// the DOM object of the context (where to search for matches)
var markInstance = new Mark(document);
// Remove previous marked elements and mark
// the new keyword inside the context
markInstance.unmark({
	done: function(){
  	markInstance.mark("constexpr", {});
  }
});
</script>

There's more to come!

{{ endslide }}
