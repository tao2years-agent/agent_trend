> ## Documentation Index
> Fetch the complete documentation index at: /docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Merge Queue Optimizations

> Learn how to speed up your Graphite merge queue

The Graphite merge queue offers three optimizations that both speed up the merging process and reduce CI costs.

You can use all merge queue optimizations at the same time. The optimizations are:

1. Fast-forward merge (run CI on all PRs in a stack in parallel)

2. Parallel CI (run CI in parallel on multiple stacks simultaneously, and merge them as CI passes)

3. Batching (run CI and merge batches of stacks at a time, instead of one-by-one)

CI Optimization is available regardless of if you use the Graphite merge queue. It lets you skip running CI on mid-stack PRs when updates to other PRs in the stack trigger rebases.

Note that a "stack" can be a single PR.

![](https://mintcdn.com/graphite-58cc94ce/vY1t0Vsr-LRJgMIn/images/2a567c9f-1732219799-pika-1732219769508-1x.png?fit=max\&auto=format\&n=vY1t0Vsr-LRJgMIn\&q=85\&s=a1a97b33d8380c59ad3b4875a7b51f91)

## Running CI on multiple *PRs* in a stack in parallel (fast-forward merge)

Process CI on all PRs in a stack in parallel. We highly recommend keeping this setting enabled.

## Running CI on multiple *stacks* in parallel

For even faster merges, you can run CI on multiple stacks at the same time. Paired with fast-forward merging, this means you're processing PRs in each stack in parallel *and* processing the larger unit of stacks

Parallel CI speeds up your merge queue by running your CI checks in parallel for multiple stacks (including individual PRs not part of a stack) at once, without compromising on correctness. This is especially helpful if your repo sees a high volume of PRs, long CI times, or both.

> [!TIP]
>
> Companies who have enabled Parallel CI on their Graphite Merge Queues have seen **1.5x faster merges**, which includes time spent running CI (33% decrease for p95, 26% for p75).
>
> Orgs heavily using stacked PRs can expect to see even greater speed gains. Customers have seen up to **2.5x faster merges** (60% decrease for p95, 34% decrease for p75).

### How running CI in parallel works

Parallel CI uses speculative execution, similar to branch prediction, to run CI for multiple enqueued stacks at the same time. This significantly speeds up time-to-merge: instead of waiting for CI to run one-by-one, it can run (for example) 3 at a time. For repos with long queues, this can shorten your time-to-merge to a fraction of the time. In many cases, this brings the expected wait time down to just 1 CI cycle.

### Trading off speed vs. correctness

Graphite’s merge queue operates on stacks as the primary unit rather than a PR (where single PR’s are equivalent to a stack of size 1), and this applies to parallel CI as well. If any PR in the stack encounters a failure, the whole stack will fail to merge, allowing you to treat stack merges as atomic operations.

When setting up parallel CI mode, you can choose whether to:

* **Run CI on each PR in the stack individually**. This is the highest level of correctness guarantees: it ensures no PR in your stack would independently break trunk.

* **Run CI on the topmost PR in the stack.** This relaxes CI guarantees, while further reducing CI runs. If you require each merged stack to keep trunk green, but don’t have that same strictness for each PR within a stack, then we recommend this mode for a combination of higher speed and lower CI costs.

### Example of running CI in parallel

Suppose you’ve configured Graphite to run up to 3 parallel CI runs, and you have 5 unrelated stacks enqueued at a similar time: `A`, `B`, `C`, `D`, and `E`.

1\. CI starts for `A`. In parallel, Graphite creates these temporary groupings and starts CI at the same time:

* `A` ← `B` (i.e. `B` rebased on `A`), thereby testing this group of 2 PR’s at once

* `A` ← `B` ← `C`, thereby testing this group of 3 PR’s at once

2\. Once `A` succeeds, it’s merged.

* Graphite then starts CI for the grouping: `B` ← `C` ← `D`, thereby testing this group of 3 PR’s at once.

3\. Once `B` succeeds, the same process repeats: a group for `C` ← `D` ← `E` is created and CI runs.

4\. If at this point `C` fails, then:

* `C` is evicted from the queue.

* The runs for groups `C` ← `D` and `C` ← `D` ← `E` are both canceled.

5\. `D` then becomes the first PR in the queue:

* CI starts for `D`.

* Graphite starts CI for the grouping: `D` ← `E`.

If your CI tests aren’t flaky, the cost is low and the benefits are high: parallel execution only runs more CI when CI fails in the merge queue.

However, because parallel CI assumes that your CI tests in the merge queue will pass, be careful with flaky tests. If CI tests fail, you not only need to evict the failing PR, but restart CI runs on any subsequently enqueued PR’s with speculatively running CI. While this doesn’t make your time-to-merge any slower than when parallel CI is disabled, it does generate more CI runs.

### Enabling parallel CI

**Prerequisites**:

* You must allow the `graphite-app` bot in GitHub to bypass merge restrictions, via your existing branch protection rules or rulesets. See how to set up this up [here](/docs/set-up-merge-queue.md#bypass-pr-permissions)

* Your repo must support [draft PR's](https://github.blog/2019-02-14-introducing-draft-pull-requests/)

**To enable:** go to *Merge queue* in [your Graphite app settings page](https://app.graphite.com/settings/merge-queue), and:

1. If you haven't already, [enable the Graphite merge queue](/docs/set-up-merge-queue.md#enable-the-graphite-merge-queue-for-your-repository) in your repo

2. If you already have the merge queue enabled in the repo, find it in the list and click the **Edit** icon

3. In the merge queue configuration panel, enable **Parallel CI**

4. Select an option for **How should CI run?** - see the section above for more details.

5. Specify a **Concurrency** value, which determines the number of stacks to run CI for in parallel

> [!TIP]
>
> Not sure which concurrency value to use? You'll get the most benefit by from having enough concurrent runs to handle your PR volume given your typical CI runtimes. For example, if your CI takes 30min, and your peak hour PR volume is 3 PR's per 30min, 3 concurrent runs will give you the most benefit.
>
> If your tests are flaky, you may want to start lower and then gradually increase it as you see how your CI performs.

### End-user experience when using parallel CI

In order to implement this strategy, Graphite groups stacks into a temporary draft PR. This draft PR is used to execute CI runs. The Graphite PR page will point you to this draft PR. These PRs’ titles are always prefixed with `[Graphite MQ] Draft PR` to make them easy to identify. Once the enqueued PR finishes merging, its associated draft PR is automatically closed.

When Graphite groups stacks in the merge queue for running CI, it creates a branch with a predictable prefix: `gtmq_`. You can use this for customizing CI runs or other behavior for enqueued PR’s.

When an enqueued PR merges, it will be marked as *closed* in GitHub instead of *merged*. Graphite will render and treat it as *merged* across the product, including the PR inbox, PR page, and statistics shared by Insights. This allows you to keep the GitHub branch protection rule on to require a linear history.

![](https://mintcdn.com/graphite-58cc94ce/vY1t0Vsr-LRJgMIn/images/8278df1d-1709237882-screenshot-2024-02-29-at-3-17-49-pm.png?fit=max\&auto=format\&n=vY1t0Vsr-LRJgMIn\&q=85\&s=a27d50cbbfe83bf2a376d3ce38ad0146)

### Further reading about parallel CI

* Read more about [speculative execution](https://www.uber.com/blog/bypassing-large-diffs-in-submitqueue/) in Uber's paper

* If you use tools that monitor whether the PR is merged, your integration may stop working. Many tools have options to monitor merged commits rather than PR status: for example, see [Linear's guide on linking commits](https://linear.app/docs/github#link-using-commits).
  * Linear can also detect the `externally-merged` label if it is added before the PR is closed. This tells Linear to treat the pull request as successfully merged even though it was closed. See [Linear's documentation for custom merge queues](https://linear.app/docs/github#custom-merge-queues).

## Running CI on multiple *groups* of stacks in parallel (batching)

> [!NOTE]
>
> This feature is available in private beta. Please [contact support](https://graphite.com/contact-us) for access.

![](https://mintcdn.com/graphite-58cc94ce/vY1t0Vsr-LRJgMIn/images/2a679334-1732229774-pika-1732225950829-1x.png?fit=max\&auto=format\&n=vY1t0Vsr-LRJgMIn\&q=85\&s=2f00e34fbf5cda622c2f0b77fd07bde4)

To increase merge queue throughput and speed up merges, the Graphite merge queue also supports processing groups of stacks simultaneously.

![](https://mintcdn.com/graphite-58cc94ce/v5snjlX4njZhFyeg/images/b98850c1-1738093764-image.png?fit=max\&auto=format\&n=v5snjlX4njZhFyeg\&q=85\&s=11769854ace1d16bf954b90e2b3acf69)

When a batch merge fails, Graphite can automatically handle the failure by identifying the offending change:

**1. The system identifies which stacks in the batch caused the failure by running CI on smaller subsets of the batch**

**2. Stacks that pass CI are automatically added back to the merge queue to continue processing**

**3. Stacks that fail CI are identified and removed from the queue**

This process ensures that even if only one stack in a batch causes issues, the other stacks can still merge without manual intervention.
Two strategies are supported:

1. Full parallel isolation (default): By checking every stack in the batch in parallel, the problematic stacks are identified quickly.

2. Bisection: By using a bisection approach, problematic stacks are identified efficiently with fewer CI runs, as each iteration verifies half of the remaining stacks as safe.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.