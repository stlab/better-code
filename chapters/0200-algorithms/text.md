---
---

## Algorithms

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
