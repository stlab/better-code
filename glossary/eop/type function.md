A mapping from a type to an affiliated type. 

A type function may be _indexed_ with an additional constant integer parameter. For example, a type function returning the type of the ith member of a structure type (counting from 0).

See also: [[type attribute]].

# Examples

- Given a "pointer to `T`", the type `T`.
- If `F` is a [[functional procedure]] type, the type function `Codomain(F)` returns the type of the result.
- If `F` is a functional procedure type and `i < Arity(F)`, the indexed type function `InputType(F, i)` returns the type of the ith parameter (counting from 0)

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.7