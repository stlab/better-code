# Key Takeaways

- Emphasize the relevance to day-to-day programmers 
    maybe by saying "this is relevant whenever you write a loop"
- Avoid colorful comments / observations that are not going to be thoroughly addressed in the talk.
- If you're going to ask a question to the group, please put the question on the slide.
- Need to add a reference section
- Need to introduce the term "semantics"
- Dwell on key points, like
    "iterators point between the elements"
- Use Dave's algorithms lecture - improvements on stable partition animations
- Avoid "require" and "ensure" in favor of "precondition" and "postcondition"

# Attendees
Bob Archer
Foster Brereton
Laura Savino

Dave Abrahams
Nick DeMarco (Notetaker)
Sean Parent
David Sankel

# Raw Notes

## During

loops slide, remove implies, replace with comma
if n is negative we don't decrease (n - i); does that matter?
have a refresher on "efficiency" before discussing it here

## After

Michael:
    The stable_sort example can get people excited about power through layering algorithms.
    People will feel their lack of knowledge of these algorithms - perhaps present 5 core building blocks to algos like this.
        Or, do in the homework - highlight some of the more useful core algorithms.
    Sean: Should introduce taxonomy of the standard library

Laura:
    What percentage of engineering time at Adobe, or worldwide, is spent writing things that operate on large data sets?
        How much is wrestling with frameworks, trying to get login to work, fighting yaml, etc. 
        There's a kernel here of taking these steps and recognizing patterns in a group of steps
            what to pull out, when it's worth your time to invest in making something more performant
            I could tell other people were nerd sniped by stable_partition, but I was not.
            Not sure how many engineers will care about this - how does it help me light up my feature better?
    Sean: These slides came from c++ seasoning; slide and gather comes from a google code review (chromeos window drag)
        Not sure if we want to add that full context
    David: Confirming what Laura is saying - I know very good engineers that don't care about "ivory tower" BS. 
        Thier day-to-day doesn't look like this at all. It would be good to pre-empt this response.
    Foster: In PS, I call `gather` in the paths panel, to let you take a disjoint selection of paths.
    Laura: Not saying this isn't real, but this kind of work is real but rare. 
    Sean: The point we're trying to make is: if you're never writing loops at all, in your code, then yes.
        But there's a lot of code with a lot of loops. 
    Laura: Say that!
    Dave: If your work doesn't look like this, it might be because the algorithms are hiding in the object networks you're building; they're incidental algorithms. Go look for them - sometimes they're in a loop, sometimes they're in a class hierarchy. 
    Laura: I want to see more emphasis on performance, tuning existing code by recognizing algorithmic composition
    Sean: Performance is actually secondary here, naming and vocabulary building is crucial - that's the main point
        I was taught that you should make a function when you go to copy/paste the code
        But that's terrible - you want to make something a function even if it's only ever called once
        Dave: Which gives you local reasoning!

Bob:
    No raw loops, raw is perfectly decent, but in past two talks it's been mentioned twice without defining it. 
        NRL is not a common concept, and it deserves more emphasis and clarification
    I'm not sure that you're explaining things well enough to other people - you're very smart and are struggling to communicate clearly to people that are less familiar with the material.
        I found the discussion with Laura (tree structure of views devolving into bad performance) more compelling than the talk itself
    Talked about semantically weak/void, and that's a level of intellectual language that many people may not be familiar with.
    The preconditions/postconditions/invariants slide is more technical than most people are used to.
    Some property of the loop decreases on each iteration - "never thought of it like that before"
        ** I need to work this out, but I didn't have time to digest it properly **
    Bertrand Russel: it takes 70 pages to explain that 1 + 1 = 2
        There are bits of this that feel a little like that, I'm worried about this being too formal, low level
    Sean: For folks with CS degrees, did you have to take a formal methods class?
        Proving algorithms, formally proving code. 
        All: lots of no, very few details 
    Nick: Education is producing engineers focused on writing glue code - because that's what industry demands.

    Bob: I just wanted a damn loop, and you've insisted on putting these other things on it. 
        More about conveyance than anything else. 

    Was there a reason for choosing a while loop over a for loop?
        Dave: Wanted to keep the value of i after it was over
    
    Capture loops in functions, that's what makes it non-raw

    Comment on developing things outside-in. I found it interesting, pre/postconditions -> implementation
        Struck me like test driven development. 
    
    You changed N to a size_t - I'm prepared to do battle with you.
        Sean: I'm also prepared to do battle with you.
    
    "The name of a function comes from naming the postconditions" - Quote of the week.
        Foster: a corollary of that is, "why do you wrap loops in functions" - the postcs of the loop are the name of the function. 
        Laura: and that's a callback to local reasoning - you can just look at one thing which is the name of the function you called.
        Bob: That's relevant to glue-code programmers.

    Naming & Complexity, liked that it was presented as a proposal.

    Iterators being between the elements, a throwaway comment that was very interesting. 

    Scan & Reduction as base algorithms, but then gave no examples of scan and reduction. 
        Sean: That's coming in a later draft

    I didn't understand the explanation of the stable partition of a single element. 
        Sean: Explains inductive base of stable_partition

    I'm concerned about your tendency to toss in distracting, but related ideas. Don't mention it if you're not ready to explain it.
        Laura: Use what you include!
    
Laura:

    I finally understood raw - when you see it in the code, it tells you very little about the code. 
    What's for dinner? "It's carbon" - huh? Example to clarify the importance of explaining things at the right abstraction level. 

    Here's what I think invariants are: I think an invariant is something you can "ignore" - it's static
        Dave: Exactly right - you're looking at a dynamic system and identifying static properties that you can assume are true.
        Laura: Please say that in plain english
    
    You're saying, naming is really helpful, but then you've got a lot of conditions that are just expressions,
        they mean things - (describing the postconditions) please put a comment on each of these lines
            "this means not found", this means "it was found". I want those comments so I can reason about what symbols you're putting on screen
        That's your point, and you're undermining it with how you express the preconditions/postconditions/invariants.
    
    If you're going to ask a question to the group, please put the question on the slide.

    Phrase, "what if n is negative" as "what are the edge cases", "what are things that make this break"?
        I could have answered that question, but I couldn't answer "have you captured all of the preconditions"

Dave: 

    I believe motivating loop analysis should start with the binary search example, then ask those questions.
        And then go to the simpler example of "find".
        Maybe show binary search inside of the context of its declaration. 
    
    I dislike the flow starting with deriving the preconditions/postconditions with the loop in isolation, without the function signature or any understanding of the intent. 
        IRL, there's context, and this example lacks context.
        I've seen it twice, and I still had a hard time absorbing the logic - I get the point is that it's complicated, but that's too complicated. 
        We need to put it in context and start there.
        Sean: The difference is between Hoare Logic (inside out) and Design by Contract (which is outside in)
            I want to make it clear that it's easier to specify something and then implement it to meet the spec
                than it is to look at an arbitrary piece of code and derive what some code is supposed to be doing
            Dave: I think I'll have made that point already in the contracts section. 
                I'm not sure that making the point from the ground up is all that useful.
            David: You're comparing two different approaches for writing code, but nobody's doing them in practice.
                So the distinction is lost on them. 
    
    Need to add a point: we're not talking about all algorithms
        there are graph algorithms, machine algorithms, ML algorithms, load balancing, etc.
        We're talking about sequences. 

    This is the place where you want to say that thinking about dynamic systems is hard
        We write loop invariants to make static statements about dynamic systems.
        But you said "we want to write an invariant for everything that changes in the loop"
        What you want to do is "describe the static property that the changes preserve"

    On naming: I agree with reflecting the performance in the name
        "greater" is not a noun, we should clean that up a bit
    
    Please don't write "require" and "ensure" - use "precondition" and "postcondition" - we're giving too many words for the same idea. 
        It's worth adding to contracts that precondition = require, post = ensure. But should avoid using habitually.

    In a past run through, you said, "because we've put it in a function, we don't need to state the postconditions of the loop"
        Don't say that - not every algorithm with a loop in it ends with the loop. Some things have effects after the loop.
    
    Think about everything you say as if you're talking to a novice. Don't say something unless you're prepared to explain it. 
        Sean: This is where I need the most help. I had a unique education, then spent a good chunk of my career with stepanov, so struggle with what to expect of other's knowledge.
        Dave: That's a skill we can learn
    
    Slide numbers!

    On the silverstein slide, remember to phrase the incorrect position clearly as belonging to silverstein

    sort() transforms find() - no, sort transforms "finding"
    
    I improved on the stable partition diagram by coloring the elements, there's other improvements that can make this a stronger talk. (from WWDC talk)
    
    Foster: Are there "calls to action" for more resources and related content? Including WWDC

David:

    Rubric: No Raw Loops, show an example of a raw loop

    Contracts & Semantics: I don't think people know what semantics is. Mathy stuff, brain turns off.
        Dave: Could just use "meaning"
        David: But I want to see "semantics", for some reason
        Foster: I like "intent"
        Bob: "semantics" is an accurate word that we want students to have learned at the end of the course. 

    People are just going to give up and do what they did before. 
        We need to connect it to day-to-day programming or people will give up and return to existing practice

    At one point, you say not to call "find" "search", but it wasn't clear to me why that was important. 

    We should describe what people actually do when they look at a loop.
        They might get a hunch, a few edge cases, the jist of the intent.

    Sean: I've been trying to avoid showing "bad" examples, except a bad implementation of min.
        For things like binary search or find, I can easily show subtly broken examples.
        I can walk the audience through figuring out why it's wrong, but that feels contrived.
        Laura: I agree with the direction of not using "bad" examples
            the power of the algorithms is in encapsulating a series of steps that we can reason about.
            it's not about "does this line do the right thing"
        Foster: Showing a raw loop as a "dull knife" and showing how people cut themselves on it.

    Dave: To make this relatable, I constructed a scenario of the object-editing program like illustrator.
        That makes it feel more like a day-to-day thing.

    stable_partition is unknown to most C++ developers, and most developers in other languages. Please ELI5. 
        this problem feels far removed from what most programmers write - but I'm not sure why.

    scan & reduction are primitive algorithms: I don't know what they are or why they're primitive
        Dave: Or leave it out.

    Green guys and white guys: use inclusive language like blocks
        avoid anthropomorphizing anything

    might be interesting to get feedback from folks disinclined to agree with the premise.
        want feedback from people that have the "ivory tower" complaint, but it would be valuable. 

    Sean: My 30 years of experience makes me sure that this material isn't ivory tower stuff

    Bob: a lot of your job, in terms of the talk, is explaining why this matters. 

    Foster: we just want to get people writing code to notice when they're about to write an algorithm, to stop, go to guild-cpp, and solicit help on discovering the right algorithm.
        Want to build that crossroads into people's minds
    
    We might want to look at the PR stream for photoshop and see what we find. If only for a data stream. 
        Dave: not just Photoshop - find the loops everywhere.

    It's challenging for the thought leader to write the tutorial. 
        Stepanov wrote the STL, using precise language, but I read Niko's book using more natural language.
        It's hard for the thought leader to communicate on their level.

    