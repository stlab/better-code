## Terminology

- **Safety** in engineering is the prevention of harm through system design.

- An **operation** is any executable program or program fragment, from an integer addition to a whole application.


- A **[safety property](https://en.wikipedia.org/wiki/Safety_and_liveness_properties)** is the *impossibility* of some occurrence *when an operation is used correctly*.  For example, this function upholds the safety property that nothing is printed to the console:

  ```swift
  /// Returns `x`.
  ///
  /// - Precondition: `x >= 0`
  func identity(_ x: Int) -> Int {
    if x < 0 { print("Precondition violated!") }
    return x
  }
  ```
To be a safety property, it must *compose*.  That is, when any two operations *P* and *Q* uphold the property, so does *P* followed by *Q*. For example, freedom from data races is a safety property, but freedom from logical races is not, because when two consecutive non-racy mutations are composed into a larger mutation, another thread can observe the partially mutated state between the two steps.

- A **[liveness property](https://en.wikipedia.org/wiki/Safety_and_liveness_properties)** is the *guarantee* of some occurrence when an operation is used correctly.  For example, this function upholds the liveness property that it eventually returns:

  ```swift
  /// Returns `x`.
  ///
  /// - Precondition: `x >= 0`
  func identity2(_ x: Int) -> Int {
    while x < 0 { /* loop forever */ }
    return x
  }
  ```

- An ***X* safe operation** upholds some safety property *X* **even if preconditions are violated**. [^qualification]  For example, when `a` is an array, `a[0] = 3` never modifies a variable not mentioned in the expression, even if `a` is empty (which violates the precondition of `a[0]`).  We might say that the operation is “expression-mutation safe.” 

[^qualification]: note this important distinction—an operation can uphold the memory safety property but not be memory-safe by this definition, because the former depends on preconditions being satisfied but the latter does not.

- An ***X* safe language** is one where all primitive operations are *X safe*.  It follows that all non-primitive operations—and all possible programs in the language—are *X safe*. A language subset, such as “Swift programs in which no identifier contains the substring `Unsafe` or `unsafe`,” can be considered a language.

- **Memory safety**: the property that invalid memory operations such as out-of-bounds accesses and use-after-free do not occur.

- **Type safety**: the property that an instance of one type is never accessed as an instance of another type.

- **Thread safety**: the property that a data race does not occur. Sometimes “thread safe” is used to mean that, additionally, deadlock does not occur. Freedom from deadlock can also be viewed as part of a liveness property guaranteeing forward progress. 

- **Data race safety**: the property that a data race does not occur (explicitly excluding freedom from deadlock as a constraint).

- **Undefined behavior** is not bounded by any constraints and thus nullifies every safety property.  An operation that can have undefined behavior, or a language that includes such an operation, is never *X* safe for any *X*.  

  Violations of memory safety, type safety, and data race safety have effects that can't be usefully described in terms of any portable programming language. For example, the effects of an out-of-bounds write can be understood when memory is viewed as a linear collection of bytes, but can't be described in terms of distinct variables and constants of many types, because portable languages do not specify the layout relationships among distinct stored values.  Therefore, in unsafe programming languages, these violations typically cause undefined behavior.[^java-data-race]

- A **safe operation** will never exhibit undefined behavior, even if preconditions are violated. Safety is often a consequence of type checking (you can't access `x.5` when `x` is a 2-element tuple), but sometimes runtime checks are needed, as when indexing a variable-length array. “Trapping” or otherwise stopping the program when preconditions are violated is one way to achieve safety.

- A **safe language** (such as Java or Haskell) has only safe operations, so all possible programs in the language are safe.  The distinction is important because proving a safety property of arbitrary code is tedious and sometimes very difficult, unless—as with a safe language—all code is safe by construction.

- In practice, “**memory-safe language**” is synonymous with “safe language.” Since undefined behavior invalidates all guarantees (including memory safety), a memory-safe language can have no undefined behavior and is therefore a safe language.  Because the behavior of a memory safety violation can't be defined at the language level (see the discussion after the definition of *undefined behavior*), any safe language must be memory safe.

- A **safe-by-default language** (such as Swift or Rust) contains a minority of unsafe operations that can be easily recognized by tooling and banned or flagged for extra scrutiny in code review. This arrangement provides unconditional safety in most code while allowing the direct use of primitive operations such as pointer dereferencing, without expensive validity checks.  When unsafe operations are used correctly in the implementation details of safe abstractions, the vocabulary of safe operations grows, with little compromise to overall security.  Safe-by-default languages are often casually referred to as “memory safe” despite the availability of operations that can compromise memory safety.

- The **safe subset of a safe-by-default language** is a safe language.

[^java-data-race]: Some languages, such as Java and JavaScript, define the behavior of data races, but in such a way as to be useless for most programming.


----

In Lamport’s framework, safety is defined semantically—as a prefix‑closed set of behaviors—but this definition alone does not guarantee compositionality under functional composition. As Abadi and Lamport show in Composing Specifications, and as later clarified by Abadi and Plotkin’s work on refinement‑preserving transformations, safety properties become compositional only when the functions involved are themselves safety‑preserving. In other words, from the fact that a safety property p holds for f(x) and for g(x), nothing follows about p(f(g(x))) unless f and g each preserve p. This distinction—emphasized in surveys such as Freiling and Santen’s work on compositional reasoning—makes clear that prefix‑closure characterizes the semantic nature of safety, while congruence under composition requires an additional structural assumption about the operators acting on behaviors.

preserving.dvi
https://lamport.org/pubs/abadi-preserving.pdf
lamport.org


99583.99626
https://dlnext.acm.org/doi/pdf/10.1145/99583.99626
dlnext.acm.org


On the Composition of Compositional Reasoning | Springer Nature Link
https://link.springer.com/chapter/10.1007/11786160_8
link.springer.com

https://lamport.azurewebsites.net/pubs/abadi-composing.pdf
