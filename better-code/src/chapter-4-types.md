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

Every instance of a type has a notional value.  The value of a
`Point2D` is directly represented by the values of its stored
properties, so let's examine a more interesting case:

```swift
/// A [directed simple
/// graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph).
struct DirectedGraph {
  /// A identity of a vertex.
  public typealias Vertex = Int

  /// For each vertex u, the target vertices of edges originating at u.
  private var spine: [Vertex: Set<Vertex>] = [:]

  /// The vertex that will be added by the next call to makeVertex().
  private var nextVertex: Vertex = 0

  /// Returns a new vertex.
  public mutating func makeVertex() -> Vertex {
    defer { nextVertex += 1 }
    spine[nextVertex] = []
    return nextVertex
  }

  /// Adds an edge from `source` to `target`.
  public mutating func addEdge(from source: Vertex, to target: Vertex) {
    precondition(spine.index(forKey: source) != nil)
    precondition(spine.index(forKey: target) != nil)
    spine[source]!.insert(target)
  }

  /// All the vertices.
  public var vertices: some Collection<Vertex> {
    spine.keys
  }

  /// The vertices reachable from `v` in one step.
  public func successors(_ v: Vertex) -> some Collection<Vertex> {
    spine[v]!
  }
}
```

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
