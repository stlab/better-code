A [[procedure]] parameterized by types and constant values, with requirements on these parameters. 

In C++, we use function templates and function object templates. The parameters follow the `template` keyword and are introduced by `typename` for types and `int` or another integral type for constant values.

Requirements are specified via the `requires` clause, whose argument is an expression built up from constant values, concrete types, formal parameters, applications of type attributes and type functions, [[equality]] on values and types, concepts, and logical connectives.

# Example

```cpp
template <typename Op>
	requires(BinaryOperation(Op))
Domain(Op) square(const Domain(Op)& x, Op op) 
{
	return op(x, x);
}
```