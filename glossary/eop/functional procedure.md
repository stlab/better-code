A [[regular procedure]] defined on [[regular type|regular types]], with one or more direct inputs and a single output that is returned as the result of the procedure. 

The regularity of functional procedures allows two techniques for passing inputs. When the size of the parameter is small or if the procedure needs a copy it can mutate, we pass it [[pass by value|by value]], making a local copy. Otherwise, we pass it by [[pass by constant reference|constant reference]]. A functional procedure can be implemented as a C++ function, function pointer, or function object. 

# Examples

This is a functional procedure:

```cpp
int plus_0(int a, int b)
{
	return a + b;
}
```

This is a semantically equivalent functional procedure:

```cpp
int plus_1(const int& a, const int& b)
{
	return a + b;
}
```

This is semantically equivalent but is not a functional procedure, because its inputs and outputs are passed indirectly:

```cpp
void plus_2(int* a, int* b, int* c)
{
	*c = *a + *b;
}
```

In `plus_2`, `a` and `b` are input objects, while `c` is an output object. The notion of a functional procedure is a syntactic rather than semantic property: In our terminology, `plus_2` is [[regular procedure|regular]] but not [[functional procedure|functional]].

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.6