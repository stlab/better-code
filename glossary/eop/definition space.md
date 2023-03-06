(For a [[functional procedure]]) is that subset of [[value|values]] for its inputs to which it is intended to be applied.

A functional procedure always terminates on input in its definition space; while it may terminate for input outside its definition space, it may not return a meaningful value.

# Examples

```cpp
int square(int n) { return n * n; }
```

While the domain and codomain of `square` are `int`, its definition space is the set of integers whose square is representable by `int`, and its [[result space]] is the set of square integers representable by `int`. 

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.6