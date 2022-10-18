Describes a [[Type]] which matches the built-in type semantics for a particular language (conventionally, C++). 

While built-in types in C++ vary substantially in the number and semantics of built-in operators rhey support, there is a core set of built-in operators which are defined for all built-in types:

| Operation | Syntax |
|---------------------|----------|
| Default Constructor | `T a;`     |
| Copy Constructor    | `T a = b;` |
| Destructor          | `~T(a);`   |
| Assignment          | `a = b;`   |
| Equality            | `a == b;`  |
| Inequality          | `a != b;`  |
| Ordering            | `a < b;`   |

# Resources
Alex Stepanov: [Fundamentals of Generic Programming](http://stepanovpapers.com/DeSt98.pdf)

