# Key Takeaways

- Consider an (additional) example more relatable to product developers
- Consider keeping "Evaluation" on screen throughout example to build up guidelines
- Need to address Efficiency

# Raw Notes

David: re: Compilers use local reasoning
    illustrate with some code

Michael: when discussing pre/post conditons, often see it in search-esque examples
    providing an example of a more real-world, commonly-seen example day to day would be helpful
    How can we apply this sort of reasoning to the code you write daily
    Dave: Not sure what that would look like - suggestions?
    Sean: Part of class invariants
    Dave: No plan to discuss class invariants in this section

    Foster: Worth being explicit about class invariants - most of the functions I write are inside classes
        which clearly contain invariants
    Dave: Invariants matter inside the function, not at the api boundaries. 
        They're not part of the contracts of the functions, they're part of the implementation we abstract away. 
    
Sean: Documenting a member function would make it more relatable
Dave: Trying not to introduce type construction, which includes class invariants, but contracts may get too large.

Foster: Just saying put a pin in "invariants" - we'll get deeper into that with classes and class member functions. 
    With this class of function, they behave like this, when we talk about class invariants, we'll go deeper.

Laura: Scoping sequence is hard. 
    Wondering if each chapter is going to be two lectures, some might make sense distributed across the series - we could interleave, contracts pt 2 later.

Sean: Everything in this course is circular

Bob: +1 to the "pin in it" point from Foster. We don't need to do everything all at once, we can get back to it later.

Bob: Local Reasoning
    Semi-transparent image on first slide did not return. Thank you.
    I struggle with slides that look like they've been designed by designers. 
    I have met people who can keep a whole program in their heads, they lack empathy, they're bad programmers.
    Glad to hear Local Reasoning will return, good topic.
    Sad to hear about big wins from inlining; that's a big topic, don't want people to think it's a silver bullet
    No Raw Loops - that's a big deal, and should be said as such. Not commonly discussed in the programming community, that deserves more attention when its first introduced. Most people don't see Sean Parent talks.
        Dave: But in this chapter, I'm not really making that point in this chapter. 
    Did not mention testing the search function at all, which is worth discussing
        On preconditions, testing is also required for any software at scale. 
    Are we expecting interactive participation?
        Dave: Yes, but I don't do that well on remote presentations. 
        Bob: Tricky to do remotely, perhaps prompt for a type into the chat box
    
    First spec does not completely describe the function
        Dave: Really?
        Bob: What about when argc is 0?
        Dave: That's covered
        Bob: Will argc return 0?
        Dave: You've found a bug

    Almost nobody has heard of Betrand Meyer

    Complex documentation means you might not have a good API

    The code you write is not what most programmers write - pleased you acknowledged it. 
        Other speakers don't acknowledge this; we do not live in a world of high quality code. 
        Dave: we're asking people to navigate into unfamiliar territory - we should clarify that in lecture 0.

    Foster: re: report card for the state of the program.
        let's keep that report card around for the rest of the presentation
        watch the red x's turn into green checks, and then say these are your guidelines. 
        Dave: There's more guidelines I'd like to add that can't fit into a single example
        Foster: Loved having a summary of your evaluation of code kept on screen.
        
Michael: The example you used to build up the toolkit is good, but perhaps as a follow-on, here's an example for how we'd describe the contract for a mutating member function on a class, and get progressively more complex. 

    Foster: We could get a function out of a function from real life (Photoshop), and have a dynamic interaction in class. 

Laura:
    The variable names were a little confusing
        Dave: We get there - choosing the name becomes part of the contract description

    In the loop section, I would like to hear about what makes the loop hard to reason about. Be more explicit?
        Might be worth repeating the point - get it to sink in.
        David: Maybe pull "no raw loops" from this section
    
    Interested in seeing more up-and-down helpfulness of the documentation strings. 
        What's the minimum contract we could do? What's the most verbose we can be? Find the sweet spot.
    
    Want to see more about error handling about pre/post conditions
        I absolutely would do this in my day-to-day, how can I apply it?

    Look at code and apply preconditions if it didn't already have them;    
        is there some way to talk about how to apply local reasoning in a codebase with globals?
        what are some tools we can use to turn it into something we can reason locally about?
            Bob: There's entire books on the subject

            Sean: hoping people take away the ability to create islands of purity in your codebase. 
                I write code in a scratch project, no dependencies, test it out. 
                Then I factor it into a bunch of files, and connect it to Photoshop 
                Laura: perhaps this is the common tool
                Sean: might be worth putting into the introduction
    
    Is a contract a specification?
        Dave: Design by contract is what I was trying to impart on software at scale, not just preconditions.
        Bob: Might be a mistake of my note-taking.
        Dave: A contract is a specification. It's a way to approach writing specifications based on the relationship in a legal contract between people.
        Laura: It's not the API itself, it's what people decided the API should to. 
        Dave: Depends.
        Laura: It's not just the function signature
        Dave: Right

    How does looking up documentation relate to local reasoning?
        Is it still local if you're looking up docs?
        Dave: Good question - yes, because you don't end up diving into the implementation of the documented code. The boundary stops there.
        Bob: By looking up documentation, do you mean going to the declaration of the function with a helpful comment / doxygen.
            "Looking up" can be varying degrees removed from the actual sources.
        David: This is called "local neighborhood" - you can look at the documentation of all the functions you call, but not the functions they call - that's the boundary of your neighborhood.
        Laura: So you need to know "valid C-string"
        Dave: Note in written documentation I say null-terminated byte string, never wrote "c-string"
    
    Loved:
        Connective tissue was a good metaphor, please call back to it
        Video of how it actually worked - made it blindingly obvious
        Correctness of undocumented code is impossible to determine
        Slide animation to Bertrand was excellent, and then going back, super useful.

        Talked about when the STL came out, and what a difference that made,
            I do not know what that really implies.
            Dave: explains STL
            Laura: Maybe explain what STL was
            Dave: Maybe cut the line
            Laura: But it's a good story!

            Dave: Need to say something about efficiency in the contracts chapter

            Bob: Complex documentation is a bad API, STL shows the opposite.
