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
: - Can reason about main more easily; hint in name
  - Could think about reuse, establishing `find` as vocabulary function.
  - Now I have a question

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

## About the artist
{:.community-about-slide .evans}

## The End
{:.community-closer-slide .evans}
