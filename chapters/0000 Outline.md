## Outline

### Introduction
This is a course/book on engineering

#### Definition of Engineering:

> The creative application of scientific principles to design or develop
> structures, machines, apparatus, or manufacturing processes, or works
> utilizing them singly or in combination; or to construct or operate the same
> with full cognizance of their design; or to forecast their behavior under
> specific operating conditions; all as respects an intended function, economics
> of operation and safety to life and property.

—American Engineers' Council for Professional Development, according to
https://en.wikipedia.org/wiki/Engineering.

But that's a bit wordy and vague. Boiling it down to its essence,
1. It's designing and building stuff
2. It's subject to real-world constraints, e.g.
    * Shipping dates
    * Available tooling
    * Hardware available for deployment
    * Laws of physics

And as engineers we have to juggle all of this and make a set of informed
tradeoffs to find the best solution.  Real-world constraints mean engineers will
always confront trade-offs, so much so that making these trade-offs could be
said to be the essence of the activity.

> Engineering is making informed tradeoffs to produce the best design or
> artifact possible given a set of constraints.

#### Instructor/Author Bias

We hope this course/book is generally applicable, but of course we come from a
set of experiences that will color what we think is important.  We've attempted
to be responsible for our biases.  In full disclosure, you can read our
backgrounds from the overleaf/here they are.

#### Truth

One thing we both believe is that in grappling with problems, if you apply
yourself, you can discover deep platonic truths.  This course/book is about
finding deep truths about programming.

#### Better Code

This is a course/book about producing better code.  To do that, we need to
understand what good code is, and to do it together we need to agree on that
definition.  Rather than try to list these properties up front, we're going to
discover the properties of good code as we go along, by looking at real
examples.

- we're trying to get to some some universal truths about about good
  programming.
- We believe these truths exist, but they are always manifest within some system
  of real-world constraints.
- It's important to distinguish situational compromises from universal truth.

DWA: Now we have a slide with a list of some properties of good code, which we
said we weren't going to do.  Which is it?

#### On Readabilty

Readability is often misunderstood as meaning “use of a primitive vocabulary.”
This is like saying, “instead of calling `sort()` in the code, use loops,
iterate the elements, and place each one in the right place.”  Problems:

1. Meaning is lost: reader must derive that the code sorts rather than plainly
   seeing it, i.e. it's less readable.
2. It's probably less efficient.
3. It's probably not correct.

Although it contributes to scalability, readability can't reasonably take
priority over most other properties of good code, such as correctness or
efficiency.  With sufficient time, readability and these other factors need not
be mutually exclusive.

#### Software is Physics

- Your code is (part of) a physical system
- It is constrained by the laws of physics
- The laws of physics are how we explain to ourself that the machine works
- We have to discover/document the laws of our code in order to explain that it
  works.

#### What to expect
##### Programming Language

The principles of this course are not specific to any one programming language,
Often we'll talk about some programming idea and then talk about the best way to
render that idea in a given language. The fit will not always be elegant; this
is an engineering reality (tradeoffs!)

##### Structure of the Course
- Goals [should be positive things, e.g. not “no _________”]
##### Conventions used throughout
###### Unscalable constructs
[This is what we were calling “raw.”  Unscalable is far from a perfect word.
“Raw” connotes “unencapsulated” or “exposed” but Sean was also trying to get at
a word for the property that causes us to *want* to encapsulate these things,
which are two separate ideas.  Unscalable is my approximation]

- There are easily-applied constructs that undermine local reasoning and thus
  quickly lead to chaos unless encapsulated.
- These will break your relationship to your code if not carefully managed.

- Synchronization primitives
- Loops
- Pointers
- incidental data structures
- incidental algorithms
- shared state

- House of cards makes a good metaphor.

##### Pointers to materials
##### Useful tools

### Algorithms

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
- Show a precondition (find a `double`; no NaNs).
- Show genericity
  - show lifting of EqualityComparable concept
  - show how genericity aids readability
- Show simple mutation
  - introduce aliasing and how it creates preconditions, giving us a platform
    for value semantics
  - aliasing is an unscalable construct
...
- Show how algorithms compose
  - Show some examples of how to decompose real things into other algorithms
    - Gather (case-wise)
    - Elementwise
      - Relate back to find, which is elementwise composition with itself
      - Rotate on forward iterators, a beautiful and more complicated example
    - Stable partition (top-down divide-and-conquer rotates)
    - Reverse (bottom-up)

### Types

### Material to be Reviewed / Added

Sections, thoughts, etc., that don't yet have an associated section in the
outline.

#### Computational and efficient bases

- Must be measured relative to an intended abstraction.  A type with just
  zero, increment, and is_odd is a computationally complete boolean but not a
  computationally complete integer.
- Raises the questions:
  - What *is* this thing you're building (to its clients)?
  - What are its observable parts?
  - What is its value?
- DWA: given that efficiency matters, is computational completeness, on its own,
  an interesting distinction?

#### Necessary ingredients for Scalable/Sustainable Software

If we can make this list long enough, it could be a theme threaded through the
book.

- Local reasoning
- Preconditions, postconditions, and invariants (techniques for local reasoning)

#### Safety

We define a function or method as safe if it cannot cause undefined behavior in
a single-threaded program. This is close to the traditional meaning of “type
safe and memory safe.”

[Undefined behavior may manifest at an arbitrary time in the future, so if an
operation X can cause later safe operations to manifest undefined behavior, X is
unsafe.  This reasoning allows us to classify `std::move` as unsafe in C++. See
below for more.]

A safe operation can have preconditions, but its response to preconditions being
violated must be defined or unspecified, not undefined.

- Note: unspecified outcomes are needed because
  - Completely specifying the possible results of a failed operation, such as a
    sort, often creates complexity and has no upside (thus the “basic guarantee”).
  - Sometimes even in the case of success, completely specifying the result might
    be the wrong thing, e.g. the tail of the original sequence after a
    `std::remove` should maybe not be specified.

##### C++ limitations on safety

Safety for C++ is complicated because common coding patterns, such as mutation,
depend on fundamentally unsafe constructs like pointers and references.
Therefore we define “C++-safety,” and a set of C++-safety rules that, if
followed, make the use of “C++-safe” operations, actually safe by the
definition above.

A C++-safe function or method may generally assume:

- A parameter passed by `const` reference, or `*this` in a `const` method, will
  not be mutated during the call, including by operations on the call's other
  parameters such as function objects. In other words, a `const` reference
  parameter can be treated as though it was passed by-value; passing by `const`
  reference is merely a way of optimizing away the copy.

- An object to be mutated will not be observed or mutated through multiple
  accessed paths.  For example, a function with the signature of `std::swap` can
  assume it is passed references to distinct objects, and a function with the
  signature of `std::iter_swap` can assume it is passed iterators to distinct
  objects.  A function that copies an element from offset `i` to offset `j` in
  an array can assume `i != j`.  This guarantee is analogous to Swift's “law of
  exclusivity.”

A safe operation is free to make additional guarantees, e.g. specifying
well-defined behavior if some of its reference arguments are aliased.

C++ has “implementation limits,” such as stack depth, which, when exceeded, can
cause undefined behavior. We have no special strategies for mitigating the risk
of exceeding these limits; C++-safety depends on staying within them.

- All built-in casts are unsafe for some combinations of arguments.
- An object upcast is safe.  A pointer or reference upcast is unsafe because,
  e.g., it allows the base part of an object to be subsequently modified or
  destroyed.
- `std::move` is unsafe because it allows an otherwise-safe operation like
  move-assignment to leave its argument in a condition that does not satisfy
  invariants. See [Move semantics and invariants](#move-semantics-and-invariants).

#### Move Semantics and Invariants

C++ has non-destructive move semantics.  That was a mistake, but that's how it
is. Unfortunately, there are some types (or some type invariants) for which no
safe + efficient non-destructive move operation exists—patching up an object
that's been emptied of its resources is not always easy/efficient, and weakening
invariants to accomodate the empty state is bad for reasoning about the rest of
the program.

One possible conclusion is that move operations (move assignment and move
construction) should be regarded as unsafe, because they may leave the object
with broken invariants. That would weaken the whole concept of class invariants,
which are supposed to hold unconditionally, after any public operation.
Invariants are powerful tools for creating simple abstractions precisely because
they *do not need to be stated as preconditions*, which would be necessary if
they could be left unsatisfied.

Instead, we can observe that move operations in code without `std::move` (or
some equivalent cast) are only applied to rvalues: the language prevents the
moved-from state from being observed except by the destructor that is about to
run, and once the object is destroyed, the temporary breakage of invariants is
irrelevant. Therefore, as long as the destructor is written to deal with
moved-from states, we can view the fused move+destroy as being safe.

That leaves only moves from lvalues, which occur only after calls to `std::move`
or equivalent casts. The language does *not* prevent a moved-from lvalue from
being passed to, and observed by, a function whose correctness depends on the
class invariants. As noted above, the invariant is not stated as a precondition,
so such a call must be regarded as “usage according to contract.”  Because the
behavior of such a call could be undefined, `std::move` must be regarded as an
unsafe operation (conveniently, just like any other cast).

Many use cases for moving from lvalues demand replacing unsafe, moved-from,
lvalues with safe values. In-place destruction + construction creates problems
for exception safety (the construction might throw, leaving a destroyed object),
so a single operation is required, and for better or worse, C++ chose to spell
this operation the same way as an ordinary assignment.  Thus, in addition to the
destructor, copy- and move-assignment operators must be written to deal with
moved-from states.  Every other public operation can depend on invariants being
satisfied, but not these three.


- A Big-O difference means “in practice it matters.”
