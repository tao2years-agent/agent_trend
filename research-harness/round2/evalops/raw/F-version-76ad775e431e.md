---
title: Version Control
seoTitle: "Prompt Version Control"
sidebarTitle: Version Control
description: Use prompt labels to fetch specific prompt versions in the SDKs.
---

# Prompt Version Control

In Langfuse, version control & deployment of prompts is managed via `versions` and `labels`.

## Implementation

### Versions & Labels [#versions--labels]

Each prompt version is automatically assigned a `version ID`. Additionally, you can assign `labels` to follow your own versioning scheme.

Labels can be used to assign prompts to environments (staging, production), tenants (tenant-1, tenant-2), or experiments (prod-a, prod-b).

**Langfuse UI**

Use the Langfuse UI to assign labels to a prompt.

_[Video: Promote a prompt version to production](https://static.langfuse.com/docs-videos/deploy-prompt.mp4): Prompts > qa-answer-with-context-chat with the latest version (#12) selected. Click “Add label”, tick production under “Promote to production?” and click “Save and promote to production”; the production label moves to #12. The video then selects #9 and promotes it back to production._

**Python SDK**

Use the Python SDK to assign labels to a prompt when creating a new prompt version.

```python {5}
langfuse.create_prompt(
    name="movie-critic",
    type="text",
    prompt="As a {{criticlevel}} movie critic, do you like {{movie}}?",
    labels=["production"],  # add the label "production" to the prompt version
)
```

Alternatively, you can also update the labels of an existing prompt version using the Python SDK:

```python {5}
langfuse = Langfuse()
langfuse.update_prompt(
    name="movie-critic",
    version=1,
    new_labels=["john", "doe"], # assign these labels to the prompt version
)
```

**JS/TS SDK**

Use the JS/TS SDK to assign labels to a prompt when creating a new prompt version.

```ts {5}
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

await langfuse.prompt.create({
  name: "movie-critic",
  type: "text",
  prompt: "As a {{criticlevel}} critic, do you like {{movie}}?",
  labels: ["production"], // add the label "production" to the prompt version
});
```

Alternatively, you can also update the labels of an existing prompt version using the JS/TS SDK:

```ts {5}
await langfuse.prompt.update({
  name: "movie-critic",
  version: 1,
  newLabels: ["john", "doe"],
});
```

## Fetching by Label or Version

When fetching prompts to use them in your application you can either do so by fetching a specific version or label.
Here are code examples for fetching prompts by label or version.

**To "deploy" a prompt version**, you have to assign the label `production` or any environment label you created to that prompt version.

Some notes on fetching prompts:

- The `latest` label points to the most recently created version.
- When using a prompt without specifying a label, Langfuse will serve the version with the `production` label.
- If no version carries the requested label, the request fails with `404 Not Found`. Langfuse never silently falls back to `production` or `latest`; see [how label resolution works](#label-resolution).

**Python SDK**

```python
from langfuse import get_client

# Initialize Langfuse client
langfuse = get_client()

# Get specific version
prompt = langfuse.get_prompt("movie-critic", version=1)

# Get specific label
prompt = langfuse.get_prompt("movie-critic", label="staging")

# Get latest prompt version. The 'latest' label is automatically maintained by Langfuse.
prompt = langfuse.get_prompt("movie-critic", label="latest")
```

**JS/TS SDK**

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Get specific version of a prompt (here version 1)
const prompt = await langfuse.prompt.get("movie-critic", {
  version: 1,
});

// Get specific label
const prompt = await langfuse.prompt.get("movie-critic", {
  label: "staging",
});

// Get latest prompt version. The 'latest' label is automatically maintained by Langfuse.
const prompt = await langfuse.prompt.get("movie-critic", {
  label: "latest",
});
```

### How label resolution works [#label-resolution]

The SDKs fetch prompts from `GET /api/public/v2/prompts/{name}`, so these rules apply whether you call the API directly or use `get_prompt` / `prompt.get`:

| You pass                      | Langfuse returns                                                                                                            |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Neither `label` nor `version` | The version labeled `production`. If no version has that label, the request fails with `404`.                               |
| `label="staging"`             | The version that currently carries `staging`. If no version does, `404` — there is no fallback to `production` or `latest`. |
| `version=3`                   | Version 3, regardless of its labels.                                                                                        |
| Both `label` and `version`    | A `400` error: the two are mutually exclusive.                                                                              |

Because a missing label is an error rather than a fallback, a typo in a label name or an environment whose label was never assigned surfaces immediately as a failed fetch, not as the wrong prompt being served. The SDKs handle this with a [fallback prompt](/docs/prompt-management/features/guaranteed-availability) if you configure one; otherwise the error propagates to your code.

To check which labels exist without fetching a specific version, list prompts: `GET /api/public/v2/prompts` returns every prompt with its `labels` array, and `GET /api/public/v2/prompts?label=staging` returns only prompts that have a version carrying that label. Labels are also visible on the prompt's version table in the UI.

## Operational workflows

### Rollbacks

When a prompt has a `production` label, then that version will be served by default in the SDKs. You can quickly rollback to a previous version by setting the `production` label to that previous version in the Langfuse UI.

### Prompt Diffs

The prompt version diff view shows you the changes you made to the prompt over time. This helps you understand how the prompt has evolved and what changes have been made to debug issues or understand the impact of changes.

_[Video: Compare two prompt versions](https://static.langfuse.com/docs-videos/prompt-changes.mp4): Prompts > support-reply with the latest version (#5) selected. Hover an older version in the version list and click its compare icon; the “Changes v2 → v5” dialog shows the content and config diff. Close it._

### Protected prompt labels [#protected-prompt-labels]

**Where is this feature available?**

| Plan | Availability |
| --- | --- |
| Hobby | Not Available |
| Core | Not Available |
| Pro | Teams Add-on required |
| Enterprise | Available |
| Self Hosted | Enterprise Edition |

Protected prompt labels give project admins and owners ([RBAC docs](/docs/rbac)) the ability to prevent labels from being modified or deleted, ensuring better control over prompt deployment.

Once a label such as `production` is marked as protected:

- `viewer` and `member` roles cannot modify or delete the label from prompts, preventing changes to the `production` prompt version. This also blocks the deletion of the prompt.
- `admin` and `owner` roles can still modify or delete the label, effectively changing the `production` prompt version.

Admins and owners can update a label's protection status in the project settings.

_[Video: Protect prompt labels](https://static.langfuse.com/docs-videos/250402-protected-prompt-labels.mp4): Project Settings > “Protected Labels”. Pick production in “Select or enter a label” and click “Add”, then do the same for staging. Only admins and owners can now set or remove these labels on prompts. Enterprise feature._

## Related Resources

- Prompts are scoped to a project — if you use separate projects for different environments, see [how to sync prompts between them](/faq/all/managing-different-environments)
- To compare prompt versions on a dataset before promoting a label, run [Experiments](/docs/evaluation/core-concepts#experiments).

<!-- agent-instructions -->

---

## Agent Instructions

This page is part of the [Langfuse](https://langfuse.com) documentation, published as plain Markdown for AI agents. Every page is available as Markdown by appending `.md` to its URL, or by sending an `Accept: text/markdown` header. This page: `https://langfuse.com/docs/prompt-management/features/prompt-version-control.md`.

### Querying these docs

If the answer is not on this page, query the documentation instead of guessing:

- **Semantic search** across all Langfuse docs, returning an answer with the relevant pages and excerpts. Ask a specific, self-contained question:

  ```bash
  curl -sG "https://langfuse.com/api/search-docs" --data-urlencode "query=How do I trace a LangGraph agent?"
  ```

- **Index of every page**: <https://langfuse.com/llms.txt>, with per-section indexes [llms-docs.txt](https://langfuse.com/llms-docs.txt), [llms-integrations.txt](https://langfuse.com/llms-integrations.txt), and [llms-self-hosting.txt](https://langfuse.com/llms-self-hosting.txt).

### Before writing Langfuse code

- **Install the [Langfuse Agent Skill](https://langfuse.com/docs/api-and-data-platform/features/agent-skill).** It encodes Langfuse's own best practices for instrumentation, prompt management, and evaluation, and materially improves results.
- **Read [What does a good trace look like?](https://langfuse.com/docs/observability/best-practices.md)** before instrumenting an application.
- **Verify endpoints, parameters, and response fields** against the [API reference](https://api.reference.langfuse.com) instead of inferring them from code examples.
- **Use the [Langfuse CLI](https://langfuse.com/docs/api-and-data-platform/features/cli)** (`npx @langfuse/cli api <resource> <action>`) to read or write traces, prompts, datasets, and scores from the terminal.

Found an error in these docs? Please open an issue at <https://github.com/langfuse/langfuse-docs/issues>.
