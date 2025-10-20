# Algorithms

>_<center>No raw loops.</center>_

The most important part of software development is that the purpose of the code
is to compute _something_. Algorithms are an abstraction of computation, and
every program is an algorithm. It is easy to be distracted by class hierarchies,
software architecture, design patterns, etc. Such things are helpful only in so
far as they aid in implementing a correct and efficient algorithm.

**Algorithm** (n.): _a process or set of rules to be followed in calculations or
other problem-solving operations, especially by a computer_ (New Oxford American
Dictionary).

```swift
{{#include test.swift:2:5}}
```

```swift
func partitionPoint<T>(_ array: [T], _ predicate: (T) -> Bool) -> Int {
    var left = 0
    var right = array.count
    while left < right {
        let mid = (left + right) / 2
        if predicate(array[mid]) {
            left = mid + 1
        } else {
            right = mid
        }
    }
    return left
}

let array = [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10]
let index = partitionPoint(array, { $0 <= 5 }) // lower bound?
```

## Closed-Form Algorithms
## Sequential Algorithms
## Composition
## Algorithmic Forms
### In-Place
### Functional
#### Eager
#### Lazy
## Efficiency
