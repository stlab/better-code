
# Types

Types are a way of assigning meaning to raw bits.  Consider this type:

```swift
/// A point in the [Cartesian
/// plane](https://en.wikipedia.org/wiki/Cartesian_coordinate_system#Cartesian_plane).
struct Point2D {
  /// The first coordinate (abcissa).
  public var x: Float

  /// The second coordinate (ordinate).
  public var y: Float
}
```

`Point2D` represents more than just `(Float, Float)`—or even `(x:
Float, y: Float)`—does, because of the meaning implied by its
documentation.

## Value

Every instance has a notional **value**, expressed in terms of the
operations on its type. 64 bits can be used to represent an integer, a
finite set (by using each bit as a `Bool` denoting membership), a
short string (as UTF-8), etc., but in ``1 as UInt64` the bits
represent the mathematical integer value 1.  We know it's a
mathematical integer not only from the documentation, but also from
the available operations—such as addition—on the instance, and their
meanings.  Although `UInt64` *has* the operations necessary for
treating instances as finite sets, doing so requires assigning a layer
of additional meaning to operations such as division and modulus.

> **Note**: every instance of a type should have exactly one
> clearly-defined value. [^bitwise]

[^bitwise]: Arguably, `Int` and friends do not follow this rule
because bitwise operations directly offer an interpretation of the value
as a sequence of bits.  To clarify the value, these operations could
have been made available only on some type that can be constructed
from the `Int`. That, however, would break strong precedent from other
languages, which is arguably more important.

## Equality

The fact that instances have values implies they can be compared for
equality: at the risk of stating the obvious, two instances are equal
when the have the same value.

## Range

We call set of (non-negative) mathematical integers the **notional
range** of `Int64`.  At a high level, we program as though types can
represent all members of their notional range, but due to the
finiteness of memory and for performance reasons, a type's actual
**range**—the set of values it can represent—is often limited.

Types can take different approaches to this discrepancy.  Integer
arithmetic operations cause a fatal error when the result can't be
represented—representability is a precondition.  Floating point
operations give approximate results.  Approximation is very difficult
to specify and work with, so a representability precondition is almost
always the preferred approach.

The notional value of an `Int` is some
mathematical integer. You know that

The notional value of `x` `let x = 1` is the
mathematical integer value 1.  We know that's the case because
even though you can view
an `Int` as a

The value of a `Point2D`
instance is directly represented by the values of its stored `x` and
`y` properties.

### Fundamental Value Operations

Because instances have values, we can

### Graph

Let's examine a more interesting case:

```swift
/// A [directed simple
/// graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph).
struct DirectedGraph {
  /// A location that may be connected to other locations via a
  /// directed edge.
  public typealias Vertex = Int

  /// For each vertex u, the target vertices of edges originating at u.
  private var successors_: [Vertex: Set<Vertex>] = [:]

  /// The vertex that will be added by the next call to makeVertex().
  private var nextVertex: Vertex = 0

  /// Returns a new vertex.
  public mutating func makeVertex() -> Vertex {
    defer { nextVertex += 1 }
    successors_[nextVertex] = []
    return nextVertex
  }

  /// Adds an edge from `source` to `target`.
  public mutating func addEdge(from source: Vertex, to target: Vertex) {
    precondition(successors_.index(forKey: source) != nil)
    precondition(successors_.index(forKey: target) != nil)
    successors_[source]!.insert(target)
  }

  /// All the vertices.
  public var vertices: some Collection<Vertex> {
    successors_.keys
  }

  /// The vertices reachable from `v` in one step.
  public func successors(_ v: Vertex) -> some Collection<Vertex> {
    successors_[v]!
  }
}
```

The value of a `DirectedGraph` is captured in the identities of its
vertices and the edges between them.  While all that information is
present in its `successors_` property, it is not directly represented, which
is why `successors_` is private.

## Meaning => Operations

The meaning of a type implies a set of operations.  For example,

```swift
extension Point2D {
  /// Returns the length of the line segment between `self` and
  /// `other`.
  public func distance(to other: Point2D) -> Float {
    (x * other.x + y * other.y).squareRoot()
  }
}
```

## Basis Operations

The minimal set of operations required to implement all other
meaningful operations on a type is called its *complete basis*.  The
*complete basis* of `Point2D` is simply provided by read/write access
to its stored properties.  The minimal set of operations required to
implement all others *with maximal efficiency* on a type is called its
*efficient basis*.

- Array of pairs efficient basis


## Copy, Equality, Hash, etc.

And their relationships

- Copying
- Equality
- Hashing
- Comparison
- Assignment
- Serialization
- Differentiation

* Regular

## Problems With References

### Spooky action
### Incidental algorithms
### Visibly broken invariants
### Race conditions
### Surprise mutation
### Unspecifiable mutation

### Beware Mutable Captures

## The whole-part relationship

## Where ~Copyable Fits

## Representing Graphs

## Copy On Write, ManagedBuffer, et. al.


## Misc

- Value
  - Types can be viewed as sets of values
  - Point
  - Set
  - Notional value often not representable.
    - Bool is an outlier
    - Finite sets in general
    - Float
- Composite Types
  - Reachability of Parts (Equational Completeness) Set
- How to Compromise Notional Value (limits of finite representations)
- Non-salient properties: floating point -0, +0
- NaN, domain of operations (outside of value set - doesn't obey equality laws)
- Type invariants mention

----

- Sets shouldn't be collections
- non-salient properties
- points, vectors, pairs
- strong type information and engineering tradeoffs
- documenting types
- types and naming
- when to expose properties (computed or stored).
- subscripts

- law of exclusivity
- basis operations
  - completeness - implement equality
  - efficiency
