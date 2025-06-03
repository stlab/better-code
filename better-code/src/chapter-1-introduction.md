# Introduction

This book is the product of our shared belief that programs and
programming can be better.  Over the years we've seen philosophies
about how to do software engineering come and go; we've listened to
the experts and applied their tips (sometimes to our detriment!)
Looking back, though, the key ideas underlying our best work weren't
the popular ones, and aren't widely known or taught today.  We wrote
this book because we think they could make a difference for
you, too.

The book's title comes from Sean's *Better Code* series of talks.  The
first of these, subtitled “Three Goals for Better Code” was given over
a decade ago, after Herb Sutter suggested Sean lay out practical
tips a developer could apply immediately to improve their code.  So
this is above all a practical book.  The authors each have more than
40 years' experience writing code that powers real applications in all
sorts of contexts; the ideas you'll encounter here are the ones that
stood the test of time and delivered results at scale.  We think
you'll also discover, as we have, that the most impactful practical
advice is also deeply principled and satisfying—both aesthetically
and, in some sense, scientifically.

Better code has more of three ingredients: **correctness, efficiency,
and abstraction**. Most people have a good intuitive sense of what
correctness and efficiency are, though we will try to deepen and
solidify all three ideas throughout the book. Abstraction is less
commonly understood, so, briefly, it's the quality of code that is
more reusable—and paradoxically, more understandable—because
inessential detail has been “lifted” out. It's what many people would
call “higher-level code.”

Code usually doesn't get better all at once.  Often we make
incremental improvement along one of the three axes as we discover the
nature of the problem we're solving.

We've tried to structure the book so chapters build on one another,
but they are interdependent.  A later chapter may deepen an earlier
one, so we encourage you to circle back and re-read earlier material.
Each chapter begins with a rubric such as “no raw loops.”  The rubrics
are often phrased in the negative, to call out red flags, and are
intended to be aspirational touchstones, not hard rules.  That said,
we've found they are most powerful when we violate them only as an
absolute last resort, and we suggest you do the same.

Although the ideas you'll find here are applicable to any programming
language, we've chosen to write our examples in Swift, for its direct,
safe support of mutable value semantics (see chapter XX), and generic
programming (see chapter XX), and because we are able to express them
without language-specific wrinkles that would need to be explained,
lengthening the text and distracting from the real issues.  If you
don't already know Swift, we've provided a brief introduction in
appendix YY.

Out of pursuing better code, you should find you have greater
confidence in your work and that you produce quality results more
quickly, with less code.  Programs become easier to maintain, and—when
a bug inevitably occurs—to debug.  At a metaphysical level, Better
Code is a journey of discovery.  For us it has been an exhilarating
one.  Wherever you are on that road, we hope you have the same
experience, and that this book serves as a guide and an ongoing
companion.
