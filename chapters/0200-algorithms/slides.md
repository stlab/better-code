---
---

# Algorithms
{:.community-title-slide .evans}
## Or, what computers actually do<br/>Adobe Software Technology Lab  |  https://stlab.cc
{:.subtitle}

## Definition  |  Algorithm, *n*

> a process or set of rules to be followed in calculations or other
> problem-solving operations, especially by a computer.

—New Oxford American Dictionary

<br/><br/><br/>

Algorithm
: the most important computing abstraction
{:.fragment}

%speaker
: Every program is an algorithm

  It's easy to be distracted by class hierarchies, software architecture, and
  design patterns.

  Where's the computation? Computers compute. Algorithms are the “stuff” of
  computing. Do not overlook them.

  Let's take a look at an example.

## Example

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>

int main(int argc, char* argv[]) {
  if (argc < 2) { std::exit(1); }

  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }

  if (j != argc) { std::cout << j; }
}
```
{:data-mark='|6|8|9|10|11|14||8-12'}

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

## Factor out the raw loop

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>



int algorithm(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}

int main(int argc, char* argv[]) {
  if (argc < 2) { std::exit(1); }

  const int j = algorithm(argc, argv);

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
{:data-mark='/find/,/find(?=.*;)/'}

%speaker
: - Can reason about main more easily
  - Could establish `find` as vocabulary function, enabling reuse.
  - Now I have a question about find

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
  2. ADVANCE, Ask how they know their answer is right.

## Document every declaration

```cpp



/// Returns the least `j` such that
/// `j > 1 && j < argc && std::strcmp(argv[1], argv[j]) == 0`,
/// or `argc` if no such `j` exists.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```
{:data-mark='4-6'}

<div markdown=1>
🔑 Summary paragraph is a sentence *fragment*.

🔑 Document non-mutating functions in terms of **what they return**.
</div>
{:.fragment}

%speaker
: 1. What's good about this comment? Discuss.
  2. ADVANCE
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
/// Returns the least `j` such that
/// `j > 1 && j < argc && std::strcmp(argv[1], argv[j]) == 0`,
/// or `argc` if no such `j` exists.
///
/// Requires: `argv[j]` is a NTBS where `j >= 1 && j < argc`.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```

%speaker
: - Is that the only precondition?

## Documentation feedback loop

```cpp



/// Returns the first index `j` of `v` such that
/// `j > 1 && j < n && std::strcmp(v[1], v[j]) == 0`,
/// or `n` if no such `j` exists.
int find(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}
```

%speaker
: - What's wrong with this comment? Discuss
  - Advance
  - Ask people to answer

![warn](/submodule/adobe-reveal-theme/icon/warning.png){:height='100px' align='center'} Documentation reads like code
{:.fragment}

## About the artist
{:.community-about-slide .evans}

## The End
{:.community-closer-slide .evans}
