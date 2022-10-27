# STLab Glossary 

**The contents of this directory should be considered alpha-quality**. 

The glossary is currently compatible with [Obsidian](https://obsidian.md/), but this support is not guaranteed in the future. Cross-file references may be made with double-brackets, like: `[[Term]]`.

Each file in this directory, (except this README) shall define a single term relevant to rigorously-specified programs. 

# Style Guide
1. Do not create links to a page within that page. It provides no additional benefit.
2. Page titles should always be capitalized. 
3. References to terms should always be capitalized, even if they would not be in natural English. For example:
	1. The set of [Operations](Operation.md) at a particular [[Abstraction Layer]] which are irreducible.
4. Prefer wiki-style `[[]]` links. Use markdown-style links `[]()` when the construction of a sentence requires a different part of speech. For example:
	1. `A strategy for handling an [[Error]] in which the program reports and [Terminates](Termination.md).`
5. For each term, please provide a `# Resources` section pointing to materials that either explain or use the term in an exemplary manner. 