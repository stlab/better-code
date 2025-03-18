An object is valid if it meaningfully represents an concrete or abstract entity or relationship. An object which is not valid (invalid) is required to be destructible, and if assignable, it is required to be assignable-to. No other operations are required. Examples of objects in an invalid state:

- A pointer to a deleted object is invalid.
- An unitialized integer is invalid.
- Many inserting an element into a container will invalidate any iterators into the container if there is not sufficient capactiy.