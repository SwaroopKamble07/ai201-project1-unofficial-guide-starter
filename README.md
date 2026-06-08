# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
I chose the domain of student experiences with on-campus housing at my university, the University of Texas at Dallas. This knowledge is valuable because it is crucial to help student decide whether to choose to live on or off campus, and what they can expect to experience if they live on campus. This can't really be found through official channels because the university only publishes basic information about what's included with on-campus housing, but not any student reviews or any of the downsides that may come from living on campus. 
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Best Student Housing University Of Texas At Dallas | YouTube | https://www.youtube.com/watch?v=ZoanKQ0wrCA |
| 2 | University Village Apartments - Richardson, TX | UT Dallas On Campus Student Housing | YouTube | https://www.youtube.com/watch?v=fRG2uwTNZ8U |
| 3 | Canyon Creek Heights Apartments - Richardson, TX | UT Dallas On Campus Student Housing | YouTube | https://www.youtube.com/watch?v=GvXyADz0sYY |
| 4 | How is housing this bad??? | Reddit | https://www.reddit.com/r/utdallas/comments/1b1q20n/how_is_housing_this_bad/ |
| 5 | UTD housing (incoming freshmen) | Reddit | https://www.reddit.com/r/utdallas/comments/1tq5ghl/utd_housing_incoming_freshmen/ |
| 6 | Need advice on dorms | Reddit | https://www.reddit.com/r/utdallas/comments/1j63bv1/need_advice_on_dorms/ |
| 7 | What are dorms/housing like on campus? What do I need to bring? | Reddit | https://www.reddit.com/r/utdallas/comments/lc26tv/what_are_dormshousing_like_on_campus_what_do_i/ |
| 8 | Which dorm/housing should I choose? | Reddit | https://www.reddit.com/r/utdallas/comments/sz7f3z/which_dormhousing_should_i_choose/ |
| 9 | Best housing option for sophomore year? | Reddit | https://www.reddit.com/r/utdallas/comments/d894jm/best_housing_option_for_sophomore_year/ |
| 10 | Housing Questions | Reddit | https://www.reddit.com/r/utdallas/comments/5v79qe/housing_questions/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 350 tokens

**Overlap:** 50 tokens

**Why these choices fit your documents:** I chose 350 tokens for the chunk size because Reddit comments are commonly only 100 or 200 tokens and are very compact, but YouTube transcripts are very long and sparse, so larger chunks are better for those. A reasonable midpoint of 350 tokens per chunk should work well. For the overlap, I chose 40 tokens since an overlap that is too big would result in lots of repeated information between the different chunks, especially with the Reddit comments.

**Final chunk count:** 47

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:** If I was deploying this for real users without any cost constraints, I would go for a significantly larger model that may be much slower, but also much more accurate. Since cost corresponds to the amount of processing power used and cost is not a constraint, the amount of processing power would not be a constraint, and thus, the embedding model would not be too slow to run for the users. Therefore, having a model such as OpenAI's text-embedding-3-large would offer a good tradeoff since it has a large context length, good multilingual support, and high accuracy on domain-specific text, all without having too much latency.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** You are The Unofficial Guide, a question-answering assistant about \
student experiences with on-campus housing at the University of Texas at Dallas (UTD).

Follow these rules without exception:
1. Answer ONLY using the information in the CONTEXT provided in the user message. \
Do not use any outside knowledge or anything from your training data.
2. If the CONTEXT does not contain enough information to answer the question, reply with \
exactly this sentence and nothing else: "{refusal}"
3. Never invent details, numbers, names, or facts that are not stated in the CONTEXT.
4. Do not mention or cite source files yourself — the system adds source attribution \
automatically after your answer.
5. Never use the word "CONTEXT" in your response. Answer naturally and directly, \
as if the information is simply what you know.

Every part of your answer must be traceable to the CONTEXT.""".format(refusal=REFUSAL)

USER_TEMPLATE = """CONTEXT:
{context}

QUESTION: {question}

Answer using only the CONTEXT above."""

**How source attribution is surfaced in the response:** The ask() function finds the names of the source files from the metadata of the unique chunks, and then the Gradio app displays the sources below the answer box. This guarantees that the source file attribution is correct since it is generated by the Python program and not the output of the LLM, which may be prone to errors.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Are Canyon Creek Heights apartments furnished? | Yes, Canyon Creek Heights apartments are fully furnished. Residents only need to bring their clothes, as all furniture is provided. In addition, all utilities including electricity, Wi-Fi, water, and laundry are included in the rent. | Yes, Canyon Creek Heights apartments are fully furnished and all utilities are included. | Relevant | Accurate |
| 2 | Are the UTD dorms single occupancy or shared rooms? | UTD freshman dorms feature individual private bedrooms with shared bathroom facilities and common living areas. Each suite consists of three private bedrooms, with residents sharing one toilet, one shower, and multiple individual sinks. | UTD freshman dorms have individual furnished bedrooms, and shared living rooms and bathrooms, but each student has their own sink. | Relevant | Accurate |
| 3 | Do the Canyon Creek Heights apartments include utilities in rent? | Yes, Canyon Creek Heights apartments include comprehensive utilities coverage in the rent, including electricity, water, Wi-Fi, internet access, and laundry facilities. Residents do not incur additional utility costs beyond the base rent. | Yes, Canyon Creek Heights apartments include utilities in rent, so residents don't need to arrange or pay for those separately. | Relevant | Accurate |
| 4 | Is Canyon Creek Heights safe? | Canyon Creek Heights maintains robust security measures including Comet Card (student ID) access control and regular campus police patrols conducted approximately every thirty minutes throughout the residential area. | Canyon Creek Heights is considered safe, because there are police patrols, a gated community, and Comet Card scanners that residents need to use to unlock the doors| Relevant | Partially accurate |
| 5 | Are there any problems with maintenance or insects? | Yes, there are some problems with maintenance, particularly in the UV apartments, with several people reporting problems with sink drainage, hot water, mild ant problems, and flooding washers. At CCHN, there was also a mold problem | Yes, there are problems with maintenance, such as ants, drainage issues, and hot water issues in UV, and mold in CCHN. At Northside, a fridge broke and it took 4 weeks to fix it. | Partially relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Are there any problems with maintenance or insects?

**What the system returned:** "Yes, there are problems with maintenance or insects. At UV, one resident had issues with sinks not draining, no hot water in the shower, and a washer that was flooding and wouldn't drain, which took over 2 months to get fixed. Another resident mentioned having a couple of ants occasionally at UV. At Northside, a refrigerator broke and it took 4 weeks to fix it. At CCHN, there was a mold problem."

**Root cause (tied to a specific pipeline stage):** The part that was not relevant was the part where it mentioned student experiences with Northside. While that information was correct, the Northside apartments are actually considered off-campus housing, and not on-campus housing. This is tied to the document ingestion stage, because mentions of specific student experiences with off-campus housing should have been removed, but in this case, this mention was not removed.

**What you would change to fix it:** To fix this irrelevant response behavior, I would filter the sources better for mentions of specific student experiences with off-campus housing and remove them. However, I would not remove every single mention of off-campus housing since they are still sometimes useful when discussing on-campus housing, so I would need to be selective as to which mentions to keep and which to remove.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec helped me a lot during the implementation by giving me the exact information I needed to plan out step by step what I should provide Claude with in order to have it build the program according to the proper specifications. Furthermore, it also prompted me to truly consider which specific models and parameters to use for things such as chunk size.

**One way your implementation diverged from the spec, and why:** I ended up changing my chunk and overlap sizing from 250 to 350 tokens and 40 to 50 tokens respectively, since I was initially getting very high distance scores. This helped me because it resolved a lot of issues I had with getting chunks that had fairly low distance scores, but were not very relevant to the prompts.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude Code my documents folder along with my chunking strategy specifications from the planning file. I asked it to inplement the ingest.py program using those specifications so that they would work with my documents.
- *What it produced:* Claude Code successfully produced most of the final ingest.py that is in this repo, which accurately chunks the sources according to the given paramters.
- *What I changed or overrode:* During testing, after finding issues with chunk and overlap sizes of 250 and 40 tokens respectively, I manually changed the sizes for each of those sizes to 350 and 50 tokens respectively to improve performance.

**Instance 2**

- *What I gave the AI:* I gave Claude Code the task in Milestone 4 of helping me call the embedding model and applying it to the chunks produced by ingest.py, and then storing and calling that information using ChromaDB.
- *What it produced:* Claude produced most of the currently present embed.py file, which calls the all-MiniLM-L6-v2 embedding model and stores/retrieves the embedded vectors using ChromaDB.
- *What I changed or overrode:* After getting absurdly high (>0.8) distances for chunks that had almost the exact same wording as the prompts, I knew something was wrong with the embedding model. After double checking what Claude gave me, I had it fix the distance similarity from the Euclidean distance it initially outputted to cosine similarity.
