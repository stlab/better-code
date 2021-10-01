---
title: Slide Scratchpad
---

{% include slideshow.liquid %}

## Scratchpad

> This is a deck for experimentation with slide technology, not intended to be
> part of the course, but where we can effectively prove that techniques will
> work in-situ as part of the course site.

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

### Something with Fragments

1. {:.fragment}First Item
2. Second Item
3. {:.fragment }Third Item


```c++
// A code fragment
auto f() -> int { return 4; }
```
{:.fragment }

{{ __ }}

### Stick around 0

```c++
x = 1;
y = 2;
z = 3;
```

There's more to come!

{{ __ }}

### Stick around 1

```c++
x = 1;
y = 2;
z = 3;
```
{: data-mark="1" }

There's more to come!

{{ __ }}

### Stick around 2

```c++
x = 1;
y = 2;
z = 3;
```
{: data-mark="|1-2|2-3|1,3" }

There's more to come!

{{ __ }}

### Stick around 3

This:

```c++
A = 1;
B = 2;
C = 3;
```
{: data-mark="1|2-3" }

then this:

```c++
X = 1;
Y = 2;
Z = 3;
```
{: data-mark="3|2|1" }

{{ __ }}

### A long example

```c++
/**************************************************************************************************/
/**
    \ingroup name
    A compile-time precursor to name_t.
    This type is especially useful for setting up keys in advance, as work is
    done at compile-time to make conversion from a static_name_t to a name_t to
    be faster than creating a name_t at runtime. static_name_t does no work at
    runtime, instead leveraging c++11's `constexpr` feature to precompute token
    string hash values for immediate insertion into the underlying name table.
    \note
    You *cannot* create a `static_name_t` any way other than through the user
    defined literal. They can only be created at compile-time.
    \complexity
    The first time a static_name_t with a particular string is converted to a
    name_t is a `O(log N)` operation. Thereafter conversion of that same literal
    from a static_name_t to a name_t is on average `O(1)`.
    \promotes_to
        name_t
*/
struct static_name_t {
    /**
        \return
            \false iff the instance is equal to the empty string.
        \complexity
            O(1)
    */
    explicit operator bool() const;

    friend bool operator==(const static_name_t& x, const static_name_t& y) {
        return x.hash_m == y.hash_m;
    }

    friend bool operator!=(const static_name_t& x, const static_name_t& y) { return !(x == y); }

    friend bool operator<(const static_name_t& x, const static_name_t& y);

private:
    static_name_t() = delete;

    constexpr static_name_t(const char* str, std::size_t hash) : string_m(str), hash_m(hash) {}

    friend struct name_t;

    friend constexpr static_name_t literals::operator"" _name(const char* str, std::size_t n);

    friend std::ostream& operator<<(std::ostream& s, const static_name_t& name);

    const char* string_m;

    std::size_t hash_m;
};
```
{: data-mark="10|20-22|30-35|48" }

{{ endslide }}
