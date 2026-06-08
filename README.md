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

**Why these choices fit your documents:** I chose 350 tokens for the chunk size because Reddit comments are commonly only 100 or 200 tokens and are very compact, but YouTube transcripts are very long and sparse, so larger chunks are better for those. A reasonable midpoint of 350 tokens per chunk should work well. For the overlap, I chose 50 tokens since an overlap that is too big would result in lots of repeated information between the different chunks, especially with the Reddit comments.

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
- *What I changed or overrode:* During testing, after finding issues with chunk and overlap sizes of 250 and 40 tokens respectively, I manually testing with different sizes until settiling on 350 and 50 tokens respectively to improve performance.

**Instance 2**

- *What I gave the AI:* I gave Claude Code the task in Milestone 4 of helping me call the embedding model and applying it to the chunks produced by ingest.py, and then storing and calling that information using ChromaDB.
- *What it produced:* Claude produced most of the currently present embed.py file, which calls the all-MiniLM-L6-v2 embedding model and stores/retrieves the embedded vectors using ChromaDB.
- *What I changed or overrode:* After getting absurdly high (>0.8) distances for chunks that had almost the exact same wording as the prompts, I knew something was wrong with the embedding model. After double checking what Claude gave me, I had it fix the distance similarity from the Euclidean distance it initially outputted to cosine similarity.

---

## Sample Chunks

Five representative chunks drawn from five different source documents, produced by `ingest.py` with a chunk size of 350 tokens and an overlap of 50 tokens.

**Chunk 1 — source1.txt (YouTube: "Best Student Housing University Of Texas At Dallas"), chunk index 0**

> we want to talk about some on-campus housing well the residence Halls you know the hostels are mostly undergrads there's on-campus housing like the UV University Village Apartments which are a little bit older but super convenient being in the heart of campus and available to Masters and PhD students and there's a newer construction called Canyon Creek which um newer nice kind of apartment dorms on campus which is available also for higher grad students so what are some uh things that people need to know about the on campus housing well the first thing is it gets sold out quickly like this it's high demand it's it's totally hiding demand but yeah if you are considering suppose you want a diversity of students you want to get it over there because very few Indian students they usually in on-campus housings uh that being said uh believing in on campus is really fun because University is a stressed inside you I mean beside you you can just walk by you get everything covered in there itself in the whole rent media electricity or be it your Wi-Fi thing which is of course the university Wi-Fi so all the things are covered but it's super high in demand it goes out quickly you have to book it like way before time you have to give it at least one semester ahead yeah one semester you have to give it you have to give a deposit which is like an unrefitable thing so you are not sure

**Chunk 2 — source10.txt (Reddit: "Housing Questions"), chunk index 0**

> Title: Housing Questions
>
> Post: Hey guys, the last question I found about residency was posted about 4 years ago, so I thought I would re-ask this question to see if anything changed. I'm an incoming freshmen, and am wondering if I should stay in the honors dorm, the living learning community, or a campus apartment. My friend from high school wants to split an apartment with me, he's going to be a freshman as well, but I believe that it would be better to stay in the dorm and have an easier time making new friends. One thing I heard about the living learning community is that you can get closer to professors and potentially research opportunities. As a computer science major, this would interest me as well. Yet I do not want to be stuck with only computer science majors, and like a bit of diversity as well. Thanks for your opinions on this matter in advance!
>
> Comments:
>
> I have no idea how dorms work, so are the dorms, at least on the same floor, are co-ed? And how much do you stand to gain from LLC activities, e.g. getting closer to professors etc.
>
> Is the LLC open only to freshmen? As I currently live in Austin, I would stay on campus for all 4 years. Do you move around each year to another dorm or apartment?

**Chunk 3 — source2.txt (YouTube: "University Village Apartments"), chunk index 0**

> hey everybody Rob here at Cheyenne coaching my friend with my friend here akshay hello Akshay introduce us and tell people where we're at hello I'm moksha I'm the 416 student studying computer science masters here in utd college and currently I'm staying in the inner city believes housing it's an on-campus housing and not outside the campus and currently we are in a 1 BHK room and this you can see is the hall of the and the living room of the room and you can see is the bedroom so basically usually housing you have to pay eight seventy five dollars for this one pH scale room comparatively to others the outside campus you're basically paying it's 30 or something like that and this utility housing it is inclusive for all the utilities on the prices and what is a two-bedroom go for here two-bedroom go for a thousand five hundred so it will having two rooms and each person stays in one room so basically are paying 750 per room okay yeah actually tell us about some of the amenities or conveniences here about stayin at the University Village Apartments on campus sure the thing is if you stay on campus you don't have to travel by bus so if you stay off campus the bus will take you from off campus and to the college and that takes a lot of time because there are a lot of students and sometimes you can't even get on the bus because it's a motional time it's full so if you stay on the

**Chunk 4 — source3.txt (YouTube: "Canyon Creek Heights Apartments"), chunk index 0**

> Hey friends, welcome to Chai and Coaching. Rob here. We're going to do another quick housing tour. We are at the Canyon Creek Heights apartment on campus here at UTD. We're going to give you a full tour of this on-campus housing option and compare it with off-campus and it's going to be really helpful. Check it out.
>
> This is going to be our tour guides. Go ahead and introduce yourselves.
>
> I'm Yes and I'm doing my master's in computer science here, living at Canyon Creek. Hello everyone. I'm Shel and I'm pursuing a master's in computer science here at UTD and I'm living at Valencia. Hey, my name is Neil and I'm a graduate student of computer science and I live here at Canyon Creek Heights North. And where are you guys from? We are all from Ahmedabad, Gujarat. Awesome. Well, let's start the tour.
>
> We are here at the Canyon Creek Heights North apartment. Can you tell us about Canyon Creek? It's our on-campus apartments where we have two parts — Canyon Creek North and South. The main biggest benefit here is we live on campus so we don't have to worry about buses or anything. We can simply walk in 10 minutes to our place and we also have Comet Cards which help a lot — you will be at your class in 2 minutes. Utilities and electricity are all covered in rent, that's also a good point.

**Chunk 5 — source4.txt (Reddit: "How is housing this bad???"), chunk index 0**

> Title: How is housing this bad???
>
> Post: I'm a freshman and I was hoping to live on campus again next year. I was looking forward to living in UV since I've been pretty happy with my dorm this year. While my groups priority could've been better, our appointment was this morning so I thought our chances were pretty good since it only opened yesterday. Well, we opened up the room selection to find out that there's no rooms left in UV or Canyon Creek and hardly anything left in Northside. We managed to grab an apartment in Northside but it might be too expensive for some of us so we might have to split up and some in my group aren't from the area. So, our plans might be ruined if Northside doesn't work out.
>
> How does this school not have enough room for everyone who wants to live on campus to actually do that? With the way priority works I don't even understand how I'd ever be able to get an apartment in UV or CC in the future, if I even stay here for junior year. I've never heard of another college having this issue it's ridiculous.
>
> Does anyone have recommendations for cheaper, nearby, off campus apartments just in case Northside doesn't work for us?

---

## Retrieval Examples

Three queries run against the live ChromaDB collection. Each shows the top returned chunks with their cosine distance scores (lower = more similar).

---

### Query 1: "Are Canyon Creek Heights apartments furnished?"

| Rank | Source | Chunk index | Distance |
|------|--------|-------------|----------|
| 1 | source3.txt | 1 | 0.2944 |
| 2 | source3.txt | 2 | 0.4883 |
| 3 | source9.txt | 1 | 0.4887 |

**Top chunk text (source3.txt, chunk 1):**

> Canyon Creek Heights North and South are both especially for graduate students and PhD students. So if anyone is coming here for the first time and thinking about on-campus housing, only graduate and PhD students stay over here. How old is this building? It's just 2 or 3 years old. So it's a very new construction.
>
> There are different types of apartments — we are living in a two-bedroom shared apartment, and there are also individual rooms available in South. The greatest benefit here is that even the University Village apartments are totally unfurnished, but these are furnished apartments. You get everything and you just have to take your clothes and come to stay. This is a completely furnished apartment — all light bills, electricity bills, Wi-Fi bills, everything is covered. Water is also covered. We don't need to arrange for anything else when we first come here. We just take our bags and our clothes. Plus for laundry, we have a laundry room downstairs and it's free — it's all included.

**Why these chunks are relevant:** The top result (distance 0.2944) contains the exact phrase "furnished apartments" and the specific detail "you just have to take your clothes and come to stay," which directly and completely answers the furnishing question. The second result adds pricing and utility context confirming the all-inclusive rent claim. Both chunks come from the Canyon Creek Heights video tour — the most authoritative source for this question — making the retrieval highly precise.

---

### Query 2: "Are the UTD dorms single occupancy or shared rooms?"

| Rank | Source | Chunk index | Distance |
|------|--------|-------------|----------|
| 1 | source7.txt | 0 | 0.3837 |
| 2 | source7.txt | 1 | 0.3918 |
| 3 | source6.txt | 0 | 0.4337 |

**Top chunk text (source7.txt, chunk 1):**

> 1. Individual rooms are spacious for college dorms. Each has space for a twin-sized bed, a desk, and a dresser (all included). University Housing has a virtual tour and specs available on its website.
> 2. Incoming freshmen (and only freshmen) who choose to live on campus must live in University Commons (the residence halls). Compared to other housing, Canyon Creek Heights North and South are very comparable to the residence halls in terms of space (just being slightly larger due to having a kitchen in each unit), and the apartments in University Village are just what you'd expect for a college apartment: not too big, but just big enough for a living room and maybe (depending on floorplan) a dining nook. There is more variety in upperclassmen housing; if you wish to live alone or only with one roommate, there are 1x1 and 2x2 units for that in UV and CCHS.
> 3. If you're into a more social scene, Northside (technically off campus) tends to contain more of a "college life" atmosphere. If you would prefer not having to deal with furniture during move-in/move-out and don't mind a 10 minute walk to campus every day, Canyon Creek Heights is just for you. Otherwise, University Village should work if you want to stay on campus and don't mind the issues that come with apartments built over 20 years ago.

**Why these chunks are relevant:** The query uses the phrase "single occupancy or shared rooms" and the top two chunks both come from the Reddit thread specifically addressing dorm structure. source6.txt chunk 0 states "All the rooms are 3 individual bedrooms (your own), 3 sinks, 1 toilet, and 1 shower" — a first-hand, precise answer about room-sharing configuration. The embedding model correctly matched "dorms" and "single/shared" to occupancy-focused content rather than returning price or safety chunks.

---

### Query 3: "Are there any problems with maintenance or insects?"

| Rank | Source | Chunk index | Distance |
|------|--------|-------------|----------|
| 1 | source8.txt | 2 | 0.7582 |
| 2 | source9.txt | 3 | 0.8139 |
| 3 | source3.txt | 3 | 0.8201 |

**Top chunk text (source8.txt, chunk 2):**

> I would personally recommend against UV. My experience there was very poor. My sinks never drained and I didn't have hot water in the shower for the later half of the year. Yes I complained, no they didn't fix it. My washer was flooding and wouldn't drain when I moved in as well and that took over 2 months to get fixed. Loud neighbors (though obviously that depends on the year). The pool filled with leaves and turned green, and they never cleaned it until I was about to move out. Also they will send inspectors into your unit to make sure you're following dorm rules. That being said my rent after stipend was around $400 a month for a single so hard to beat that price.
>
> Yeah it's mainly the price that had me all good with UV. But I also never had any maintenance problems or just problems in general.
>
> My main issue now at Northside (I'm applying for on-campus housing as soon as I can though lol) is trying to get ANYTHING resolved. Our refrigerator broke and it took 4 weeks to fix it. This was after I had switched rooms twice ($500 each time) because the roommates were unbearable.

---

## Example System Responses with Source Attribution

Two complete query-and-response examples as generated by the live pipeline (retrieval → LLM → grounded answer → programmatic source attribution). Source names are attached by `query.py`, not by the LLM.

---

**Query:** Are Canyon Creek Heights apartments furnished?

**Answer:** Yes, the Canyon Creek Heights apartments are furnished. According to the information provided, "these are furnished apartments. You get everything and you just have to take your clothes and come to stay." This means that the apartments come with all the necessary furniture, and residents do not need to bring their own or arrange for any additional items.

**Retrieved from:**
- source3.txt
- source9.txt
- source7.txt

---

**Query:** Are the UTD dorms single occupancy or shared rooms?

**Answer:** The UTD dorms have individual rooms, but they are shared in the sense that three students share a common area with 3 sinks, 1 toilet, and 1 shower, and a living room space. Each student has their own individual room with a twin-sized bed, a desk, and a dresser.

**Retrieved from:**
- source7.txt
- source6.txt
- source8.txt

---

## Out-of-Scope Refusal Example

When a query's top-k chunks all have a cosine distance above the relevance cutoff (0.85), `query.py` refuses without calling the LLM and returns the fixed refusal string.

**Query:** What is the best pizza topping?

**Answer:** I don't have enough information on that.

**Retrieved from:** (no sources — the guide didn't have enough information)

---

## Query Interface

The system is served as a Gradio web app (`app.py`). The interface has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| **Your question** | Text input (2 lines) | Where the user types a question about UTD on-campus housing. Pressing Enter or clicking **Ask** submits it. |
| **Ask** | Primary button | Triggers the retrieval-and-generation pipeline. |
| **Answer** | Text output (8 lines) | Displays the LLM-generated, grounded answer. If no chunk clears the relevance cutoff, it shows the fixed refusal message instead. |
| **Retrieved from** | Text output (4 lines) | Lists the source file names (e.g., `source3.txt`) that contributed to the answer. Generated programmatically from chunk metadata — not by the LLM. |

Pre-loaded example questions are shown below the input box so users can click to auto-fill without typing.

**Sample interaction transcript:**

```
User input (Your question):
  Are Canyon Creek Heights apartments furnished?

[User clicks Ask]

Answer:
  Yes, the Canyon Creek Heights apartments are furnished. According to the
  information provided, "these are furnished apartments. You get everything
  and you just have to take your clothes and come to stay." This means that
  the apartments come with all the necessary furniture, and residents do not
  need to bring their own or arrange for any additional items.

Retrieved from:
  • source3.txt
  • source9.txt
  • source7.txt
```
