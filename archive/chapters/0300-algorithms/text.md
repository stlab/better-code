---
---

## Algorithms

_New Oxford American Dictionary_ defines _algorithm_ as:

Algorithm, _n_
: a process or set of rules to be followed in calculations or other problem-solving operations, especially by a computer.

Algorithms are an abstraction of computation, and every program is an algorithm. It is easy to be distracted by class hierarchies, software architecture, design patterns, etc. Such things are helpful only in so far as they aid in implementing a correct and efficient algorithm.

<!-- Tie to David's introduction -->


<!-- This section will be revisited after the contracts chapter is complete - this is just a rough -->

The last chapter introduced contracts to specify an algorithm's domain and semantics. We use functions to name algorithms, preconditions define the domain of the algorithm, and postconditions define the semantics. Here is a simple operation to illustrate:

```cpp
// returns the minimum value of `a` and `b`
int min(int a, int b) {
    return (a < b) ? a : b;
}
```

The `min` function has no preconditions which is another way of saying the domain of `min` is the set of values representable by a pair of `int` types.

<!-- not ready for this yet.

Let's look at the `find()` algorithm developed in the last chapter:

```cpp
/// Returns the first index of `argv`'s 2nd element in the remainder of `argv`,
/// or `argc` if it can't be found.
///
/// - Requires: `argv` is an array of `argc` C-strings.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```

-->



---

- Let's honor what computers are actually all about: computation.  Algorithms
  are an abstraction of computation. Doing so has consequences:
  - Naming
  - Documentation
  - Complexity analysis
- Doing so serves:
  - efficiency
  - maintainability
  - local reasoning

#### Flow

- Every function is an algorithm
- Trivial example (e.g. find an `int`)
  - do this from `main`

- Find a double
  - Show a precondition (find a `double`; no NaNs).
  - put them in the same program, use the same name as overloads
  - provides a place to document the precondition
  - hinting at no raw loops - show power of identifying the algorithms
  - begin the discussion of documentation practice; identify as a thread that
    will extend through everything we do.

- Show genericity
  - show lifting of EqualityComparable concept
  - show how genericity aids readability

- Show simple mutation (e.g. replace first instance).
  - introduce aliasing and how it creates preconditions (copy range to
    overlapping-but-not-identical range), giving us a platform for value
    semantics.
  - aliasing is an unscalable construct

- Understanding the domain
  - The domain has started to become evident (example of discovery)
  - There are other domains (numerics, graphs, ...); we are working with sequences.
  - Discuss properties of sequences, half-open ranges, iterators

- Show how algorithms compose
  - Show some examples of how to decompose real things into other algorithms
    - Slide (break down into three cases)
      - Gather as an elaboration.
    - Elementwise
      - Relate back to find, which is elementwise composition with itself
      - Rotate on forward iterators, a beautiful and more complicated example
         - Forward partition might be simpler...
    - Stable partition (top-down divide-and-conquer rotates)
    - Reverse (bottom-up)

- (maybe with reverse) a conversation on complexity and efficiency
  - Show quadradic (delete by predicate)
  - You want contiguous memory, which has random access
  - You don't want to use the random access (memory works like a tape drive)
  - A few algorithms like reverse win by using bidirectional traversal \[benchmark\]
  - Complexity goes in the documentation
  - What every programmer should know about memory (Drepper)

  - Below here goes someplace...
  - limit the depth of undocumented preconditions as a way to introduce new
    function boundaries.
  - Discussion of
    - insitu vs functional
    - (functional) lazy vs eager
  - in concurrency chapter show how more complex algorithms may parallelize
    better and be more/less efficient

Tasks for Dave
- [] incorporate material from Embracing Algorithms, particularly big-O
