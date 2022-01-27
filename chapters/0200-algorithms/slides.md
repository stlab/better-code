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

%speaker
: Every program is an algorithm

  We often don't talk that way.  Instead we talk about:
  - class hierarchies
  - software architecture
  - design patterns

  Algorithms are the “stuff” of computing.

## Example

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>

int main(int argc, char* argv[]) {
  if (argc < 2)
    std::exit(1);
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  if (j != argc)
    std::cout << j;
}
```
{:data-mark='|6|7|8|9|10|11|13|14||6-7|8-12|13-14||8-12'}

%speaker
: - Walkthrough. On loop, “let's see if we can figure this out”
  - In summary, 3 parts:
    - input validation
    - search
    - output

  - One of these parts requires some thinking.

## Naming the raw loop

```cpp
// indexof.cpp
#include <cstdlib>
#include <iostream>

int find_2nd_in_remainder(int argc, char* argv[]) {
  int j = 1;
  while (++j < argc) {
    if (std::strcmp(argv[1], argv[j]) == 0)
      break;
  }
  return j;
}

int main(int argc, char* argv[]) {
  if (argc < 2)
    std::exit(1);

  const int j = find_2nd_in_remainder(argc, argv);

  if (j != argc)
    std::cout << j;
}
```
{:data-mark='6-10|15-16|18|20-21'}

## About the artist
{:.community-about-slide .evans}

## The End
{:.community-closer-slide .evans}
