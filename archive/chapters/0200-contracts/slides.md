---
---

# Abstraction and Contracts
{:.community-title-slide .evans}
## Adobe Software Technology Lab  |  https://stlab.cc
{:.subtitle}

## A program

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>

int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cerr << "missing argument/n";
    std::exit(1);
  }
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  if (j != argc) {
    std::cout << j - 2;
  }
}
```
{:data-mark='|6-9|10|11-14|15-17||6-9|10-14|15-17'}

```
$ indexof
missing argument
$ indexof C   A B C D
2
$ indexof X   A B C D
$
```
{:.fragment}

Can we make it better?

%speaker
: Walkthrough

  First, error if there's less than 1 arg

  At `while`, “let's see if we can figure this out”

  In summary, 3 parts:
  - input validation
  - search
  - output

  One of these parts required some thinking.
    What can we do to make this code better?

## A program
{:.images-with-headers}

`indexof.cpp`
: ```cpp
  // indexof.cpp
  #include <cstdlib>
  #include <iostream>

  int main(int argc, char* argv[]) {
    if (argc < 2) {
      std::cerr << "missing argument/n";
      std::exit(1);
    }
    int j = 1;
    while (++j < argc) {
      if (std::strcmp(argv[1], argv[j]) == 0)
        break;
    }
    if (j != argc) {
      std::cout << j - 2;
    }
  }
  ```
  {:data-mark='|6-9|10|11-14|15-17||6-9|10-14|15-17'}


  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
  incididunt ut labore et dolore magna aliqua.

Console
: ```
  $ indexof
  missing argument
  $ indexof C   A B C D
  2
  $ indexof X   A B C D
  $
  ```

  Dolor sed viverra ipsum nunc aliquet bibendum. Tortor at risus viverra adipiscing at in.


## Factor out the raw loop

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>

int search(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}

int main(int argc, char* argv[]) {
  if (argc < 2) { std::exit(1); }

  const int j = search(argc, argv);

  if (j != argc) { std::cout << j; }
}
```
{:data-mark='8-12|/algorithm/,/algorithm(?=.*;)/'}

%speaker
: We can put the part that's hard to reason about into a separate function.

  OK, “algorithm” is a ridiculous name for an algorithm.
  Just like “string” is a ridiculous name for a string.

## Give it a name

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>



int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}

int main(int argc, char* argv[]) {
  if (argc < 2) { std::exit(1); }

  const int j = find(argc, argv);

  if (j != argc) { std::cout << j; }
}
```
{:data-mark='/find/,/find(?=.*;)/|7-14'}

%speaker
: - Can reason about main more easily
  - Could establish `find` as vocabulary function, enabling reuse.
  - Now I have a question about `find`, so let's look at it on its own.

## Is it correct?

```cpp






int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```

How can you tell?
{:.fragment}

%speaker
: 1. Get a show of hands for incorrect and correct.
  2. ⮕ Ask how they know their answer is right.

## Document every declaration

```cpp



/// Returns the least `j` such that j > 1 && j < argc
/// && std::strcmp(argv[1], argv[j]) == 0`, or `argc` if no such `j` exists.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```
{:data-mark='4-4'}

<div markdown=1>
✅ Summary paragraph is a sentence *fragment*.

✅ Document non-mutating functions in terms of **what they return**.
</div>
{:.fragment}

%speaker
: 1. It's far from perfect, but what's good about this comment? Discuss.
     - it's short
  2. ⮕
     - A sentence fragment is usually sufficient for usability
       - if not, be uncomfortable.
       - incentivizes commenting.
  3. What's missing here or implicit?

## Definition  |  Precondition, *n*

> a condition or predicate that must always be true just prior to the execution
> of some section of code or before an operation in a formal specification.

—Wikipedia ([wikipedia.org/wiki/Precondition](https://en.wikipedia.org/wiki/Precondition))


## An explicit precondition

```cpp
/// Returns the least `j` such that `j > 1 && j < argc
/// && std::strcmp(argv[1], argv[j]) == 0`, or `argc` if no such `j` exists.
///
/// - Requires: `argv[j]` is a C string where `j >= 1 && j < argc`.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```
{:data-mark='4|/j >= 1/|1-2'}

%speaker
: - This precondition is actually implied by the documented semantics
  - ⮕ The precondition is minimal. What do we think about that?
    **Discuss**. Before we can address that…
  - ⮕ What do we think of this documentation? **Discuss**
  - There's a problem. ⮕
  - Why is that a problem?
    - Not much to verify against.
    - Hard to use.
    - Meaning, abstraction, and semantics are missing
    - Let's make the API more meaningful

Sean notes Hoare logic is bottom-up and propagates complexity.  DBC is top-down
and minimizes it.

- Works as coded

![warn](/submodule/adobe-reveal-theme/icon/warning.png){:height='100px'
align='center'} Red flag: documentation reads like implementation.
{:.fragment}

## Meaningful APIs  |  Step 1

```cpp
/// Returns the first index of `argv`'s 2nd element in the remainder of `argv`,
/// or `argc` if it can't be found.
///
/// - Requires: `argv[j]` is a C string where `j >= 1 && j < argc`.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```
{:data-mark='1-2|4'}

%speaker
: - Is that better?  We dropped a couple of things.
  - ⮕
  - “The position of `argv[1]`” by itself means find the same pointer value.
  - ⮕ We can cover most of this missing information *and* the precondition.
^
Dropped information:
: `argv` is interpreted as an array of C-strings.
: `argv` has length `argc`.
: “the remainder” is prone to misinterpretation.
{:.fragment data-fragment-index='1'}

## Meaningful APIs  |  Step 1

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
{:data-mark='4|1-2'}

%speaker
: Is this precondition better than before?

  ⮕ In raising abstraction of the precondition, we also tightened it

  ⮕ Now we can use the summary to think about

<div markdown=1>
👉🏿 Precondition is tightened
- `argv[0]` is now a C-string
- `argc` > 1
</div>
{:.fragment}

## Meaningful APIs  |  Documentation feedback

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
{:data-mark='4'}

## About the artist
{:.community-about-slide .evans}

## The End
{:.community-closer-slide .evans}
