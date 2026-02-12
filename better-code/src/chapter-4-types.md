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

Every instance has a notional value.  The value of a `Point2D`
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

## Misc

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
