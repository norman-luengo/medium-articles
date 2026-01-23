# What We Learned After Shipping a Company-Wide GenAI Chatbot

We recently deployed a GenAI chatbot for a large, enterprise-scale organization.

The application looks deceptively simple from the outside: a ChatGPT-like interface where employees can ask questions and get answers. Under the hood, however, it’s a fairly complex system. The backend is built with **FastAPI** and **LangGraph**, the frontend with **Nest.js**, and the whole platform runs on **AWS**, relying heavily on **Bedrock** for LLM inference.

The chatbot answers generic questions using the model’s own knowledge, but it also goes much further: creating IT and support tickets, querying structured data tables, and answering domain-specific questions across areas like contracting, onboarding, travel & expenses, and more.

This article is not a product announcement. It’s a reflection on what worked, what didn’t, and what we would do differently if we were starting again today. Some of these lessons were expensive to learn, so hopefully they’ll save others some time.



## AI & Architecture Learnings

### 1. Multi-agent architectures dramatically improve conversational quality

Our first iterations followed a fairly classic pipeline approach: intent detection, query condensation, routing, response generation.

The jump to a **multi-agent architecture**,with a supervisor orchestrating specialized agents, was a turning point.

The improvement in perceived intelligence was immediate and significant. Conversations felt more natural, reasoning became clearer, and the system aligned much better with what users expect from a modern GenAI application.

If you’re building a conversational system today, this is one of the highest-leverage architectural decisions you can make.

---

### 2. The LangGraph ReAct pattern caused serious issues

We initially used the **ReAct pattern** in LangGraph. In practice, it created more problems than it solved:

- Agents getting stuck in tool-search loops  
- Excessive token usage  
- A large number of LLM calls per request  
- Increased latency  

With the current generation of models, this pattern feels effectively deprecated. Our strong recommendation: **avoid it**. Simpler, more explicit control flows perform better and are much easier to reason about.

---

### 3. Supervisors should not do everything

Over time, our supervisor agent accumulated responsibilities:

- Delegation  
- Translation  
- FAQ validation  
- JSON response generation  
- Follow-up suggestion creation  

This made prompt debugging painful. Fixing a translation issue could suddenly break structured output formatting or delegation logic somewhere else.

The key realization was that **A single agent should not be responsible for lots of things**.

A better approach would have been a hybrid system where:

- Classical **LLM** components handle deterministic tasks (translation, query condensation, FAQ checks)
- Agents focus on reasoning, decision-making, and task execution

This separation of concerns would have made prompts easier to design, debug, and evolve over time.

---

### 4. Prompt caching was the single most impactful optimization

If we had to pick one MVP feature, this would be it.

Our prompts were long and complex, and we averaged **around seven LLM calls per user request**. Unsurprisingly, we quickly ran into token limits and cost constraints.

Prompt caching completely changed the game:

- Dramatically lower token consumption  
- Better scalability  
- Significant cost reduction  

One important gotcha: **prompt caching is not enabled by default in AWS Bedrock**. You must explicitly configure it. If you’re running at any meaningful scale, this is non-negotiable.

---

### 5. Streaming responses are a major UX improvement

Without streaming, complex queries could take **20–30 seconds** before the user saw anything. That feels broken, even if the final answer is good.

With streaming enabled, tokens arrive almost immediately. The perceived latency drops dramatically, and users feel like the system is responsive and alive.

In our case, we implemented a simple `streaming: true | false` flag:

- Enabled in production for optimal UX  
- Disabled for debugging, Swagger, automated tests, and local development  

Streaming complicates observability, but for conversational applications, it should be considered **mandatory**.

---

### 6. Regression testing for prompts is absolutely mandatory

We learned this the hard way.

Prompts are fragile. A small change intended to improve one behavior can silently break another that was previously working well.

Without systematic validation, regressions are almost guaranteed.

Our takeaway is simple: **treat prompts as production code**.

That means:

- Validation  
- Automated regression testing  
- Clear ownership and review  

If your prompts are not tested, your system is not stable, no matter how good it looks today.

---

### 7. Model upgrades require a defined, repeatable process

We started on **Claude Sonnet 2.0** and are currently running **Sonnet 4.5**, going through multiple intermediate versions along the way.

Every single upgrade broke prompts.

Even when instructions were explicit. Even when behavior had been stable for months.

Some observations:

- Most intermediate upgrades provided little to no quality improvement  
- Meaningful gains only came from major generational jumps (2.0 → 3.0 → 4.0)  
- The rapid model release cadence is misaligned with application development cycles  

To make things harder, AWS actively pressures teams to migrate by reducing quotas for older models, even when there’s no product benefit.

This is not sustainable.

We urgently need standardized processes for model upgrades, including:

- Prompt versioning  
- Systematic evaluation  
- Tooling (MLflow or similar)  

This is an industry-wide problem, and it’s not going away.

---

## Scalability & Concurrency Learnings

### 8. Boto3 being synchronous is a major bottleneck

One of our biggest challenges was that **boto3 is synchronous**. Bedrock calls cannot be truly async.

That forces the use of threads, which in Python:

- Adds overhead  
- Limits effective concurrency  
- Makes performance harder to reason about  

I previously wrote in more detail about this topic here:  
[*Exploring Python’s GIL: Single/Multithreading vs. Multiprocessing and the Impact of GIL Removal*](https://medium.com/sdg-group/exploring-pythons-gil-single-multithreading-vs-multiprocessing-and-the-impact-of-gil-removal-ee8b6dd610f4)

---

### 9. Async wrappers can be misleading

Many libraries expose `async` APIs, but that doesn’t mean they’re truly asynchronous.

For example:

```python
await model.ainvoke()
```

Under the hood, LangChain:

- Calls the synchronous boto3 client

- Executes it inside a thread

The same applies to other integrations:

- Pinecone is synchronous

- LangChain’s async vector stores rely on threads

The lesson: **never trust async wrappers blindly. Always inspect what’s actually happening underneath**.


Even though we use FastAPI and our codebase is fully async the application is not truly asynchronous due to the synchronous SDKs underneath.

Threads prevent event-loop blocking, but they don’t magically unlock high concurrency. Understanding this is critical when planning for scale.

---
### 10. Horizontal scaling was the only viable solution

To handle high levels of concurrent usage, we had to scale aggressively:

- 9 Uvicorn workers per replica

- 5 application replicas

- Total: 45 running instances

Autoscaling was enabled up to 20 replicas to handle launch-day spikes.

After extensive stress testing, this setup gave us the reliability and headroom we needed.

Sometimes, brute force really is the only practical answer.

---
### Final Takeaways
- Multi-agent systems significantly improve conversational UX

- Supervisors should not be overloaded with responsibilities

- Prompt caching and streaming are essential at scale

- Prompts require regression testing and versioning

- Model upgrades are costly and must be managed deliberately

- Synchronous SDKs severely limit concurrency, verify your stack

- When all else fails, horizontal scaling works

Shipping a GenAI application in production is very different from building a demo. Beyond the code, production exposes the full complexity of business logic, workflows, and edge cases that a demo never reveals.


If you’re on a similar journey, I hope these lessons help you avoid at least a few painful detours.