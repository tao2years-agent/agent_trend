> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://www.comet.com/docs/opik/llms.txt.

# Annotation Queues

Your support leads, lawyers or doctors know when your agent is wrong. An annotation queue gives them a list of
traces or threads to label, in a view that shows each item the way they judge it. Their labels land on the traces
as feedback scores, ready to align your LLM judges and to build test suites.

## Create a queue

Open your project, go to **Annotation queues** and click **Create queue**. Give it a name, pick what it holds
(traces or threads) and write the instructions annotators read before they start.

![The queue creation sidebar with instructions, feedback scores, annotator settings and automation](/docs/opik/_fern-files/_img/9eafc2afec78ba1c9e1f7b0c7ce3c73725512d3d99a8b3972f6e7a950e600734.webp)

Then set:

* **Feedback scores**: what annotators fill in for each item. They are workspace-wide
  [feedback definitions](/docs/opik/administration/workspace-settings/feedback_definitions), so create them first. Use a
  category for a decision (Correct, Too generous, Should escalate) and a number for a rating such as reply tone.
  A few scores with clear descriptions get better labels than a long list.
* **Annotators per item**: how many people must score an item before it is done. Keep 1 for a fast pass. Use 2 or
  more when you need agreement between experts, for example to align a judge.
* **Lock timeout**: how long an annotator's review slot stays reserved. When it expires, another annotator can
  take that slot. If the queue requires multiple annotators per item, they can review the same item at once using
  separate slots. Raise the timeout when items take longer to review.
* **Automation**: add traces or threads to the queue when their scores match conditions, for example
  `policy_judge < 0.5`. See [Add items to the queue](#add-items-to-the-queue).

> **Note**
>
> You can also ask your coding agent to create the queue through the [Opik MCP server](/docs/opik/mcp-server).

## Customize the annotator view

Without a custom view, annotators see a trace's input, output and metadata as code blocks, or a thread as a chat.
That is fine for a quick check, but raw JSON slows reviewers down and hides what matters. A custom annotator view
lays out each item around the decision the annotator makes: the email next to the reply, the order next to the
policy, the numbers that break a rule.

![A custom warranty review view showing a headlamp's coverage timeline, customer report, agent resolution and policy reference](/docs/opik/_fern-files/opik.docs.buildwithfern.com/485fa8d8b8086a42500c4aaf71f1f4fd9961b45df482080dfae1b926962ab029/img/evaluation/annotation_queue_warranty_view.png)

A view is a small HTML page that Opik renders for every item in the queue. Scoring, comments and navigation stay
in Opik's own panel, so a view only changes how the item reads.

#### With your coding agent

Connect your coding agent to the [Opik MCP server](/docs/opik/mcp-server) (`uvx opik mcp configure`), then describe what
annotators need to see:

```text wordWrap
Give the "Refund decisions review" queue in my Trailhead Support Agent project a custom annotator view: the decision and refund amount up top, the customer email next to the agent reply, the order with how many days since delivery against the return window, and the judge score hidden until the annotator reveals it.
```

The agent reads real traces from the project to learn their shape, writes the view and saves it on the queue. It
answers with a link to the queue and a link to the page your annotators use.

#### With Ollie

On Opik Cloud, [Ollie](/docs/opik/ollie) writes and refines the view next to a live preview. Open the queue, click
**Edit**, and open the preview in the **Annotator view** section. Tell Ollie what to show, hide or highlight. Each
version shows up in the preview, on real items from the queue, before you save.

When the view fails on an item, the preview offers to fix it with Ollie.

* **Trace views** can use the trace's `input`, `output`, `metadata`, `tags`, `feedback_scores`, timing, token usage
  and cost. Spans are not included.
* **Thread views** get the thread and its traces in order, one per turn.
* **Judge scores** are in `feedback_scores`. Hide them behind a **Reveal** button so annotators give their own
  verdict first.

The view runs in a sandbox with no network access or external scripts, images or fonts, and follows Opik's light
and dark themes. If it fails on an item, Opik shows the default view for that item so annotators can keep working.

## Add items to the queue

There are two main ways to add traces or threads to an annotation queue: select them from the logs, or set up
automation to add them as new feedback scores arrive.

On your project's **Logs** page, select the traces or threads you want reviewed and click
**Add to > Annotation queue**. You can also add an individual item while viewing it.

To keep the queue filled as your agent runs, turn on **Automation** when creating or editing the queue. Set
conditions on feedback scores, such as `policy_judge < 0.5`, to route low-scoring items to your experts. Opik checks
for matches when new scores arrive, including from [online evaluation rules](/docs/opik/production/online-evaluation/rules),
and adds items that meet all conditions. Set **Cap automatically added items at** to limit how much work enters
the queue.

Automation starts with new scores on traces and threads logged by your application. It does not backfill older
scores or re-add items that were previously in the queue; add those manually when needed.

You can also [add items with the SDK](#manage-queues-with-the-sdk). In the queue's items table, the **Source** column
shows how each item was added.

## Review and score items

Open the queue and click **Share** to copy the link for your annotators. Annotators must be members of your
workspace, so [invite them](/docs/opik/administration/workspace-settings/workspace_members) first. Click **Annotate** to
work the queue yourself.

Annotators read the instructions, then go through the items one at a time. For each item they pick the feedback
scores, add a reason or a comment, and go to the next one. Items they finish move to **Processed**, where they can
go back and change a score.

## Use annotations to improve your agent

Annotator scores are feedback scores on the traces and threads, marked as human. You can filter and sort the logs
by them, and chart them on dashboards. Then put them to work:

* **Align your LLM judges**: compare a judge's scores to your annotators' labels and fix the judge where they
  disagree. See [Judge alignment](/docs/opik/evaluation/judge_alignment).
* **Build test suites**: turn the items your annotators flagged into test cases, so the next version of your agent
  is tested against them. See [Building test suites](/docs/opik/evaluation/advanced/building-test-suites).

## Manage queues with the SDK

The Python and TypeScript SDKs create, fill, read and delete queues. Custom annotator views are set through the
MCP server or in the UI.

#### Create a queue

**`Python`**

```python title="Python" wordWrap
import opik

client = opik.Opik()

queue = client.create_traces_annotation_queue(
    name="Refund decisions review",
    project_name="Trailhead Support Agent",
    instructions="Check each decision against the refund policy.",
    feedback_definition_names=["Refund decision", "Reply tone"],
)

print(f"Created queue: {queue.name} (ID: {queue.id})")
```

**`TypeScript`**

```typescript title="TypeScript" wordWrap
import { Opik } from "opik";

const client = new Opik();

const queue = await client.createTracesAnnotationQueue({
  name: "Refund decisions review",
  projectName: "Trailhead Support Agent",
  instructions: "Check each decision against the refund policy.",
  feedbackDefinitionNames: ["Refund decision", "Reply tone"],
});

console.log(`Created queue: ${queue.name} (ID: ${queue.id})`);
```

#### Add traces to a queue

**`Python`**

```python title="Python" wordWrap
import opik

client = opik.Opik()

queue = client.get_traces_annotation_queue("queue-id")

# Search for traces and add them to the queue
traces = client.search_traces(
    project_name="Trailhead Support Agent",
    filter_string="feedback_scores.policy_judge < 0.5",
)
queue.add_traces(traces)

# For a single trace, wrap it in a list
single_trace = client.get_trace_content("trace-id")
queue.add_traces([single_trace])
```

**`TypeScript`**

```typescript title="TypeScript" wordWrap
import { Opik } from "opik";

const client = new Opik();

const queue = await client.getTracesAnnotationQueue("queue-id");

// Search for traces and add them to the queue
const traces = await client.searchTraces({
  projectName: "Trailhead Support Agent",
  filterString: "feedback_scores.policy_judge < 0.5",
});
await queue.addTraces(traces);

// For a single trace, wrap it in an array
const singleTrace = await client.api.traces.getTraceById("trace-id");
await queue.addTraces([singleTrace]);
```

#### Read queue items

`get_items()` returns the traces (or threads, for a thread queue) in a queue.

**`Python`**

```python title="Python" wordWrap
import opik

client = opik.Opik()

queue = client.get_traces_annotation_queue("queue-id")
for trace in queue.get_items():
    print(trace.id, trace.name)

# For a threads queue, get_items() returns the threads
thread_queue = client.get_threads_annotation_queue("thread-queue-id")
threads = thread_queue.get_items()
```

**`TypeScript`**

```typescript title="TypeScript" wordWrap
import { Opik } from "opik";

const client = new Opik();

const queue = await client.getTracesAnnotationQueue("queue-id");
for (const trace of await queue.getItems()) {
  console.log(trace.id, trace.name);
}

// For a threads queue, getItems() returns the threads
const threadQueue = await client.getThreadsAnnotationQueue("thread-queue-id");
const threads = await threadQueue.getItems();
```

#### Work with thread queues

**`Python`**

```python title="Python" wordWrap
import opik

client = opik.Opik()

thread_queue = client.create_threads_annotation_queue(
    name="Thread review",
    project_name="Trailhead Support Agent",
    instructions="Did the agent solve the customer's problem?",
)

threads_client = client.get_threads_client()
threads = threads_client.search_threads(
    project_name="Trailhead Support Agent",
    filter_string='tags contains "escalated"',
)
thread_queue.add_threads(threads)
```

**`TypeScript`**

```typescript title="TypeScript" wordWrap
import { Opik } from "opik";

const client = new Opik();

const threadQueue = await client.createThreadsAnnotationQueue({
  name: "Thread review",
  projectName: "Trailhead Support Agent",
  instructions: "Did the agent solve the customer's problem?",
});

const threads = await client.searchThreads({
  projectName: "Trailhead Support Agent",
  filterString: 'tags contains "escalated"',
});
await threadQueue.addThreads(threads);
```

#### Update, list and delete queues

**`Python`**

```python title="Python" wordWrap
import opik

client = opik.Opik()

queue = client.get_traces_annotation_queue("queue-id")
queue.update(instructions="Check the decision and the tone of the reply.")

# Remove traces from the queue
fast_traces = client.search_traces(
    project_name="Trailhead Support Agent",
    filter_string="duration < 10",
)
queue.remove_traces(fast_traces)

# List the project's queues
for q in client.get_traces_annotation_queues(project_name="Trailhead Support Agent"):
    print(q.name, q.items_count)

for q in client.get_threads_annotation_queues(project_name="Trailhead Support Agent"):
    print(q.name, q.items_count)

queue.delete()
```

**`TypeScript`**

```typescript title="TypeScript" wordWrap
import { Opik } from "opik";

const client = new Opik();

const queue = await client.getTracesAnnotationQueue("queue-id");
await queue.update({
  instructions: "Check the decision and the tone of the reply.",
});

// Remove traces from the queue
const fastTraces = await client.searchTraces({
  projectName: "Trailhead Support Agent",
  filterString: "duration < 10",
});
await queue.removeTraces(fastTraces);

// List the project's queues
const tracesQueues = await client.getTracesAnnotationQueues({
  projectName: "Trailhead Support Agent",
});
for (const q of tracesQueues) {
  console.log(q.name);
}

const threadsQueues = await client.getThreadsAnnotationQueues({
  projectName: "Trailhead Support Agent",
});
for (const q of threadsQueues) {
  console.log(q.name);
}

await queue.delete();
```

## Next steps

* [Opik MCP server](/docs/opik/mcp-server): connect your coding agent to Opik.
* [Judge alignment](/docs/opik/evaluation/judge_alignment): use your annotators' labels to improve your LLM judges.
* [Online evaluation rules](/docs/opik/production/online-evaluation/rules): score production traces, and feed the low scores into a queue.
* [Feedback definitions](/docs/opik/administration/workspace-settings/feedback_definitions): set up the scores annotators give.