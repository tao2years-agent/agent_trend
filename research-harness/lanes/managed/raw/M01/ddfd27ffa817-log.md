# Full Changelog

Every notable change across the Factory App, Droid CLI, and other product surfaces, newest first.

## CLI v1.16.0 · Desktop v1.16.0 (November 20, 2026)

Clickable login and MCP links, Script step titles, lower usage limits, and fixes across the CLI and app

### Improvements

- **Script step titles** - Each Script step's calls now show the step's title with a bar beside them
- **Error toast details** - Error toasts now show short guidance, and the full error goes to your bug report
- **New session default model** - A new session now starts on a model you can run instead of Auto
- **Exported metric name prefix** - Organizations can now set a name prefix for the metrics Droid exports to their collector
- **Device login link** - The login screen now shows a clickable link that carries your device code
- **Clickable MCP authorization links** - An MCP authorization link is now clickable in the MCP views and command output

### Bug fixes

- **Model change notices** - Switching the model on your own session no longer shows a model change notice
- **GitLab.com repository access** - Syncing or reconnecting GitLab.com no longer loses access to your repositories
- **Cancelled question choices** - A cancelled question now lists the choices Droid offered instead of hiding them
- **Terminal input after an editor** - Returning from a suspended editor now restores typing in the next foreground session
- **Sandbox write probe failures** - A refused sandboxed launch now names which protected entry failed its write check
- **Ctrl+C during startup** - Pressing Ctrl+C while Droid starts now restores your terminal before exiting
- **Empty reply messages** - An empty reply now says whether it was cut off or spent its output budget

### Deprecations

- **Lower five-hour and weekly limits** - Most paid plans now have lower five-hour and weekly usage limits, with monthly limits unchanged
- **Session sync setting locked** - Plans outside Enterprise can no longer turn session contents sync off, and the setting reads as locked
- **Legacy Cloud workspaces** - Legacy Cloud workspace sessions are now read-only history, without restart or download actions

## CLI v1.15.0 · Desktop v1.15.0 (November 19, 2026)

Subagent folding in the session picker, connector reconnect links, and Windows and Linux desktop fixes

### New features

- **Subagents in the session picker** - The session picker now folds Task subagent sessions under the session that started them

### Improvements

- **Neon and SonarQube Cloud connectors** - Connectors settings now shows a logo, category, and description for the Neon and SonarQube Cloud connectors

### Bug fixes

- **Connector logos in dark mode** - Connector logos now follow the row text color on dark surfaces, and Google Maps and Bitly move to new categories
- **Pull requests with slow connections** - Pull request lists now keep the results from source control connections that answered when another runs out of time
- **Background refresh error toasts** - A background refresh that fails while your data is on screen no longer shows an error toast
- **Enter during an image paste** - Pressing Enter while a pasted image path is still loading now sends the image with your message
- **Connector reconnect messages** - A connector call whose saved credentials are rejected now returns a reconnect link and the likely cause
- **Stopping a finished Script run** - Stopping a Script run that just finished now reports it as not found instead of a system error
- **Linux install script** - The Linux installer now stops and prints a working install command where the system restricts user namespaces
- **Toast rounded corners** - Toasts no longer show a square background behind their rounded corners
- **Repository folders on Windows** - On Windows, a session now opens its repository folder instead of failing when another session removes one at the same time
- **Stopping escaped child processes** - Stopping a command now also ends child processes that left its process group instead of leaving them running
- **Windows update restarts** - Restarting to update on Windows now reopens your previous windows instead of a single new window

## CLI v1.13.0 · Desktop v1.13.0 (November 17, 2026)

Add to chat for pull requests and files, smoother streamed replies, and fixes across CLI, app, and API

### New features

- **Add to chat** - Pull requests and files in a session's panels now offer Add to chat, attaching them to your next message (app)

### Improvements

- **Run-as service accounts** - The public API can now list the service accounts you may run automations as
- **Context on Droid's questions** - A question from Droid can now explain why it is asked and what the choice affects
- **Grouped web lookups** - Fetching a page now groups with web searches in one transcript row (app)
- **Notification sound defaults** - Notification sounds now default to playing only while Factory is in the background, without a doubled system sound (app)
- **Health and billing limit operations** - The public API reference now documents the health check and your organization's billing token limits
- **Account and organization operations** - The public API reference now documents reading your account and listing the organizations you belong to

### Bug fixes

- **Whole-process sandbox on macOS** - A whole-process sandbox launch on macOS no longer fails before Droid starts
- **Session sidebar edge fades** - The session list's scroll fades now blend into the translucent sidebar instead of showing a band (app)
- **Connectors during a delegation** - A connector you link while a delegation thread is running now reaches its next message
- **Truncated tool result notices** - A long tool result is now cut between whole characters and its notice sizes the text in bytes
- **Hook refusal errors** - A message a hook refuses now reports one error carrying the hook's reason instead of a model failure
- **SessionStart hooks during shutdown** - A session created while Droid is stopping no longer runs its SessionStart hooks
- **Escape sequences before emoji** - An escape sequence before an emoji no longer leaves a stray character in a tool row
- **Streamed reply pacing** - A streaming reply again flows in a few characters at a time, fading in its newest text (app)
- **Long query strings** - A public API request with more than 1,000 query parameters now reads every parameter instead of dropping the rest
- **Reconnecting a connected app** - An authorization request for an app that still reads as connected now shows a working Reconnect button (app)
- **File paths for connector tools** - A connector tool that takes file bytes now accepts a local file path, so larger files work
- **Session search results** - Command palette search now separates session titles from transcript matches, and the Sessions tab scrolls (app)
- **Following a sent message** - The transcript keeps following along after you send a message with images or long text (app)
- **Failed startup output** - A start that fails now ends on one error line and restores your terminal instead of dumping a stack
- **Continue in new session** - Continuing a stopped side chat in a new session now opens it instead of doing nothing (app)
- **Worktree cleanup on exit** - A finished run whose worktree files are still being deleted now exits cleanly and says where they are
- **Usage limit notices in delegations** - A delegation that runs out of model usage now names whose limit ran out and links usage settings

## CLI v1.12.0 · Desktop v1.12.0 (November 14, 2026)

Namespaced tool names, fewer terminal redraws, and fixes across sessions, settings, and connectors

### Improvements

- **Namespaced tool names** - Tool rows now show the namespace and capability for Droid command, connector, and MCP calls
- **Push and pull request risk** - A plain push or pull request now counts as medium risk, while force pushes stay high
- **Service account key audits** - Revoking a service account key now records an audit entry for your organization
- **Automation sessions in the sidebar** - The session sidebar now hides automation sessions until you turn that filter on

### Bug fixes

- **Organization settings after account switch** - Switching accounts no longer saves one account's organization settings under the other
- **Code spans across lines** - A code span that crosses a line break no longer joins the words around it
- **Todo list updates** - A todo list is now recorded once, in the session whose call wrote it
- **Terminal resize redraws** - Resizing the terminal no longer blanks the screen while the transcript is redrawn
- **Resumed session history** - Starting a run on a saved session id now sends its earlier conversation with the first request
- **Connector load errors** - Connectors settings now shows a load error with Retry instead of saying none are available
- **Folder trust after /cwd** - Trusting a folder from /cwd no longer clears the terminal or erases the change notice
- **New sessions after switching accounts** - Starting a session right after switching accounts now runs as the account you are signed in to
- **Artifacts from failed commands** - A failed gh or glab command whose error a pipe hides no longer records an artifact
- **Alerts in narrow panes** - Alert actions now stack under the text in narrow panes instead of squeezing it
- **Renaming a session** - Renaming a session no longer clears the terminal and replays the transcript
- **Telemetry setting coverage** - Turning telemetry off now also stops onboarding events from being sent

## CLI v1.11.0 · Desktop v1.11.0 (November 13, 2026)

Windows command sandboxing, translucent sidebar, external browser for HTML files, and fixes across sessions, hooks and Scripts

### New features

- **Open in external browser** - Right-clicking an HTML file link in chat now offers Open in external browser
- **Windows command sandbox** - Sandboxing now covers commands, hooks, and connector servers on Windows 11 hosts that support it
- **Translucent sidebar setting** - Appearance settings now offer a translucent sidebar on macOS and Windows 11

### Improvements

- **Session archiving speed** - Archiving a session no longer reads every session on your machine, so it finishes faster
- **Hook result handling** - Hook exit codes and JSON output now mean the same thing on every hook event
- **Public API reference coverage** - The public API reference now documents six more operations and the errors each can return
- **Image and PDF reads** - A Script's image or PDF read now records one line naming its type and size

### Bug fixes

- **Model region availability** - Droid now says when a model is not available in your region and asks you to pick another
- **API key creation messages** - The API Keys section now names what blocks creation only once your organization settings have loaded
- **Blank session renames** - Renaming a session to a blank title is now refused instead of leaving the session untitled
- **Script runs at session stop** - Stopping a session now reports only the Script runs still running instead of repeating one that ended
- **Source control connection errors** - A failed source control check now names the connection and host, and GitLab Cloud repository lists refresh again
- **Session titles with special characters** - A session title containing a null character now saves instead of failing
- **Task rows in transcripts** - A Task row now ends instead of staying Running when a running Task absorbs or declines your message
- **Stopping an exec run** - Interrupting an exec run now ends the turn instead of continuing after the signal
- **Archiving an open session** - Archiving a session while it opens no longer loads it, and a restored session stays visible
- **Autonomy and mode shortcuts** - Ctrl+L and Shift+Tab now do nothing while a session's settings are still loading
- **Stopping a Script with hooks** - Stopping Droid no longer leaves later file edits waiting on a notification hook from a Script
- **Organization policy on credential errors** - A credential Droid cannot read no longer drops your organization settings as if you signed out
- **Pending questions across clients** - A question Droid no longer waits on now closes everywhere instead of staying answerable
- **Background Tasks in Script** - A Script now fails when a background Task it launched was refused instead of reporting success
- **Quoting a streaming reply** - A reply that starts with a code block can now be quoted and copied while it streams
- **Model fallback notices** - A notice that your session moved to another model now appears only in that session
- **Script starts on Windows** - A Script no longer fails as already running on Windows when nothing else holds its lock
- **Hook context in long sessions** - Context from SessionStart and PostToolUse hooks now survives compaction and a hook that stops the batch

### Security

- **Upfront Script approvals** - An upfront approval no longer covers a nested command once your autonomy level or ask rules refuse it

## CLI v1.10.1 · Desktop v1.10.1 (November 13, 2026)

Organization GitHub connections work again

### Bug fixes

- **Organization GitHub connections** - You can now connect an organization's GitHub installation when you administer every repository it covers

## CLI v1.10.0 · Desktop v1.10.0 (November 12, 2026)

Disk space banner, automation schedules, smoother streaming, and fixes across sessions and models

### New features

- **Monthly weekday schedules** - A schedule can now run on a chosen weekday of the month, such as the second Monday
- **Computer disk space banner** - A computer low on disk space now names its biggest consumers and offers to reclaim space

### Improvements

- **Automation runs in sessions** - An automation run delivered into a session now shows as its own row instead of your message
- **Streaming across open sessions** - Streamed replies no longer slow the app when several sessions are open at once
- **Combined schedule phrases** - A schedule phrase that joins two times, such as every Monday and Friday at 9am, now saves

### Bug fixes

- **Missing model errors** - Droid now says a model is unavailable right away instead of retrying and showing a generic error
- **Droid notices in transcripts** - Notices Droid writes into a session no longer count as your messages in search results and titles
- **Connector rate limit retries** - Droid now waits out a connector rate limit instead of repeating the same requests until it clears
- **Tool grants in Tasks** - A custom Droid running as a Task now gets a tool you approved when it lists that tool
- **Automation update responses** - Updating an automation now answers with the record that update saved, even when another change lands at once
- **Sessions with missing folders** - Opening a session whose folder is gone now names the folder and continues once it is back
- **Readiness report upload notice** - The readiness report upload notice now states who can see a report after it is uploaded
- **Context limits in long sessions** - A session that reaches a model's context limit now compacts instead of failing
- **Task failure reporting** - A Task that failed as its process closed now reports that error instead of a bare exit
- **Model change notices** - The notice about a model change now names the model your session actually runs
- **Exec updates after exit** - Updates from an exec run now finish syncing after the process exits instead of being dropped
- **Permission requests in forks** - A forked session's permission request now stays separate from the request in the session it came from
- **Reopening a streaming session** - Reopening a session while Droid replies no longer replaces newer text with an older snapshot

## CLI v1.9.0 · Desktop v1.9.0 (November 11, 2026)

Open in Browser links, hook fixes, safer file edits, and fewer stuck sessions

### New features

- **Open in Browser menu** - Right-clicking a web link in the desktop app now offers Open in Browser, which opens your default browser

### Improvements

- **Task concurrency limits** - Running many Tasks at once no longer fails on a separate limit, and new sessions keep room to start
- **Public API reference** - The public API reference now gives every operation a stable identifier and consistent error responses

### Bug fixes

- **Hook entry validation** - One invalid hook entry no longer disables the rest of the file, and Droid reports it
- **Transcript position on resize** - The transcript keeps its place instead of sliding under the composer when the composer changes height
- **Tasks inside Script runs** - A Task no longer blocks the other calls in a Script run, and a failed run names the Tasks it stopped
- **Personal code provider connect** - A personal code provider row now explains that your organization must set up its app instead of opening setup
- **Autonomy level in hooks** - Hooks in an exec run now report the run's autonomy level and working directory from the first event
- **Sign-in errors during outages** - A sign-in service outage now returns a temporary error instead of telling you to sign in again
- **Plugin hook environment** - Plugin hooks now run with their own environment and arguments, and a plugin manifest's hooks load with it
- **Enterprise control history actors** - Enterprise control history now names every actor instead of leaving some unnamed in a large organization
- **Pending tool calls on reload** - A tool call Droid will never run now ends as interrupted instead of returning as pending on reopen
- **Approved edits and rewind** - Approved edits now match the preview you saw, and rewinding a moved file restores it instead of losing it
- **Stopping a stalled session** - Stopping a session is now answered instead of waiting behind an earlier request that never finished
- **Windows file writes** - Saving on Windows no longer fails when another Droid process releases the same file's lock
- **Sandboxed Script on Linux** - Sandboxed Script now starts on Linux hosts where its sandbox tools sit outside the default search path
- **Hooks with large inputs** - A large message no longer stops a hook from running, and one failing hook keeps the others' results
- **Slack workspace reinstall** - Reinstalling Factory in a new Slack workspace now matches your members again instead of leaving them unlinked
- **Custom Droid tool restrictions** - Editing a custom Droid now keeps its tool restriction instead of giving it every tool
- **Checkout cleanup safety** - A session's checkout is now kept when a commit lands while its cleanup runs

### Security

- **Organization owner safeguards** - Concurrent member changes can no longer leave an organization without an Owner

## CLI v1.8.0 · Desktop v1.8.0 (November 11, 2026)

Identity settings page, connector rate-limit notices, and Windows Script and exec fixes

### Improvements

- **Identity settings page** - API keys and service accounts now share one Identity page in Settings, and old links redirect

### Bug fixes

- **Model defaults autonomy levels** - The model defaults popover now offers the same autonomy levels as the composer
- **Animated image frame limit** - Animated image generation now caps at 16 frames instead of accepting more and then failing
- **Exec session machine conflicts** - Exec now refuses to take over a session another machine holds and points you to resume
- **New API key reveal** - A new API key now appears as soon as you create it, without waiting for the list
- **Blocked Git actions button** - The Git actions button no longer draws a gray box behind its icon while Droid works
- **Connector rate limit notices** - Connector settings now name the rate limit you hit instead of showing a raw error
- **Script tool on Windows** - The Script tool now runs on Windows without a separately installed Visual C++ runtime

## CLI v1.7.1 · Desktop v1.7.1 (November 10, 2026)

Stale thinking no longer fails the next message in a session

### Bug fixes

- **Thinking after context changes** - Droid now continues a session whose earlier thinking went stale instead of failing your next message

## CLI v1.7.0 · Desktop v1.7.0 (November 10, 2026)

Session sidebar performance, spec and merge commit fixes, and clearer sign-in and token messages

### Improvements

- **Session sidebar performance** - Streaming sessions no longer redraw the whole session list, keeping the sidebar responsive during busy sessions
- **Environment panel git actions** - Git actions in the environment panel now open from a menu on the Changes row
- **Offline Droid Computer retries** - An offline Droid Computer no longer retries connections in a loop that slows the session sidebar
- **Next question for typed answers** - In a set of questions, typing your own answer now shows Next question instead of only accepting Enter
- **Cloud machine deprecation notices** - Cloud Machine notices now name Environments as the replacement and link to Environments settings

### Bug fixes

- **Checks on merge commits** - Committing a merge now checks only your conflict resolutions instead of every change the merge brings in
- **GitLab token scope errors** - Saving a GitLab token that lacks a required scope now says so instead of calling it invalid
- **Sign-in walls when fetching pages** - Droid now reports a page that requires sign-in and offers the matching connector to connect
- **Approved spec after compaction** - Compacting a long session now keeps the spec you approved and the comment you left with it

## CLI v1.6.0 · Desktop v1.6.0 (November 7, 2026)

Side chat with /side, desktop telemetry and dragging fixes, and tidier settings and skills screens

### New features

- **Side chat with /side** - The /side command now opens Side Chat, matching /btw

### Improvements

- **Settings page layout** - Settings pages now space sections evenly and share one loading, empty, and error state
- **Faster worktree session archiving** - Archiving or deleting a worktree session no longer waits for its checkout files on macOS and Linux
- **Bug report export note** - The bug report modal's export note now matches the smaller body text around it
- **Session view while verifying computers** - Verifying a Droid Computer's identity no longer reloads the session view you are reading
- **Create Skill modal layout** - The Create Skill modal now leads with the description field, then examples and a short how-it-works list
- **Skills search focus** - Opening the skills browser now focuses its search field so typing filters the list
- **Custom deployment sign-in naming** - Sign-in now offers a Factory Custom Deployment instead of naming it Factory Private
- **New session startup** - Starting a new session no longer flashes Initializing Session before the session opens

### Bug fixes

- **Steered background Task answers** - A background Task now reports its final answer when you steer a message into it
- **Sidebar header window dragging** - You can again drag the desktop window by the open sidebar header
- **Telemetry setting in Desktop** - The desktop app now honors telemetry turned off in your user or organization settings
- **Sidebar text font** - The sidebar profile name and the Show more row now use the sidebar font
- **Paused computer status** - A paused Droid Computer no longer shows as running after a delayed status update

## CLI v1.5.0 · Desktop v1.5.0 (November 6, 2026)

New automation menu, older message loading fixes, connectors, and safer Environment choices

### New features

- **New automation menu** - New automation on the Automations list now offers Create from template, Create with Droid, or Create manually

### Improvements

- **Simpler custom model form** - Adding a custom model now keeps Behaves like under Advanced options instead of the main form
- **Tool rows in light mode** - Tool labels in light mode now sit back from Droid's text the way they do in dark mode

### Bug fixes

- **Saved pull request titles** - The environment panel now shows a saved pull request's own title instead of a placeholder
- **Environment choices in New Session** - New Session now offers only Environments your organization's computer policy allows, and explains a failed launch
- **Connector logos and categories** - Splunk, Elasticsearch, and Google BigQuery now show their logo, description, and category in Connectors settings
- **Older messages after compaction** - Reopening a session whose history was compacted now loads all of its older messages
- **Older messages on short sessions** - Short transcripts now load their older messages instead of leaving a button that never loads
- **Environment names on shared automations** - Automations shared by other members now name their Environment instead of showing Unknown environment

### Deprecations

- **PR Babysitter template removed** - The automation template gallery no longer offers the PR Babysitter guided setup

## CLI v1.4.0 · Desktop v1.4.0 (November 5, 2026)

Loops on Droid Computers, session resume and Windows command fixes, and clearer app panels

### New features

- **Loops on Droid Computers** - Loops now run on Droid Computers and keep their schedule across idle pauses

### Improvements

- **Environment panel popover tooltips** - Tooltips in the environment panel popover now open beside it instead of covering nearby rows
- **Empty usage table message** - The usage limit table now says No usage found when it lists no rows
- **Long session updates** - Droid now spends far less time and memory refreshing sessions with thousands of messages
- **Session tree view** - The /tree view stays readable in long sessions, and /sessions groups forked sessions together
- **Secret name entry** - A computer secret name now uppercases as you type, with a clearer placeholder and error text
- **Image preview toolbar** - Navigation, zoom, download, and close now share one floating toolbar in the image preview
- **Loading placeholders** - Loading placeholders in the session sidebar and the new computer repository list are now visible

### Bug fixes

- **Usage bar label alignment** - Bars in a usage list now share one start and length instead of shifting per row
- **Messages during environment launch** - A message sent while an environment starts now arrives even if you leave the session page
- **Icons beside long labels** - An icon next to a truncated label now keeps its size instead of shrinking to a sliver
- **Notion artifact titles** - Notion pages and databases in the environment panel now show their real titles
- **Text size inside alerts** - Text nested in an alert now matches the alert description size instead of rendering larger
- **Resuming after a task ends** - Resuming right after a delegated task finishes no longer fails with an exit error
- **Resumed session saving** - Resuming an older session now saves its messages and settings instead of silently dropping each turn
- **Exit while a session loads** - Pressing Ctrl+C while a session is still loading now stops its work before Droid exits
- **Windows command cleanup** - Commands on Windows no longer wait five seconds for cleanup on a busy machine
- **Queued messages for offline machines** - A queued message for an offline remote machine now waits instead of resending and repeating notices
- **Droid Shield on large renames** - A change with many renamed files no longer pushes Droid Shield into an extra approval
- **Stopped delegated task waits** - Droid stops waiting on a delegated task that was shut down while its approval went unanswered
- **Models added mid-session** - Picking a model your organization added after the session started no longer fails as unknown
- **Unreachable computer on follow-up** - A follow-up now reboots a computer that stays unreachable and reconnects instead of failing
- **Plugin marketplace syncing** - A plugin marketplace whose manifest starts with a byte order mark now syncs instead of failing

## CLI v1.3.0 · Desktop v1.3.0 (November 4, 2026)

Email draft cards, faster replies with many tools, and CLI connection and plugin fixes

### New features

- **Editable email draft cards** - Email drafts now render as editable cards you can copy or open in your mail app

### Improvements

- **Onboarding finish on mobile** - Phones and tablets now get a finish-on-your-computer note instead of desktop and CLI install cards
- **Instant sidebar view switching** - Moving between the sessions sidebar and Settings, Wiki, or Analytics now renders at once without a slide
- **Faster replies with many tools** - Droid starts replying sooner in sessions where hundreds of tools are available
- **Task permission inheritance** - Tasks Droid starts now inherit the run's permission skipping instead of stalling for approval
- **Model switching in long sessions** - Switching to a model from another provider is faster in sessions with long histories

### Bug fixes

- **MCP sign-in from remote sessions** - Adding an OAuth MCP server from a session on another computer now signs in through your browser
- **Local notices on remote reload** - Local notices such as clipboard warnings now stay in place when a remote session reloads
- **Computer port forward uploads** - Large uploads through a computer port forward no longer lose bytes or grow memory use
- **GitHub plugin sources** - Plugins from a GitHub source now install from that repository, and plugin errors name the cause
- **macOS startup with many skills** - Droid no longer stalls at startup on macOS with many skill files and reloads skills behind symlinks
- **Reconnect attempt limits** - Droid now stops after the configured reconnect attempts instead of retrying a failing connection forever

### Security

- **Public API identifier validation** - Requests carrying a malformed identifier now return a validation error instead of an unexpected result

## CLI v1.2.0 · Desktop v1.2.0 (November 3, 2026)

Settings search fixes, safer API key actions, screen reader labels, and sturdier desktop windows

### Improvements

- **Exec startup with many tools** - Starting a non-interactive run no longer slows down when hundreds of tools are available
- **Screen reader tab names** - Screen readers now announce tab lists by name instead of an unnamed list (app)

### Bug fixes

- **Settings search results** - Searching settings now matches row descriptions and finds rows that never appeared before (app)
- **Closing a restarting computer** - You can now dismiss the restart confirmation and close the manage computer dialog while a computer reboots (app)
- **Remote machine reconnects** - Droid now redials a remote machine whose connection died during sleep instead of failing your message
- **Organization policy load timeouts** - Droid no longer reports an organization policy timeout when the answer arrives at its deadline
- **Stopping during turn wrap-up** - Stopping Droid as a turn finishes now ends the turn instead of starting another one
- **Progress after interrupted thinking** - Droid now takes a concrete next step when a long thinking stretch is cut short
- **Wiki search accessibility** - Screen readers now name the wiki search dialog and announce the restricted access notice (app)
- **API key reveal dialog** - A newly created API key stays on screen until you deliberately close it (app)
- **API key revoke confirmation** - Revoking an API key now asks you to confirm, so a misclick cannot remove it (app)
- **Blank window recovery** - A window whose view crashes now reloads itself instead of staying blank until you relaunch (app)
- **Editor selection in VS Code** - Focusing the Droid terminal now keeps your current editor selection as the shared context

## CLI v1.1.0 · Desktop v1.1.0 (October 30, 2026)

Droid doctor install checks, session file drops, a public audit API, and onboarding fixes

### New features

- **Starter ideas without GitHub** - New session starter ideas that need no setup now appear before you connect GitHub
- **Organization audit API** - Enterprise owners can now poll organization audit events through a documented public endpoint
- **Doctor duplicate install check** - The doctor command now lists every Droid install on your PATH with its version
- **Continue in browser on Linux** - Linux and ChromeOS users can now continue to Factory in the browser after onboarding
- **Clearer session file drops** - Dragging files over a session now dims the pane and animates them into the composer

### Improvements

- **Slack reply names** - Droid now tags people in Slack only when asked and leaves names out when unsure

### Bug fixes

- **Members table narrow layout** - A member's email now folds under their name when the members table is narrow
- **Markdown checklist layout** - A Markdown checklist in a message now flows and wraps inline instead of splitting into columns
- **Onboarding payment errors** - A failed payment during onboarding now keeps your billing details and shows what went wrong

## CLI v1.0.0 · Desktop v1.0.0 (October 29, 2026)

Multi-line answers, faster turn preparation, a doctor self-launch check, and CLI and app fixes

### New features

- **Doctor self-launch check** - The doctor command now checks that Droid can start itself and warns when startup is slow

### Improvements

- **Typing during startup** - Text typed or pasted while Droid starts now edits the same way as the composer
- **Turn preparation speed** - Starting a turn is far faster when many custom models are configured
- **MCP server actions** - Disabling or removing an MCP server now shows right away instead of waiting for it to exit

### Bug fixes

- **New session defaults** - New sessions now preselect a model you can run and keep a starter suggestion as an editable draft
- **Saved session compatibility** - Saved sessions now keep their messages readable when an update adds new fields to them
- **Remote background processes** - The footer now lists background commands running on another computer and stops them there
- **Repository lookup in subfolders** - Readiness commands and built-in skills now find a repository cloned below your working folder
- **Duplicate session copies** - A session stored twice now appears in session lists from its readable copy
- **Multi-line answer editing** - Answer boxes and the /btw draft now take multi-line text and move between rows like the composer
- **Unreachable project folders** - A project folder on a disconnected drive or share no longer stalls the session list
- **Copying command output** - Copying build or command output now pastes plain text without terminal escape codes

## CLI v0.251.0 · Desktop v0.208.0 (October 27, 2026)

Faster session and composer rendering, clearer transcript grouping, wiki and enterprise fixes, and retired legacy pages

### New features

- **Marketplace plugin picker** - Admins now choose plugins from their registered marketplaces instead of typing plugin names by hand

### Improvements

- **Background session updates** - The open session no longer redraws when a background session changes its state (app)
- **Hiding sidebar items** - A hidden sidebar item now folds away instead of snapping the list shut (app)
- **Composer typing after a paste** - Typing stays responsive after you paste a long log into the composer (app)

### Bug fixes

- **Model switch notice** - A session now explains why your model changed when your plan no longer covers it (app)
- **Connector run grouping** - A long run of connector actions now stays in one transcript group instead of splitting (app)
- **Pull requests from shell scripts** - A pull request Droid opens inside a shell script now appears on its session
- **Wiki reader header actions** - The wiki reader's version, export, share, and refresh buttons now respond, and a narrow header fits (app)
- **Transcript row spacing** - A blank gap no longer opens between Droid's thinking and the tool it runs next (app)
- **Usage by Session card** - The Personal Usage page now keeps its Usage by Session card instead of dropping it
- **Self-hosted Git connections** - A self-hosted GitHub or GitLab connection no longer disconnects when two token refreshes overlap

### Deprecations

- **Legacy analytics pages** - The legacy analytics pages are retired, and their saved links open the matching page in Analytics
- **Onboarding checklist** - The post-onboarding checklist is gone, and New Session starter ideas suggest what to try next (app)

## CLI v0.250.0 · Desktop v0.207.0 (October 27, 2026)

Collapsible long messages, pull request state on sessions, Slack fixes, and CLI and app fixes

### New features

- **Long message collapsing** - A long message you sent now starts clipped behind a Show more toggle so it no longer buries the transcript (app)
- **Pull request state on sessions** - A session now shows whether its pull request is a draft, open, merged, or closed (app)

### Improvements

- **Slack channel decisions** - Droid now opens a Slack channel only for a new code change it writes and stays in the thread otherwise

### Bug fixes

- **Browser pane page size** - The browser pane now keeps its own page size instead of staying cropped by a viewport change (app)
- **Partial search results** - A search now returns the matches found past an unreadable path, and a failed search says why
- **Session list renames** - Renaming a session to an empty title now keeps it, and the session list tabs stay on one line
- **MCP settings layout** - The MCP tools, add server, and registry views now keep their section spacing and title style (app)
- **Command cleanup with worker threads** - Droid keeps stopping a command's processes when its main thread exits while other threads still run
- **Starter ideas spacing** - The installed plugin row now sits below the starter idea cards instead of flush against them (app)
- **Stopped message with images** - Stopping Droid now returns your mid-turn message with its images to the composer (app)
- **Refused safe commands** - Droid no longer refuses safe commands such as batch-mode top or a redirect to /dev/null
- **Model after compaction** - A session returns to your chosen model once compaction clears the content that forced a fallback
- **Recovery later in a run** - A long run now recovers from a refused request again instead of only the first time
- **Early Slack channel messages** - A message sent while a Slack code channel is still starting now waits instead of starting a second session
- **Duplicate Slack messages** - A Slack turn no longer opens with two near-identical messages from Droid

### Security

- **Browser panel permissions** - The browser panel now denies device access and asks before opening another app (app)
- **Folder trust on resume** - Opening a saved session from another folder now asks you to trust that folder first

## CLI v0.249.0 · Desktop v0.206.0 (October 24, 2026)

Resumable update downloads, faster session opening, plugin MCP counts, and CLI and app fixes

### Improvements

- **Session opening speed** - Opening a session is now faster on machines that hold many project folders
- **Suggestion menu responsiveness** - The slash and mention menus now respond faster as you move through their entries
- **Slack channel context notice** - Droid now says it sees only the opening message in a Slack channel it did not create

### Bug fixes

- **Spec folder in settings** - Settings now shows the folder specs save to, and a Default row keeps it unset
- **Update checks after sign-in** - Droid now checks for an update after you sign in instead of skipping it for that run
- **Startup draft slash menu** - A slash command typed while Droid starts now opens its menu without another keypress
- **Resumable update downloads** - An update download interrupted by a dropped connection now resumes instead of failing
- **Plugin MCP server count** - The startup header now counts MCP servers that come from plugins

## CLI v0.248.0 · Desktop v0.205.0 (October 23, 2026)

Faster composer and settings search, steadier reconnects, and CLI and app fixes

### New features

- **Store session titles control** - Organizations that turn session contents sync off can now allow Factory to store session titles

### Improvements

- **Session view during reconnect** - A session no longer flashes a loading message when its computer reconnects within a moment
- **Disabled auto-update message** - The update command now explains why updates are off instead of assuming an npm install
- **Settings search responsiveness** - Settings search now stays responsive while you type instead of redrawing every previewed page
- **Composer file search speed** - Typing an @ file search in the composer no longer slows the rest of the session page
- **Slash menu with many commands** - The slash menu now opens and filters quickly no matter how many commands and skills exist
- **Faster first turn** - The exec command now reaches its first turn sooner after startup

### Bug fixes

- **Session contents sync value** - The session contents sync setting now shows its saved value instead of appearing on while loading
- **MCP policy disclaimer spacing** - The MCP Server Policy note now sits clear of the allowlist field instead of flush against it
- **File tree search field** - The search field in a narrow file tree now fits its column instead of clipping
- **Sending while reported offline** - A session now connects and sends instead of refusing when the browser wrongly reports being offline
- **Session renames in cloud sync** - Renaming a session in the terminal now updates the stored name instead of only the local one
- **Attachments while a computer reconnects** - The composer now asks you to wait for the computer instead of rejecting a file as unsupported
- **New session branch picker** - The branch picker now appears only in a folder that is a repository
- **Auto after a policy change** - Choosing Auto now works right after your organization's model policy starts allowing it
- **Session start hook time** - A session now waits up to a minute for your session start hooks to finish
- **Connectors empty state wording** - The connectors empty state now tells admins they can enable connectors themselves
- **Empty session in the sidebar** - Restarting the app no longer leaves an untitled empty session in the sidebar
- **Text between grouped tools** - An answer written between two file reads now stays in the chat instead of disappearing
- **Message draft saving** - Message drafts now keep saving instead of failing silently once saved history grows large
- **Settings in symlinked folders** - Droid now reloads settings and custom Droids from symlinked folders instead of reusing the startup copy
- **Created file line counts** - A created file's summary now counts its added lines without an extra trailing line
- **Reused connection status** - A session on an already connected machine stays Ready instead of flashing a connecting state
- **Crash on tool rows** - The terminal no longer crashes when a tool call reports a path in an unexpected form

## CLI v0.247.0 · Desktop v0.204.0 (October 22, 2026)

PDF preview rendering, Environment session grouping, Files panel speed, and CLI and app fixes

### Improvements

- **PDF preview rendering** - A PDF preview now shows its first pages right away and draws the rest as you scroll
- **Files panel responsiveness** - The Files panel and file previews now stay responsive in long sessions
- **Markdown table spacing** - A table in a message now has even spacing above and below the surrounding text

### Bug fixes

- **Usage totals for retries** - Usage totals now count every billed model attempt, including ones that were retried or refused
- **Environment session grouping** - Sessions started on an Environment now appear under that Environment instead of an unregistered computer
- **Invalid API key responses** - A request with a malformed API key now returns an invalid format error instead of a server error
- **Message box after slash commands** - Submitting a slash command no longer restores earlier text in the message box
- **Ports in the address bar** - The compact address bar now keeps a local server's port instead of dropping it
- **Session defaults from chat** - Asking Droid to change session defaults no longer fails while the app's settings finish loading
- **Environment panel in tiles** - Showing the environment in one tiled chat no longer opens that panel in every tile
- **Missing session folder message** - Opening a terminal for a session whose folder is gone now names the missing folder
- **Plugin status without settings** - Plugins now show as disabled until settings load instead of appearing enabled

## CLI v0.246.0 · Desktop v0.203.0 (October 21, 2026)

Chat image gallery navigation, faster transcripts, authentication progress, browser panel safety, and CLI and app fixes

### New features

- **Chat image gallery** - Step through the images of one message in the full-screen preview with arrow keys, buttons, or dots

### Improvements

- **Session transcript rendering** - Long session transcripts now stay responsive while the session page updates
- **Credits in usage notices** - The high-cost model notice and limits modal now describe usage in credits instead of tokens
- **Planning status for actions** - Droid now shows one planning status with the number of actions instead of a row per guessed call
- **Fetching public URLs** - Droid can now read any public URL with FetchUrl instead of only URLs you supplied

### Bug fixes

- **Buy Extra Usage notice** - The Buy Extra Usage modal now asks for a payment method instead of promising to charge a card
- **Download save dialog** - Downloading a file from a remote session now opens the save dialog right away
- **Questions written as text** - Droid now asks its question when a model writes the request as plain text instead of showing markup
- **Unarchive button size** - The Unarchive button in an archived session's bar now matches the size of the other controls
- **Selector menu icons** - Icons in the project, branch, and machine selector menus now sit centered in their rows
- **Authentication progress** - A session now shows when it is authenticating instead of looking idle
- **Terminal tab title** - The terminal tab now keeps the current session's title instead of taking one from another session
- **Slack session titles** - A session started from Slack no longer shows raw mention codes in its title
- **Desktop sign-in retries** - The desktop app now retries a connection instead of reporting a failed sign-in when verification is unreachable
- **Subagents on Auto model** - A subagent left on Auto now keeps the tools its chosen model needs instead of running without them
- **Tables on narrow screens** - Tables in settings now keep their columns readable on narrow screens instead of collapsing

### Security

- **Browser panel link rules** - Links a page opens in the browser panel now follow the same rules as the address bar

## CLI v0.245.1 · Desktop v0.202.1 (October 21, 2026)

Personal GitLab Self-Hosted accounts for organization members

### New features

- **Personal GitLab Self-Hosted accounts** - Members can connect their own account on an organization's self-hosted GitLab, and managers can require it for repository access

## CLI v0.245.0 · Desktop v0.202.0 (October 20, 2026)

Chrome cookie import, folder links in the Files panel, voice dictation answers, and CLI and app fixes

### New features

- **Chrome cookie import** - The built-in browser can import your Chrome cookies on macOS, so you stay signed in to your sites
- **Folder links in chat** - Clicking a folder path in Droid's message now opens the Files panel and reveals that folder

### Improvements

- **Voice dictation answers** - Droid's questions now take a dictated answer, and the dictation level meter has a new design
- **Remote session footer** - The footer now separates a remote session's location from its branch with a dot
- **Thinking label shimmer** - The shimmer on the thinking label now lines up with the text it covers

### Bug fixes

- **MCP tools with union inputs** - An MCP tool whose input schema uses a top-level union now works instead of failing
- **Blocked request errors** - A refused request now shows a readable message instead of an empty error
- **Saved project in New Session** - New Session now shows your saved project right away instead of waiting for your computers to load
- **Resuming remote sessions** - Resuming a remote session no longer delays your messages while it loads that machine's scheduled runs
- **Reserved MCP server names** - Adding an MCP server under a reserved name now reports an error instead of saving nothing
- **Wiki repository URL matching** - The wiki commands now find a repository's wiki when its URL is written in another form
- **Plugin MCP server paths** - A plugin's MCP server now resolves its plugin folder instead of reporting an unset variable
- **Newly added GitHub repositories** - Repositories added to your GitHub connection now show up in the repository picker
- **Linux in-app updates** - Updating the desktop app on Linux now unpacks the release instead of failing
- **Stuck background commands** - Droid no longer keeps waiting on a command whose process has already exited
- **Compaction notice on reopen** - Reopening a running session no longer adds compaction notices that were never shown live
- **Composer focus after dictation** - The chat box takes focus again when dictation ends, so Enter sends your message
- **Force restart during resume** - Forcing a restart on a computer now works while that computer is still resuming
- **Background process shortcut** - Pressing down now reaches background processes once a session's Droids have finished
- **Crash with many Droids** - Resuming a session with many Droids no longer crashes the terminal interface

## CLI v0.244.0 · Desktop v0.201.0 (October 16, 2026)

Offline session archiving, session arrangement tiles, signed macOS download, and CLI and app fixes

### New features

- **Session arrangement tiles** - New sessions now open in an empty arrangement slot, and you can drag dividers to resize tiles

### Improvements

- **Welcome screen title** - The welcome screen now leads with its title instead of a decorative label above it
- **Update download progress** - Running an update now shows how much of the download has finished
- **Late connector tools** - A turn that began before your connector or MCP tools finished loading now continues once they are ready

### Bug fixes

- **Archiving offline sessions** - Archiving a session on a disconnected machine now succeeds right away, and that machine catches up when it reconnects
- **Signed macOS download** - The macOS desktop app download is now signed and served from a stable link
- **Organization-required review workflows** - A required review workflow whose rule names a branch now runs Droid instead of being refused
- **Markdown table columns** - Narrow columns in a markdown table now keep their words whole when the table shrinks
- **Plan status replies** - Droid no longer shows a plan status line in the transcript when no work is left
- **Replies after interrupted tools** - A message sent right after you interrupt a tool now gets an answer instead of another tool call
- **Spec comment box** - Starting a comment on a long spec now keeps the spec and the comment box in view

## CLI v0.243.0 · Desktop v0.200.0 (October 16, 2026)

Browser pane input, upload cancellation, large file reads, sign-in, and required review fixes

### Bug fixes

- **Machine details after reload** - A reloaded desktop window now picks up the local machine's details instead of leaving them unknown (app)
- **Browser pane keyboard input** - Droid's keystrokes now reach the browser pane they target, and fail clearly when it cannot take focus (app)
- **Multi-select custom answer** - The custom answer row in a multi-select question now shows a checkbox that checks itself once you type (app)
- **Canceling file uploads** - An attachment that is still uploading can now be canceled from the chat box (app)
- **Network failure toasts** - Returning to the app after sleep no longer repeats failed request toasts for background refreshes (app)
- **Pattern kill commands** - A kill by pattern no longer ends the command that ran it
- **Sign-in across tabs** - Opening the web app no longer signs you out when another browser tab is stuck refreshing your session
- **Reading very large files** - Droid now reads a range of a very large file without running out of memory
- **Background rm commands** - A background command that deletes a file with rm -f is no longer refused
- **Pull request in footer** - The footer now updates its pull request when the session changes folder
- **Organization-required Droid reviews** - A review workflow required across an organization now runs Droid on new pull requests
- **Subagent transcript scrolling** - The subagent transcript popup now keeps following new output as it arrives (app)

## CLI v0.242.0 · Desktop v0.199.0 (October 15, 2026)

Ask Side Chat about highlighted text, resume a session by id, and CLI and app fixes

### New features

- **Ask Side Chat about text** - Highlighting Droid's response now offers Ask side chat, which opens the side chat with the text quoted
- **Resume a session by id** - The new /resume command, and /sessions, now open a session directly when you pass its id
- **Continue a spec in chat** - An approved spec can now continue in a new chat that starts with the spec's context

### Bug fixes

- **Request timeout retries** - A request that times out is now retried instead of immediately failing your turn
- **Custom model output limits** - Requests to a custom model now stay within the output limit configured for it
- **Output after a model switch** - A turn that switches models no longer keeps the first model's unfinished reasoning or tool calls
- **Browser pane auto-open** - The desktop browser pane now opens only after Droid loads a page, and stays closed briefly after you dismiss it
- **Secret scan time limit** - Scanning a long push history now gets more time before the scan blocks the command
- **Connector logos while scrolling** - Connector logos in a tool summary no longer paint over the pinned message while you scroll
- **Deleted Slack message error** - A request started from a Slack message that was deleted now returns a clear error
- **Long responses cut short** - A response cut off mid-stream is now retried so the turn can finish
- **Duplicate usage reports** - Usage reported for your own model key is no longer recorded twice when a report is retried
- **Right pane key presses** - Pressing Enter on a right pane control no longer answers a pending question in chat
- **Automation folder icons** - A project group in the sidebar now shows the automation folder icon only when every session is an automation
- **Process kill commands** - Droid now refuses a kill command that would signal its own process

### Security

- **Excel skill dependencies** - The Excel skill now installs a pinned spreadsheet library and skips its install scripts

## CLI v0.241.0 · Desktop v0.198.0 (October 13, 2026)

Design mode comment batching, Slack follow-up guidance, plus CLI and app fixes

### New features

- **Batched design mode comments** - Design mode now queues several comments in the browser panel or file preview and sends them as one message (app)

### Improvements

- **Slack follow-up guidance** - A Slack direct message from Droid now tells you to reply in the thread to follow up

### Bug fixes

- **Windows input wrapping** - Long input on Windows now wraps after the mode label, and accented characters and emoji stay whole
- **Script startup fallback** - Droid now runs commands directly for the rest of a turn when Script fails to start
- **Context usage after compaction** - The context breakdown now measures the active conversation after a compaction instead of the whole history
- **Sidebar update badge** - The update badge now aligns with the sidebar buttons and collapses to an icon when narrow (app)
- **Cut-off model responses** - A response cut off mid-stream is now retried instead of running a tool with incomplete input
- **Command output after reload** - Tool details in a reloaded session now expand again when hooks ran during it (app)
- **Remembered New Chat picks** - The model, effort, autonomy, and mode you pick for a new chat now persist (app)
- **Duplicate Slack error** - An error about a Slack account that cannot be matched no longer appears twice

## CLI v0.240.0 · Desktop v0.197.0 (October 13, 2026)

Droid doctor checks, connector counts in the startup header, one-step onboarding checkout, plus CLI and app fixes

### New features

- **Droid doctor checks** - Droid doctor can now check model connectivity, MCP servers, and a complete turn when you opt in

### Improvements

- **Enabling Extra Usage** - The limits pane can now turn on Extra Usage in one click when you have an unused balance
- **Onboarding checkout step** - Signing up now takes the payment method and billing address in one step (app)
- **Connector count in header** - The startup header now shows how many connectors are connected
- **Credits usage chart loading** - The credits usage chart now appears before its filter options finish loading (app)

### Bug fixes

- **Remembered composer settings** - The mode and autonomy you last chose now win over organization session defaults (app)
- **Background command cleanup** - A background command now stops when the Droid process that started it exits
- **Selecting skills with Enter** - Enter now selects the highlighted skill in the menu, the same as Tab
- **Cross-region sign-in** - Signing in to an organization in another region no longer loops between regions (app)
- **Sidebar session timestamps** - Session rows in the sidebar now refresh their age as time passes (app)
- **Organization switching** - Switching organizations now keeps the organization you selected after the reload (app)
- **MCP server recovery** - Droid now sees a failed MCP server recover instead of treating it as unavailable

### Security

- **Mentioned file safety** - Text inside a file you mention with @ can no longer change Droid's instructions
- **Runtime settings isolation** - Hooks, MCP servers, and commands Droid starts no longer inherit the runtime settings file

## CLI v0.239.1 · Desktop v0.196.1 (October 12, 2026)

The desktop app keeps the organization you selected after switching

### Bug fixes

- **Organization selection persists after switching** - The desktop app now keeps the organization you selected after a switch instead of reverting to your default

## CLI v0.239.0 · Desktop v0.196.0 (October 12, 2026)

Latest model pinning, clearer Script status, and CLI and app reliability and security fixes

### New features

- **Latest model aliases** - Model flags and session defaults can now pin the newest model in a tier or version line

### Improvements

- **Script status lines** - Every Script run now ends with a status line carrying its result and wall time
- **Script progress reporting** - Checking an unfinished Script run now reports its progress instead of calling it stalled
- **Ignored exec flag warning** - Droid exec now warns which flags have no effect when you drive it with streaming input
- **Redesigned support page** - The support page now shows version, platform, and connection details with copyable diagnostic rows

### Bug fixes

- **Script observation windows** - A Script call now returns at its own wait window instead of blocking on nested work
- **Large attachments in requests** - Older images and PDFs are dropped so a turn with large attachments still goes through
- **Script runs at exit** - Droid exec now waits once for a running Script and names any run it stops
- **Request too large errors** - A request refused for its size now explains that large attachments or tool output caused it
- **Empty update version** - Droid update now rejects an empty version instead of quietly installing the latest release
- **Empty deployment section** - General settings no longer show a deployment section with nothing in it
- **Compaction after a model switch** - A session that switched models now compacts at the context limit instead of getting stuck
- **Responses with no output** - Droid now stops with guidance when a model keeps ending its response before any output
- **Failed tool calls with images** - A failed tool call that produced an image no longer makes the next request fail
- **Delegated tasks in exec** - Droid exec no longer exits while a task it delegated in the background is still working
- **Repeating output recovery** - Repeating output later in a turn is now retried instead of ending the turn
- **Staying signed in** - Droid no longer signs you out when several requests renew your session at the same time

### Security

- **Credentials in wiki commands** - Wiki commands now strip credentials from a repository URL before sending or printing it

## CLI v0.238.0 · Desktop v0.195.0 (October 10, 2026)

Chat history on scroll, a stricter telemetry opt-out, plus Script, plugin, and MCP improvements

### New features

- **Older chat messages on scroll** - Older messages now load as you scroll up instead of needing a button

### Improvements

- **Remote Control naming** - Registering your own computer for remote access is now called Remote Control
- **Running Scripts after compaction** - Droid keeps track of Scripts still running after a session compacts
- **Plugin loading at startup** - Startup no longer waits on plugin downloads, and installed plugins stay available while updates finish
- **Long Script waits** - Droid can now wait on a running Script for about an hour instead of stopping early
- **MCP server display names** - MCP servers now show their official names in settings, the tools view, and search

### Bug fixes

- **Context view for custom models** - The /context view now sizes itself from a custom model's declared context limit
- **Telemetry opt-out** - Turning telemetry off now stops every Factory-bound log, trace, and metric from the CLI
- **Pinned sessions in the sidebar** - Pinned sessions now show their details even when they fall outside your recent history
- **Files created under sudo** - Running Droid with sudo no longer leaves files in your Factory folder owned by root
- **Faster reconnect after sleep** - Remote Control reconnects a computer sooner after it sleeps instead of waiting out the full timeout

### Security

- **Editor MCP server access** - The editor MCP server now accepts only local connections and rejects browser requests

## CLI v0.237.0 · Desktop v0.194.0 (October 9, 2026)

Script approvals before running, images from Script calls, and connector tool recovery

### Improvements

- **Script approvals before running** - Script calls with fixed inputs now show their real values in the approval request before the Script runs

### Bug fixes

- **Connector tools after slow loads** - Connector tools lost to a slow first load now recover later in the same run
- **Images from Script calls** - An image produced by a tool inside a Script now shows in the transcript instead of encoded text

## CLI v0.236.0 · Desktop v0.193.0 (October 8, 2026)

Terminal activity status, Script permission requests, skills in delegated tasks, plus CLI and app fixes

### New features

- **Terminal activity status** - Terminals that support it now show whether Droid is working, waiting on you, or done

### Improvements

- **Headers in managed settings** - Organization-managed custom model settings can now carry request headers that hold no credentials
- **Faster session opening** - Opening a session no longer waits on a load that never started (app)
- **Active tool call summaries** - Tool summaries now read in present tense with counts while Droid is still working (app)
- **Resume by session link** - Droid resume now accepts a session link in place of the session id

### Bug fixes

- **Script permission requests** - Script calls whose input is built at run time now ask for permission when they run
- **Custom Droid models** - A custom Droid set to inherit now keeps the session's model and reasoning effort
- **Slash command menu flicker** - The slash command menu no longer blinks a loading row or flashes the footer
- **Sessions that pull from origin** - A first message that pulls from origin no longer leaves the session stuck on a slow fetch (app)
- **Disabled models in session defaults** - Models your organization disabled now show as unavailable in session default settings (app)
- **Session search while typing** - Session search now waits for a pause in your typing instead of piling up searches (app)
- **Wiki upload cleanup** - A wiki upload that asks for cleanup now keeps your local files unless every target succeeded
- **Skills in delegated tasks** - A task delegated with a leading skill command now starts instead of being refused
- **Startup errors in the terminal** - Startup failures such as an unknown session id or a bad folder now print in the terminal
- **Search limit validation** - Session search now rejects an invalid limit instead of silently using a different number
- **Exec input format validation** - Droid exec now rejects an unknown input format and a message passed with streaming input
- **Status pane input** - Opening the status pane no longer erases text you type right after it
- **Images on custom models** - Sending an image to a model that cannot read images now explains how to fix it
- **Custom model credential timeouts** - A credential command that times out now reports the timeout instead of waiting through another run
- **Resuming your own model sessions** - Droid exec now resumes a session on your own model credentials without a Factory sign-in
- **Dropped file paths** - A file path dropped into the composer is now sent as a message instead of an unknown command

## CLI v0.234.0 · Desktop v0.191.0 (October 6, 2026)

Legacy model upgrades, MCP tools on the first message, plus Script, plugin, and app fixes

### New features

- **Legacy model upgrades** - A session on a legacy model now runs its replacement, and you can keep the legacy model

### Improvements

- **MCP tools on first message** - Your first message can use MCP tools from your last session while servers finish connecting
- **Command summary capitalization** - Command summaries in a Droid message now start with a capital letter (app)
- **Notification volume slider** - The notification volume setting now uses the standard slider control with a percentage label (app)
- **Script wait visibility** - Pending Script waits now stay visible with elapsed time, and failed waits stay listed
- **macOS Mission Control overlay** - The overlay in macOS Mission Control now fades with a lighter tint and names the session (app)

### Bug fixes

- **Interrupted Script calls** - A Script call left unresolved by a restart is now marked interrupted when the session reopens
- **Computer repository selection** - Creating a Droid Computer now limits repository selection to the number it can clone (app)
- **Hooks that block messages** - A hook can now block the message you submit instead of letting the turn run
- **Connection retry label** - A session that loses its connection now shows a clear Retry connection action (app)
- **File links inside links** - A file path inside a link opens the file, and a modifier click opens the link (app)
- **Reopening Script sessions** - Reopening a session with Script output still pending no longer hangs
- **Droid Computer startup** - A new Droid Computer no longer fails to start before provisioning finishes (app)
- **Plugin install files** - Installing a plugin now keeps its own MCP server and custom Droid files intact
- **Editor MCP server sessions** - A session started from an editor that supplies its own MCP servers now opens
- **Dismissing new model notices** - The New notice for a model your organization disabled can now be dismissed in the model picker

## CLI v0.233.0 · Desktop v0.190.0 (October 3, 2026)

Resume with a message, Script output trimming, plus model window, custom model, and app fixes

### New features

- **Message when resuming a session** - Text after a session id in a resume command now runs in that session

### Improvements

- **Script output trimming** - Script results too long to keep in full now preserve their start and end

### Bug fixes

- **Cut-off replies now retry** - A reply that ends early on some models now retries instead of showing cut-off output
- **Connector list actions** - Actions in the connectors list no longer overlap a connector's category tag
- **Requests over the model window** - Droid now shrinks an oversized request before sending it and stops retries that cannot shrink
- **Custom model error guidance** - A broken custom model entry now explains the failure and leaves your other models working
- **Callout spacing in messages** - Callouts in a Droid message keep their padding instead of sitting against the edge
- **Resuming a paused computer** - A Droid Computer resuming after a pause no longer reports a failed sign-in
- **Malformed tool arguments** - A tool call with unreadable arguments now returns a correctable error instead of running with invented values
- **Oversized message handling** - A message larger than the model window is now refused with its size instead of silently trimmed
- **Session history after reload** - Reloading a session keeps its earliest messages above the newest page

## CLI v0.232.0 · Desktop v0.189.0 (October 2, 2026)

Legacy model warnings, session sidebar sorting, faster MCP connections, plus Windows and Slack fixes

### Improvements

- **Model discount labels** - Model pickers now state a discounted model's savings as a plain percentage off
- **Session sidebar sorting** - Sort sessions by status so ones needing input come first, and let recently active groups rise (app)
- **Legacy model warning** - Picking an older model now warns you first and offers to switch to its newer version
- **Faster MCP connections** - MCP servers you reach over HTTP now connect faster when a session starts

### Bug fixes

- **Windows command output** - Commands Droid runs on Windows no longer write stray output into the terminal interface
- **Rejected credential errors** - A turn that stops because your model credentials were rejected now reports a credential failure
- **Managed settings by region** - Droid now reads organization-managed settings from your organization's own region
- **Plugin marketplace removal** - A plugin marketplace your organization or project provides can no longer be removed by hand
- **Slack channel failures** - Droid now tells you when a Slack channel you asked for could not be created
- **Session transcript recovery** - A session whose saved history holds an unusual line separator character now loads instead of failing

## CLI v0.231.0 · Desktop v0.188.0 (October 1, 2026)

Transcript history paging, legacy models toggle, side chat shortcuts, template refresh, plus terminal and app fixes

### Improvements

- **Side chat keyboard shortcuts** - Side chat now takes multi-line messages and keeps its keys from acting on the main session (app)
- **Compression progress spinner** - A spinner now shows while a session's history compresses (app)
- **Scheduled template refresh** - Droid Computer templates now refresh on their own once they fall out of date
- **Legacy models toggle** - The model picker now groups older models under a legacy toggle and marks them clearly
- **Faster first response** - Droid now starts answering your first message sooner because setup work no longer blocks it
- **Transcript history paging** - Alt or Option with the arrow keys now pages a session's full saved history in the terminal

### Bug fixes

- **Session settings at launch** - Launching a session on a Droid Computer now keeps the model and settings you chose (app)
- **Readable model errors** - A model that cannot be served now reports it is temporarily unavailable instead of an empty error
- **Workflow task identifiers** - Droid Shield no longer flags a workflow task identifier in a commit as a secret
- **Service account session privacy** - Sessions you do not operate on a service account's computer stay out of your list and open read-only
- **Starting local sessions** - You can now start a local session without waiting for the template list to load (app)
- **Questions written as text** - A question Droid writes as raw markup now appears as a question you can answer
- **Interrupted reply handling** - A reply cut off mid-stream is now discarded instead of running unfinished tool calls
- **Resumed session failures** - A resumed session no longer fails when earlier reasoning cannot be reused
- **Self-hosted host errors** - Setting up a self-hosted GitHub or GitLab host now shows why its hostname failed to resolve
- **Session titles from Slack** - A session started from Slack no longer shows thread markup in its title
- **Slack image attachments** - Images attached in Slack no longer add a raw file listing to the conversation
- **Sidebar section width** - Expanded sidebar sections no longer run past the sidebar edge and hide project actions (app)
- **Scoped Git secret scans** - Droid Shield now checks only the content a Git command includes, so fewer clean commands are blocked
- **Custom model tool calls** - Droid no longer drops a tool call when a custom model reports several at once
- **MCP server recovery** - An MCP server that exited now restarts on the next call instead of failing
- **Dropped streamed replies** - Droid no longer drops a streamed reply or its error when the stream is compactly formatted
- **Locked settings while provisioning** - The model and autonomy controls are now disabled while a Droid Computer provisions from a template (app)

### Security

- **Private Slack channel names** - Slack channel settings no longer show private channel names to members who are not in them

## CLI v0.230.0 · Desktop v0.187.0 (September 30, 2026)

Attached images kept across turns, faster Windows startup, plus session, Slack, and API fixes

### Improvements

- **Session artifact actions** - Session records now report viewed, updated, closed, and merged pull requests and issues, not only created ones
- **Enterprise command lists** - Custom blocked commands collapse behind a count, and long command lists scroll in place
- **Faster Windows startup** - Droid starts faster on Windows by skipping a redundant console setup step

### Bug fixes

- **Startup with many sessions** - Droid no longer freezes at startup on machines that hold thousands of sessions
- **Pending questions across restarts** - A question Droid is waiting on now survives a restart, so you can still answer it
- **Session message order** - A session now lists its messages in the order they happened
- **Task reports after hooks** - A background task now reports its full result even when a hook ran during the turn
- **Faster reply after connection failure** - Droid now starts its reply immediately instead of waiting out a retry delay after a failed connection
- **Parallel tool results with images** - A turn where parallel tools return images or documents no longer fails with some models
- **Slack channel lists** - Slack channel lists now show only real channels, not the conversations behind Droid sessions
- **Images attached in earlier turns** - Sending a message no longer deletes the images you attached in earlier turns
- **File path chip size** - A file path in a Droid message now matches the height of nearby inline code
- **Image input for GLM-5.3-Flash** - An image you attach now reaches the model instead of being dropped

## CLI v0.229.0 · Desktop v0.186.0 (September 29, 2026)

Custom model management, PDF viewer, quoted replies, voice dictation key, plus terminal and app fixes

### New features

- **Custom models in terminal** - You can now add, edit, and remove your own custom models from the terminal
- **Scheduled loops indicator** - A pill above the chat input lists a session's loops and can pause, resume, or stop them (app)
- **Quote a Droid reply** - Select text in a Droid response and add it to your next message as a quote (app)
- **Voice dictation key** - Pick a single key that starts and stops voice dictation, or turn the shortcut off (app)
- **PDF viewer** - PDF files now open in a scrolling viewer with a page rail, thumbnails, and zoom (app)
- **Save files outside the workspace** - The Files panel can now save a file that lives outside your workspace folder (app)

### Improvements

- **Custom model JSON editing** - You can now edit one of your own custom models as a form or as raw JSON (app)
- **Session list edge fades** - The session list now fades at its top and bottom edges while you scroll (app)
- **Smoother file opening** - Opening a file from a tool call no longer stutters as the side pane slides in (app)
- **Faster repository lists** - Pages that list your repositories now load much faster
- **Side chat controls** - Side chat now shows its tool calls live and lets you stop or clear a question (app)
- **Idle Slack channel archiving** - Channels Droid opens for a session in Slack are archived once they sit idle
- **Migration files pill** - A Migration pill above the chat input opens the files for an active migration (app)

### Bug fixes

- **Mobile onboarding payment** - Onboarding on a phone now walks through plan selection and billing as separate steps
- **Diagram pan and zoom** - Panning an expanded diagram no longer shrinks it, and pinch and arrow keys work (app)
- **Leftover subagent processes** - Subagent runs no longer leave stray processes behind when they finish
- **Droid Shield false positives** - Droid Shield no longer blocks a commit on identifiers or secrets already in the repository
- **Failed delegation replies** - Droid now reports a failed turn in Slack and Linear instead of leaving the thread silent
- **Sidebar resize handle** - Dragging the sidebar edge near the top of the window now resizes it (app)
- **Truncated diff rendering** - A very large set of uncommitted changes now renders the files it can instead of nothing (app)
- **File preview flicker** - A file preview no longer flickers while Droid runs terminal commands in the background (app)
- **Missing GitHub App errors** - A repository without the Factory GitHub App installed now returns a clear not-installed error
- **Custom models per session** - A session now lists the custom models from your settings and from its own project
- **Setup scripts on Droid Computers** - Setup scripts now run for repositories cloned onto a Droid Computer

## CLI v0.228.1 · Desktop v0.185.1 (September 28, 2026)

Side chat context, live tool calls, and per-question stop, plus a clickable Migration pill

### Improvements

- **Side chat context and controls** - Side chat now sees in-progress work, shows tool calls live, and lets you stop one question
- **Migration pill opens files** - Clicking the active Migration pill opens that session's migration files in the Files panel

## CLI v0.228.0 · Desktop v0.185.0 (September 26, 2026)

Command palette rebuild, migrate command, mid-message skills, in-place compression, plus terminal and app fixes

### New features

- **Migration files view** - When a /migrate workflow is active, the files panel can show its plan and validation documents (app)
- **Delegation audit events** - Audit logs now record who started a Droid session from a connected tool
- **Image generation model choice** - You can now choose which model Droid uses when it generates an image
- **Expand attached images** - You can now open an attached image at full size before you send it (app)
- **Skills anywhere in a message** - You can now complete and highlight a skill anywhere in your message, not only at the start
- **Migrate workflow command** - Run /migrate to take large work from an agreed plan to a verified outcome

### Improvements

- **Slack post attribution** - Slack messages Droid posts outside your conversation now name the person who asked
- **Command palette coverage** - The command palette now reaches every page and setting, with category tabs and ranked results (app)
- **Mid-session plugin discovery** - Entering a repository during a session now loads that project's plugins
- **In-place context compression** - /compress now summarizes your current session, and /handoff starts a summary-only successor
- **Faster file suggestions** - Mentioning a file now returns suggestions faster, including in very large repositories

### Bug fixes

- **Custom model fallback** - A session set to a custom model you no longer have now falls back to an available one
- **macOS sign-in reliability** - Signing in now succeeds on macOS when the system keychain cannot be used
- **Newlines during startup** - Text with newlines typed before Droid finishes starting now stays in your draft
- **App zoom persistence** - Your zoom level now survives page changes, reloads, and new windows (app)
- **Slack file uploads** - Files you upload in a Slack channel now reach Droid instead of being dropped
- **Connection list refresh** - Disconnecting an integration now updates your connection lists right away (app)
- **Session resume memory use** - Resuming a long session no longer runs out of memory while loading its history
- **Plan kept across compaction** - Your open plan now survives context compaction instead of disappearing
- **Background task reports** - A session now stays loaded until its background task work finishes, so reports arrive
- **Windows startup stalls** - Droid no longer stalls at startup while it looks for PowerShell on Windows
- **Repository and template lists** - Repository and computer template lists no longer fail to load for some organizations
- **Queued messages on disconnect** - A queued message now stays put when another computer's connection drops
- **Shifted key combinations** - Ctrl+Shift+C inside a terminal pane no longer interrupts your session

## CLI v0.227.0 · Desktop v0.184.0 (September 25, 2026)

Model selector improvements, inline settings in chat, Droid Shield Git scanning, and transcript and compaction fixes

### Improvements

- **Settings search focus** - Opening settings now puts your cursor in the search box so you can type right away (app)
- **Light mode diff colors** - Syntax colors in light mode diffs are now dark enough to read comfortably (app)
- **Sessions awaiting your confirmation** - The sidebar now bolds sessions that are waiting for you to confirm a tool call (app)
- **New model badge** - The model selector now marks recently added models as new (app)
- **Skill activation in chat** - Chat now shows a skill activation as a muted skill row instead of an ordinary message (app)
- **Inline settings editing** - You can now review and apply more settings changes in chat instead of opening the settings page (app)
- **Diagram zoom steps** - The expanded diagram view now zooms in ten percent steps for finer control (app)
- **Tool schemas from the SDK** - The SDK can now require input schemas when listing the tools a session offers
- **Recent models in composer** - The composer model selector now lists the models you picked most recently (app)
- **Running subagent indicator** - Droid now shows an indicator in the terminal and app while your subagents keep running

### Bug fixes

- **Model choice in Spec Mode** - Your main model now stays as you chose it while Spec Mode runs with its own model
- **Context limit compaction** - Reaching the context limit now compacts your session instead of failing to summarize it
- **Droid Shield staged commits** - Droid Shield now scans what a staged commit records instead of refusing to run it
- **Leftover hook sessions** - Sessions that leftover hook entries created are now archived out of your session list
- **Transcript after compaction** - Your earlier messages now stay in the transcript after compaction and when you resume a session
- **Organization managed connector setup** - Saving an organization managed Databricks or ServiceNow app no longer fails
- **Spec Mode subagent resume** - Resuming a subagent from a Spec Mode session now keeps the mode it started with instead of switching to read-only

## CLI v0.226.1 · Desktop v0.183.1 (September 24, 2026)

Leftover hook entries no longer start a session

### Bug fixes

- **Leftover hook entries ignored** - Hook entries left by a removed capability are skipped instead of starting a session

## CLI v0.226.0 · Desktop v0.183.0 (September 23, 2026)

Voucher credits, ServiceNow connector, notification volume, draft copying, and session and chat fixes

### New features

- **Notification volume setting** - You can now set the volume of Droid's notification sounds in terminal and app settings
- **Copy draft shortcut** - Ctrl+Shift+C now copies your unsent message in the terminal and confirms the copy
- **Organization managed ServiceNow connector** - Administrators can now set up ServiceNow so members connect it with their own account
- **Voucher credit redemption** - You can now redeem a voucher for account credit and keep your current plan (app)

### Improvements

- **Background task handling** - Droid now finishes its reply while background tasks keep running instead of waiting for their reports
- **Repository picker in Changes** - Sessions with several repositories now switch repository in Changes, while Files and Terminal stay in the session folder (app)
- **Session title search** - Command-K search now finds sessions by title and ranks title matches above message matches (app)
- **Fixing Droid Shield blocks** - When you ask, Droid can now fix files Droid Shield flagged and rerun the blocked command
- **Origin sync on hover** - The origin sync menu on the new session page now opens on hover, without the branch comparison indicator (app)

### Bug fixes

- **Droid Shield command scanning** - Droid Shield now scans commits and pushes whose output is redirected instead of refusing to check them
- **Voucher credit confirmation** - Billing settings now highlights credit from a voucher you just redeemed, and voucher previews quote clearer prices (app)
- **File tree path truncation** - File paths in the file tree no longer show false truncation marks at fractional zoom levels (app)
- **Dialog keyboard handling** - Keys you press in a dialog no longer trigger page shortcuts such as changing session reasoning (app)
- **Tool call header values** - Tool call headers in chat now show list values with nested data instead of an unreadable placeholder (app)
- **Changes panel stability** - The changes view no longer goes blank or errors when you switch between sessions and branches (app)
- **Queued messages after restart** - A message you queued now arrives once after your session restarts instead of staying stuck
- **Session list machine labels** - The session list now labels each session as local or on a computer from your own connection (app)
- **Chat file path links** - Clicking a file path in chat now opens the file even when it is not indexed yet (app)
- **Sessions on their computer** - Opening a session that lives only on one computer now connects to that computer (app)

## CLI v0.225.0 · Desktop v0.182.0 (September 22, 2026)

Default app file opening, subagent controls, Droid Shield accuracy, and desktop sign-in and menu fixes

### New features

- **Open files in default app** - You can now open a session's files with your operating system's default application (app)
- **Stop a running subagent** - You can now stop a running subagent from its panel in the session transcript (app)

### Improvements

- **Droid Shield false positives** - Droid Shield now stops fewer safe Git commands and flags fewer harmless strings as secrets
- **Faster plugin marketplace installs** - Installing and updating plugins from a Git marketplace now downloads only the files those plugins need
- **Environment panel on narrow layouts** - Environment now opens in a popover when the session is too narrow for the side rail (app)
- **Streaming table columns** - Markdown tables in chat now size their columns to the content while they stream (app)
- **Connector catalog entries** - Three more connectors now show their icon and category in connector settings (app)
- **Branch menu styling** - The branch menu in environment and diff views now matches the rest of the app's menus (app)
- **Windows menu styling** - Windows title bar menus now use muted labels with hover and focus highlighting that follows your theme (app)

### Bug fixes

- **Desktop sign-in failures** - Failed desktop sign-ins now stop retrying and report back to the window you started in (app)
- **Connector settings navigation** - Opening connector settings from a session now stays in the app instead of a new browser window (app)
- **Session selection after archive** - Archiving a session no longer replaces the session you just opened with the new session screen (app)
- **Organization model policy fallback** - Starting a session with a model your organization blocks now switches to an allowed model and tells you which one
- **Desktop menu clickability** - Menus that open over the window title area now stay clickable instead of dragging the window (app)
- **Plugin MCP servers** - MCP servers that come with a plugin now load right after the plugin installs
- **Regional sign-in handoff** - Signing in now sends you to your organization's regional app instead of a manual handoff step (app)
- **MCP server list loading** - The MCP screen now waits for your session to load instead of showing an empty list
- **Session status with subagents** - The session list now shows a session as running while its subagents are still working (app)
- **Idle update restarts** - Droid now waits for your session to be idle before restarting to finish an update
- **Organization switcher layering** - The organization switcher now opens above session error messages instead of behind them (app)
- **Spec Mode for subagents** - Subagents resumed from a session in Spec Mode now stay read-only instead of regaining editing tools
- **Control tooltips in chat** - Buttons in chat, file, and specification panels show their tooltips again (app)

### Security

- **Droid Shield commit scanning** - Droid Shield now scans the exact changes a commit or push publishes before allowing it

## CLI v0.224.0 · Desktop v0.181.0 (September 21, 2026)

Computer management in sessions, onboarding plan selection, specification downloads, and CLI and chat fixes

### New features

- **Manage computer from session** - You can now check usage, update Droid, reconnect, or reboot a session's computer from the session (app)
- **Computer secrets settings** - Computer secrets settings now separate personal and organization secrets with search and role-aware controls (app)
- **Plan selection during onboarding** - Onboarding now lets you choose a plan before entering payment details (app)
- **Download specification proposals** - You can now download a specification proposal as a Markdown file from its review panel (app)

### Improvements

- **QA setup self review** - The QA setup command now reviews the files it generates before showing you the summary
- **Review action version findings** - Reviews no longer report a finding only because the review action version is pinned or older
- **Steadier session list** - The session list now stays responsive while sessions update, instead of redrawing every row (app)
- **Composer during streaming** - The composer now stays responsive while a reply streams in (app)

### Bug fixes

- **Diagram label wrapping** - Diagram labels now wrap correctly when the display is scaled, in previews, lightboxes, and exports (app)
- **Standalone browser sessions** - The browser pane now stays closed when Droid starts a browser it does not manage (app)
- **Session repository row** - Sessions on a computer with no cloned repository no longer show a repository row (app)
- **Specification review comments** - Comments you leave on a specification are now kept when you request changes (app)
- **Open sessions in VS Code** - Opening a session's files in VS Code now works in the desktop app (app)
- **Specification iteration status** - Choosing to keep iterating on a specification now shows a neutral changes requested status instead of an error (app)
- **Composer clearing on send** - The composer now clears your message and attachments as soon as you send instead of after delivery (app)
- **Sidebar menu layering** - Sidebar menus now open above page overlays and stay clickable (app)
- **Streaming inactivity timeouts** - Long responses no longer fail as inactive while data is still arriving
- **Resumed session history** - Resuming a session from the startup picker now keeps its earlier messages
- **Reasoning kept in transcript** - Chat now keeps a reply's reasoning visible when its tool runs are grouped into one row (app)
- **Markdown blockquote rendering** - Quoted blocks in Droid replies now render with continuous borders and keep their paragraph breaks
- **Voucher redemption in onboarding** - Onboarding now lets you switch between entering a card and redeeming a voucher to finish setup (app)

### Security

- **Whole process sandbox coverage** - Whole process sandbox mode now also applies to the child Droid processes a session starts

## CLI v0.223.0 · Desktop v0.180.0 (September 19, 2026)

Session forking, PyCharm, Databricks connector, streaming chat tables, and custom model credential fixes

### New features

- **Fork sessions from sidebar** - You can now fork a session from its row in the session list (app)
- **Organization managed Databricks connector** - Administrators can now set up Databricks so members connect it with their own account
- **PyCharm editor option** - You can now open a session's files in PyCharm from the editor menu (app)
- **Hook risk level setting** - Hooks that rewrite a command can now be set to keep its existing risk level

### Improvements

- **Streaming chat tables** - Markdown tables in chat now reveal complete rows as they stream instead of partial ones (app)
- **Default autonomy level** - Sessions now default to medium autonomy instead of off when you have not chosen one (app)
- **Typing during startup** - New sessions now let you type your first message while Droid finishes starting up
- **Custom model list length** - The model picker now shows eight custom models before you expand the full list
- **Custom model credential notices** - Sessions now tell you at startup when a custom model's credentials could not be resolved
- **Legacy custom model migration** - Custom models saved in the older configuration file now move into your settings at startup

### Bug fixes

- **Onboarding payment errors** - Onboarding now explains payment and promotion failures and offers a way to continue (app)
- **Custom model credential commands** - Credential commands for custom models now run once per session start instead of twice
- **Windows plugin installs** - Plugin installs and session saving on Windows no longer fail when a folder already exists
- **Browser pane auto-open** - The browser pane now opens only when Droid actually uses the browser (app)
- **Bug report progress** - Submitting a bug report now shows sending progress and errors above the form (app)
- **3D Secure payment notice** - Payment steps now state that payments requiring 3D Secure authentication are not supported (app)
- **Slack mentions in tasks** - Mentions you include when starting or following up on a Slack task are now kept

### Security

- **Disk write command safeguards** - More disk writing commands now require your confirmation before Droid runs them

## CLI v0.222.0 · Desktop v0.179.0 (September 18, 2026)

Force reboot for computers, repository panels, VSCodium, Windows MSIX packaging, and organization skill policy

### New features

- **Force reboot computers** - You can now force reboot an unresponsive computer from its actions menu, keeping persisted files (app)
- **Repository selection in panels** - Files, diffs, previews, and new terminals can now target another repository without moving Droid's working directory (app)
- **VSCodium editor option** - You can now open a session's files in VSCodium from the editor menu (app)
- **Open sessions in new tabs** - Ctrl or Command clicking a session now opens it in a new browser tab or desktop window (app)
- **Organization skill policy** - Organizations can now disable skills, and members see them marked as disabled by their organization
- **Windows MSIX installer** - Windows desktop is now available as a signed MSIX package that updates in place under device policy
- **Slack channel lookup** - Droid can now list the Slack channels it can post to when you name a channel

### Improvements

- **Windows window chrome** - The Windows app now has a compact title row, text menus, and a continuous rounded frame (app)

### Bug fixes

- **Session notification clearing** - Desktop notifications for a session now clear when you open or focus that session (app)
- **File change labels** - File changes now show consistent Create and Edit labels across approvals, failures, and subagent results
- **Read-only session controls** - Read-only session banners now keep their close control instead of hiding it (app)

### Deprecations

- **Legacy repository enrollment controls** - Repository settings no longer show the retired enrollment and review toggles (app)

## CLI v0.221.0 · Desktop v0.178.0 (September 17, 2026)

Session drafts, settings changes in chat, cleaner CLI transcripts, and clearer Slack help

### New features

- **Settings changes in chat** - Droid can now propose settings changes in chat for you to review and apply (app)
- **Session draft indicator** - Sessions holding an unsent message now show a draft mark in the session list (app)

### Improvements

- **Cleaner plan updates** - Successful plan updates no longer add rows to the transcript, and the pinned plan stays
- **Custom model capabilities** - Custom models now take reasoning and image support from the base model you select
- **Slack help guide** - Sending !help in Slack now lists each command and explains which identity a session runs as

### Bug fixes

- **MCP tool readiness** - Exec sessions that wait for MCP servers now also wait for their tools to register
- **Session filter menu height** - Long project lists in session filter menus now scroll inside a capped menu (app)
- **Thinking output alignment** - Thinking labels and text now line up with tool names and render in italics
- **Command blocklist matching** - Blocked command patterns now match package runner commands that pin a package version
- **Task result recovery** - A Task that already finished now reports its result instead of a timeout
- **Session type filter** - The session Type filter now stays open while you select several options (app)
- **Pinned message handoff** - A newer message now layers above the pinned message instead of overlapping it while scrolling (app)
- **Oversized request recovery** - Requests rejected for being too large now compact and retry instead of failing the turn

## CLI v0.220.0 · Desktop v0.177.0 (September 16, 2026)

Slack connect command, connector refresh, wrapping chat tables, and promotion verification retry

### New features

- **Slack connect command** - Sending !connect in Slack now replies with instructions to connect to that session's computer

### Improvements

- **Image and PDF limits** - Sessions that pass the image or PDF limit now stay faster as you add more attachments
- **Model picker labels** - Droid Core models no longer repeat the label in each name, keeping it in the section heading
- **Wrapping chat tables** - Wide markdown tables now wrap to fit the message column before falling back to scrolling
- **Connector refresh status** - The connectors view now shows the last refresh time and refreshes on demand with R
- **Connector loading tooltip** - The composer tool button now says connectors are loading instead of referring to MCP

### Bug fixes

- **Promotion code verification** - Onboarding now offers a retry when a promotion code cannot be verified, or continues without it
- **Template launches across windows** - Starting a session from a template now creates one computer instead of one per open window
- **Messages during reconnects** - Approval and question messages now stay visible when a session's connection is replaced
- **Azure AI Services credentials** - Custom Azure credentials now accept AI Services endpoints alongside Azure OpenAI ones
- **Inline diff comment threads** - Opening and closing an inline diff comment now settles immediately instead of animating

## CLI v0.219.0 · Desktop v0.176.0 (September 15, 2026)

Hidden files, sidebar settings shortcut, expandable panes, Slack follow-ups, and steadier subagent progress

### New features

- **Sidebar settings shortcut** - The sidebar profile row now has a settings button that opens general settings (app)
- **Local session policy** - Organizations can now stop members from starting Local desktop sessions and require remote targets
- **Hidden files in Files panel** - The Files panel now lists dot-prefixed entries and lets you toggle their visibility (app)

### Improvements

- **Grouped organization settings** - Organization session defaults are now grouped into separate searchable sections in settings
- **Expandable session panes** - Files, diffs, and browser panes now expand to full width from the session toolbar (app)
- **Integration connection errors** - A failed connection attempt now returns to settings with the reason and where to fix it (app)
- **Slack participant mentions** - Droid can now mention the right people by handle when replying in a Slack thread
- **Task parent session IDs** - The sessions API now reports the parent session that launched each subagent session

### Bug fixes

- **Voice dictation composer** - The composer hides the recording waveform when dictation is off and keeps your draft (app)
- **Connector tool updates** - Connector tool changes now apply on the next turn after you leave tool settings
- **Pinned messages on mobile** - Chat on narrow mobile screens no longer overlays the pinned message on the transcript
- **Copy session link** - Copying a session link now gives its hosted address, and local-only sessions hide the action (app)
- **Image-heavy session compaction** - Compaction now counts image size, so sessions with many screenshots stay within request limits
- **Mode selector hover hint** - Hovering the mode selector now shows its mode and shortcut instead of a generic hint (app)
- **Resumed session titles** - Resuming a heavily compacted session keeps its title and skips repeated first-turn context
- **Slack follow-up replies** - Follow-ups sent while Droid is finishing a reply in Slack now get answered
- **Organization picker sizing** - The settings organization picker fits the selected organization and truncates only on narrow screens (app)
- **Exec authentication errors** - Non-interactive runs now report the real authentication failure instead of an unrelated final message
- **API key validation errors** - Droid now says when your API key could not be validated because Factory was unreachable
- **Computer resume reliability** - Paused computers now come back reliably when a fast resume is unavailable
- **Integration disconnect guidance** - Disconnect confirmations now say where to uninstall Factory for each connected workspace (app)
- **Unmatched account guidance** - When Droid cannot match your chat account, it now asks you to align your account email
- **Uploaded file previews** - Files uploaded to a computer now stay visible as previews in the composer (app)
- **Live subagent progress** - Subagent activity keeps updating after a reconnect instead of appearing already finished (app)
- **Bug report progress** - The bug report dialog now shows progress while your report is submitted (app)
- **Template session labels** - Session headers now show the template name that created the session, matching the sidebar (app)

### Security

- **Workspace connection conflicts** - Connecting an integration workspace that another organization already holds is now rejected

## CLI v0.218.0 · Desktop v0.175.0 (September 11, 2026)

Faster CLI startup, a role setting, delegation help, session resume, and chat fixes

### New features

- **Work role preference** - You can now see and change the work role you picked during onboarding in settings (app)
- **Delegation help command** - Sending !help in a connected Slack or Linear thread now replies with usage guidance

### Improvements

- **Faster first response** - Droid now starts your first reply without waiting on usage limit checks to finish

### Bug fixes

- **File citation line ranges** - File citations written with an en dash between line numbers are now clickable in chat (app)
- **Large session resume** - Large sessions now resume with their latest messages and page back through older history (app)
- **Find in focused panel** - Pressing find in a diff or file view now searches that panel instead of the transcript (app)
- **Startup theme detection** - Terminal theme detection no longer waits for settings to load, so startup finishes sooner

## CLI v0.217.0 · Desktop v0.174.0 (September 11, 2026)

Browser shortcuts, smoother command animations, cleaner retries, and clearer organization controls

### Improvements

- **Smoother command animations** - Long-running commands now keep a steady animation speed instead of visibly slowing down

### Bug fixes

- **Large request retries** - Oversized requests now recover without repeating the same connection failure
- **Startup input handling** - Terminal detection no longer leaves stray characters in the input field when Droid starts
- **MCP allowlist autocomplete** - Selecting an MCP server suggestion now adds an allowlist entry that permits the selected server (app)
- **Retried response cleanup** - Droid now removes unfinished response text and tool call displays before retrying an interrupted reply
- **Model policy name matching** - Allowed models no longer fail organization policy checks when saved under an earlier name
- **Browser tab shortcuts** - Browser tab shortcuts no longer switch Factory sessions, while numbered session shortcuts remain available in Desktop

## CLI v0.216.0 · Desktop v0.173.0 (September 9, 2026)

Managed computers on Pro, faster connector connection status, MCP allowlist wildcards, and steadier Gemini streams

### New features

- **Managed computers on Pro** - The Pro plan now includes managed computers with five compute hours each month

### Improvements

- **MCP allowlist wildcards** - Organization MCP server allowlists now accept hostname wildcards, so one entry can cover many hosts
- **Connector connection updates** - Connectors now show as connected right after you finish authorizing, instead of after a delay (app)
- **Generated image previews** - Generated images now show a loading frame, then reveal the image with open and download actions (app)

### Bug fixes

- **Gemini stream recovery** - Gemini responses that fail mid-stream now retry instead of ending with missing content
- **Model selector shortcut** - The keyboard shortcuts list now shows Ctrl+N for the model selector on every platform (app)
- **Pending session launches** - New sessions now finish starting instead of being dropped mid-launch (app)
- **Onboarding subscription button** - The onboarding payment step now labels its button Start subscription and matches the charge notice (app)
- **Droid wordmark rendering** - The Droid wordmark on the new session screen now renders cleanly without visible seams (app)

## CLI v0.215.1 · Desktop v0.172.1 (September 9, 2026)

Wildcard hostname patterns for organization MCP allowlists

### New features

- **Wildcard MCP allowlist entries** - Organization MCP allowlists now accept wildcard hostname patterns like *.example.com to approve many remote server hostnames at once

## CLI v0.215.0 · Desktop v0.172.0 (September 8, 2026)

Streaming terminal responses, organization Web Search control, unified connector settings, and steadier sessions

### New features

- **Stream responses as they arrive** - A new terminal setting renders Droid's replies and thinking progressively instead of waiting for each block to finish
- **Web Search control** - Organization managers can now remove the Web Search tool so Droid cannot search the public web

### Improvements

- **Payment during onboarding** - Paid signup now collects card or bank payment details directly in the onboarding flow (app)
- **Composer mode descriptions** - The composer mode menu now explains what each mode does (app)
- **Consistent panel animations** - The file tree and right panel now open and close with the session sidebar's timing (app)
- **Model access exceptions** - Managers can now block individual models while new ones stay available under Allow All
- **Unified connector settings** - Connectors and integrations now share one settings table, with organization availability moved under Enterprise Controls (app)
- **Session Wiki navigation** - The session Wiki action now opens the full Wiki page instead of an inline panel (app)

### Bug fixes

- **Scrollbar and notification behavior** - Interrupted scrollbar drags no longer clear text selection, and new notifications no longer inherit an earlier timer (app)
- **Bring your own key errors** - Retry failures with your own model key can now show the provider's status code and message
- **Network error details** - Network errors now name the host, protocol, and port that actually failed
- **Usage limit resets** - The first message after your usage limit resets is no longer treated as over the limit
- **Session titles under model policy** - Sessions in organizations that restrict models now get generated titles instead of failing
- **Expanded browser panel toolbar** - The expanded browser toolbar now clears the macOS window controls and keeps its sidebar button (app)
- **Live command output** - Running commands can now be expanded to watch their output before the result arrives (app)
- **Factory name on macOS** - Desktop now shows the Factory name in macOS system UI instead of its executable name (app)
- **Computers stay active while typing** - A cloud computer no longer pauses while you type in its session or reconnect to it (app)
- **Local MCP server sign-in** - Desktop now completes MCP server sign-in on your own machine for local sessions (app)
- **Continued model discounts** - A discounted model rate now continues when a shorter promotion on the same model expires
- **Fewer false secret warnings** - Droid Shield no longer warns about public service identifiers that are safe to commit

## CLI v0.213.0 · Desktop v0.170.0 (September 5, 2026)

LaTeX rendering, settings search, reliable keyboard input, and clearer connector controls

### New features

- **LaTeX math in chat** - Chat messages now render supported LaTeX math expressions instead of displaying their markup (app)
- **Settings search** - Search settings by name from the sidebar to find matching pages and controls (app)

### Improvements

- **Service account connector warning** - Connecting a service account connector now shows a shared-access warning before you continue (app)
- **Status command details** - The /status command now shows your user ID and connection details for troubleshooting
- **Organization connector controls** - Organization managers can now control connector availability from the Connectors settings page (app)

### Bug fixes

- **Mermaid diagram labels** - Mermaid diagrams now improve label contrast on custom node backgrounds (app)
- **Git commit authorship** - Droid now uses your configured Git identity when creating commits
- **Lossless keyboard input** - Fast typing and pastes now preserve characters across input updates
- **Named worktree branches** - Passing an existing branch name to --worktree now checks out that branch instead of creating a copy
- **Thinking block duration** - Thinking durations now stop updating when Droid starts replying or running tools
- **MCP server status** - MCP servers blocked by your organization now show as disabled instead of appearing to connect
- **Auto Model after compaction** - Auto Model now reevaluates its model choice after conversation compaction

## CLI v0.212.0 · Desktop v0.169.0 (September 4, 2026)

Faster startup, simpler tool selection, steadier responses, and clearer app views

### New features

- **Exec tool selection** - Select tools with --only-tools, --add-tools, and --remove-tools, including individual MCP tools or entire servers

### Improvements

- **Faster terminal startup** - The CLI now overlaps startup work with settings loading so you can begin typing sooner
- **Expanded table viewing** - Expanded tables now use more of the window while keeping their scrollbars visible (app)
- **Quiet command efficiency** - Long-running commands with little output now use less CPU while running in the CLI
- **Environment panel default** - The environment panel now opens by default unless you previously chose to close it (app)
- **Consistent monospace text** - Monospace text now uses Geist Mono (app)

### Bug fixes

- **Follow-up message handling** - Droid now carries earlier instructions forward when several follow-up messages arrive while it is working
- **Droid logo display** - The Droid logo no longer shows unwanted scrollbars (app)
- **Desktop download links** - Selecting a Desktop download now opens the installer link correctly (app)
- **Stalled response recovery** - Improved recovery when a response stops arriving midstream
- **Empty session directory changes** - Changing directories with /cwd before your first message no longer leaves the session unable to reload
- **VS Code diff fallback** - The CLI now stays open and keeps the inline diff visible when the VS Code command is unavailable
- **Large local file attachments** - Oversized or unsupported files can now be attached by reference in local Desktop sessions (app)
- **Background task display** - Background tasks no longer cause duplicated status lines or overwritten rows in long terminal conversations
- **Empty response recovery** - Droid now retries more transient empty responses before ending the turn with an error
- **Custom model recovery** - Custom models can now recover from an initial setup failure when you send a message

### Deprecations

- **Worktree directory option** - --worktree-dir now shows a deprecation warning directing you to the worktree directory setting

## CLI v0.211.0 · Desktop v0.168.0 (September 2, 2026)

A recent-session picker, scrollable side answers, session recovery fixes, and preserved answer drafts

### New features

- **Recent session picker** - Use --resume to choose a recent session, or add --last to reopen the latest session in the current folder

### Improvements

- **Web access after signup** - Paid accounts now have a Continue on web link after completing signup (app)
- **Mission input indicators** - Started missions now show an amber status and a sidebar indicator when they need your response (app)
- **Rename while sharing** - Rename your session directly from the sharing dialog (app)
- **Update status notices** - Update completion and error notices now appear even with drafted text, and dismiss when you edit it
- **Droid Shield setting descriptions** - The Droid Shield setting now shows its description inline instead of in a tooltip (app)

### Bug fixes

- **Task session recovery** - Task sessions now resume after permission timeouts without a temporary reload error (app)
- **Session tile drops** - Dragging external text or links into Desktop no longer creates an invalid session tile (app)
- **Interrupted session loading** - Returning to a session now recovers loading interrupted by navigation instead of leaving the session stuck (app)
- **Usage statistics heading** - The /stats view now uses a year-neutral heading instead of outdated annual recap text
- **Task approval status** - Tasks waiting for your approval now show Waiting for confirmation instead of appearing complete (app)
- **Repeated response recovery** - Droid now retries once when a response gets stuck repeating itself
- **Airgapped security reviews** - Deep security reviews now support airgapped environments using your configured custom model
- **Unsent answer drafts** - Answers to Droid questions now survive switching sessions, including typed text and selected options (app)
- **Hook command rewrites** - Commands changed by hooks now run as edited, and their displayed details match
- **Session reconnection before sending** - Sending a message now attempts to reconnect disconnected sessions before submission (app)
- **Grouped exploration activity** - Consecutive file browsing and search activity now stays grouped across longer transcript sections (app)
- **/btw answer scrolling** - Scroll long /btw answers with Alt or Option and Up or Down while keeping the question input visible

## CLI v0.210.0 · Desktop v0.167.0 (September 2, 2026)

Clearer questions, steadier menus, readable diagnostics, reliable mission resumes, and cleaner app sessions

### Improvements

- **Numbered question options** - Questions now show number shortcuts beside the first nine answer options
- **You.com server icon** - You.com tool results now display the service’s icon instead of a generic icon (app)
- **Clickable file references** - Droid now formats workspace file references as clickable paths in chat (app)
- **Configuration diagnostics** - The doctor command now includes configuration checks and lets you run them separately with --config

### Bug fixes

- **Mission session ordering** - Mission sessions now follow their numbered order instead of placing validation sessions first (app)
- **Menu scroll stability** - Model and MCP menus no longer jump when you move between search and the results list
- **File editor alignment** - The file editor now keeps the cursor aligned with the text you are editing (app)
- **HTML file attachments** - You can now attach HTML files to chat, including when starting a session (app)
- **Empty session visibility** - Empty sessions now stay hidden from the sidebar unless selected or still running (app)
- **Diagnostic text wrapping** - Long paths and error messages now wrap to fit the diagnostics panel
- **Mission resume recovery** - Paused missions now resume the current session rather than an outdated one
- **Custom model retries** - Custom model requests now retry temporary capacity errors for longer before stopping
- **Accurate edit counts** - Edit results now keep their full added and removed line counts when previews are shortened
- **Built-in tool responsiveness** - Built-in tools no longer wait for an unresponsive MCP server before running
- **Interrupted message drafts** - Interrupting a session no longer inserts unrelated system notices into your input field (app)

## CLI v0.209.0 · Desktop v0.166.0 (September 1, 2026)

Session archiving from chat, a new default model, faster startup, and steadier app views

### New features

- **Archive sessions from chat** - Archive the current session with /archive or Ctrl+X, and restore sessions from the Archived tab

### Improvements

- **New default model** - Sessions with no model selected now default to GPT-5.6 Sol
- **Faster startup with organization settings** - The CLI now starts on time when organization settings load slowly, applying them once they arrive

### Bug fixes

- **Diff text selection** - Text selected in a diff no longer clears when the session sidebar updates (app)
- **Environment panel visibility** - The environment panel now stays visible while repository details load or refresh (app)
- **File link line targets** - Opening a file link now centers the target line in the file view (app)
- **Droid Core model suggestion** - Running out of credits now suggests an available Droid Core model instead of a retired one

## CLI v0.208.1 · Desktop v0.165.1 (August 29, 2026)

60% off GPT and Grok models

### Improvements

- **GPT and Grok discount** - GPT and Grok models now bill at 60% off for a limited time, with the discount shown in the model selector

## CLI v0.208.0 · Desktop v0.165.0 (August 29, 2026)

Sharper image reading, resilient MCP servers, faster slash commands, Windows hook fixes, and verified domain invitations

### New features

- **Verified domain invitations** - Organization owners can now require people on verified email domains to join by invitation instead of creating a new organization

### Improvements

- **Sharper image reading** - Screenshots, diagrams, and tables now keep fine detail when Droid resizes images
- **New session progress** - The /new and /clear commands now show progress while your next session is created
- **You.com MCP server** - You.com is now available in the MCP server registry for web search and research
- **Faster slash commands** - Built-in slash commands now run immediately instead of waiting for command discovery to finish

### Bug fixes

- **Mission milestone validation** - Mission milestones now run their validation steps even after a session is interrupted, paused, or resumed
- **Windows plugin hooks** - Plugin hooks now run on Windows when their command path contains spaces
- **Unresponsive MCP servers** - Unresponsive MCP servers no longer stall the CLI, and a notice names the server that failed
- **Airgapped session warnings** - Airgapped sessions no longer log blocked connection warnings, and /bug explains it cannot send reports
- **Exit command** - Typing /exit now quits the CLI instead of running a different suggested command
- **Local session loading** - Opening a local session from the sidebar now shows a loading state while its details load (app)
- **Desktop integration sign-in** - Connecting an integration from Desktop now uses the organization you selected (app)

## CLI v0.206.0 · Desktop v0.163.0 (August 28, 2026)

Faster CLI startup, reliable session controls, project guidance across repositories, and resilient commands

### Improvements

- **Cross-repository guidance** - Droid now applies project guidance when searching or listing files outside the current repository
- **Faster CLI startup** - The CLI now accepts input sooner by postponing work until it is needed

### Bug fixes

- **Session reconnections** - Long-running sessions now continue cleanly when Droid needs to reconnect
- **Responsive session controls** - Session archiving, renaming, and selection no longer hang when favorites fail to refresh
- **First message cancellation** - You can now cancel your first message immediately after sending it
- **Custom model context limits** - Droid now recognizes more custom model context limit errors and recovers normally
- **Sleeping laptop commands** - Running commands no longer time out solely because your laptop went to sleep
- **Connected tool cancellation** - Interrupting a turn now cancels active connected tool calls instead of leaving the session stuck

## CLI v0.205.0 · Desktop v0.162.0 (August 26, 2026)

Account switching, unread sessions, smoother updates, and clearer file handling

### New features

- **Mark sessions unread** - You can now mark a session as unread from its sidebar menu for later review (app)

### Improvements

- **Smoother background updates** - Background updates now keep the CLI responsive while you type

### Bug fixes

- **VS Code windows** - Opening a project in VS Code now creates a new window and handles folder paths correctly (app)
- **Smoother account switching** - Switching organizations now starts a fresh session, while logout returns directly to the login screen
- **Local session creation** - Local sessions can now start without waiting for organization defaults to load (app)
- **Pending session requests** - Pending questions and approvals now remain available when a session reconnects (app)
- **Clearer file failures** - Failed file changes now display a clear error state without misleading diff details (app)

## CLI v0.204.0 · Desktop v0.161.0 (August 25, 2026)

Droid diagnostics, quicker one-shot commands, reliable MCP connections, steadier session resumes, and clean response completion

### New features

- **Droid diagnostics** - Use Droid doctor to diagnose connectivity and local setup issues with focused or JSON output

### Improvements

- **Quicker one-shot commands** - One-shot commands now start without waiting for unrelated connections unless the command needs them

### Bug fixes

- **MCP connections** - MCP connections now work reliably across the CLI and app without repeatedly asking you to reconnect
- **Resumed session state** - Resuming a session now restores pending questions and approvals without stale working states or duplicate replay
- **Completed responses** - Responses now finish cleanly instead of hanging after Droid has completed its answer

## CLI v0.203.0 · Desktop v0.160.0 (August 25, 2026)

Queued messages are now editable, skill commands work after other text, and session switching, voice dictation, and large attachments are steadier

### New features

- **Edit queued messages** - You can now move a queued or pending steering message back into the composer to change its text or attachments before it is sent (app)

### Improvements

- **Retention change warnings** - Turning on or shortening session retention now warns you that existing sessions past the limit are permanently deleted before you save

### Bug fixes

- **Inline skill commands** - You can now start a skill command after other text in your request, and text that begins with an unmatched slash submits normally instead of being blocked
- **Session switching** - Switching between sessions no longer flashes, drops focus in the composer, or scrolls the page unexpectedly (app)
- **Session reload on focus** - A session now reloads when you focus the window again, so it recovers after the app has been minimized (app)
- **Voice dictation at usage limits** - Voice dictation now stops cleanly when you reach a usage limit instead of continuing to record audio it cannot transcribe (app)
- **Large document attachments** - Attaching a very large spreadsheet or document no longer stalls the session on every turn (app)

## CLI v0.202.0 · Desktop v0.159.0 (August 21, 2026)

The CLI starts faster, admins can turn image generation off, and a batch of app fixes land for sessions, billing, and markdown tables

### New features

- **Image generation control** - Org admins can now turn off image generation for everyone in the organization
- **Voucher redemption** - You can now redeem a voucher from your billing settings, including on an annual plan (app)

### Improvements

- **Faster CLI startup** - The CLI now starts up faster
- **Markdown table rendering** - Markdown tables in a session now render more clearly (app)
- **Message actions on hover** - The actions for a message now appear when you hover over it (app)
- **Generated document downloads** - Documents Droid generates now finish as files you can download (app)
- **Apply changes tooltip** - A tooltip now explains why Apply changes is unavailable (app)

### Bug fixes

- **Lifecycle hooks** - Lifecycle hooks now run again instead of being skipped
- **Local plugin caches** - A damaged local plugin cache now repairs itself instead of leaving your plugins unavailable
- **Chinese translations** - Simplified Chinese text in the interface is now translated correctly
- **Unarchived sessions** - Your sessions now load right after you unarchive one (app)
- **Session state across pages** - Your open session is kept when you move to another page in the app and come back (app)
- **Overage preference updates** - Your overage preference now shows the new setting right after you change it (app)
- **Self-hosted Git connections** - You can again start a self-hosted Git provider connection from Source Control settings (app)
- **Stray startup notification** - The app no longer shows a startup notification when it connects to your local machine (app)
- **Complete org member list** - The org members list now shows every member of your organization

## CLI v0.200.0 · Desktop v0.157.0 (August 20, 2026)

Background processes report real process IDs, MCP connections stay authenticated across reconnects, and the model list is searchable in the app

### Improvements

- **Failed pull confirmation** - When a Git pull fails, Droid now asks before changing your working tree to fix it instead of doing so on its own
- **Faster session startup** - File search tooling now loads only when it is needed, so a session is ready to use sooner
- **Model list search** - The model list now has a search box, so you can find a model without scrolling through the whole list (app)

### Bug fixes

- **Background process IDs** - Starting a command in the background now reports its real process ID, so you can check on it or stop it
- **MCP server reauthentication** - Connections to MCP servers now stay authenticated instead of asking you to sign in again on the next reconnect
- **Inherited subagent reasoning** - A subagent can now inherit the session's reasoning setting instead of being forced onto a fixed one (app)

## CLI v0.199.0 · Desktop v0.156.0 (August 18, 2026)

The explorer droid can use every read-only tool, agent questions are easier to answer from the keyboard, and diagrams and long sessions render better in the app

### New features

- **SDK custom system prompts** - The TypeScript SDK can now set a custom system prompt for a session, and it is kept when the session resumes
- **Managed BYOK model defaults** - Org admins can now pick BYOK custom models as managed defaults for sessions and subagents in Enterprise Controls
- **Service account model policies** - Service accounts now appear in Enterprise Controls model policies, so admins can set which models each one may use

### Improvements

- **Explorer tool access** - The built-in explorer droid can now use every read-only tool, including command execution, web search, and MCP tools, while file edits stay blocked
- **Question prompt keyboard controls** - You can now pick answers with Space or the number keys, move between questions with Tab, and go back to edit an answer you already gave
- **Mermaid diagram rendering** - Diagrams in a session now render with the official Mermaid engine, so more diagram types display correctly (app)
- **Faster session rendering** - Long sessions and streaming command output now render with less lag, so scrolling and typing stay responsive while the agent runs (app)
- **Mission model settings** - You can now choose the models and reasoning defaults a mission uses from its settings (app)

### Bug fixes

- **Agent question context** - The context the agent includes with a question now stays visible while you answer it

## CLI v0.198.0 · Desktop v0.155.0 (August 17, 2026)

Diff lines wrap by default, plus fixes for diff search, the model selector, empty sessions, and mission models

### Improvements

- **Diff line wrapping** - Long lines in a diff now wrap by default so you can read them without scrolling sideways (app)
- **Clearer empty response error** - When a model finishes without producing an answer, the message now explains why and suggests retrying or switching models

### Bug fixes

- **Diff search navigation** - Stepping to the next or previous diff search match now scrolls to it instead of stopping when the match is still loading (app)
- **Model selector search** - The model selector keeps focus in its search box so your typing is no longer lost while filtering models (app)
- **Chat activity while thinking** - The chat keeps showing the running tool while the agent is thinking instead of clearing it (app)
- **Empty draft sessions** - Sessions that were opened but never used no longer pile up in your session list and resume picker
- **Missions after sleep** - A mission now moves a stuck worker onto a fresh one after your machine sleeps instead of hanging
- **Mission model defaults** - A mission now starts with the mission models from your defaults, and every connected client shows the models the run is actually using

## CLI v0.197.0 · Desktop v0.154.0 (August 15, 2026)

More accurate voice dictation and steadier option navigation in prompts

### Improvements

- **Voice dictation accuracy** - Voice dictation now transcribes what you say more accurately (app)

### Bug fixes

- **Prompt option navigation** - Moving through the options in a question or permission prompt no longer jumps to whichever option the mouse is resting on (app)

## CLI v0.196.0 · Desktop v0.153.0 (August 14, 2026)

Forking now keeps you in your current session and credit usage moves to its own page, plus fixes for the pull request indicator, SessionStart hook context, and credit rates for two models

### Improvements

- **Fork stays in place** - Forking a session now keeps you in the original session and prints a resume command you can use to open the copy
- **Credit usage page** - Credit usage now has its own page instead of living inside Analytics (app)

### Bug fixes

- **Pull request indicator** - The linked pull request indicator stays visible when a status lookup briefly fails instead of disappearing
- **SessionStart hook context** - Context added by a SessionStart hook is kept for the session instead of being dropped
- **Model credit rates** - Credit usage for Grok 4.5 and GPT-5.3-Codex fast mode is now reported at the correct rate

## CLI v0.195.0 · Desktop v0.152.0 (August 13, 2026)

Escape now confirms before interrupting a run, plus fixes for sidebar width, text selection after resizing, recent sessions in the sidebar, repeated polling tool calls, and plugin file watchers

### Improvements

- **Escape interrupt confirmation** - Pressing Escape while the agent is running now asks whether to stop it, and remembers your choice (app)

### Bug fixes

- **Stable sidebar width** - The sidebar keeps the width you set when you resize the window or collapse and reopen it (app)
- **Text selection after resizing** - Text stays selectable and clicks keep working after a panel resize is interrupted (app)
- **Recent sessions in the sidebar** - Your most recent sessions stay visible in the sidebar instead of being crowded out by sessions with many child sessions (app)
- **Polling tool calls** - A turn no longer stops early when the same tool call is repeated to watch output that keeps changing
- **Plugin file watching** - Droid no longer uses up your system's file watchers when you have plugin marketplaces installed, and cleans up files left behind by an interrupted install

## CLI v0.194.0 · Desktop v0.151.0 (August 12, 2026)

Session message access and a specification mode helper in the TypeScript SDK, plus fixes for pinned mission proposals, custom model credential errors, copied line breaks, and the idle todo spinner

### New features

- **Session messages in the SDK** - Sessions returned by the TypeScript SDK session list can now fetch their own messages directly
- **Specification mode SDK helper** - The TypeScript SDK can now take a session out of specification mode with a single call

### Bug fixes

- **Pinned mission proposals** - A pinned mission proposal now keeps its heading and full text instead of rendering garbled
- **Custom model credential errors** - A custom model whose endpoint has no working credentials now reports the problem right away instead of retrying the same request several times
- **Copied text line breaks** - Copying text out of a session now keeps its line breaks instead of collapsing everything onto one line (app)
- **Idle todo spinner** - The todo list no longer shows a spinner when nothing is running (app)

## CLI v0.193.0 · Desktop v0.150.0 (August 11, 2026)

Faster session search, fixes for repeated tool calls, lowercase proxy variables, the credits usage chart, and diff loading, plus the MiniMax M2.5 retirement

### Improvements

- **Faster session search** - Searching your session history now returns results faster

### Bug fixes

- **Repeated tool call recovery** - A turn now recovers when the same tool call repeats instead of getting stuck
- **Lowercase proxy variables** - Droid now honors lowercase proxy environment variables such as https_proxy in addition to the uppercase ones
- **Credit usage chart dates** - Daily totals in the credits usage chart now land on the correct day (app)
- **Diff loading retries** - A diff that fails to load no longer retries in a loop (app)

### Deprecations

- **MiniMax M2.5 retirement** - MiniMax M2.5 is no longer available for selection

## CLI v0.190.0 · Desktop v0.147.0 (August 7, 2026)

Claude Opus 5 in Auto model, HTTPS proxy support, and GitLab CI setup for automated QA, plus fixes for GitLab authentication, empty responses, and disconnected sessions

### New features

- **QA setup for GitLab CI** - The install-qa skill can now set up automated QA on GitLab CI and include video evidence in its reports

### Improvements

- **Opus 5 in Auto model** - Auto model now upgrades to Claude Opus 5 when a task needs a stronger model
- **HTTPS proxy support** - Droid now uses your HTTPS_PROXY setting when it connects, so sessions work behind a corporate proxy
- **Clearer connection errors** - A session that cannot connect at startup now explains what went wrong instead of showing a generic failure

### Bug fixes

- **Empty response recovery** - A turn now recovers when the model returns an empty response instead of ending with an error
- **GitLab authentication per host** - GitLab commands now authenticate against the host you are working with instead of a single default
- **Usage dashboard filters** - The usage dashboard filter bar now wraps so every filter stays visible (app)
- **Disconnected session state** - A session that loses its connection now keeps its state instead of resetting (app)
- **Archiving a running session** - Archiving a session that is still running now offers to stop it first instead of leaving it running (app)

## CLI v0.189.0 · Desktop v0.146.0 (August 6, 2026)

Session filtering in the command palette, faster session default changes, and fixes for status line failures, custom model key helpers, and empty responses

### New features

- **Command palette session filter** - The command palette now filters your sessions as you type instead of showing a fixed list (app)

### Improvements

- **Faster session default changes** - Changing a session default in settings now takes effect immediately instead of pausing while it saves

### Bug fixes

- **Status line failures** - A custom status line that fails now names the problem and points you to `/statusline` instead of leaving a blank row
- **Custom model key helpers** - Custom models that get their key from a helper command now start up instead of failing without a static API key
- **Empty final responses** - A turn that ends with an empty response now finishes successfully instead of failing with a no-output error
- **Openable file path links** - File paths in a response are only shown as links when they can actually be opened, and the tooltip says where they will open (app)
- **Recent session ordering** - Sending a message moves that session back to the top of your recent sessions right away (app)

## CLI v0.188.0 · Desktop v0.145.0 (August 4, 2026)

Fixes for plugin marketplace status, authentication for manually added MCP servers, diff colors, the thinking timer, member pickers, and opening markdown files

### Bug fixes

- **Marketplace status reporting** - A plugin marketplace that is working is no longer reported as missing
- **Manually added MCP servers** - MCP servers you add by hand can now finish authenticating instead of failing to connect (app)
- **Thinking timer stability** - The thinking timer keeps counting correctly when you move between views instead of restarting (app)
- **Diff colors by theme** - Added and removed lines in a diff now use the colors that match your light or dark theme (app)
- **Paginated member pickers** - Member pickers now page through everyone in your organization instead of showing only the first results (app)
- **Markdown in default app** - Markdown files now open in your default app instead of being blocked (app)

## CLI v0.187.0 · Desktop v0.144.0 (August 4, 2026)

Usage limits filtered by limit type, plus fixes for PDF attachments, plugin marketplace updates, and file diff counts

### Improvements

- **Usage limits by type** - Usage limits can now be filtered by limit type so you can narrow the list to the one you are looking for (app)
- **Voucher redemption confirmation** - Redeeming a voucher that changes your plan now shows what will change and asks you to confirm first (app)

### Bug fixes

- **PDF attachment fallback** - Attaching a PDF now falls back to its extracted text when the selected model cannot read PDFs, instead of failing
- **Skills with broken symlinks** - A skill with an unresolved symlink is now skipped instead of stopping your other skills from loading
- **Marketplace updates with local changes** - Updating a plugin marketplace now succeeds when its checkout has local changes instead of failing
- **Inline file diff counts** - File diffs show their added and removed line counts again (app)
- **Updates after canceled quit** - The app keeps checking for updates after you cancel quitting instead of waiting until the next launch (app)

## CLI v0.186.0 · Desktop v0.143.0 (July 31, 2026)

Support for GitHub Enterprise and self-hosted GitLab remotes, clickable links in tmux, and fixes for transcript performance, command denylists, and table scrollbars

### New features

- **Self-hosted Git remotes** - Repositories hosted on GitHub Enterprise or a self-hosted GitLab are now recognized as Git remotes

### Improvements

- **Streaming transcript performance** - Long streaming responses no longer slow the transcript down while they render (app)
- **Cmd-click hint on file paths** - File path links now show a tooltip explaining that Cmd-click opens the file (app)

### Bug fixes

- **Clickable links in tmux** - Links in the terminal are now clickable when you run the CLI inside tmux
- **Command denylist matching** - A denylisted command no longer blocks unrelated commands that happen to share a subcommand name
- **Table scrollbar overlap** - Scrollbars in tables no longer sit on top of row content (app)

## CLI v0.185.0 · Desktop v0.142.0 (July 30, 2026)

A per-server MCP connect timeout, plus fixes for stuck approval prompts, spec mode colors, and sign-in across multiple windows

### New features

- **Per-server MCP connect timeout** - MCP server configs accept a `connectTimeout` so a slow-starting server gets more time to connect instead of failing at startup

### Bug fixes

- **Stuck approval prompts** - An approval prompt no longer stays wedged when the request behind it is already gone, so Enter and Esc respond again
- **Spec mode message color** - Messages you send in spec mode keep the spec color when the view repaints or you resume the session, instead of looking like a normal turn
- **Sign-in with multiple windows** - Sign-in and MCP authorization now finish in the window that started them instead of hanging when more than one window is open (app)
- **File diff animations** - Opening and closing a file diff animates again instead of snapping into place (app)

## CLI v0.183.0 · Desktop v0.140.0 (July 29, 2026)

Multi-select questions from the agent, a fullscreen file preview, and a round of app improvements and fixes

### New features

- **Multi-select questions** - Questions the agent asks you can now accept more than one answer, so you can pick several options at once
- **Fullscreen file preview** - The file preview panel can now be expanded to fullscreen and back with a toggle (app)

### Improvements

- **MCP tool details** - Tool calls from MCP servers now show their details in the transcript instead of hiding them (app)
- **Queued attachment previews** - Attachments on a queued message now show a preview before the message is sent (app)

### Bug fixes

- **Git connection errors** - Errors while connecting a Git provider are now shown in the app instead of failing without explanation (app)
- **Pinned session dragging** - Dragging a pinned session no longer unpins it when another target handles the drop (app)
- **Show in folder on WSL** - Revealing a file in its folder now works for paths inside WSL (app)

## CLI v0.182.0 · Desktop v0.139.0 (July 28, 2026)

Audit log scope filter, user removal in the Admin Console, and a round of CLI session and authentication fixes

### New features

- **Audit log scope filter** - The audit log can now be filtered by scope, so you can narrow it to the events you are looking for (app)
- **Admin Console user removal** - Admins can now remove a user from the organization directly in the Admin Console (app)
- **Image copy context menu** - Images in a session can be copied to the clipboard from a right-click menu (app)

### Improvements

- **Recurring prompts in Loop** - Creating, listing, and cancelling recurring prompts is now one Loop tool instead of separate cron tools
- **Image thumbnails in previews** - Artifact preview cards in chat now show a thumbnail of the image instead of a generic card (app)

### Bug fixes

- **Forked session sync** - Sessions you fork now sync to the cloud instead of staying only on the machine that forked them
- **Expired session errors** - The CLI now reports an authentication error when the stored session token has gone missing
- **Re-authentication default** - Re-authenticating is now the preselected option when your session has expired
- **BYOK model names** - Bring-your-own-key models no longer show an extra suffix after the model name
- **Session and mission pickers** - Typing `q` in the session or mission picker now filters the list instead of closing it
- **Duplicate AGENTS.md** - AGENTS.md files are no longer added to context twice when discovery runs more than once
- **Header state** - The header now follows tool execution as it happens instead of lagging behind the agent
- **Transcript order** - Session transcripts stay in the right order when the system clock jumps
- **Reconnect after slow startup** - A local session that takes a long time to start now reconnects instead of staying disconnected (app)
- **Side Chat focus** - Running `/btw` now moves focus into Side Chat (app)
- **Repository access during setup** - Connecting a Git provider no longer fails when a single repository in the account cannot be read (app)

## CLI v0.181.0 · Desktop v0.138.0 (July 27, 2026)

Slash commands while the agent runs, MCP OAuth resource override, and subagent and Git fixes

### New features

- **Slash commands while the agent runs** - Slash commands now work during an active agent turn, so you no longer have to wait for it to finish
- **MCP OAuth resource override** - MCP server configs accept a `resource` field to send a different OAuth resource indicator, or omit it entirely

### Improvements

- **Subagent delegation** - The agent now delegates to subagents more selectively when using OpenAI models
- **Subagent results** - The agent reuses a subagent's report instead of re-reading the files it already covered, making follow-up work faster

### Bug fixes

- **Git index lock** - Checkouts now retry when another process is holding the Git index lock instead of failing
- **BYOK models** - Bring-your-own-key models are now scoped to the selected computer (app)

## CLI v0.180.0 · Desktop v0.137.0 (July 24, 2026)

Gemini 3.6 Flash support, a revamped keyboard shortcuts dialog, and faster session search

### New features

- **Gemini 3.6 Flash support** - Gemini 3.6 Flash is now available in the model selector
- **Disable built-in skills in the app** - You can now turn off Factory-provided built-in skills from the app (app)

### Improvements

- **Keyboard shortcuts help** - Redesigned the keyboard shortcuts help dialog so shortcuts are easier to scan (app)
- **MCP readiness** - Agent turns now wait until your MCP servers finish loading, so their tools are available from the first message
- **Session search** - Session search, sorting, and paging now run server-side for faster results in long histories, and you can look up a session by its ID (app)
- **MCP sign-in** - MCP authentication in the app now matches the CLI flow (app)

### Bug fixes

- **Spec proposal order** - Spec proposals now stay in chronological order in the chat transcript
- **Image loading** - Fixed images that failed to load in the desktop app, and cards now hide broken images instead of showing a placeholder (app)

## CLI v0.179.0 · Desktop v0.136.0 (July 23, 2026)

Sandbox and macOS hardening, plus mission, dictation, and app UI fixes

### Improvements

- **Sandbox hardening** - Strengthened isolation of processes running inside the command sandbox
- **macOS hardening** - Hardened macOS releases against code injection

### Bug fixes

- **Mission approvals** - The mission proposal body now renders once during approval instead of repeating
- **Capacity errors** - The CLI now backs off gracefully when a model is temporarily at capacity and no alternative is available
- **Voice dictation** - Long voice dictations are no longer cut off (app)
- **Visualization flicker** - Streamed visualizations no longer flicker while rendering (app)
- **Autonomy chip** - The autonomy chip in the composer now keeps a fixed width (app)
- **GitHub Enterprise Server repositories** - Repository lists are now correctly scoped to your organization (app)

## CLI v0.178.0 · Desktop v0.135.0 (July 22, 2026)

Keep-awake setting, system certificate trust, plus MCP, model, and invite fixes

### New features

- **Keep-awake setting** - A new setting keeps your machine awake during agent runs so long tasks aren't interrupted by sleep (app)

### Improvements

- **System certificate trust** - The CLI and desktop now trust your system's certificates at startup, improving connectivity in environments with custom certificate authorities

### Bug fixes

- **MCP confirmations** - Autonomy upgrades now apply correctly to MCP tool confirmations
- **MCP OAuth** - Signing in to MCP servers over OAuth is now more reliable
- **Hook display** - Hook metadata now stays on a single row
- **Verified domains on invite** - Invitations now respect your organization's verified domains (app)

## CLI v0.177.0 · Desktop v0.134.0 (July 21, 2026)

Open artifacts in your default app, plus mission, transcript, and app UI fixes

### New features

- **Open artifacts externally** - Artifact preview cards can now open in your default app (app)

### Improvements

- **Code block font** - Code blocks now render in Geist Mono for clearer monospaced text (app)
- **Attachment-only messages** - You can now send chat messages that contain only attachments (app)

### Bug fixes

- **Approval details toggle** - Option+E dead-key accents no longer interfere with toggling approval details
- **Transcript repaint** - The transcript now repaints correctly after viewing plan details
- **Computer removal** - Removing a computer no longer shows a spurious session-archiving warning
- **Mission interrupts** - Missions now pause correctly when the orchestrator is interrupted
- **Agent browser cleanup** - Orphaned browser automation processes are now cleaned up reliably
- **Unavailable sessions** - Sessions that can't be loaded now show a clear unavailable state (app)
- **Skill colors** - Loaded skills now display with the correct colors (app)

## CLI v0.176.0 · Desktop v0.133.0 (July 20, 2026)

Windows ARM64 desktop, disable builtin skills, plus session recovery and Auto model fixes

### New features

- **Disable builtin skills** - New `--disable-builtin-skills` flag turns off Factory-provided skills while keeping your own skill sources
- **Windows ARM64 desktop** - The desktop app now ships a native Windows ARM64 build (app)
- **Usage cap alert emails** - Admins now receive email alerts as usage approaches configured caps (app)

### Bug fixes

- **Session recovery** - Cancelling a tool no longer corrupts session history, and existing corruption is repaired automatically
- **Auto model retries** - Auto model turns now retry automatically when a model is unavailable
- **Disconnected prompts** - Permission and input prompts are now suppressed while disconnected
- **macOS sleep** - Notification sounds no longer prevent macOS from going to sleep (app)
- **PDF generation** - PDF generation errors now surface immediately instead of hanging (app)

## CLI v0.175.0 · Desktop v0.132.0 (July 17, 2026)

Auto-opening file previews, task ID prefixes, and /btw, model settings, wiki, and plugin fixes

### New features

- **File previews** - Generated files now open in a preview automatically (app)

### Improvements

- **Task ID prefixes** - `TaskOutput` and `TaskStop` now accept task ID prefixes so you can reference background tasks more easily

### Bug fixes

- **/btw mid-stream** - `/btw` now handles mid-stream forks correctly and submits follow-ups
- **Model settings** - Spec and normal mode model settings now persist correctly
- **Wiki shareable links** - Wiki runs can now generate shareable links
- **Plugins overlay** - The plugins overlay now closes on Esc from any tab

## CLI v0.173.0 · Desktop v0.130.0 (July 15, 2026)

Skill disable controls plus loop, plugin, hook, and settings fixes

### New features

- **Skill controls** - You can now disable individual skills and see how skill settings resolve across scopes

### Bug fixes

- **Repeated tool calls** - The agent now stops looping when it repeats the same tool call
- **Plugin loading** - Enabled plugins now load correctly across all install scopes
- **Hook execution** - Hooks now run exactly once per event
- **Settings writes** - Concurrent settings updates are no longer overwritten by stale cached writes
- **Mission Control** - The chat now repaints correctly when you close Mission Control (app)
- **Sidebar update button** - Fixed alignment of the sidebar update button (app)

## CLI v0.172.0 · Desktop v0.129.0 (July 14, 2026)

Mission side panel, add project folder, and PDF, MCP auth, and markdown fixes

### New features

- **Mission side panel** - Added a unified Mission side panel for managing missions (app)
- **Add project folder** - New button to add a local project folder, streamlining local project setup (app)

### Improvements

- **Consistent text editing** - Text-editing keys now behave consistently across all input fields

### Bug fixes

- **`/clear` preserves model** - `/clear` now keeps your current model and autonomy settings
- **Password-protected PDFs** - Password-protected PDFs no longer lock up the session
- **MCP authentication** - MCP sign-ins now refresh tokens silently and avoid duplicate authentication prompts
- **Markdown line breaks** - Soft line breaks in markdown now render correctly

## CLI v0.171.0 · Desktop v0.128.0 (July 13, 2026)

MCP connect timeouts, theme detection over SSH, and mission, model, and notification fixes

### Improvements

- **Context usage on resume** - Context usage now displays immediately when you resume a session
- **Windows installer architecture** - The CLI installer now detects the native Windows architecture

### Bug fixes

- **MCP connection timeout** - stdio MCP servers now time out on connect instead of hanging
- **Grep and Glob timeouts** - Grep and Glob timeouts now surface as actionable errors
- **Theme detection over SSH** - Fixed theme auto-detection over remote terminal sessions
- **Todo status colors** - Todo status colors now render correctly
- **Completion notification** - The turn-completion notification now fires before the CLI exits
- **Subagent reports** - The end-of-turn todo reminder no longer swallows subagent reports
- **Mission settings** - Fixed updating mission settings in the desktop app (app)
- **Mission notifications** - Mission mode now fires audio and badge notifications (app)
- **Model defaults** - Model defaults now persist correctly (app)
- **Reasoning tooltip** - The reasoning tooltip now dismisses when you start typing (app)
- **Local storage failures** - The app no longer breaks when local storage is unavailable (app)

## CLI v0.170.0 · Desktop v0.127.0 (July 10, 2026)

Legacy file encoding support, plus browser and composer refinements

### Improvements

- **Browser panel suggestions** - Local suggestions in the browser panel are now deduplicated and better ranked (app)
- **Prompt history recall** - Refined recall of previous prompts in the composer (app)

### Bug fixes

- **Legacy file encodings** - File tools now preserve legacy text encodings such as ISO-8859-2 and CP1250 instead of converting them

## CLI v0.169.0 · Desktop v0.126.0 (July 9, 2026)

macOS process sandbox, spec rendering fixes, and MCP session improvements

### New features

- **macOS command sandbox** - Added whole-process sandbox support on macOS for safer command execution

### Improvements

- **Clearer send button** - The composer now explains why the send button is disabled (app)
- **Safer web tools** - WebSearch and FetchUrl now require at least low autonomy before they run

### Bug fixes

- **Image-only messages** - Fixed sending messages that contain only an image
- **Plan todos** - Plan todo lists are now bounded and the full todo displays correctly
- **Wide tables** - Wide markdown tables now scroll horizontally
- **MCP footer** - The MCP status footer now appears immediately
- **MCP session notices** - MCP status and auth notices now stay scoped to their session instead of leaking into untouched sessions
- **Spec rendering** - Spec contents now render in the approval details screen, and the spec body shows when the plan heading matches the title
- **Update rollback** - Hardened the update rollback flow (app)

## CLI v0.168.0 · Desktop v0.125.0 (July 8, 2026)

Pin local sessions, working directory in the desktop app, and CLI and app fixes

### New features

- **Pin local sessions** - You can now pin local sessions that aren't synced to the cloud (app)
- **Working directory in desktop** - The desktop app now brings your current working directory into the session (app)

### Improvements

- **Slash command search** - Improved slash command search results
- **Skills count** - The header now shows an accurate skills count
- **Wiki permalinks** - Added repository permalink support in wikis

### Bug fixes

- **Session token usage** - Session token usage is now counted only on successful turns
- **Unread sessions** - Unrelated unread sessions are preserved when a window regains focus (app)
- **Notification hook** - The `idle_prompt` Notification hook now fires on cancelled turns
- **Reasoning effort** - `set-default` now preserves your session reasoning effort
- **Bash mode** - Pressing backspace on empty input now exits bash mode
- **Spec proposals** - Empty spec proposal bodies are now rejected
- **Ghostty Open In** - Fixed launching Ghostty from the Open In deeplink (app)
- **Window close warning** - The app now only warns on window close when it will actually quit the app (app)
- **MCP OAuth screen** - Aligned the MCP OAuth callback screen

## CLI v0.167.0 · Desktop v0.124.0 (July 7, 2026)

Port-forwarding for droid computers, faster startup and search, and Windows and Linux fixes

### New features

- **Port-forward for droid computers** - New `droid computer port-forward` command to forward ports from a droid computer to your local machine

### Improvements

- **Faster app startup** - Startup boot phases now run in parallel, reducing time to a usable window (app)
- **Faster session search** - Session search is quicker and returns better-ranked results
- **Full-screen help** - Help now opens as a full-screen overlay you can dismiss with `?` or `Esc`
- **Slash menu filtering** - Filtered slash menu results are flattened with a clearer category block
- **Cleaner model names** - Model names display more clearly across the app (app)
- **Cleaner chat transcript** - Internal tool lookups no longer clutter the chat transcript (app)
- **Update rollback** - The app can now roll back to a previous version when needed (app)

### Bug fixes

- **Image paste on Windows** - Fixed pasting images into the composer on Windows
- **Safe exit during updates** - You can now exit safely while a background update is in progress
- **SessionStart hooks** - A hung `SessionStart` hook no longer blocks session initialization
- **Completion sound** - Restored the completion sound
- **Windows home directory** - Fixed resolving the home directory for non-ASCII Windows usernames
- **Draft attachments** - Draft attachments are now preserved when the screen repaints
- **Sandboxed hooks** - Fixed hook command execution under the sandbox
- **Detailed transcript freeze** - Capped detailed transcript tool results to stop `Ctrl+O` from freezing
- **New session shortcut** - The new-session shortcut now ignores Shift (app)
- **Truncated sessions** - Fixed context handling in truncated sessions
- **Linux clipboard** - Text clipboard is now Wayland-first on Linux
- **Special characters** - Typing `å`, `Å`, or `´` is no longer treated as an Option shortcut
- **Unavailable tools** - Calls to unavailable tools are now clearly marked as errors
- **Highlighted code** - Highlighted code text is now preserved (app)
- **Airgap mode** - Improved the reliability of airgap mode (app)

## CLI v0.164.0 · Desktop v0.121.0 (July 2, 2026)

Grouped slash commands, cloud sync control, and MCP and login fixes

### New features

- **Grouped slash commands** - Slash commands are now organized by category for easier browsing
- **Cloud sync control** - New setting to control whether your data syncs to the cloud (app)

### Improvements

- **Linear model picker** - Model names now display cleanly in the Linear delegation picker (app)
- **Computer provisioning wizard** - Clarified copy in the droid computer provisioning wizard (app)

### Bug fixes

- **MCP tool names** - Tool names containing dots are now accepted per the MCP specification
- **MCP authentication** - Restored sign-in to MCP servers that reject certain OAuth client registration
- **Background processes in droid exec** - Agent-spawned background processes now keep running after `droid exec` exits
- **Editor for allow/deny lists** - The CLI now honors `$EDITOR` when editing allow and deny lists on headless hosts
- **Gemini reasoning** - Fixed handling of invalid Gemini reasoning blocks
- **Droid computer SSH** - Fixed connecting to a droid computer by its exact name
- **Cross-org login** - Fixed login issues when working across multiple organizations (app)

## CLI v0.162.0 · Desktop v0.119.0 (June 30, 2026)

Cloned repos in projects, lower memory use, and rendering and auth fixes

### New features

- **Cloned repos in projects** - Cloned repositories now appear in the new-session projects dropdown (app)

### Improvements

- **Lower memory usage** - Reduced memory use during long and idle sessions
- **Word-wise navigation** - Option+Left/Right now jumps between words in secondary text inputs

### Bug fixes

- **Resumed hooks** - Hook rows now render correctly after you resume a session
- **File encoding** - Edited files now keep their original encoding instead of always saving as UTF-8
- **MCP authentication** - Restored basic auth fallback when signing in to MCP servers over OAuth
- **Org switching** - Fixed selecting the active organization when switching organizations, including in the EU (app)

## CLI v0.161.0 · Desktop v0.118.0 (June 29, 2026)

Hooks manager overhaul, chat transcript search, and faster searches

### New features

- **Hooks manager overhaul** - Redesigned the hooks manager for viewing and configuring your hooks
- **WezTerm setup** - Added terminal setup support for WezTerm
- **Chat transcript search** - Search within a chat transcript (app)

### Improvements

- **Faster searches** - Avoided unnecessary search cache rebuilds

## CLI v0.159.0 · Desktop v0.116.0 (June 25, 2026)

Archive projects with clearer MCP authentication guidance

### New features

- **Archive projects** - Archive projects you're no longer working on to keep your project list tidy (app)

### Improvements

- **Clearer MCP auth guidance** - When an MCP server fails to authenticate, the CLI now explains how to resolve it

### Bug fixes

- **MCP config errors** - MCP configuration parse errors are now surfaced clearly instead of failing silently

## CLI v0.158.0 · Desktop v0.115.0 (June 24, 2026)

Plugin toggles, tab slash-command completion, and login and rendering fixes

### New features

- **Enable and disable plugins** - Turn individual plugins on or off with a new toggle

### Improvements

- **Tab to complete slash commands** - Press Tab to complete slash commands
- **MCP authentication** - Improved handling of MCP authentication responses and desktop redirects
- **Account credit checkout** - Subscribe to or upgrade your plan using account credit

### Bug fixes

- **Invalid API key login** - The CLI now exits with an error on an invalid `FACTORY_API_KEY` instead of stalling at login
- **Cancel AskUser prompts** - Cancelling an AskUser prompt now interrupts the agent instead of letting it continue
- **Duplicate tool approvals** - Approval-gated tool executions now render only once
- **Windows background processes** - Fixed cleanup of background processes on exit on Windows
- **Document skills location** - Document skills are now written to your current working directory
- **Dark mode toggles** - Dark mode toggles are now visible and loading spinners animate correctly (app)
- **Editable composer** - The composer stays editable during session blockers (app)

## CLI v0.157.2 · Desktop v0.114.2 (June 24, 2026)

Slack follow-up prompt fix

### Bug fixes

- **Slack follow-up prompt** - Fixed a duplicate "tag to follow up" prompt that could appear in Slack threads

## CLI v0.157.0 · Desktop v0.114.0 (June 23, 2026)

External prompt editing and input and onboarding fixes

### New features

- **Edit prompts externally** - Open and edit your prompt in an external editor for composing longer messages

### Bug fixes

- **Caps-lock cursor keys** - Fixed cursor key handling when caps lock is on
- **Onboarding crash** - Fixed a crash that could occur when connecting before onboarding finished (app)

## CLI v0.156.2 · Desktop v0.113.2 (June 22, 2026)

Conversation rewind and reliability fixes

### New features

- **Rewind conversation** - The new `/rewind-conversation` command rewinds the chat and restores your files to an earlier point (app)
- **Org hooks governance** - Organizations can now centrally control hooks settings across their members

### Improvements

- **Clickable message links** - URLs in your messages are now clickable
- **Light terminal colors** - Improved white rendering in the light terminal theme

### Bug fixes

- **Reasoning indicator** - Non-thinking models no longer show a reasoning indicator
- **Execute step shimmer** - Fixed a stale loading shimmer left on completed execute steps
- **Windows hooks** - Preserved command quoting for hooks on Windows
- **MCP server logos** - MCP server logos now keep their original colors

## CLI v0.152.0 · Desktop v0.109.0 (June 18, 2026)

Command-line autonomy flag, org MCP and marketplace controls, and reliability fixes

### New features

- **Autonomy flag** - Set Droid's autonomy level straight from the command line with `droid --auto high`
- **Org MCP and marketplace controls** - Organizations can centrally govern MCP server and plugin marketplace access
- **In-app membership controls** - Manage organization members directly in the app (app)

### Improvements

- **Private npm registry plugins** - Plugin sources can now authenticate to private npm registries using an auth token environment variable
- **Onboarding copy** - Clearer guidance during Droid setup onboarding (app)

### Bug fixes

- **Status after interrupt** - Droid's status now clears correctly after you interrupt it
- **Event hooks** - Multiple hooks configured for the same event are now combined correctly
- **Summaries across directories** - Fixed conversation summaries when your working directory changes
- **Streaming placeholder** - Fixed a stale placeholder that could linger in the chat (app)
- **Connection stability** - Reduced session UI flicker during brief connection drops (app)

## CLI v0.151.0 · Desktop v0.108.0 (June 17, 2026)

Branded macOS installer with MCP and session reliability fixes

### New features

- **Skill slash commands in editors** - Skill slash commands are now available when connecting from external editors

### Improvements

- **macOS installer branding** - The macOS DMG installer is now branded (app)
- **MCP results as markdown** - MCP tool results returned as JSON now render as formatted markdown

### Bug fixes

- **Session reconnection** - Sessions now stay rendered and reconnect instead of redirecting to a Session Unavailable page (app)
- **Org switcher** - The desktop organization switcher now shows the currently selected organization (app)
- **Desktop MCP sign-in** - Improved desktop MCP authentication callback handling (app)
- **Composer actions layout** - Composer actions now stay on a single line (app)

## CLI v0.150.0 · Desktop v0.107.0 (June 16, 2026)

npm plugin sources and long-session performance

### New features

- **npm plugin sources** - Plugin marketplace definitions can now reference plugins published as npm packages
- **Quit confirmation** - Desktop now asks for confirmation before quitting or closing would interrupt an active Droid session (app)

### Improvements

- **Long session performance** - Improved chat performance in long sessions (app)
- **MCP authentication page** - Polished the MCP authentication success page
- **Overdue invoice banner** - Billing settings now show a banner when an invoice is overdue (app)

### Bug fixes

- **Rate limit reset display** - Fixed the rate limit reset time shown for sub-hour resets

## CLI v0.149.0 · Desktop v0.106.0 (June 15, 2026)

Canva MCP authentication fix

### Bug fixes

- **Canva MCP authentication** - Added a fallback so connecting the Canva MCP server works more reliably

## CLI v0.148.1 · Desktop v0.105.0 (June 15, 2026)

Air-gapped CLI binary distribution fix

### Bug fixes

- **Air-gapped binaries** - Air-gapped CLI binaries are now properly signed and published so air-gapped installs receive the latest builds

## CLI v0.148.0 · Desktop v0.105.0 (June 14, 2026)

MCP connection status, org-wide auto-update control, and reliability fixes

### New features

- **MCP connection status** - `droid mcp list` and your session now show each MCP server's connection and authentication status
- **Org-wide auto-update control** - Organizations can turn off CLI auto-updates with a new `disableAutoUpdate` setting

### Improvements

- **Log rotation** - The CLI now rotates its log files to avoid filling up disk space
- **Faster MCP loading in editors** - MCP servers load without blocking when connecting from external editors
- **Streamlined desktop sign-up** - Signing up on desktop now takes you straight to login (app)
- **Clearer unsaved changes banner** - The unsaved changes banner is now easier to spot (app)

### Bug fixes

- **Duplicate BYOK models** - Removed duplicate models from the bring-your-own-key model selector
- **BYOK custom endpoints** - Fixed compatibility with custom bring-your-own-key model endpoints
- **Duplicate transcript** - Fixed a duplicate transcript appearing in the session view
- **Plugins slash command** - The `/plugins` command now appears before a session finishes initializing (app)
- **Wiki reader dragging** - Restored window dragging in the wiki reader (app)
- **MCP authentication notices** - Improved how MCP authentication prompts are shown

## CLI v0.147.0 · Desktop v0.104.0 (June 12, 2026)

Command blocklist, MCP OAuth improvements, and welcome screen sign-in

### New features

- **Command blocklist** - The new `commandBlocklist` setting hard-stops specified commands so they can never run, even under full autonomy or skipped approvals
- **Welcome screen sign-in** - Added log-in and sign-up CTAs to the welcome screen (app)

### Improvements

- **MCP OAuth** - MCP servers can now authenticate using Client ID Metadata Documents (CIMD), with improved compatibility for servers that require a resource indicator
- **Updated tooltips** - Refreshed tooltips for clearer guidance

### Bug fixes

- **Ctrl+Enter tooltip** - Fixed the Ctrl+Enter tooltip
- **Desktop MCP OAuth banner** - The MCP OAuth banner now points at the MCP button (app)

## CLI v0.146.0 · Desktop v0.103.0 (June 12, 2026)

Browser-based desktop onboarding, air-gapped mode improvements, and chat, MCP, and onboarding fixes

### New features

- **Browser-based desktop onboarding** - Desktop onboarding now opens in your browser for a smoother first-run setup (app)

### Improvements

- **Queue message shortcut** - Queue a message with Ctrl+Enter
- **Earlier session titles** - Droid now names your session earlier in the conversation
- **Air-gapped BYOK defaults** - Air-gapped mode auto-picks a sensible default BYOK model, and configuration errors point you at `settings.json`

### Bug fixes

- **Chat cursor on resize** - The chat input now keeps your cursor position when the terminal is resized
- **Context summarization hangs** - Fixed a rare hang that could occur while summarizing long conversations
- **Content filtering** - Responses blocked by a content filter are now surfaced as a clear moderation error
- **Desktop MCP OAuth** - Desktop MCP OAuth now flows through the hosted callback (app)
- **Desktop onboarding top bar** - The top bar can now be dragged on desktop onboarding screens (app)
- **Data retention dialog** - The data retention dialog no longer interferes with desktop navigation (app)

## CLI v0.144.2 · Desktop v0.101.2 (June 10, 2026)

MCP authentication fixes

### Bug fixes

- **MCP authentication** - Improved MCP sign-in reliability for servers that advertise no scopes
- **Desktop MCP OAuth banner** - The MCP OAuth banner no longer overlaps the top bar (app)

## CLI v0.144.1 · Desktop v0.101.1 (June 9, 2026)

More reliable context summarization when a model declines a request

### Bug fixes

- **Context summarization fallback** - When a model declines to summarize your conversation, Droid now falls back gracefully instead of retrying repeatedly

## CLI v0.144.0 · Desktop v0.101.0 (June 9, 2026)

Session file suggestions, safer command risk handling, and MCP reliability fixes

### New features

- **Session file suggestions** - The new session page now suggests relevant files as you get started (app)

### Improvements

- **Safer command risk handling** - Commands that could destroy your working tree are now treated as high risk
- **tmux key support** - Improved keyboard handling when running inside tmux

### Bug fixes

- **MCP reliability** - Improved reliability of MCP authentication and connectors

## CLI v0.143.1 · Desktop v0.100.1 (June 9, 2026)

Maintenance and stability release

### Improvements

- **Maintenance and stability** - Routine maintenance and reliability updates under the hood

## CLI v0.143.0 · Desktop v0.100.0 (June 8, 2026)

Richer Jira details

### New features

- **Self-serve organization deactivation** - Deactivate your organization yourself, with subscription cancellation now available in billing settings (app)

### Improvements

- **Richer Jira details** - Fetching a Jira issue now includes more fields, comments, and linked-issue URLs
- **Quieter hooks** - Hooks can hide their output block in the TUI by setting `suppressOutput`

### Bug fixes

- **Windows home directory** - Fixed home directory resolution on Windows to avoid username corruption (app)
- **Session integrity** - Fixed an issue that could overwrite an existing session

## CLI v0.142.0 · Desktop v0.99.0 (June 5, 2026)

GitLab code review setup and chat stability fixes

### Improvements

- **GitLab code review setup** - The install-code-review skill now configures review pipelines using a GitLab CI Component

### Bug fixes

- **Duplicate chat messages** - Fixed duplicate messages appearing in chat
- **Diff viewer counts** - The diff viewer now refreshes its change counts correctly (app)

## CLI v0.141.0 · Desktop v0.98.0 (June 4, 2026)

More reliable command output and CLI fixes

### Improvements

- **Large command output** - Command execution now handles very large outputs more reliably

### Bug fixes

- **Input hint placement** - The running hint now stays below your typed input
- **Guidelines in non-git projects** - Droid no longer looks for guideline files in parent directories when you're not inside a git repository

## CLI v0.140.1 · Desktop v0.97.1 (June 4, 2026)

Maintenance and stability release

### Improvements

- **Maintenance and stability** - Routine maintenance and reliability updates under the hood

## CLI v0.140.0 · Desktop v0.97.0 (June 3, 2026)

Claude Opus 4.8 and Gemini 3.5 Flash support, MCP tool search, incident response, and stability fixes

### New features

- **Claude Opus 4.8** - Added support for Claude Opus 4.8, including a faster Fast Mode variant
- **Gemini 3.5 Flash** - Added support for Gemini 3.5 Flash
- **MCP tool search** - Droid can now search and load MCP tools on demand, keeping large MCP setups fast and context-efficient
- **Incident response** - Droid can automatically investigate production alerts posted to a configured Slack channel and work toward a root-cause analysis

### Improvements

- **Accurate status banners** - Spinner status banners now reflect the true state of the current turn
- **Context menu text actions** - Added text actions to the right-click context menu (app)

### Bug fixes

- **Terminal write errors** - The CLI no longer crashes when the terminal rejects output writes
- **Paste handling** - Fixed a crash on certain pasted input and corrected handling of split bracketed pastes
- **Agent loop stalls** - The agent loop no longer runs unbounded when turns produce no output
- **Empty chat placeholder** - Restored the placeholder shown in empty chats (app)
- **Machine connection crash** - Fixed a crash when loading sessions with older machine connection types (app)

## CLI v0.139.0 · Desktop v0.96.0 (June 2, 2026)

Custom commands and skills in the slash menu and MCP fixes

### New features

- **Custom commands and skills in the slash menu** - Your custom commands and skills now appear directly in the slash menu

### Bug fixes

- **MCP schema compatibility** - Improved handling of MCP servers with incompatible tool schemas
- **Clearing MCP server fields** - You can now clear fields when editing an MCP server
- **Local session labels** - Local sessions are now labeled "Local" instead of "Ephemeral" (app)

## CLI v0.138.0 · Desktop v0.95.0 (June 1, 2026)

MCP management upgrades, Mermaid export, and stability fixes

### New features

- **Interactive MCP management** - Add, remove, and list MCP servers interactively
- **MCP credential variables** - MCP server configs can now expand credential variables at runtime
- **Configurable MCP call timeout** - Set a custom timeout for MCP tool calls
- **`mcp off` shortcut** - Quickly disable MCP servers with a new shortcut
- **MCP servers for custom droids** - Choose which MCP servers are available to custom droids
- **Per-server MCP risk** - Configure command risk levels for each MCP server
- **Mermaid export** - Export Mermaid diagrams from chat (app)

### Improvements

- **Highlighted new models** - New models now appear highlighted at the top of `/models`
- **MCP embedded resources** - MCP servers' embedded resources are now surfaced in chat
- **Composer loading state** - The message composer now shows a loading state (app)
- **Session archiving** - Unified the session archive flow across the app and desktop (app)
- **Pinned messages** - Clicking a pinned message now scrolls to its source (app)

### Bug fixes

- **Turn cancellation** - Canceling a turn now takes effect immediately
- **Session rename** - Renamed session titles are now trimmed of extra whitespace (app)

## CLI v0.137.0 · Desktop v0.94.0 (May 29, 2026)

Usage stats, airgapped BYOK, and stability fixes

### Bug fixes

- **Duplicate thinking output** - Thinking output no longer renders twice
- **MCP permission persistence** - MCP permissions now persist across all confirmation paths
- **Context usage meter** - Fixed alignment of the context usage meter

## CLI v0.136.0 · Desktop v0.93.0 (May 28, 2026)

Deep review skill, side questions in the app, session compression controls, and stability fixes

### New features

- **Deep review skill** - New `/deep-review` skill for a more thorough, multi-pass code review
- **Side questions in the app** - The `/btw` side questions panel is now available in the app (app)
- **Auto-compression toggle** - Turn automatic session compression on or off to manage long sessions
- **Configurable compression model** - Choose which model handles automatic session compression

### Improvements

- **Org details in `/status`** - The `/status` command now shows your organization details
- **Standardized hooks config path** - Hooks configuration now uses a standardized file path with automatic migration
- **Faster large pastes** - Sped up pasting large amounts of text
- **Tool summary hover affordance** - Tool summaries now show a hover affordance for available actions (app)

### Bug fixes

- **Autoscroll fixes** - Fixed several autoscroll issues in the session view (app)
- **Reasoning-only turns** - Fixed sessions stalling when the assistant returned only reasoning
- **DeepSeek tool calls** - Improved reliability of multi-step tool calls when using DeepSeek models

## CLI v0.135.0 · Desktop v0.92.0 (May 27, 2026)

Adaptive terminal theme, agent-browser update, and stability fixes

### New features

- **Adaptive terminal theme** - The CLI now auto-detects your terminal background and picks a matching theme

### Improvements

- **Agent-browser update** - Updated the bundled `agent-browser` skill to a newer release with better automation reliability
- **Subagent type badges** - Subagent type badges in `TaskOutput` now render in PascalCase for easier reading

### Bug fixes

- **Message draft attachments** - Message draft attachments are now preserved when switching contexts (app)
- **Session activity indicator** - Improved the activity indicator in the session panel (app)
- **Enterprise Controls forms** - Empty arrays and records are no longer written when saving Enterprise Controls (app)
- **Enterprise Controls layout** - Aligned control heights across Enterprise Controls forms (app)

## CLI v0.134.0 · Desktop v0.91.0 (May 26, 2026)

Stability fixes and UI polish

### Improvements

- **Figma helper skill** - The built-in Figma skill has been renamed from `figma-mcp-promotion` to `figma-mcp-helper`
- **System-managed settings** - System-managed settings are now loaded from standard platform paths

### Bug fixes

- **File tool rendering** - File tool inputs now wait for streaming to complete before rendering to avoid showing partial data
- **Slash command suggestions** - Slash command suggestion rows now keep a consistent height
- **Pending command approvals** - Capped the number of pending command approvals shown at once
- **New session sidebar animation** - Smoothed the animation when starting a new session from the sidebar (app)
- **Session titles in sidebar** - Session titles are now preserved correctly in the sidebar (app)
- **AskUser question labels** - Question labels now pluralize correctly when multiple questions are asked

## CLI v0.133.1 · Desktop v0.90.1 (May 25, 2026)

Context window modal, audio cues, sidebar session menu, and stability fixes

### New features

- **Context window** - New `/context` slash command and modal for inspecting the current session's context usage
- **Audio cues** - Optional sounds when a session finishes or is awaiting your input (app)
- **Sidebar session menu** - Right-click sessions in the sidebar for quick actions (app)

### Bug fixes

- **Final output visibility** - The final output now stays visible above the input box
- **New session draft cleared** - New session drafts now clear after submitting (app)
- **Linear Computer setup link** - The "set up Computer" call to action in Linear now points to the correct settings page
- **Desktop zoom stability** - Hardened desktop zoom handling against host zoom errors (app)

## CLI v0.132.0 · Desktop v0.89.0 (May 22, 2026)

Render deployments and stability fixes

### New features

- **Deploy to Render** - New `/deploy-to-render` skill helps you deploy projects to Render

### Improvements

- **Security review scope confirmation** - The `/security-review` skill now confirms the scope and audit branch with you before running
- **Faster EU connections** - Reduced connection latency for users in the EU region

### Bug fixes

- **Disabled model selector rows** - Restored disabled rows in the model selector so all options are visible
- **Missions across reconnects** - Active missions now keep running through network reconnects
- **Mission computer in mission control** - The active mission computer now appears on the mission control page (app)
- **Windows desktop setup** - Fixed setup and scripts for the Windows desktop app (app)
- **Rich text autofocus** - Improved autofocus reliability for rich text inputs (app)

## CLI v0.131.0 · Desktop v0.88.0 (May 21, 2026)

Maintenance release

### Improvements

- **Maintenance release** - with under-the-hood improvements.

## CLI v0.130.0 · Desktop v0.87.0 (May 20, 2026)

Model favorites, spec save directory, paste expansion, and stability fixes

### New features

- **Model favorites** - Mark and quickly access your preferred models from the model selector
- **Spec save directory** - Configure where specs are saved with a new setting
- **Expand pasted placeholders** - Press Alt+Shift+V (Opt+Shift+V on macOS) to expand truncated paste placeholders inline

### Improvements

- **Refined model selector** - Streamlined the model selector submenu
- **BYOK model parity** - Brought the BYOK model experience in line with the rest of the model picker
- **Clearer help output** - Improved formatting of the `help` command output

### Bug fixes

- **Image paste on Linux** - Pasting images now works on Linux, with a graceful fallback when clipboard data is unavailable
- **MCP OAuth clients** - Static MCP OAuth clients are now supported during authentication
- **OAuth provider errors** - 4xx responses from connected OAuth providers are now surfaced as user-facing errors
- **ApplyPatch new files** - New files in ApplyPatch results now render correctly as creates
- **CLI update reliability** - Prevented restart races during CLI daemon updates
- **PowerShell under `exec`** - PowerShell commands now run non-interactively in `exec` mode
- **Slack first-mention indicator** - Slack now shows the typing indicator from the very first mention
- **Daemon auth on reconnect** - Daemon auth tokens now refresh when reconnecting (app)
- **Desktop paid onboarding** - The onboarding finish screen is now skipped on the desktop paid flow (app)

## CLI v0.129.0 · Desktop v0.86.0 (May 18, 2026)

Streaming file hook events, faster large sessions, and stability fixes

### New features

- **Streaming file hook events** - File hook execution events now stream so you can follow progress as hooks run

### Improvements

- **Faster large session rendering** - Large session transcripts now render faster by trimming at the cutoff before derivation

### Bug fixes

- **Esc cancels tool activity** - Pressing Esc now reliably cancels in-progress tool activity
- **MCP tools with complex schemas** - Listing MCP tools no longer fails when schemas contain unresolvable references
- **Claude Code subagent import** - Subagent import is now skipped when there is no project root to import into
- **Session load file snapshots** - File snapshots are now initialized when reloading a saved session
- **ACP todo updates** - Hardened parsing of todo updates over ACP against missing fields
- **Read-only badge layout** - Read-only badges no longer get compressed in narrow layouts (app)
- **Pinned group new session action** - Removed an unintended new-session action on pinned groups (app)
- **Desktop session recovery** - Desktop sessions now recover after a period of daemon inactivity (app)

## CLI v0.128.0 · Desktop v0.85.0 (May 15, 2026)

Stability fixes

### Bug fixes

- **Stale Computer registrations** - Sessions now reconcile stale Droid Computer registrations automatically

## CLI v0.126.0 · Desktop v0.83.0 (May 14, 2026)

Bulk session archiving, faster Computer restarts, EU data residency, and stability fixes

### New features

- **Bulk session archiving** - New settings page for managing and bulk-archiving sessions (app)
- **EU data residency** - Sessions and LLM inference for EU customers now stay within an EU-only data plane
- **Built-in security review** - The `/security-review` skill is now bundled with the CLI by default
- **Copy bug report ID** - Added a copy button next to bug report IDs (app)

### Improvements

- **Faster Computer restarts** - Sped up restarting Droid Computers (app)
- **Lighter CLI startup** - Reduced redundant requests during CLI startup
- **Persistent desktop preferences** - Desktop preferences are now saved alongside other settings (app)
- **Windows pending update cleanup** - Cleaned up stale pending updates on Windows

### Bug fixes

- **Structured output validation** - Strengthened validation of structured tool output
- **Task token count** - Removed an incorrect zero token count from Task tool results
- **Windows installer packaging** - Repaired Windows installer packaging
- **Limits reset on plan change** - Plan changes now correctly reset usage limits (app)
- **MCP servers for running sessions** - MCP servers now load when reopening already-running sessions (app)
- **Local daemon warning during setup** - Suppressed a spurious local daemon warning during initial setup (app)
- **Session not found errors** - Fixed spurious session not found errors (app)
- **Code block styling** - Aligned code block styling in chat (app)
- **Cross-surface integrations** - Prevented integrations from sending duplicate postbacks across surfaces
- **QA droid CLI auth** - QA droid CLI now pairs with the matching Factory API host

## CLI v0.125.1 · Desktop v0.82.1 (May 14, 2026)

Maintenance release

### Improvements

- **Maintenance release** - with under-the-hood improvements.

## CLI v0.125.0 · Desktop v0.82.0 (May 13, 2026)

ACP config options, larger Task results, and stability fixes

### New features

- **ACP config options** - The CLI now advertises configuration options to ACP clients and supports `session/set_config_option` for per-session overrides

### Improvements

- **Larger Task tool results** - Raised the truncation limit on Task tool results so more output is preserved

### Bug fixes

- **Stale tool shimmer** - Tool calls no longer leave a stale shimmer behind in the transcript
- **Stale Slack shimmer heartbeat** - Stopped a stale shimmer heartbeat from lingering in Slack threads
- **Return to session on interaction prompt** - The CLI now returns to the session view when a user interaction box surfaces
- **Gemini thinking signatures on replay** - Gemini thinking signatures are now preserved when sessions replay
- **Title bar path on hover** - The title bar now shows the full working directory path on hover (app)

## CLI v0.124.0 · Desktop v0.81.0 (May 12, 2026)

Deep and shallow security review modes, login redirect URIs, and stability fixes

### New features

- **Deep and shallow security review modes** - `/security-review` now supports dedicated deep and shallow review modes
- **Login redirect URIs** - The login flow now supports a redirect URI so you land where you started after signing in (app)

### Improvements

- **Sharper fuzzy search** - Refined fuzzy search behavior in the CLI
- **Minimum context savings shown** - Context savings now display a clear minimum percent for easier interpretation
- **Aligned MCP status indicators** - MCP server status indicators now line up consistently
- **Faster setting updates** - Settings changes are applied in place, avoiding unnecessary MCP and skill refetches (app)
- **Light mode polish** - Small component styling refinements in light mode

### Bug fixes

- **Bounded resume history** - Resume now renders a bounded history so large sessions stay responsive
- **Message send flash** - Fixed a visual flash when submitting a message (app)
- **Desktop tutorial in desktop app** - The "install desktop" onboarding step is now skipped when you're already in the desktop app (app)

## CLI v0.123.1 (May 12, 2026)

Maintenance release

### Improvements

- **Maintenance release** - with under-the-hood improvements.

## CLI v0.123.0 · Desktop v0.80.0 (May 11, 2026)

Factory token usage in mission control, model deprecation notices, and stability fixes

### New features

- **Factory token usage in Mission Control** - Factory token usage is now persisted to session settings, with a toggle to show it in Mission Control
- **Model deprecation notices** - Factory now surfaces notices when a model is scheduled for deprecation
- **Optimistic message submit** - Messages can now be submitted before the session connection is ready (app)

### Improvements

- **Clearer parallel execute approvals** - Parallel execute approval prompts now make it clearer what's being approved
- **Chat notice display** - Refreshed how chat notices render (app)

### Bug fixes

- **Spec reasoning tab cycle** - Restored cycling through tabs in the spec reasoning view
- **Duplicate spec rendering** - Specs no longer render twice
- **Padded multiline status lines** - Multiline status lines now render with consistent padding
- **Subagent tokens in Mission Control** - Mission Control token counts now include subagent tokens
- **Queued messages during /compress** - Messages typed while `/compress` is running are now queued instead of dropped
- **Stale /missions prompt** - Fixed a stale `/missions` prompt lingering after dismissal
- **Provider tool name handling** - Improved handling of tool names returned by model providers
- **Stuck session loading** - Fixed sessions that could get stuck loading (app)
- **Ghost update badge** - Fixed a spurious update-available badge caused by an update manifest mismatch (app)

## CLI v0.122.0 · Desktop v0.79.0 (May 8, 2026)

Manager-only API keys, tighter Computer name validation, and stability fixes

### Improvements

- **Manager-only API key creation** - Organization API keys can now only be created by managers (app)
- **Stricter Computer name validation** - Computer names are limited to lowercase letters, digits, and hyphens, with clearer error states (app)

### Bug fixes

- **Working directory from computer wizard** - Working directory is now seeded correctly when navigating from the computer wizard to a new session (app)
- **Duplicate collapsed groups** - Fixed duplicate collapsed groups in the CLI
- **Droid header spacing** - Restored a missing trailing space in the Droid header
- **Extra usage on subscription end** - Remaining extra usage is now transferred to your account balance when a subscription ends (app)

## CLI v0.121.0 · Desktop v0.78.0 (May 7, 2026)

Thinking duration, smoother scrollback, better session titles, and stability fixes

### New features

- **Thinking duration** - CLI and app now show how long a droid spent thinking
- **Scroll to most recent prompt** - You can now scroll down directly to the most recent prompt in the CLI

### Improvements

- **Smoother transcript scrollback** - Cached static transcript markdown rendering for faster scrolling
- **Better session titles** - Session titles are now well-formed, with redundant syncs deduplicated
- **Tighter /sessions layout** - Column widths in `/sessions` are now distributed more evenly
- **Faster setup failure feedback** - Setup now fails fast with a clearer error when the daemon can't connect

### Bug fixes

- **Pasting long blocks** - Fixed issues when pasting large blocks of text into the CLI
- **ACP tool call lifecycle** - Repaired the tool call lifecycle for ACP sessions
- **Droid binary download** - Fixed an installation error when downloading the droid binary on some systems
- **Droid Computer reconnection** - Droid Computers now reconnect automatically on activity (Factory App)
- **Clearer daemon error messages** - Improved daemon error messaging in the Factory App

## CLI v0.120.0 · Desktop v0.77.0 (May 6, 2026)

Per-user Droid Computer controls, Slack auto-run buttons, Windows performance, and stability fixes

### New features

- **Per-user Droid Computer controls** - Admins can now toggle managed and bring-your-own-machine (BYOM) Droid Computers on a per-user basis (Factory App)

### Improvements

- **Windows performance** - Sped up CLI responsiveness on Windows
- **More reliable OpenAI file edits** - File edits now use the native patch tool for better reliability on OpenAI models

### Bug fixes

- **Wrapped hyperlink targets** - Hyperlinks that wrap across lines now preserve the correct target
- **Working directory after Droid Computer change** - The working directory is now restored when the selected Droid Computer changes (Factory App)
- **Non-ASCII paths on Windows** - Native Windows tools now handle non-ASCII paths correctly
- **Repeated context management notices** - Stopped showing the same context management notice multiple times in a row
- **Windows daemon port retry** - Daemon now retries binding correctly when a port is already in use on Windows
- **Plan cache after upgrade** - Organization cache now refreshes after plan changes so the new plan appears immediately (Factory App)
- **Droid Shield reliability** - Additional fixes to Droid Shield
- **Applying patch header** - Removed a redundant "applying patch" header
- **Droid message crash** - Fixed a rare crash when rendering droid messages (Factory App)
- **Payment methods for new organizations** - Organizations without a billing profile now see an empty payment method list instead of an error (Factory App)
- **Outdated thinking settings hint** - Removed a stale hint related to thinking settings

## CLI v0.119.0 · Desktop v0.76.0 (May 6, 2026)

Windows setup script, MCP menu revamp, sticky user messages, Wiki Run deletion, and stability fixes

### New features

- **Windows setup script** - New setup script simplifies installing the Droid CLI on Windows
- **MCP menu revamp** - Redesigned MCP menu for clearer server and tool management
- **Sticky user messages** - User messages stay anchored as you scroll, with a full-session view (Factory App)
- **Delete Wiki Runs** - You can now delete Wiki Runs directly from the Factory App

### Improvements

- **Factory App auto-updater UX** - Overhauled the Factory App auto-updater experience for a clearer update flow
- **Droid Computer wizard polish** - Streamlined the new Droid Computer wizard (Factory App)
- **Cleaner ask-user prompts** - Polished the ask-user prompt UI in the CLI
- **Refined Thinking/Exploring previews** - Tightened the look of Thinking and Exploring summary previews
- **Light mode chat polish** - Improved chat styling in light mode
- **Missions overage error clarity** - Distinguishes Missions overage network errors from generic failures

### Bug fixes

- **Status line working directory** - Status line now uses the last known working directory instead of a stale path
- **AutoWiki history dropdown** - AutoWiki history dropdown is no longer cut off by the surrounding layout (Factory App)
- **BYOK reasoning effort range** - Full reasoning effort range now applies to custom BYOK models
- **Stale custom provider routing** - Fixed stale routing persisting across custom BYOK provider switches
- **Download Factory App banner on web** - "Download Factory App" banner no longer appears on the web
- **Session switching flicker** - Fixed flickering when switching between sessions (Factory App)
- **Hibernated Droid Computers for delegations** - Linear and Slack delegations now wake hibernated Droid Computers reliably
- **Credits dashboard pricing** - Credits dashboard now works for accounts with multiple price intervals (Factory App)

## CLI v0.118.1 · Desktop v0.75.1 (May 5, 2026)

Custom working directory for sessions created via the public API

### New features

- **Custom working directory for sessions** - The public Sessions API now accepts an optional `cwd` field to start Droid Computer-backed sessions in a specific directory

### Bug fixes

- **Clearer working directory errors** - Invalid working directories now fail fast with a structured error instead of silently falling back to the wrong directory

## CLI v0.118.0 · Desktop v0.75.0 (May 4, 2026)

Smarter readiness hints, bulk user limit updates, live streaming in the app, and CLI stability fixes

### New features

- **Live streaming in the Factory App** - Factory App now streams partial text and thinking updates as a droid works
- **Bulk Usage Limit updates** - Admins can update Usage Limits for multiple users at once (Factory App)

### Improvements

- **Smarter readiness hints** - Readiness hints now detect more cases where guidance helps before continuing
- **Localized review findings** - Review findings now match your language instead of the source file's language
- **Plus plan rename** - Pro Plus has been renamed to Plus throughout the product
- **Directory-managed roles** - Role dropdown is now disabled for users managed by directory sync (Factory App)

### Bug fixes

- **Paused response recovery** - Improved recovery from paused model responses
- **System notification color** - Fixed color of system notification body copy
- **Slack session link unfurls** - Session links no longer auto-unfurl in Slack threads
- **Slack persona on replies** - Droid persona is now preserved on Slack replies

## CLI v0.117.0 · Desktop v0.74.0 (May 3, 2026)

Members settings page, Individual plans, billing address at checkout, and CLI stability fixes

### Improvements

- **Individual plans** - Self-serve plans are now grouped under Individual, with smoother loading states (Factory App)
- **Sharper LLM error classification** - Overloaded and context-length errors now surface as their own error types

### Bug fixes

- **Execute summary while streaming** - Execute tool summary is now hidden while a response is still streaming
- **Chat log polish** - Minor visual fixes to the chat log
- **/missions reminder in Mission Mode** - The /missions system reminder no longer shows when you're already in Mission Mode
- **Empty template cloud session** - Submitting a cloud session with an empty template now works (Factory App)
- **Thinking signature recovery** - Improved recovery from interrupted thinking signatures

## CLI v0.116.0 · Desktop v0.73.0 (May 2, 2026)

Runtime-aware Execute tool, no-report readiness hint, payment method in onboarding, and CLI stability fixes

### New features

- **Runtime-aware Execute tool** - Execute tool descriptions now adapt to your runtime, with WSL-specific guidance and an expanded bashism detector
- **No-report readiness hint** - CLI surfaces a dynamic hint when a report isn't needed
- **Payment method in onboarding** - You can now add a payment method during the final onboarding step (Factory App)

### Bug fixes

- **Lingering prompts after resume** - User prompts are now cleared correctly after a droid resumes
- **Gemini turn handling** - Scoped Gemini reasoning signals to the active turn for more reliable continuations
- **Billing error classification** - Payment-required responses now surface as billing errors instead of generic invalid-request errors
- **Working directory persistence** - Validated working directory is now persisted and locked until the Droid Computer connects (Factory App)
- **Droid Computer details on transient errors** - Droid Computer details now remain visible during transient query errors (Factory App)
- **Factory App updater download** - Factory App updater now downloads the new version only after you click to install

## CLI v0.115.0 · Desktop v0.72.0 (May 1, 2026)

PDF support for Gemini 3.1 Pro, GLM-5.1 reasoning, bulk image drag-and-drop, PDF uploads in app, and CLI stability fixes

### New features

- **PDF support for Gemini 3.1 Pro** - Gemini 3.1 Pro now accepts PDF inputs
- **GLM-5.1 reasoning** - Added reasoning support for GLM-5.1
- **Bulk image drag-and-drop** - Drop multiple images into the CLI at once
- **PDF uploads** - Upload PDF files directly in chat (Factory App)
- **No Droid Computer state on new session** - The new session page now handles cases when no Droid Computers are available (Factory App)

### Improvements

- **Resilient session resume** - Resuming a session that references a retired model now triggers a clean model migration
- **Cloud sync stability** - Hardened cloud sync against session race conditions

### Bug fixes

- **Terminal tab title** - Terminal tab title now updates when the active session changes
- **Phantom lines in narrow terminals** - Fixed phantom lines that could appear in narrow terminals
- **Mermaid terminal rendering** - Guarded Mermaid diagram rendering in the terminal against crashes
- **Clearer auth errors** - Improved authentication error messages
- **ACP session cancellation** - You can now cancel ACP sessions, and the correct auth code is shown
- **Spinner rendering** - Fixed a spinner rendering issue
- **Linear delegation matching** - Relaxed matching in the Linear delegation picker (Factory App)
- **Session timeout messages** - Cleaner timeout messages and fixed a working directory error (Factory App)
- **Connection failure toasts** - Removed noisy connection failure toasts (Factory App)
- **Free trial onboarding** - Fixed a free trial onboarding issue (Factory App)
- **Subagent collapse** - Subagents now collapse correctly even when the parent is selected (Factory App)
- **AutoWiki export validation** - Hardened filename validation when exporting Wikis (Factory App)

## CLI v0.114.0 · Desktop v0.71.0 (April 30, 2026)

BYOM admin toggle, Droid Shield push-scan refinement, Windows Python execution fix, and CLI stability fixes

### New features

- **BYOM admin toggle** - Organization admins can now enable or disable bring-your-own-machine (BYOM) Droid Computers from enterprise settings (Factory App)

### Improvements

- **Droid Shield push scan** - Push scanning now targets only commits not yet on any remote, reducing duplicate scans
- **AutoWiki UI polish** - Visual refinements across the AutoWiki interface (Factory App)

### Bug fixes

- **Agent loop continuation** - Agent loop now continues when a model response has no visible output
- **Bash result spacing** - Removed an unwanted gap between bash commands and their results
- **AskUser answer alignment** - Your own answer row in AskUser is now aligned with other rows
- **Windows Python execution** - Python commands run on Windows now use a UTF-8 environment by default

## CLI v0.113.0 · Desktop v0.70.0 (April 29, 2026)

Mission Control shortcuts, deny-list explanations, force-kill occupied ports, draft messages, and CLI stability fixes

### New features

- **Mission Control shortcuts** - New `g`/`G` keyboard shortcuts to jump between workers and the features list in Mission Control
- **Deny-list command explanations** - CLI now explains why a command was deny-listed when prompting for approval
- **Force-kill occupied ports** - Reclaim a port that's already in use directly from the CLI
- **Readiness hints** - CLI now surfaces occasional readiness hints to help guide your next step
- **Draft messages** - Save and resume in-progress chat messages between sessions (Factory App)

### Improvements

- **Randomized Academy quiz options** - Quiz answer choices are now randomized per question (Factory App)
- **Cloud Machines status label** - Renamed Cloud Machines status from "deprecated" to "superseded" (Factory App)
- **Draggable window during startup** - Factory App window stays draggable while the app finishes loading

### Bug fixes

- **Git AI attribution** - Git AI attribution now records commit authors correctly
- **Mission skill validation** - Mission skills are now validated when starting a mission run
- **Archived sessions** - CLI no longer pulls archived sessions
- **Slack delegation formatting** - Slack-delegated sessions now respond using Slack-native formatting
- **Fewer Git diff failures** - Reduced intermittent Git diff failures during sessions
- **Invite seat limits** - Invite flow now consistently enforces organization seat limits (Factory App)
- **Default model selection** - New sessions now validate the persisted model against available models (Factory App)
- **Long repository URLs** - Avoided request errors when repository names made GET URLs too long (Factory App)
- **Academy callouts** - Academy markdown callouts now render reliably (Factory App)
- **Chat scrolling** - Fixed several scrolling issues in the chat area (Factory App)
- **macOS Factory App updater** - Fixed the Factory App auto-updater on macOS

## CLI v0.112.0 · Desktop v0.69.0 (April 28, 2026)

DeepSeek V4 Pro support, MCP elicitation resume, security review on by default, and CLI stability fixes

### New features

- **DeepSeek V4 Pro** - Added support for the DeepSeek V4 Pro model
- **Resume MCP elicitations** - Elicitation prompts from MCP tools can now be resumed after interruption
- **Extra-usage payment status** - Failed and succeeded extra-usage payment statuses are now surfaced in the payment modal (Factory App)

### Improvements

- **Security review on by default** - The security-review skill is now enabled by default
- **Non-retryable 4xx responses** - 4xx responses (other than 429) are no longer retried, so failures surface faster
- **Persistent Slack loading status** - Slack loading indicators now stay visible past status updates for clearer progress feedback (Factory App)

### Bug fixes

- **ApplyPatch absolute paths** - Absolute paths are now honored verbatim in the ApplyPatch tool
- **Working directory redraw** - Fixed working directory redraw and fork `cwd` overrides
- **Missions model settings** - Missions model settings are now snapshotted at launch so they don't drift mid-run
- **Custom statusline** - Custom statusline now uses session-scoped data instead of leaking across sessions
- **Model-switch tool history** - Tool history is now sanitized when switching models to prevent rendering issues
- **Context window error detection** - Recognize additional context-window error phrasings so recovery is more reliable
- **Spec approval comments** - Spec approval comments now align with conversation messages
- **Factory App local default** - Factory App now consistently defaults to local connections
- **Onboarding loading state** - Fixed a stuck loading state during onboarding (Factory App)

## CLI v0.111.0 · Desktop v0.68.0 (April 28, 2026)

Italian translations, interval loop command, refreshed hooks UI, faster Grep, and CLI stability fixes

### New features

- **Italian translations** - The Droid CLI is now available in Italian
- **`interval` loop command** - New CLI command for running tasks on an interval
- **Refreshed hooks UI** - Updated UI for managing hooks
- **Custom commands in Task prompts** - Task tool prompts now expand resolved custom slash commands
- **Chat transcript scroll keybinds** - New keyboard shortcuts to jump between turns in the chat view
- **Missions Rate Limits** - Missions now handle Rate Limit responses gracefully
- **Missions entry overage gating** - Missions entry now respects your organization's overage preference
- **Per-run automation viewer** - New visual viewer to inspect each automation run (Factory App)
- **Model access table** - New UI for managing organization-level model access (Factory App)
- **Factory Academy certification tiers** - Detect certification tiers and expanded quizzes to 30 questions (Factory App)

### Improvements

- **Faster Grep tool** - Grep tool now uses a hybrid ripgrep engine for better performance
- **Stronger secret scrubbing** - Expanded secret scrubber patterns and applied scrubbing to Read tool output
- **Faster `/new` and `/clear`** - Daemon session is now eagerly initialized on `/new` and `/clear`
- **Centered settings on wide screens** - Settings content is now capped at 1024px and centered on wide displays (Factory App)
- **Clearer schedule timezones** - Automation schedule timezone and run history timestamps are clearer (Factory App)
- **Devtools shortcut in Factory App** - Re-enabled the devtools keyboard shortcut in production builds
- **Clearer seat-limit errors** - Clearer error message when inviting members beyond your seat limit (Factory App)
- **Native Slack loading status** - Slack now uses native loading status indicators (Factory App)

### Bug fixes

- **Subagents during silent tools** - Task subagents are now kept alive during silent execution
- **Execute preview rendering** - Bounded Execute tool preview rendering to prevent layout issues
- **Execute approval rendering** - Stabilized rendering during Execute tool approvals
- **Image paste on Linux/SSH** - Fixed image paste in Ghostty on Linux and over SSH
- **Skill and droid preview scroll** - Skill and droid previews now scroll with arrow keys
- **Chat Esc sequence** - Codified Esc key behavior in chat
- **Spec mode editor flow** - Unblocked the spec edit flow when the editor opens via the system default
- **Terminal indicator on Windows** - Hidden the terminal indicator on Windows in the footer
- **Spec confirmation status** - Spec confirmation status is now gated on tool confirmation state
- **Missions wake-lock leaks on Linux** - Prevented wake-lock leaks during Missions runs on Linux
- **Skills rendering** - Fixed a parsing issue when rendering skills
- **Subagent nesting** - Fixed nesting of subagents in the UI (Factory App)
- **Cloud-synced Droid Computer sessions** - Cloud-synced Droid Computer sessions now display correctly (Factory App)
- **Login screen error toast** - Suppressed an `/auth/me` error toast on the login screen (Factory App)
- **Slack thread replies** - Slack now only forwards thread replies via `app_mention` (Factory App)
- **Empty GitHub repos** - Added support for empty GitHub repositories (Factory App)
- **Daemon directory paths** - Directory paths are now normalized in the daemon and render properly in the frontend (Factory App)

## CLI v0.109.3 · Desktop v0.66.3 (April 26, 2026)

Auto-fallback to Droid Core, per-tool MCP autonomy overrides, Factory App system theming, and CLI stability fixes

### New features

- **Auto-fallback to Droid Core** - Sessions that hit Rate Limits now automatically fall back to Droid Core when your overage preference is set to Droid Core
- **Per-tool MCP autonomy overrides** - New `mcpAutonomyOverrides` setting lets you configure autonomy levels for individual MCP tools
- **System theming** - Factory App now follows your system theme
- **New Factory App updater** - Improved auto-update flow for the Factory App
- **Per-channel Slack auto-run model** - Choose which model is used for each Slack auto-run channel (Factory App)

### Improvements

- **Larger Droid Shield buffer** - Increased Droid Shield max buffer from 20MB to 64MB to handle larger outputs
- **Faster hibernation detection** - Droid Computer hibernation is now detected more quickly
- **Sorted model list** - CLI model list is now sorted by release date, newest first
- **Cleaner MCP tool parameters** - MCP tool parameters show truncated JSON instead of `[object Object]`

### Bug fixes

- **Lost subagent output** - Fixed an issue where subagent output could be lost
- **MCP tool selection refresh** - Tool selection now refreshes after MCP updates
- **Slash command initialization** - Slash commands now wait for initialization to finish before running
- **Spec mode approval comments** - Spec approval comments now work in both live and resumed sessions
- **`--auto` level in exec runs** - `--auto` level is now applied in exec runs even when the session inherits spec mode
- **Tool confirmation state** - Restored correct tool execution state after a tool-confirmation approval
- **Settings theme control alignment** - Fixed alignment of the settings theme control
- **Stray hover glyphs** - Removed unintended active hover glyphs
- **Windows worker reliability** - Added retries for Windows Job Object spawn failures
- **Settings folder watcher** - Switched to native recursive watching for the settings folder
- **Cron schedules in UTC** - Scheduled Missions runs now evaluate cron expressions in UTC
- **Clearer paywall errors on Droid Computer routes** - Droid Computer routes now return a clear error when accessed from a non-paying organization
- **Slack multi-turn delegation** - Fixed multi-turn delegation when running from Slack
- **Factory App auth timeout fallback** - Fixed an auth timeout fallback in the Factory App
- **App UI polish** - Fixed various spacing, color, and chevron issues (Factory App)

## CLI v0.109.1 · Desktop v0.66.1 (April 23, 2026)

Fast-mode toggle, Droid Computer improvements, Missions artifact validation, and CLI stability fixes

### New features

- **Fast-mode toggle** - Single opt-in toggle to enable fast-mode model variants
- **Droid Computer registration improvements** - Smoother register/remove flow with better handling of duplicate Droid Computer names
- **Missions artifact validation** - Missions artifacts are now schema-validated on create, edit, and apply-patch

### Improvements

- **Faster Windows worker startup** - Reduced worker startup latency on Windows
- **Cleaner Ctrl+O transcripts** - Verbose transcript bodies are now hidden for easier reading
- **Quieter CLI logs** - Reduced noisy log volume during normal use
- **Mermaid rendering** - Various improvements to Mermaid diagram rendering

### Bug fixes

- **Spec mode approval flow** - Stabilized the approval flow in spec mode
- **IDE diagnostics on disconnect** - Guarded against errors when the IDE client is disconnected
- **Background process cleanup** - Background processes are now cleaned up when the CLI exits
- **Sessions during silent tools** - Sessions are kept alive during silent tool execution
- **Session tool IDs** - Session `enabledToolIds` are now treated as additive
- **Secret scanner on large diffs** - Improved secret scanner reliability on large diffs
- **`/rename` persistence** - `/rename` now persists across daemon sync and refreshes the cloud title (Factory App)
- **Auto-allow-new toggle** - Toggling auto-allow-new no longer clears every model (Factory App)
- **Integration modal** - Stabilized the Integration Management modal's height and scrolling (Factory App)
- **On-demand pagination** - Replaced "Load All" with proper on-demand pagination (Factory App)
- **GitLab integration reliability** - Fixed an out-of-memory issue in the GitLab integration (Factory App)

## CLI v0.108.0 · Desktop v0.65.0 (April 22, 2026)

Consolidated Missions files, compute usage on billing pages, and CLI stability fixes

### New features

- **Consolidated Missions files** - Files related to Missions now live together under `~/.factory` for easier discoverability
- **Compute usage on billing pages** - Billing and usage pages now surface compute usage alongside other usage data (Factory App)

### Bug fixes

- **Missions wake-lock on Linux** - Missions wake-lock now also blocks idle and lid-switch suspend so long-running Missions runs aren't interrupted
- **Terminal focus feedback loop** - Fixed a terminal focus-in feedback loop in the TUI
- **JSON-RPC error handling** - Improved error handling for JSON-RPC communication
- **Subagents in sidebar** - Restored subagents in the sidebar (Factory App)

## CLI v0.106.0 · Desktop v0.63.0 (April 21, 2026)

New /btw command, upgraded /copy selector, full-project security audit, and CLI stability fixes

### New features

- **`/btw` command** - New `/btw` slash command for sending side messages to the current session
- **Upgraded `/copy` selector** - Improved selector UI for the `/copy` command
- **Full-project security audit** - New full-project audit mode in the security-review skill
- **`/copy` slash command** - `/copy` slash command and user message hover actions are now available in the app (Factory App)
- **Search by session ID** - Search sessions directly by session ID (Factory App)
- **Member role filter** - Filter the organization members list by role (Factory App)

### Improvements

- **Timeout error handling** - Improved handling of timeout errors with longer retry delays
- **Corporate network error detection** - Corporate firewall, DNS, and TLS errors are now treated as non-retryable
- **Context limit classification** - Requests exceeding a model's context window are now classified as context-limit errors with clearer messaging

### Bug fixes

- **Subagent permission requests** - Subagent permission requests are now auto-rejected instead of crashing the session
- **Auto suggestions after command** - Auto suggestions no longer appear after a command is accepted
- **Auth error retries** - 401 and 403 authentication errors are no longer retried
- **Default model preserved** - The user's configured default model is no longer rewritten on reads
- **Dismissed handoff items** - Dismissed handoff items are now preserved during validation
- **Bug report fallback** - Bug reports now fall back to local submission when the background daemon is unavailable
- **Factory API key scoping** - The Factory API key list is now scoped to your current organization (Factory App)
- **Slack session owner across pages** - The saved Slack Session Owner is now correctly shown across paginated org member lists (Factory App)
- **Single pinned session** - Fixed an issue that allowed multiple pinned sessions in the sidebar (Factory App)

## CLI v0.105.1 · Desktop v0.62.0 (April 21, 2026)

Spec mode option picker refinements and CLI stability fixes

### Improvements

- **Spec mode option selection** - Simplified the flow for choosing between multiple proposal options in spec mode
- **`droid computer list` output** - Hides the default "active" status column for cleaner output

### Bug fixes

- **Kimi tool call handling** - Fixed an issue with Kimi tool calls that could cause stream errors
- **Auto-update on exit** - CLI now waits for in-flight auto-updates to finish before exiting to avoid interrupted installs
- **Droid Computer connection reliability** - Better detection and recovery when a Droid Computer connection stalls
- **Droid Computer connection warning** - Suppressed a spurious "Failed to get computer connection state" warning (Factory App)
- **Onboarding wizard display** - Fixed display issues in the onboarding wizard (Factory App)
- **Send button when disconnected** - Send button is now properly disabled in disconnected sessions (Factory App)
- **Banner import error** - Fixed a banner import error (Factory App)
- **Sidebar grouping collapse** - Fixed unrelated groups collapsing together in the sidebar (Factory App)

## CLI v0.105.0 · Desktop v0.61.0 (April 20, 2026)

Kimi K2.6 support, simplify built-in skill, AutoWiki / GitHub Wiki sync, and CLI stability fixes

### New features

- **Kimi K2.6 support** - Added support for the Kimi K2.6 model
- **Simplify built-in skill** - Simplify is now a built-in skill, no installation required
- **AutoWiki / GitHub Wiki sync** - Wikis generated by AutoWiki can now sync to GitHub Wiki, with additional Wiki reader fixes
- **Managed Droid Computer enterprise control** - New managed Droid Computer toggle in enterprise controls (Factory App)
- **Missions access policy** - Enterprise admins can now control access to Missions
- **Session title in browser tab** - Factory App sessions now use the session title as the page title
- **Revamped Droid Computer creation** - Redesigned flow for creating Droid Computers (Factory App)
- **Nested sidebar** - Sidebar now supports nesting along with other polish improvements (Factory App)
- **Droid Computer connection status** - Machine selector now shows the connection status for each Droid Computer (Factory App)

### Improvements

- **Compaction model for BYOK** - Compaction now defaults to your current model and is used for BYOK
- **PowerShell syntax warning** - Execute tool now detects PowerShell and warns when Bash syntax is used
- **Windows path normalization** - Glob tool now returns normalized backslash paths on Windows

### Bug fixes

- **Spec option selection** - Fixed the user-selected spec option not being passed to the model
- **Execute tool header** - Fixed the last character being clipped in the Execute tool header
- **Invalid JSON rendering** - JSON renderer now hides output when the JSON is invalid
- **Review guidelines skill** - CLI now handles a missing review-guidelines skill gracefully
- **Tool cancel interrupts** - Follow-up prompts now wait for tool-cancel interrupts to settle
- **TUI daemon session switching** - Previous TUI daemon session now closes only after the next one loads
- **Session title updates** - Daemon session title updates now reflect in the terminal tab
- **Missions worker permissions** - Missions worker permission requests are now auto-denied
- **Thinking traces in web chat** - Thinking traces now appear in session chat on the web
- **Ripgrep startup** - Fixed intermittent startup errors when initializing the bundled ripgrep binary
- **Truncated stream handling** - Improved error handling when model response streams are truncated
- **Stuck "Show more"** - Fixed a stuck "Show more" button after creating a session on a new Droid Computer (Factory App)
- **Slack session-owner picker** - Picker now uses server-side search with infinite scroll (Factory App)
- **Sidebar hover and selection** - Fixed hover states and highlighting in the sidebar (Factory App)
- **401 errors when logged out** - Suppressed 401 errors after logging out (Factory App)
- **Stuck loading state** - Fixed a stuck loading state in the app (Factory App)
- **Add Project modal directory** - Modal now picks up the current directory from the native browse dialog (Factory App)
- **Local machine option** - Hidden outside of the Factory App

## CLI v0.104.0 · Desktop v0.60.0 (April 17, 2026)

Custom ripgrep path, BYOK config in bug reports, and CLI stability fixes

### New features

- **Custom ripgrep path** - New environment variable to point Factory at a custom ripgrep binary
- **BYOK config in bug reports** - Bug reports now include resolved BYOK configuration to make troubleshooting easier

### Improvements

- **Full Execute command in approval** - The approval dialog now shows the full command that will run
- **Selected confirmation option visibility** - The selected option in tool confirmation prompts is now bolded for better visibility
- **Hidden daemon log output** - Background daemon output no longer appears in the session

### Bug fixes

- **Spec edits in confirmation flow** - Fixed spec edits being dropped during the confirmation flow
- **Manual spec edits respected** - Fixed manual edits to specs not being preserved during handoff
- **Image upload compression** - Fixed image upload compression issues
- **Assistant active timer** - Fixed the assistant active timer not persisting across unmounts
- **Daemon connection and bug reports** - Fixed daemon connection issues and bug report errors (Factory App)
- **Local reconnect on machine change** - Local machine reconnect now works reliably when switching connections, with a clearer warning when not connected (Factory App)
- **Tool rendering parity** - Improved DefaultTool and TaskTool rendering to match the CLI (Factory App)
- **ApplyPatch diff rendering** - Fixed ApplyPatch tool diff rendering for the CLI input format (Factory App)

## CLI v0.103.0 · Desktop v0.59.0 (April 16, 2026)

Sessions page redesign, dead code detection in reviews, and CLI stability fixes

### New features

- **Sessions page redesign** - The sessions page has been refreshed with a new layout and design (Factory App)

### Improvements

- **Denied command confirmation** - Redesigned the confirmation UI when running blocked or risky commands
- **Dead code detection in reviews** - Code review now detects dead and unused code
- **QA report formatting** - QA skill now includes structured report format sections

### Bug fixes

- **File overwriting** - File creation and patch tools can now properly overwrite existing files
- **Model selection after spec approval** - Fixed the session model not being restored after approving a spec
- **Inactive session reload** - Fixed inactive TUI sessions not reloading on demand
- **Parallel tool calls in spec mode** - Fixed tool calls running in parallel incorrectly during spec approval
- **Skill details refresh** - Fixed selected skill details not updating when the skills list changes (Factory App)

## CLI v0.102.0 · Desktop v0.58.0 (April 15, 2026)

Security review checks, AutoWiki images, and CLI stability fixes

### New features

- **Security review checks** - Code review now includes security checks for OWASP Top 10 vulnerabilities, LLM-specific risks, and supply chain issues
- **AutoWiki images** - AutoWiki pages now support and display embedded images

### Improvements

- **Max autonomy enforcement** - App now properly enforces max autonomy settings (Factory App)
- **Large PR review support** - CLI now gracefully handles large PR diffs by using local git diff as a fallback

### Bug fixes

- **Spec approval comments** - Fixed spec approval comments not being preserved during handoff
- **Tool result spacing** - Fixed excessive margin between tool header and result in the CLI
- **Mermaid diagram rendering** - Fixed rendering issues with mermaid diagrams on the web
- **Personal integrations visibility** - Fixed personal integrations not showing for regular users (Factory App)

## CLI v0.101.0 · Desktop v0.57.0 (April 14, 2026)

New /install-slack-app command, spinner redesign, and CLI stability fixes

### New features

- **`/install-slack-app` command** - New `/install-slack-app` command to set up the Slack app integration for your workspace

### Improvements

- **CLI spinner redesign** - Updated CLI spinner animation for a refreshed look
- **Usage Limit warning** - Warning banner now shown when setting a global Usage Limit (Factory App)
- **Droid Computer source control warning** - Warning displayed when creating a Droid Computer without source control configured (Factory App)
- **Usage Limits clarity** - Usage Limits now clearly display values in millions of Factory Standard Credits (Factory App)

### Bug fixes

- **File tool accuracy** - File tools now use the actual filesystem state for more reliable results
- **File edit previews** - Fixed structured previews not displaying correctly for file edit results
- **Duplicate spec sessions** - Fixed duplicate sessions being created during spec handoff

## CLI v0.100.0 · Desktop v0.55.0 (April 13, 2026)

API key creation now available for all organization members

### Improvements

- **API key creation for all members** - All organization members can now create API keys, previously limited to managers and owners (Factory App)

## CLI v0.99.0 · Desktop v0.54.0 (April 10, 2026)

Incremental AutoWiki refreshes, themed mermaid diagrams, AutoWiki search, and CLI stability fixes

### New features

- **Incremental AutoWiki refreshes** - AutoWiki refreshes now only update changed pages for faster updates
- **Themed mermaid diagram colors** - Mermaid diagrams now render with per-element colors that match your current theme
- **AutoWiki search and exports** - AutoWiki now supports keyword search, skill browsing, and page exports (Factory App)

### Bug fixes

- **Theme background override** - Fixed terminal theme background being overridden unexpectedly
- **BYOK base URL switching** - Fixed client connections not being refreshed after switching custom API base URLs
- **Context model inheritance** - Fixed context management not using the current session model
- **Spec editor terminal handoff** - Fixed spec editor not properly completing terminal handoff
- **MCP auth cancellation** - Fixed pending MCP authentication not being cancelled when closing the MCP panel
- **Tool result display** - Fixed a crash when tool results contain non-string values
- **Custom model stability** - Fixed custom model IDs changing unexpectedly between sessions
- **Directory not found error** - Directory not found errors now appear immediately when confirming a directory (Factory App)
- **BYOK Rate Limits** - BYOK users can now continue chatting when platform Rate Limits are reached (Factory App)
- **Ghost tool calls** - Fixed phantom tool calls appearing during message processing
- **Chat input** - Fixed various chat input issues (Factory App)
- **Droid Computer terminal** - Fixed terminal display issues when using Droid Computers (Factory App)
- **Machine config modal** - Fixed machine configuration modal not displaying correctly (Factory App)
- **Reasoning and model selection** - Fixed reasoning level and model selection issues (Factory App)

## CLI v0.98.0 · Desktop v0.53.0 (April 9, 2026)

Install code review skill, session renaming, Spotlight search, and CLI stability fixes

### New features

- **Install code review skill** - New built-in skill for setting up automated code review in your project
- **Session renaming** - Rename sessions directly from the app (Factory App)
- **macOS Spotlight discoverability** - Factory App is now easier to find via macOS Spotlight search

### Improvements

- **Install QA skill upgrade** - The install-qa skill now learns from test failures to improve over time
- **Faster AutoWiki loading** - Optimized AutoWiki page loading for reduced latency (Factory App)

### Bug fixes

- **Terminal palette override** - Fixed terminal color palette being overridden unexpectedly
- **Droid Shield SSH key detection** - Fixed Droid Shield incorrectly flagging SSH public keys as secrets
- **Droid Computer sessions display** - Fixed sessions not appearing when run on Droid Computers without a local directory (Factory App)
- **Droid Computer SSH** - Fixed SSH connectivity issues with Droid Computers
- **Tool status text** - Restored the "invoking tools" status indicator during tool execution
- **Escape key after spec handoff** - Fixed Escape key cancellation not working after spec approval handoff
- **Session sidebar** - Fixed various sidebar display issues (Factory App)
- **Certificate loading** - Fixed certificate loading issues that could affect connectivity
- **Chat and tool results** - Fixed display issues with chat messages and tool results (Factory App)
- **Local machine connection toggle** - Fixed the local machine connection toggle not being respected when turned off (Factory App)

## CLI v0.97.0 · Desktop v0.52.0 (April 8, 2026)

New /cwd command, GLM-5.1 model support, diff viewer for Droid Computers, and CLI stability fixes

### New features

- **`/cwd` command** - New `/cwd` command and `--cwd` startup flag to set or change the working directory for your session
- **GLM-5.1 model support** - Added GLM-5.1 as an available model option
- **Diff viewer for Droid Computers** - Added diff viewer support for viewing file changes in Droid Computers (Factory App)

### Improvements

- **Execute approval display** - Pending Execute approvals are now truncated for readability while preserving the full view via Ctrl+O

### Bug fixes

- **AskUser layout** - Fixed alignment and spacing issues in the AskUser prompt (Factory App)
- **Theme consistency on startup** - Fixed terminal theme overrides not being applied consistently on startup
- **Kitty terminal over SSH** - Fixed Ctrl+D handling in Kitty terminal when connected over SSH
- **Session settings** - Fixed settings not being applied correctly when creating a new session

## CLI v0.96.0 · Desktop v0.51.0 (April 7, 2026)

New /install-qa command, design.md support, Cmd+N for new sessions, and CLI stability fixes

### New features

- **`/install-qa` command** - New `/install-qa` command to generate automated QA skills for your project
- **`design.md` support** - CLI now supports `design.md` files alongside `agents.md` for providing design guidelines to your droid
- **Cmd+N for new session** - Use Cmd+N keyboard shortcut to quickly start a new session (Factory App)
- **Session disambiguation** - Sessions with the same name now display the full path in a tooltip for easier identification (Factory App)
- **Pre-session bug reports** - Submit bug reports from the Factory App even when no session is active

### Improvements

- **Bash mode output redesign** - Bash mode output now matches the execute tool display for a more consistent look
- **MCP tool confirmation display** - Restyled MCP tool display in the confirmation popup for better readability
- **Light mode colors** - Improved color consistency in light mode by migrating hardcoded colors to the theme system
- **Archived session access** - Archived sessions can now be viewed in read-only mode and restored when accessed directly (Factory App)
- **Consistent hover states** - All option items now have consistent hover state styling (Factory App)
- **Factory App UI polish** - Various visual refinements across the Factory App

### Bug fixes

- **Duplicate tool call messages** - Fixed duplicate tool call messages and missing updates during tool execution
- **Missions feature counts** - Fixed incorrect feature counts in `/missions`
- **Escape key handling** - Fixed prompt handling issues after pressing Escape
- **Terminal input security** - Hardened terminal input capture for improved security
- **Session creation** - Fixed an issue where sessions could be created with an empty working directory (Factory App)
- **Profile dropdown styling** - Refined profile dropdown and menu item styling (Factory App)
- **Font size consistency** - Fixed font size mismatch in the Droid Computers section (Factory App)
- **Sidebar layout** - Fixed session group header to span the full sidebar width (Factory App)

## CLI v0.95.0 · Desktop v0.50.0 (April 6, 2026)

Redesigned help menu, green progress bars, faster session reload, and CLI stability fixes

### New features

- **Redesigned help menu** - The help menu has been completely revamped with improved layout and organization
- **Green progress bars** - Progress bars now display in green while commands are running

### Improvements

- **Faster session reload** - Sessions reload significantly faster for a smoother experience
- **CLI performance** - General performance improvements for faster CLI responsiveness
- **Light mode color refinements** - Improved color palette and theme refinements for light mode (Factory App)
- **Scrollable session view** - The entire session view is now scrollable for easier navigation (Factory App)
- **Theme-aware menu colors** - Selection colors in slash command menus now adapt to the current theme
- **Keyboard shortcut footer** - Improved keyboard shortcut display in slash command menus
- **Back navigation** - Secondary pages now show a cleaner "Back to App" navigation button (Factory App)

### Bug fixes

- **Execute tool name display** - Fixed the Execute tool name being truncated in pending state
- **Session freeze prevention** - Fixed session freezes caused by interactive commands in Bash Mode and Execute
- **Tool execution after interrupts** - Tools no longer continue executing after being interrupted
- **Subagent working directory** - Fixed subagents not inheriting the correct working directory
- **ANSI escape handling** - Fixed ANSI escape sequences leaking into the input prompt
- **Todo list display** - Fixed visual issues in the todo list display
- **Custom model validation** - Fixed validation errors when using custom models in Missions workers
- **Mission Control model selector** - Fixed the model selector in Mission Control
- **Exec mode reasoning output** - Reasoning events now properly appear in stream-json exec output
- **Sidebar collapse on Windows** - Fixed sidebar collapse button location on Windows (Factory App)
- **Loading spinner** - Fixed loading spinner display issues (Factory App)
- **Chat layout spacing** - Fixed left margin alignment in chat composer and content area (Factory App)

## CLI v0.94.0 · Desktop v0.49.0 (April 3, 2026)

/limits usage panel, credit usage countdown, model selector expansion, and CLI stability fixes

### New features

- **/limits usage panel** - New `/limits` command shows an interactive credit usage breakdown with bucket views
- **Credits Balance countdown** - Live countdown timer shows remaining Credits in real time (Factory App)
- **Model selector expansion** - Model selector now includes a "show more" option to browse additional models (Factory App)

### Improvements

- **Queued message redesign** - Queued messages now display with a cleaner, user-message-style layout
- **/plugins and /skills menu refresh** - `/plugins` and `/skills` menus now match the updated `/sessions` and `/model` UI style
- **Droid Shield placeholder detection** - Droid Shield now detects additional placeholder value patterns to better protect against accidental secret exposure

### Bug fixes

- **Worker hang fix** - Fixed a regression where blocked workers could cause the CLI to hang
- **Custom model streaming** - Fixed streaming errors when using custom models
- **Long prompt handling** - Fixed an issue where long prompts could fail when passed to subagents
- **Autonomy level cycling** - Fixed Ctrl+L not correctly cycling through autonomy levels
- **Kitty terminal fix** - Fixed additional input handling issues in Kitty terminal

## CLI v0.93.0 · Desktop v0.48.0 (April 2, 2026)

GPT-5.3-Codex fast mode, markdown links, automatic agents.md detection, and session retention policies

### New features

- **GPT-5.3-Codex fast mode** - Added GPT-5.3-Codex as a fast mode model option for faster code generation
- **Markdown link rendering** - Markdown links now render as clickable links in the CLI
- **Automatic agents.md detection** - CLI now automatically detects and loads agents.md files in your project
- **Session retention policies** - Configure auto-deletion policies for sessions to manage storage (Factory App)

### Improvements

- **Plan update indicator** - A subtle "Plan updated" notification now appears when the plan changes
- **JSON rendering in chat** - JSON data now renders with improved formatting in web and Factory App chat
- **Commands near autonomy requests** - Suggested commands now appear closer to autonomy requests for easier access (Factory App)

### Bug fixes

- **Review shows LGTM** - The review command now shows "LGTM" when no issues are found
- **Long output truncation** - Long output lines in Execute tool previews are now truncated to fit terminal width
- **Message ghosting** - Fixed ghost messages appearing when sending queued messages
- **Improved error messages** - Model streaming errors now display user-friendly messages instead of raw errors
- **Session loading** - Fixed various issues with loading and resuming sessions
- **Onboarding link** - Fixed a broken link in the onboarding flow (Factory App)
- **Mission Mode input** - Fixed input field behavior in Mission Mode (Factory App)

## CLI v0.92.0 · Desktop v0.47.0 (April 2, 2026)

Unified Missions menu, settings and footer redesign, session forking, TUI charts, and SSH clipboard fixes

### New features

- **Unified /missions menu** - Redesigned the `/missions` command with model tabs and improved navigation
- **/settings redesign** - Refreshed `/settings` menu with an updated layout
- **CLI footer redesign** - Redesigned CLI footer with a cleaner layout
- **Per-worker token breakdown** - Mission Control now shows token usage breakdown per worker
- **Session forking** - New `--fork` flag to create a new session by forking an existing one
- **TUI chart rendering** - Charts and graphs now render directly in the terminal
- **Exec mode system prompt flags** - New `--append-system-prompt` and `--append-system-prompt-file` flags for customizing system prompts in exec mode
- **Cloud-synced read-only sessions** - Cloud-synced sessions are now viewable in read-only mode (Factory App)
- **Configurable per-model context limits** - New setting to configure context token limits on a per-model basis

### Improvements

- **Session loading performance** - Optimized session loading for faster startup and reduced load times
- **Faster session search** - Session search is now significantly faster (Factory App)
- **Faster Factory App session loading** - Sessions load directly from disk in the Factory App for improved speed
- **Tool routing warnings** - Tool routing warnings now suggest model-specific alternatives
- **Default model indicator** - `/model` command now highlights which model is the default
- **SKILL.md support** - Built-in skills can now be loaded from SKILL.md files
- **Sidebar polish** - Modernized sidebar user profile and dropdown animations (Factory App)

### Bug fixes

- **Clipboard copy over SSH** - Clipboard copy now works reliably over SSH connections
- **VS Code multiline input** - Fixed multiline input handling in VS Code terminal
- **MCP authentication** - Restored MCP OAuth authentication flows
- **PDF page limit error** - Added a clear error message when exceeding the 100-page PDF limit
- **Terminal cleanup on exit** - Fixed terminal escape sequences persisting after CLI exit
- **Slash command settings** - Fixed `/fast`, `/enter-mission`, `/exit-mission`, and `/new` commands not applying settings correctly
- **Parallel tool rendering** - Fixed rendering issues with parallel tool executions
- **Ghostty and xterm input** - Fixed keyboard input handling in Ghostty and xterm terminals
- **Terminal multiplexer display** - Fixed screen clearing in terminal multiplexers like tmux and screen
- **Terminal focus recovery** - Fixed terminal focus not being recovered after window switching
- **AGENTS.md session loading** - AGENTS.md guidelines now load correctly when resuming existing sessions
- **Task tool background panel** - Fixed streaming and display issues in Task tool background panels
- **Fullscreen sidebar layout** - Fixed sidebar layout in fullscreen mode on macOS (Factory App)

## CLI v0.90.1 · Desktop v0.45.1 (March 30, 2026)

Light theme readability fix

### Bug fixes

- **Light theme readability** - Fixed user message colors and help bar shortcuts in the light theme for improved contrast and readability

## CLI v0.89.0 · Desktop v0.44.0 (March 27, 2026)

Spec mode redesign, Missions worker view, fuzzy model search, and cleaner tool output

### New features

- **Missions worker view** - New view for monitoring individual Missions worker progress and output

### Improvements

- **Spec mode redesign** - Redesigned spec mode with a refreshed layout and improved workflow
- **Fuzzy search in model selector** - Model selector now supports fuzzy search for easier model filtering
- **Cleaner tool output** - Grep and Glob tool calls now display with the same clean formatting as Read tool calls
- **Plan display polish** - Improved plan display formatting and cleaner worker output
- **Changelog dismissal** - Changelog now auto-hides after first view and can be manually dismissed
- **Billable Tokens renamed to Factory Standard Credits** - "Billable Tokens" renamed to "Factory Standard Credits" throughout the UI
- **Auto-updating plugins** - Installed plugins now auto-update on CLI startup

### Bug fixes

- **Missions worker stability** - Permission blocks in Missions workers no longer terminate the session
- **/exit-mission autocomplete** - `/exit-mission` autocomplete now only appears when actively in a mission
- **Empty message handling** - Fixed empty messages appearing in sessions

## CLI v0.87.0 · Desktop v0.42.0 (March 26, 2026)

Spec approval handoff, shimmer animations for tool headers, and Missions reliability improvements

### New features

- **Spec approval handoff** - Spec approvals can now be handed off to a new session, letting you continue work separately after approving a spec

### Improvements

- **Shimmer animation for tool headers** - Tool call headers now display a shimmer animation for improved visual feedback

### Bug fixes

- **Session storage reliability** - Fixed duplicate save errors and added automatic recovery from permission issues in session storage
- **Sidebar navigation** - Fixed missing back arrow in sidebar menu titles (Factory App)
- **Missions worker startup** - Improved Missions worker startup reliability with extended timeout
- **Missions connection stability** - Increased socket connection timeout for more reliable Missions connections
- **Droid Computer session creation** - Fixed errors when creating sessions while the Droid Computer is temporarily unavailable (Factory App)

## CLI v0.86.0 · Desktop v0.41.0 (March 25, 2026)

/context slash command, automation sharing and forking, OS-level sandboxing, and terminal fixes

### New features

- **/context slash command** - New `/context` command shows a breakdown of token usage in your current session
- **OS-level sandboxing** - Added OS-level sandboxing for enhanced security when running CLI tools

### Improvements

- **Ask question tool redesign** - Redesigned the Ask Question tool with improved text wrapping and layout

### Bug fixes

- **Kitty terminal keypad keys** - Fixed keypad keys not working correctly in Kitty terminal
- **Slack DM reliability** - Fixed bot message feedback loops in Slack DMs

## CLI v0.85.0 · Desktop v0.40.0 (March 24, 2026)

Session settings override, SSE for remote MCP servers, sidebar animations, and reliability fixes

### New features

- **Session settings override** - Project and folder-level settings can now override organization session defaults
- **SSE support for remote MCP servers** - Remote MCP servers now support Server-Sent Events (SSE) transport

### Improvements

- **Session group animations** - Session groups now animate smoothly when collapsing and expanding (Factory App)
- **AutoWiki sidebar polish** - Improved AutoWiki sidebar design with smoother pan transitions (Factory App)
- **Skills browser scrolling** - Improved scrollbar styling in the Skills browser (Factory App)
- **Managed settings error messages** - Clearer error messages when loading managed settings

### Bug fixes

- **Session titles** - Fixed session titles intermittently displaying incorrectly (Factory App)
- **Missions worker BYOK settings** - Fixed Missions worker settings not persisting correctly when using custom API keys
- **Session ID display** - Fixed session IDs being truncated (Factory App)
- **Background process reliability** - Hardened background process and task store against data corruption
- **Spec mode file edits** - Fixed file edits to .factory/specs being blocked during spec mode
- **Chat message alignment** - Fixed user message text not aligning with droid answers
- **Directory selector stability** - Fixed directory selector jiggling when switching directories (Factory App)
- **Keyboard shortcuts** - Restored keyboard shortcuts in the app (Factory App)
- **Session list display** - Fixed session list not showing enough sessions
- **Droid Computer connection reliability** - Improved timeouts for initial Droid Computer connections (Factory App)
- **Unknown model handling** - Fixed handling of unknown model IDs

## CLI v0.84.0 · Desktop v0.39.0 (March 23, 2026)

Header redesign, Execute tool syntax highlighting, session type tags, and skill execution fixes

### New features

- **Header redesign** - Refreshed CLI header with an updated layout for improved readability
- **Execute tool syntax highlighting** - Execute tool calls now display with syntax highlighting for better readability
- **Session type tags** - Sessions now display type tags for Missions and subagents for easier identification
- **Usage Limits settings UI** - New interface for viewing and managing Usage Limits settings (Factory App)

### Improvements

- **Create tool display** - Improved text wrapping and syntax highlighting for Create tool results
- **CLI onboarding** - Improved onboarding flow for new CLI users

### Bug fixes

- **Semantic diff rendering** - Fixed a random character appearing at the top of semantic diffs
- **Skill execution** - Fixed skills not executing properly after being loaded
- **Gemini BYOK thinking** - Fixed thinking signature preservation for Gemini models with custom API keys

## CLI v0.83.0 · Desktop v0.37.0 (March 20, 2026)

Redesigned model selector and session list, active tool call spinner, and skill slash command fixes

### New features

- **Redesigned model selector and session list** - Overhauled model selector and session list with improved navigation and layout
- **Active tool call spinner** - A spinner now displays during active tool calls for better visibility into CLI activity
- **Configurable subagent inactivity timeout** - New `subagentInactivityTimeout` setting to customize how long subagents wait before timing out due to inactivity

### Bug fixes

- **Diff syntax highlighting** - Fixed syntax highlighting issues in diff display
- **Skill slash command arguments** - Fixed user arguments not being passed to skills invoked via slash commands
- **CLI status orb display** - Fixed random display issues with the CLI status orb
- **Double loader on new session** - Fixed a duplicate loading indicator appearing when creating a new session (Factory App)
- **Sidebar button accessibility** - Fixed sidebar buttons being covered by the draggable region (Factory App)
- **Whitespace in working directory input** - Input for working directory now correctly trims whitespace (Factory App)
- **Daemon connectivity** - Fixed daemon connection issues that could occur on some systems

## CLI v0.82.0 · Desktop v0.36.0 (March 19, 2026)

Syntax highlighting for diffs, theme engine, file uploads, and session settings fixes

### New features

- **Syntax highlighting for diffs** - Diffs displayed by the CLI now include syntax highlighting for improved readability
- **Theme engine** - New customizable theme engine for personalizing CLI colors
- **File upload support** - Upload CSV, Excel, and DOCX files directly in conversations (Factory App)
- **MCP and skills controls in new sessions** - MCP servers and skills can now be configured when creating new sessions
- **Sidebar redesign** - Revamped sidebar with improved navigation and layout (Factory App)
- **Droid Computer info in session tooltip** - Session tooltips now display connected Droid Computer details (Factory App)

### Bug fixes

- **Session settings preserved on fork** - Forking a session now preserves your session settings instead of resetting to global defaults
- **Mission Control stability** - Fixed a memory leak in Mission Control
- **Auto-update rollback** - Fixed rollback failures during CLI auto-updates
- **Mission Control resize** - Fixed Mission Control display issues when resizing the terminal

## CLI v0.80.0 · Desktop v0.34.0 (March 18, 2026)

Couchbase MCP server, AutoWiki dashboard links, and sub-agent reliability fixes

### New features

- **Couchbase MCP server** - Added Couchbase to the MCP server registry for database integration
- **AutoWiki dashboard link** - The Droid CLI now shows a direct link to the dashboard after AutoWiki uploads complete
- **Touch device controls** - Submit and cancel buttons now appear on touch devices for easier interaction (Factory App)
- **Droid Computer install commands** - The Connect to Droid Computer modal now shows curl and Windows install commands (Factory App)
- **Dynamic loading status setting** - New setting to disable dynamic loading status messages (Factory App)

### Improvements

- **SSH error messages** - Improved error messages for the SSH command
- **BYO Droid Computer setup guidance** - Better user guidance for BYO Droid Computer setup commands
- **Simplified Droid Computer setup** - Streamlined the Droid Computer setup flow

### Bug fixes

- **Sub-agent spawning** - Fixed sub-agents failing to spawn correctly
- **Esc key during tool execution** - Fixed Esc key during tool execution incorrectly interrupting the next user message
- **Model error notifications** - Model API errors are now shown as user notifications instead of being hidden
- **Daemon startup reliability** - Fixed daemon startup failures caused by insufficient timeout on slower connections
- **Usage Limits display** - Fixed Usage Limits not displaying correctly for users (Factory App)
- **Droid Computer card navigation** - Fixed click navigation on Droid Computer name cards (Factory App)
- **Debug mode logging** - Fixed debug logs not appearing when running with the --debug flag

## CLI v0.77.0 · Desktop v0.31.0 (March 17, 2026)

GPT-5.4 Mini model, faster @ search indexing, and sub-agent improvements

### New features

- **GPT-5.4 Mini model** - New GPT-5.4 Mini model available in the model selector

### Improvements

- **Faster @ search indexing** - File indexing for @ mentions now runs in a background worker for improved responsiveness
- **Faster session listing** - The `/sessions` command is now optimized with an index for quicker loading
- **Faster first prompt** - System info is now prefetched before the first prompt for quicker startup
- **Sub-agent reliability** - Redesigned sub-agent architecture for improved task delegation reliability
- **Skills preserved after compaction** - Skills invoked during a session are now preserved when context is compacted
- **Droid Computer selection UI** - Improved visual design for the Droid Computer selection interface (Factory App)

### Bug fixes

- **Slash command arguments** - Fixed slash command arguments being lost when submitting via the suggestion menu
- **Missions model selection** - Missions now correctly uses the session model instead of the global settings model
- **Worktree error messages** - Worktree setup failures now show descriptive error messages instead of generic errors
- **Stale Missions warnings** - Fixed stale Missions runs incorrectly triggering concurrent run warnings
- **Mode preservation on /new** - Fixed session mode being reset when creating a new session with `/new`
- **Permission settings persistence** - Permission settings are now preserved across session respawns
- **Chat composer undo** - Fixed undo not working after pasting text in the chat composer (Factory App)

## CLI v0.76.0 · Desktop v0.30.0 (March 16, 2026)

Configurable LLM timeout, MCP server allowlist for Enterprise Controls, and Mission Control improvements

### New features

- **Configurable LLM timeout** - LLM API timeout is now configurable via settings.json for customizing request timeout behavior
- **MCP server allowlist** - Enterprise admins can now restrict which MCP servers are allowed via a new allowlist policy in Enterprise Controls (Factory App)
- **Granola MCP server** - Added Granola to the MCP server registry for meeting notes integration

### Improvements

- **Mission Control shortcut** - Mission Control now toggles with Ctrl+T for quicker access
- **Rate Limit display** - Improved UI for Rate Limit notifications
- **Droid Computer error messages** - Clearer error messages for Droid Computer commands
- **Mission Control performance** - Reduced memory usage and latency in Mission Control
- **Session ID tooltip** - Session ID now visible in the session tooltip for easier reference (Factory App)

### Bug fixes

- **Custom model lookup** - Fixed BYOK custom model lookup failing after settings changes
- **Model selection text color** - Fixed incorrect text color in the model selection dropdown (Factory App)
- **Enterprise model defaults** - Cloud sessions now correctly respect enterprise model defaults (Factory App)
- **Model policy overrides modal** - Fixed display issues in the model policy overrides modal (Factory App)
- **Automations page layout** - Fixed automations page height in the Factory App
- **MCP OAuth connection** - Improved retry handling for MCP OAuth callback connections
- **Organization settings refresh** - Organization-managed settings now correctly refresh after login

## CLI v0.75.0 · Desktop v0.29.0 (March 13, 2026)

Bug report performance fix and connection stability improvements

### Bug fixes

- **Bug report performance** - Fixed bug reports hanging when processing large Missions runs
- **Disappearing CLI line** - Fixed a line occasionally disappearing from CLI output
- **Connection stability** - Improved handling of disconnection errors for more stable sessions

## CLI v0.74.0 · Desktop v0.28.0 (March 12, 2026)

Configurable worktree directory, Grep multiline auto-detection, and Mission Control improvements

### New features

- **Configurable worktree directory** - New setting to customize the directory used for git worktree operations

### Improvements

- **Grep multiline auto-detection** - Grep tool now automatically enables multiline mode when search patterns contain newlines
- **npm installation guidance** - CLI now provides clear instructions to add droid to your PATH after npm installation
- **Retry reliability** - Improved retry handling for transient provider errors with automatic rotation
- **System info truncation** - Large directory listings and git status output are now truncated to prevent system info overflow

### Bug fixes

- **Thinking block preservation** - Invalid thinking blocks are now preserved as text instead of being silently dropped
- **Git subdir plugin support** - Fixed support for git subdirectory plugins in project configurations
- **Mission Control UX** - Fixed various Mission Control UI and interaction issues
- **Spec mode subagents** - Subagents now correctly use read-only mode when the parent session is in spec mode
- **MCP OAuth compatibility** - Improved MCP OAuth compatibility across servers
- **Playwright MCP permissions** - Improved permission handling when using the Playwright MCP server
- **Terminal tab title on resume** - Terminal tab title now correctly updates when resuming a session
- **Concurrent session handling** - Improved detection and handling of concurrent CLI instances
- **Code server connection** - Fixed code server connection issues in the Factory App

## CLI v0.73.0 · Desktop v0.27.0 (March 11, 2026)

Emacs keybindings, remote access flag, faster response times, and reliability improvements

### New features

- **Additional Emacs keybindings** - Added more Emacs-style keyboard shortcuts for text editing in the CLI
- **`--remote-access` flag** - Remote session access now requires the explicit `--remote-access` flag for improved security

### Improvements

- **Faster time to first token** - Reduced time to first response by ~8% through lazy loading and caching optimizations
- **Session reconnection reliability** - Pending requests are now preserved and replayed when reconnecting after a disconnection (Factory App)

### Bug fixes

- **Spec mode model handling** - Fixed spec mode using the wrong model for thinking block processing
- **Auto-update reliability** - Fixed auto-update failures on read-only directories and Windows updates getting stuck in a pending state
- **Mission Control layout** - Fixed layout stability issues in Mission Control
- **Tool confirmation double-click** - Fixed tool confirmation buttons firing twice on a single click
- **Tool format tolerance** - Improved tolerance for format variations in AskUser and TodoWrite tool responses
- **Unicode character handling** - Fixed crashes caused by broken Unicode characters in messages
- **MCP OAuth security** - Improved OAuth state verification for MCP server connections
- **Multiple CLI instance isolation** - Fixed interference between multiple concurrent CLI instances
- **Tool filtering in exec mode** - Fixed incorrect tool filtering when running in exec mode
- **Model provider switching** - Fixed issues when switching between model providers mid-conversation
- **Worktree branch handling** - Fixed error when using worktrees with an already checked-out branch
- **Droid Computer connect modal** - Fixed VS Code config display in the Droid Computer connect modal (Factory App)

## CLI v0.72.0 · Desktop v0.26.0 (March 10, 2026)

GPT-5.4 Fast model, /fast command, chat UI refresh, and MCP OAuth for remote sessions

### New features

- **GPT-5.4 Fast model** - New GPT-5.4 Fast model available with a `/fast` slash command for quick model switching
- **MCP OAuth in remote sessions** - MCP servers requiring OAuth authentication now work in remote Droid Computer sessions
- **Chat UI refresh** - Refreshed chat interface with improved tool display, user message styling, and interrupt indicators
- **Mission subagent streaming** - Real-time streaming updates from subagents in mission control

### Improvements

- **Incremental rendering** - Enabled incremental rendering for smoother and more responsive CLI output
- **Faster Droid Computer sessions** - Optimistic preconnection reduces wait time when starting Droid Computer sessions (Factory App)
- **Working directory validation** - Droid Computer sessions now validate working directory configuration before starting (Factory App)

### Bug fixes

- **Grep tool overflow** - Fixed Grep tool crashing on very large search results by returning partial results with an increased buffer
- **Thinking indicator spacing** - Fixed spacing below the thinking indicator display
- **Timeout warnings** - Fixed spurious timeout warnings appearing during normal operation
- **Sentry integration reliability** - Improved reliability of the Sentry integration connection
- **Slack integration reliability** - Improved error handling for Slack integration connections
- **Mission Mode reasoning** - Fixed reasoning issues in Mission Mode

## CLI v0.71.0 · Desktop v0.25.0 (March 9, 2026)

Autofix PR button, worktree naming, and Create tool syntax highlighting

### New features

- **Autofix PR button** - Automatically fix issues found in pull requests directly from the app (Factory App)
- **MCP OAuth configuration** - Added OAuth configuration support for customizable fields in MCP server settings

### Improvements

- **Worktree naming** - The `--worktree` flag now accepts an optional name argument; the `--branch` flag has been removed
- **Create tool syntax highlighting** - Create tool results now display with syntax highlighting instead of diff format

### Bug fixes

- **Semantic diff rendering** - Fixed diff rendering in semantic diff view
- **@ search prewarming** - Fixed @ search prewarming for improved file suggestion performance
- **Factory App download button** - Fixed download Factory App button incorrectly showing in the Factory App
- **Terminal creation flash** - Fixed "(exited)" text briefly flashing when creating new terminals (Factory App)

## CLI v0.70.0 · Desktop v0.24.0 (March 6, 2026)

Git worktree support, native PDF reading, and runtime settings overlay

### New features

- **Git worktree support** - New `--worktree` flag enables native git worktree support for working across multiple branches simultaneously
- **Native PDF support** - The Read tool now natively supports reading PDF files across all model providers
- **Runtime settings overlay** - New `--settings` flag allows applying settings at runtime with organization-precedence merge
- **Skills UI for remote sessions** - Skills UI is now available in Droid Computer sessions (Factory App)

### Improvements

- **Mission Control redesign** - Refreshed Mission Control interface with a cleaner layout

### Bug fixes

- **Option+Arrow word jumping** - Restored Option+Arrow word jumping in ESC-prefix terminals
- **Background process isolation** - Background process tracking is now isolated per CLI instance to prevent cross-instance interference
- **@ search indexing** - Fixed file indexing in @ search suggestions
- **Shell environment in daemon** - Daemon now correctly inherits shell environment variables
- **Terminal compatibility** - Fixed Kitty keyboard protocol detection that could cause issues in certain terminals
- **Streaming cancellation** - Improved reliability when cancelling streaming responses
- **Daemon auto-updates** - Fixed an issue where daemon auto-updates could be incorrectly skipped

## CLI v0.69.0 · Desktop v0.23.0 (March 5, 2026)

CJK internationalization, GPT-5.4 model updates, and --mission flag for droid exec

### New features

- **CJK internationalization** - Full internationalization support for Japanese, Chinese, and Korean languages in the CLI
- **GPT-5.4 model updates** - GPT-5.4 is now a default model option with expanded context limits
- **`--mission` flag for droid exec** - New `--mission` flag enables non-interactive Missions orchestration via `droid exec`
- **Personal analytics page** - View your personal usage analytics directly in the app (Factory App)
- **Settings audit trail** - Track changes to settings values with a full audit trail (Factory App)
- **Version history for Enterprise Controls** - View configuration change history in Enterprise Controls (Factory App)
- **Combined billing summary** - Billing summary now available in both personal and organization settings views (Factory App)

### Improvements

- **Git config updates** - Git configuration can now be updated when you explicitly request it
- **BYOK Anthropic thinking** - Improved adaptive thinking support for custom Anthropic models
- **Smarter retry handling** - Improved retry delays for provider capacity errors
- **LLM timeout errors** - Clearer user-facing error messages when model requests time out
- **MCP tool rendering** - Improved MCP tool result display in the Factory App

### Bug fixes

- **VSCode keyboard shortcuts** - Fixed support for Cmd + key combinations in VSCode terminal
- **Anthropic streaming stability** - Improved streaming reliability for Anthropic models
- **Empty model responses** - Empty model responses are now handled gracefully instead of causing errors
- **Thinking recovery** - Auto-recovery from thinking signature validation errors during reasoning
- **Spec mode navigation** - Fixed back navigation from autonomy menu in spec mode
- **Mission session cleanup** - Fresh session now starts correctly when exiting a proposed mission
- **Gemini error handling** - Improved error handling for authentication and payment errors with Gemini models
- **Profile display** - Fixed user profile parsing for accounts with incomplete name fields

## CLI v0.68.1 (March 5, 2026)

VSCode Kitty protocol support and authentication fixes

### New features

- **VSCode Kitty protocol support** - Added Kitty keyboard protocol support for VSCode terminal integration

### Bug fixes

- **Authentication issues on login** - Fixed authentication issues that could occur during login

## CLI v0.68.0 · Desktop v0.22.0 (March 4, 2026)

Subagent inactivity timer, Usage Limits settings, and streaming stability fixes

### New features

- **Subagent inactivity timer** - Subagents now automatically stop after 3 minutes of inactivity to prevent idle resource usage
- **Usage Limits settings** - Configure and view Usage Limits directly within sessions and settings (Factory App)

### Bug fixes

- **VS Code auto-installation** - Fixed embedded VS Code auto-installation in the Factory App
- **Factory App stability** - Fixed daemon restart issues in the Factory App
- **Session resume** - Fixed reliability issues when resuming previous sessions
- **Streaming stability** - Fixed a crash that could occur during streaming retries
- **BYOK error handling** - Improved error messages for payment and authentication errors with custom API keys
- **Context management** - Improved handling when conversations exceed context limits
- **Image handling for text-only models** - Images are now properly handled when using text-only models
- **GLM-4.7 error handling** - Fixed error handling for GLM-4.7 model errors
- **MCP tool compatibility** - Improved MCP tool schema sanitization for better compatibility across model providers
- **Custom model streaming** - Fixed streaming issues with custom models
- **Reasoning level display** - Fixed reasoning level not displaying correctly after using /model in spec mode
- **Authentication reliability** - Reliability improvements to authentication mechanisms

## CLI v0.67.0 · Desktop v0.21.0 (March 3, 2026)

CLI banners, /stats command, skills search, and configurable image compression

### New features

- **CLI banners** - Display customizable banners in the CLI for quick access to important information
- **`/stats` command** - The `/wrapped` command has been renamed to `/stats` with date range filtering support
- **Skills search bar** - Added search bar to the skills menu for quickly finding skills
- **Configurable image compression** - New `image_quality` parameter in the Read tool for controlling image compression quality
- **Electron app automation** - The agent-browser skill now supports automating Electron desktop applications

### Improvements

- **Automation detail view** - Redesigned automation detail view to align with session UI patterns (Factory App)
- **Windows ARM64 and Zed extension** - CLI distribution now includes Windows ARM64 builds and Zed editor extension

### Bug fixes

- **Certificate loading order** - Fixed system certificate loading that could cause authentication failures on startup
- **Gemini schema compatibility** - Fixed schema compatibility issues with Gemini models
- **Payment redirect in Factory App** - Fixed payment page redirect handling in the Factory App
- **Character encoding** - Fixed display of malformed UTF characters in messages
- **Missions list formatting** - Fixed formatting of feature and worker list descriptions in Missions
- **BYOK error handling** - Improved error messages for custom model (BYOK) configurations
- **MCP server reconnection** - Fixed potential deadlock when MCP servers fail to reload during disconnection
- **Execute tool file actions** - Fixed file operations not being applied correctly during command execution

## CLI v0.66.0 · Desktop v0.20.0 (March 2, 2026)

/copy command, marketplace management, and Missions worker improvements

### New features

- **`/copy` slash command** - Copy content to your clipboard directly from the CLI
- **Marketplace management** - New UI for managing marketplace plugins under the Plugins section in enterprise controls (Factory App)
- **Factory App version display** - Factory App now shows the current version number
- **Grouped exec sessions** - Droid exec sessions are now grouped under a dedicated tab for cleaner organization (Factory App)

### Improvements

- **Missions worker reliability** - Hardened Missions worker lifecycle with improved pause and resume handling

### Bug fixes

- **Subagent model and permissions** - Fixed subagent model inheritance and permissions level
- **BYOK compaction errors** - Upstream error details are now surfaced in BYOK compaction failures
- **Cross-provider messages** - Fixed message conversion for OpenAI Responses API across providers
- **Spec model display** - Corrected spec model display in `/model` selector and prevented global fallback on clear
- **Session archiving** - Fixed session archive confirmation flow in the app
- **Chat scrolling** - Fixed scroll-to-last-message behavior in session chat (Factory App)
- **User Usage Limits modal** - Fixed scroll bug in the Individual User Usage Limits modal (Factory App)
- **Diff generation** - Fixed potential crash with non-string inputs in diff generation

## CLI v0.65.0 · Desktop v0.19.0 (February 27, 2026)

Diagnostics command, GitHub comments in diff viewer, and Mission Mode fixes

### New features

- **/diagnostics command** - New `/diagnostics` command with overlay menu and footer status for troubleshooting CLI issues
- **Unstaged changes in diff viewer** - View and manage unstaged changes directly in the diff viewer panel (Factory App)
- **GitHub comments in diff viewer** - View GitHub PR comments alongside code changes in the diff viewer (Factory App)
- **Session deep linking** - Share and navigate directly to specific sessions via deep links (Factory App)
- **Diff preview for enterprise controls** - Preview configuration diffs when managing enterprise control settings (Factory App)

### Bug fixes

- **Mission Mode model selection** - Fixed model selection issues when using Mission Mode
- **Mission Mode validation** - Validation contracts now update correctly when Mission requirements change
- **Bug report smart trimming** - Bug reports now smart-trim large files instead of failing
- **Plugin auto-install** - Fixed duplicate core plugin auto-install failures being surfaced to users

## CLI v0.64.0 · Desktop v0.18.0 (February 26, 2026)

Session archiving, inline rename, custom model reasoning effort, and Mission Mode improvements

### New features

- **Session archiving** - Archive sessions from the CLI to keep your session list clean
- **Inline session rename** - Rename sessions inline with cloud sync support
- **Custom model reasoning effort** - Added reasoning effort support for custom models
- **Concurrent Missions warnings** - Warns on Missions entry and confirms concurrent Missions runs
- **Dry-run validation** - New dry-run validation approach during Missions planning
- **/model scope clarity** - Clarified `/model` command scope and added set-as-default action

### Bug fixes

- **Mission Mode commands** - Split Mission Mode enter and exit into separate commands for improved reliability
- **Context management** - Fixed context management triggering too frequently for OpenAI models
- **OpenAI reasoning effort** - Fixed maximum reasoning effort setting for OpenAI models
- **Gemini rate limiting** - Improved Gemini 429 error handling with throttle-aware retry
- **Bedrock reasoning effort** - Fixed reasoning effort settings for Bedrock models
- **Empty end_turn responses** - No longer treats empty end_turn responses as errors

## CLI v0.63.0 · Desktop v0.17.0 (February 25, 2026)

Model selector redesign, session default settings, and Droid Shield improvements

### New features

- **Top 5 model selector** - Model selector now shows top 5 models with a "show more" option for cleaner UI
- **Session default settings** - All session default settings (model, autonomy, reasoning) now exposed in `/settings` menu

### Bug fixes

- **Droid Shield false positives** - Reduced false positives on example files and placeholders
- **Glob tool patterns** - Fixed handling of non-array patterns input in Glob tool
- **BYOK auth in exec mode** - Fixed authentication validation for BYOK custom models in exec mode
- **Session model auth** - Check effective session model for BYOK auth skip, not just CLI flag
- **Session loading** - Fixed session loading issues with long conversation histories

## CLI v0.62.0 · Desktop v0.16.0 (February 24, 2026)

Bedrock/Vertex support, session-scoped settings, readiness-fix command, and Rate Limits

### New features

- **Bedrock/Vertex support** - Added Bedrock and Vertex support for Claude Sonnet 4.6 and Opus 4.6
- **Session-scoped settings** - Model, autonomy, and reasoning settings are now session-scoped instead of global
- **`/readiness-fix` command** - New slash command to automatically fix issues found in readiness reports
- **Rate Limits UI** - Added UI handling for Rate Limit notifications
- **README requirement for Missions** - Missions now require README updates before completion

### Bug fixes

- **MCP reload prevention** - Avoided unnecessary MCP reloads on non-MCP settings changes
- **Custom model migration** - Prevented no-op custom model migration writes
- **Autonomy persistence** - Preserved autonomy level when spec sessions persist

## CLI v0.61.0 · Desktop v0.15.0 (February 23, 2026)

Vertex/Bedrock Opus support, Mission Control polish, and interactive command prevention

### New features

- **Vertex/Bedrock Opus support** - All latest Opus models now available via Vertex and Bedrock
- **Online research in Missions** - Added online research and environment setup during Missions planning
- **Recent local directories** - Quick access to recently used local directories

### Bug fixes

- **Mission Control polish** - Visual improvements to Mission Control UI
- **Interactive command prevention** - Prevent interactive command execution that could block the agent
- **Missions latency** - Reduced `/enter-mission` latency and improved daemon error UX
- **Spec/autonomy decoupling** - Decoupled spec and autonomy settings and permission outcomes

## CLI v0.60.0 · Desktop v0.14.0 (February 20, 2026)

Faster search, Missions model selector, and Missions validation overhaul

### New features

- **Missions model selector** - Choose specific models for Missions workers
- **Prevent idle sleep** - CLI now prevents system idle sleep during Missions execution

### Improvements

- **Faster search** - Sped up search functionality in large repositories with fuzzy search support

### Bug fixes

- **Missions validation overhaul** - Complete overhaul of Missions validation for improved reliability
- **Missions worker timeouts** - Improved Missions worker timeout handling
- **Subagent model inheritance** - Fixed model inheritance for subagents
- **Diff word highlights** - Fixed incorrect line wrapping in diff word-level highlights
- **Gemini tool usage** - Improved Gemini tool usage reliability
- **Readiness report sanitization** - Improved sanitization of sensitive data in readiness reports
- **TUI daemon shutdown** - Fixed stopping TUI-spawned daemon on shutdown

## CLI v0.58.0 · Desktop v0.12.0 (February 19, 2026)

Local settings override, environment variable references in custom models, and Missions UX improvements

### New features

- **Local settings override** - New `settings.local.json` for local project/folder-level settings overrides
- **Environment variable references** - Custom model API keys now support environment variable references
- **Gemini 3.1 Pro model** - Added Gemini 3.1 Pro model support
- **Missions planning pausing** - Allow pausing during planning phases with in-context resume in Mission Control view

### Bug fixes

- **Anthropic provider reset** - Fixed stale Anthropic provider state on model switch
- **MCP toggle effects** - MCP toggle changes now apply immediately without restart
- **Browser MCP isolation** - Stopped auto-adding `--isolated` flag for browser MCP servers
- **Windows PowerShell** - Fixed PowerShell execution issues on Windows
- **GLM 4.7 routing** - Fixed GLM 4.7 model routing issues
- **Ctrl+G spam prevention** - Blocked Ctrl+G while the agent is streaming to prevent notification spam

## CLI v0.57.16 · Desktop v0.11.15 (February 17, 2026)

Claude Sonnet 4.6 model support

### New features

- **Claude Sonnet 4.6** - Added Claude Sonnet 4.6 model support

## CLI v0.57.15 · Desktop v0.11.14 (February 16, 2026)

Opus 4.6 Fast Mode pricing update

### Improvements

- **Opus 4.6 Fast Mode pricing** - Removed promotional pricing for Opus 4.6 Fast Mode

## CLI v0.57.14 · Desktop v0.11.13 (February 13, 2026)

Session tags, word-level diffs, new models, and built-in skills

### New features

- **Session tags** - Categorize sessions with custom tags using the new `--tag` CLI flag for better organization
- **Word-level diff highlighting** - GitHub diff mode now highlights only changed words within lines instead of entire lines
- **GPT-5.3-Codex model** - Added GPT-5.3-Codex model with multi-turn phase support
- **GLM-5 model** - Added GLM-5 model via Fireworks
- **MiniMax M2.5 model** - Added MiniMax M2.5, replacing M2.1
- **Create-PR skill** - New built-in skill for guided pull request creation with local verification checklist
- **Worker droid** - Basic worker droid now ships as a built-in droid for task delegation
- **PR linking** - Sessions now display a status indicator showing linked PRs from git operations

### Bug fixes

- **Stdin character corruption** - Replaced text input component to eliminate character corruption and broken special keys
- **NODE_ENV injection** - Stopped injecting `NODE_ENV=production` into shell environment, fixing `npm` devDependencies issues
- **MCP SDK alignment** - Updated to MCP SDK 1.26 with proper schema validation
- **File watcher limits** - More granular file watching to avoid "too many open file descriptors" errors
- **Factory App connection race** - Fixed daemon connection race condition in the Factory App with polling retry logic
- **Sidebar sessions** - Fixed sessions disappearing from sidebar (Factory App)
- **Open in editor** - Fixed "open in editor" functionality in the Factory App

## CLI v0.57.12 · Desktop v0.11.11 (February 11, 2026)

Spec approval with comment and input stability

### New features

- **Spec approval with comment** - Added a "Proceed with comment" option to spec approval, letting you approve a spec and attach a guiding comment in one action

### Bug fixes

- **Fast model switching** - Fixed edge cases when switching models mid-conversation, including proper conversation state management
- **Invalid MCP output schemas** - Tolerates invalid MCP tool output schemas instead of crashing
- **Opus 4.5 max tokens** - Corrected incorrect Opus 4.5 max output tokens in model registry
- **Ctrl+O during AskUser** - Allows Ctrl+O (open in editor) during the AskUser tool flow
- **AskUser context** - Ensures context is clear when using the AskUser tool
- **Session file table overflow** - Limits concurrency when fetching sessions in daemon to avoid "file table overflow" errors
- **Duplicate plan steps** - Fixed duplicate plan steps in web UI when multiple TodoWrite calls share the same title (Factory App)

## CLI v0.57.11 · Desktop v0.11.10 (February 10, 2026)

Subagent fixes and model switching improvements

### Bug fixes

- **Subagent prompting** - Fixed subagent tool prompting and description handling
- **AskUser tool** - Handles edge cases preventing stuck states when sessions are interrupted or messages arrive out of order (Factory App)
- **Sidebar staleness** - Fixed missing last message and stale status indicators on the session sidebar (Factory App)

## CLI v0.57.10 · Desktop v0.11.9 (February 9, 2026)

Skills UX overhaul, terminal tab titles, Factory App notifications, and mobile experience

### New features

- **`/skills` UX overhaul** - Tabbed layout with pagination and a dedicated detail view for browsing and importing skills
- **Terminal tab titles** - Terminal tab now displays the session name so you can identify Droid sessions across multiple tabs
- **`droid update` command** - New command to manually update the CLI, plus ability to disable autoupdate via `/settings`
- **Session end hooks** - Hooks now fire when running `/clear` or `/new`, enabling custom cleanup workflows
- **Factory App notifications** - Native macOS and Windows notifications when sessions complete, with configurable preferences
- **Factory App native view redesign** - Refreshed sidebar layout with smooth animations, new terminal editor icons, and keyboard shortcut formatting
- **Mobile experience** - Overhauled mobile and responsive layout with touch-friendly settings and onboarding flows (Factory App)

### Bug fixes

- **`/bug` command memory** - Optimized log loading with streaming I/O to prevent out-of-memory on large log files
- **Session persistence** - Thinking and reasoning fields now preserved correctly when saving sessions
- **MCP settings UI** - Filled toggle style, clickable tool rows, and capitalized server names (Factory App)
- **Git timeout** - Increased git timeout to 60 seconds to prevent failures on slow connections or large repos

## CLI v0.57.9 · Desktop v0.11.8 (February 7, 2026)

Opus 4.6 Fast Mode and pricing update

### Improvements

- **Opus 4.6 Fast Mode** - Renamed from "Opus 4.6 Fast" to "Opus 4.6 Fast Mode" for clarity
- **Opus 4.6 Fast Mode promo pricing** - Updated Model Multiplier from 12x to 6x promotional rate

## CLI v0.57.7 · Desktop v0.11.6 (February 6, 2026)

Opus 4.6 Fast, /fork command, session archiving, and org-managed settings

### New features

- **Claude Opus 4.6 Fast** - Added Opus 4.6 Fast as a new model option in the model selector
- **`/fork` command** - Duplicate your current session with all messages preserved into a new session
- **Org-managed settings** - Local settings that are set by your organization are now locked from editing
- **Session archiving** - Archive sessions from the web app to keep your sidebar clean (Factory App)

### Bug fixes

- **Shell environment loading** - Shell environment now loads consistently across Factory App, sandbox, and computer platforms
- **Orphaned browser processes** - Agent-browser daemon processes are now cleaned up properly
- **Task tool output** - Progress updates from Task tool are now truncated to prevent UI overflow

## CLI v0.57.5 · Desktop v0.11.4 (February 5, 2026)

Opus 4.6, semantic diffs, npm package, plugin hooks, and startup optimizations

### New features

- **Claude Opus 4.6** - Added Claude Opus 4.6 model support
- **Semantic structured diffs** - Code change diffs now use semantic structure-aware rendering for better readability
- **Plugin hooks** - Added support for plugin hooks with Claude hooks format compatibility
- **npm package** - CLI is now installable via npm: `npm install -g droid`
- **User-invocable skills as slash commands** - Custom skills marked as user-invocable are now registered as slash commands
- **`FACTORY_LOG_FILE` and `FACTORY_DISABLE_KEYRING` env vars** - New environment variables for log file output and keyring control
- **Enterprise Controls** - New settings page for managing agent behavior, command policy, model access, and security (Factory App)
- **Skills UI** - Skills button and modal added to the chat input for easy skill access (Factory App)
- **Ask User tool** - Ask User tool now available in the web and Factory App surfaces

### Improvements

- **Startup latency** - Optimized CLI startup with sub-metric tracking for faster launch times

### Bug fixes

- **Unicode crash** - Fixed CLI crash when sessions contain certain unicode characters
- **Marketplace auto-update** - Auto-update now only runs in interactive mode, not during `droid exec`

## CLI v0.57.3 · Desktop v0.11.2 (February 3, 2026)

Task tool streaming, image pasting, and skills improvements

### New features

- **Task tool live streaming** - Real-time subagent tool progress display and Execute tool output streaming in web and Factory App surfaces
- **Image pasting** - Paste images directly into the chat composer (Factory App)
- **`.agent` skills folders** - Skills can now be loaded from `.agent` folders in your project for custom skill support

### Improvements

- **Skills filtering** - Skills are now filtered by model invocability so only relevant skills appear in the Skill tool

### Bug fixes

- **File suggestion UX** - Trailing space now added after file suggestion selection for smoother typing

## CLI v0.57.2 · Desktop v0.11.1 (January 30, 2026)

Full text search, MiniMax M2.1, and AskUser improvements

### New features

- **Full text search** - Search across your session history and codebase directly in the CLI
- **MiniMax M2.1** - Added MiniMax M2.1 model support

### Bug fixes

- **AskUser tool** - Improved questionnaire parsing and interaction reliability

## CLI v0.57.0 · Desktop v0.11.0 (January 29, 2026)

Plugin hooks and ASCII mermaid diagrams

### New features

- **ASCII mermaid diagrams** - Mermaid diagrams now render as ASCII art directly in the terminal

## CLI v0.56.1 · Desktop v0.10.2 (January 28, 2026)

MCP tool management and Read tool fixes

### Improvements

- **MCP tool management** - Improved MCP tool status tracking to prevent cross-contamination between servers

### Bug fixes

- **Read tool images** - Fixed image support in the Read tool, along with rate limit retry and reasoning fixes
- **Cache block limits** - Ensured no more than 3 cache blocks are sent to the LLM to prevent context issues

## CLI v0.56.0 · Desktop v0.10.2 (January 27, 2026)

ACP daemon mode, lazy session loading, and model updates

### New features

- **ACP daemon mode** - New daemon mode for Agent Control Protocol enabling persistent background sessions with improved session loading
- **Lazy session loading** - Sessions now load messages lazily for faster startup when resuming large sessions
- **Dynamic default settings** - Settings now support dynamic defaults for better configuration flexibility

### Improvements

- **Parallel context gathering** - Missions workers now encouraged to read all context files in parallel for faster startup

### Bug fixes

- **MCP tool schema isolation** - Broken tool schemas in one MCP server no longer affect other MCP servers
- **Symlinked skill directories** - Fixed discovery of symlinked skill directories in `.factory/skills`
- **Windows spec mode UI** - Fixed spec mode UI and autonomy mode text rendering on Windows
- **AskUser parallel tool calling** - Fixed parallel tool calling with AskUser tool
- **Skills menu rendering** - Fixed skills menu to always render correctly
- **OpenAI custom model routing** - Fixed routing bug for OpenAI custom models
- **Linear remote delegation** - Fixed Linear remote delegation issues
- **Authentication atomic writes** - Auth writes now use atomic operations to prevent corruption
- **ACP session loading** - Fixed multiple issues with ACP session loading

## CLI v0.55.2 · Desktop v0.10.1 (January 23, 2026)

Marketplace auto-updates and background processes flag

### New features

- **Marketplace auto-updates** - New management UI with auto-update setting and silent auto-installation of missing marketplaces on startup
- **`--allow-background-processes` flag** - Added flag support for interactive and resumed sessions

### Bug fixes

- **AskUser tool parsing** - Improved parsing logic for questionnaire formatting

## CLI v0.55.1 · Desktop v0.10.1 (January 22, 2026)

OTEL tracing, bug reporting improvements, and review command fixes

### New features

- **OpenTelemetry tracing** - Implemented OTEL tracing for the CLI to improve observability and debugging
- **Mandatory bug report titles** - Added title requirement for `/bug` reporting to ensure clearer issue tracking

### Bug fixes

- **`/review` default branch** - Fixed the `/review` command to correctly identify and use the repository's default branch
- **Authentication** - Fixed several issues around authentication persistence and stability

## CLI v0.55.0 · Desktop v0.10.1 (January 21, 2026)

Autonomy mode reskin and agent-browser integration

### New features

- **Autonomy mode reskin** - Refreshed UI for autonomy mode indicators and transitions for better clarity
- **Agent-browser integration** - CLI now uses the `agent-browser` CLI for browser automations, providing more reliable and token-efficient interactions

## CLI v0.54.0 · Desktop v0.10.0 (January 20, 2026)

Readiness report improvements and AskUser fixes

### New features

- **OTEL metrics for hooks and slash commands** - Customer metrics for `droid.hook.invocations` and `droid.slash_command.invocations`
- **Optional `/readiness-report` model switching** - Users can now continue with their current model while seeing a recommendation, instead of being forced to switch

### Improvements

- **Autonomy indicator format** - Updated format to show `Spec | Auto (X)` when spec mode is active; `Medium` shortened to `Med`

### Bug fixes

- **AskUser tool improvements** - Questionnaire parsing now supports bullets/`1)` numbering, ignores headers/code fences, normalizes multi-word topics. AskUser can now run alongside TodoWrite with other tools deferred properly. Fixed TUI input handling via `KeypressProvider` subscription
- **Windows UI** - Improved autonomy/spec mode status text rendering on Windows terminals

## CLI v0.53.0 · Desktop v0.10.0 (January 16, 2026)

Readiness report in exec mode and settings stability

### New features

- **`/readiness-report` in exec mode** - Support for `/readiness-report` slash command in droid exec mode with optional custom instructions

### Bug fixes

- **Settings.json corruption prevention** - Settings file now uses atomic writes to prevent corruption
- **Terminal info disabled** - Disabled getTerminalInfo to prevent issues
- **Authentication stability** - Bundled keychain dependency in packaged builds to reduce flaky sign-in setups

## CLI v0.52.0 · Desktop v0.9.3 (January 15, 2026)

Session sharing, ctrl+z suspend, and bug fixes

### New features

- **`/share` command** - Share your current session with organization members, copies share URL to clipboard

### Improvements

- **Ctrl+Z suspend** - Handle ctrl+z suspend like other TUIs
- **Decoupled modes and autonomy** - Modes and autonomy levels are now independent settings in the TUI

### Bug fixes

- **Task tool view** - Fixed Ctrl+O view for Task tool
- **Settings file writes** - Avoid unnecessary file writes when updating unrelated settings
- **Unified tool display** - Fixed tool result pending display issue
- **Subagent version** - Fixed subagent spawning to use correct droid version

## CLI v0.49.0 · Desktop v0.9.2 (January 14, 2026)

CLI Axiom skill, custom model fixes, and bug fixes

### New features

- **CLI Axiom skill** - New skill for querying CLI metrics and logs with relevant datasets and fields

### Improvements

- **Custom model requests** - Custom models now properly map to equivalent built-in models for correct request formatting

### Bug fixes

- **iTerm scrollback clearing** - Fixed scrollback clearing for iTerm users with "Disable E3 scrollback clearing" preference enabled
- **Memory leak fix** - Fixed memory leak by cleaning up Performance API entries and hinting Bun GC
- **Session title generation** - Fixed session title generation for empty strings
- **Warmup requests** - Warmup requests no longer consume unnecessary tokens by disabling thinking budget
- **Light mode submenus** - Fixed light mode display issues for submenus
- **Linux autoupdate** - Fixed autoupdate issues on Linux

## CLI v0.48.0 · Desktop v0.9.2 (January 13, 2026)

ACP streaming, Windows autoupdate, and bug fixes

### Improvements

- **Windows autoupdate** - Updates now work correctly on Windows using a deferred update strategy, applied on next startup
- **Model selector** - Removed GLM 4.6 from the model selector

### Bug fixes

- **Tool result rendering** - Internal placeholder markers no longer displayed in CLI output
- **Session loading** - Fixed "Failed to load session" errors on cloud sessions
- **Droid startup timeout** - Increased timeout for start droid to prevent timeouts

## CLI v0.47.0 · Desktop v0.9.1 (January 12, 2026)

Bug fixes

### Bug fixes

- **Read tool infinite loop** - Fixed infinite loop when Read tool returns empty string
- **Session title generation** - Fixed race condition causing "Session must have at least 1 message" error
- **Windows sound paths** - Fixed Bun virtual FS sound path extraction on Windows

## CLI v0.46.0 (January 9, 2026)

Session rename, cloud sync, and bug fixes

### New features

- **`/create-skill` command** - Create custom skills directly from the CLI with guided flow
- **Skills in exec mode** - Skill tool now enabled when running `droid exec`
- **`/rename` command** - Rename sessions with a new slash command, plus auto-generated session names based on conversation content

### Improvements

- **PR overview in FetchUrl** - GitHub PR fetch results now include an overview section with files changed, comment counts, and table of contents
- **Create-skill UX** - Improved create-skill flow with better guidance and examples
- **Review branch fetch** - Git review now fetches current branch when opening instead of on mount

### Bug fixes

- **Background process output** - Output from background processes now properly piped to droid
- **Cloud sync settings** - Fixed settings cloud sync with droid status tracking
- **ESC cancel duplication** - Fixed queued messages being duplicated when pressing ESC to cancel

## CLI v0.45.0 (January 8, 2026)

Bug fixes and improvements

### Bug fixes

- **Ctrl+O detailed view** - Now shows full accumulated command output instead of truncated view
- **File autocomplete** - Menu now closes properly on Ctrl+C
- **MCP modal** - Fixed modal and status notification display issues
- **Autonomy level** - Fixed autonomy level not being applied correctly

## CLI v0.44.0 (January 7, 2026)

Custom status line, bulk MCP tool management, and UX improvements

### New features

- **`/statusline` command** - Configure custom status line, can import PS1 from shell config
- **Bulk MCP tool management** - Manage multiple MCP tools at once via ToolsOverviewView
- **Auto-include Skill tool** - Custom droids (subagents) now automatically include the Skill tool

### Improvements

- **Expand diffs with Ctrl+O** - Tool confirmation prompts now support Ctrl+O to expand diffs

### Bug fixes

- **Session resume system info** - Session resume now shows correct/up-to-date system info and local date
- **Model display alignment** - Fixed model display alignment in UI
- **MCP project server config** - MCP tool modifications now work correctly for project-defined servers

## CLI v0.43.0 (January 6, 2026)

Terminal and chat UI fixes, improved spec mode

### Bug fixes

- **Terminal panel display** - Fixed terminal being cut off when plan panel is shown
- **Chat input width** - Chat input now extends to full terminal width
- **Spec mode transitions** - `droid exec --use-spec` correctly exits spec mode after `ExitSpecMode`
- **Default session settings** - Session defaults properly loaded from settings.json on each new session

## CLI v0.42.2 (January 5, 2026)

GLM 4.7 support, Gemini improvements, and bug fixes

### Improvements

- **GLM 4.7 support** - Updated GLM model deployments
- **Gemini SDK upgrade** - Improved Gemini support
- **Expandable tool results** - Tool results can now be expanded to show full details in web and Factory App surfaces

### Bug fixes

- **Fixed light mode color themes in expanded mode**
- **Fixed memory leak from unbounded tool executions**
- **Fixed GitHub app installation OAuth flow**
- **Fixed dotenv loading order with settings**
- **Fixed token usage not preserved across manual compaction**
- **Fixed onboarding error when user has existing org (Factory App)**
- **Fixed users getting stuck in onboarding due to stage issues (Factory App)**
- **Fixed mobile onboarding layout (Factory App)**

## CLI v0.41.0 (December 30, 2025)

Year-in-review /wrapped command, PDF uploads, and faster model switching

### New features

- **`/wrapped` command** - Year-in-review stats showing your Droid usage, badges earned, model preferences, and session metrics (cli)
- **Fast model switching** - Faster provider/model switches without LLM compaction (cli)
- **Batched tool permissions** - Parallel tool calls now show single permission prompt (cli)
- **Custom BYOK models** - Custom models now appear in model selector (cli)
- **Auto-sync repos** - GitHub/GitLab repos sync when opening template modal (Factory App)

### Improvements

- **PDF & text file uploads** - Attach PDFs and text files to chat in web and Factory App surfaces
- **Send button** - Visual send button in session chat input (Factory App)
- **ASCII startup animation** - Animated Droid logo on CLI startup (configurable) (cli)
- **Model Multiplier display** - Shows Factory model multipliers in model descriptions (cli)

### Bug fixes

- **Fixed users getting stuck in broken onboarding state (Factory App)**
- **Fixed CLI onboarding redirect for terminal-only users**
- **Fixed missing repos in GitHub org management modal (Factory App)**
- **Fixed multi-option spec mode selection (cli)**
- **Fixed catch-22 bug preventing subscription start (Factory App)**

## CLI v0.40.0 (December 23, 2025)

Custom models, parallel tool confirmations, and settings file watching

### New features

- **Custom models from settings** - Load custom models directly from settings.json
- **Parallel tool confirmations** - Single permission request for parallel tool calls instead of individual prompts
- **Multi-option spec mode** - Spec mode can now present multiple implementation options for user selection
- **Settings file watching** - Settings automatically reload when the settings file changes
- **Token usage in exec mode** - Token usage is now displayed in exec streaming output
- **Stop hook improvements** - Decision and reason support for Stop hook to match Claude code spec

### Bug fixes

- **Opus 4.5 model fix** - Fixed Opus 4.5 to work as an effort model with thinking guard improvements
- **Tool completion fix** - Fixed issue where tools weren't properly completed on new assistant messages
- **Web search date fix** - Web search tool now includes dynamic date for more accurate results

## CLI v0.39.0 (December 19, 2025)

Context utilization setting and Custom Droids enabled by default

### New features

- **Context utilization setting** - New setting to display token usage indicator in the status bar
- **Custom Droids enabled by default** - Custom Droids feature is now available to all users without requiring opt-in

### Bug fixes

- **Grep tool fix** - Fixed pattern argument handling in the Grep tool
- **BYOK Grok fix** - Fixed crash when using Grok models with thinking/reasoning streams
- **Warmup improvements** - Added option to disable warmup requests and skip warmup for slash commands
- **Non-git directory support** - Use current working directory as project directory when not in a git repository

## CLI v0.38.0 (December 18, 2025)

GPT-5.2 improvements and .env loading fix

### Bug fixes

- **GPT-5.2 improvements** - Fixed request parameters and reasoning effort options for better model performance
- **Prevent .env auto-loading** - CLI no longer automatically loads `.env` files from the working directory in standalone builds, making behavior more predictable

## CLI v0.37.0 (December 17, 2025)

Todo tool improvements, Chrome DevTools MCP, and model cleanup

### Improvements

- **Todo tool improvements** - Simplified todo format and refreshed UI for better reliability
- **Chrome DevTools MCP server** - Added Chrome DevTools Protocol to the MCP registry
- **Model cleanup** - Removed obsolete models

### Bug fixes

- **Fixed API request handling for Codex models**

## CLI v0.36.6 (December 17, 2025)

Gemini 3 Flash, terminal links, and terminal reliability fixes

### New features

- **Gemini 3 Flash model** - Added support for Gemini 3 Flash

### Improvements

- **Agent readiness signals** - Expanded agent readiness signals in readiness reports

### Bug fixes

- **Fixed overly strict filtering by allowing common read-only `git` commands**
- **Fixed copy/paste issues on WSL**
- **Fixed repository deduplication in `/readiness` reports**

## CLI v0.36.2 (December 13, 2025)

GPT-5.2 model and MCP tool management

### New features

- **GPT-5.2 model** - Added support for GPT-5.2 model
- **MCP tool enable/disable** - Add ability to enable/disable individual MCP tools per server

## CLI v0.36.0 (December 10, 2025)

MCP tools in droid creation and droid management fixes

### New features

- **MCP tools in droid creation** - MCP tools are now displayed during custom droid creation and edit flows

### Bug fixes

- **Fixed droid deletion when filename doesn't match metadata name**
- **Standardized help text position and format in droid creation/edit flows**
- **Add reasoning_effort to stream-json system init event**

## CLI v0.33.0 (December 8, 2025)

Autonomy mode fixes and file handling improvements

### Bug fixes

- **Fixed autonomy mode not being properly set on tool confirmations**
- **Improved @-tagged file truncation by character count to prevent context overflow**
- **Updated Opus 4.5 pricing with dismissible notice**
- **Restored Figma MCP server to the registry**

## CLI v0.32.0 (December 5, 2025)

Readiness report command, ESC key improvements, and input fixes

### Bug fixes

- **Press ESC to close the expanded tool result view**
- **Improved input box cursor up/down movement with wrapped lines**
- **Fixed Windows pasting issues**
- **Fixed `npm run format` conflict with legacy Windows format command in denylist**
- **Fixed auth issues with Microsoft MCP servers**
- **`/readiness` command is now enabled by default**

## CLI v0.31.0 (December 4, 2025)

GPT-5.1-Codex-Max model, image compression, IDE auto-connect, and input fixes

### New features

- **GPT-5.1-Codex-Max model** - Added support for GPT-5.1-Codex-Max model
- **Image compression** - Images are now compressed before upload to reduce bandwidth
- **IDE auto-connect setting** - Added setting to automatically connect to IDE from external terminals
- **Disable hooks flag** - Added `--no-hooks` flag to disable hooks execution

### Bug fixes

- **Improved Droid docs search**
- **Long Execute tool commands now truncated in the UI header**
- **Fixed on-disk images not being cleared after upload**
- **Fixed thinking level changing mid-conversation by locking it per agent turn**
- **Fixed review preset items using incorrect color for non-selected items**
- **Fixed input box handling of multi-width characters like CJK and emoji**
- **Fixed left/right arrow key navigation when @ suggestion menu is open**
- **Bundled code-signed ripgrep binary for improved security and reliability**

## CLI v0.30.0 (December 3, 2025)

Hidden file search, session search, image indicators, and ESC key fixes

### New features

- **Search hidden files** - Grep and Glob tools now include hidden files in search results
- **Session search** - Added search functionality to the session selector for quickly finding sessions
- **Image indicator** - User messages now display an image indicator when images are attached

### Bug fixes

- **Fixed EPERM permission errors on certain file operations - Windows file rename retry logic**
- **Fixed ESC key navigation in `/review` and `/bg-process` commands for Ghostty terminal**
- **MCP registry updates**

## CLI v0.28.1 (December 2, 2025)

Certificate caching, image upload limits, and settings rendering fixes

### Improvements

- **Certificate caching** - Certificates are now cached on startup for faster loading
- **Image upload limits** - Conversation images are now limited to prevent 413 errors when uploading large images
- **MCP registry helper** - Added note for STDIO servers in MCP registry explaining installation requirements

### Bug fixes

- **Fixed invalid signature in thinking block after assistant message interrupt**
- **Fixed settings menu not showing all options when loading asynchronously**

## CLI v0.28.0 (December 1, 2025)

Session management, slash command navigation, thinking improvements, and Figma MCP support

### New features

- **Show all sessions** - View and manage all your sessions across directories
- **Windowed slash command navigation** - Improved navigation in the slash command menu with windowed scrolling
- **Improved thinking display** - Refactored thinking block rendering for better clarity
- **Figma MCP server** - Added support for Figma MCP server integration

### Bug fixes

- **Fixed detection of Cerebras-style context length exceeded errors**
- **Fixed duplicate spec modes and double empty line above input**
- **Added promo price label for Opus model**
- **Fixed `/install-github-app` command issues**

## CLI v0.27.4 (November 28, 2025)

Interleaved thinking support, show thinking setting, and hooks permanently enabled

### New features

- **Interleaved thinking support** - Display multiple thinking blocks during streaming, including redacted thinking blocks with safety messages
- **Show thinking setting** - Show AI thinking/reasoning on the main view, turn on/off in `/settings`
- **Hooks always enabled** - The hooks feature is now permanently enabled and available via the `/hooks` command

### Bug fixes

- **Fixed ESC/Q navigation in `/model` menus - pressing ESC or Q now properly navigates back to previous menu level instead of closing all menus**
- **Fixed garbage characters appearing in prompt input caused by terminal response bytes leaking into stdin**
- **Fixed reasoning effort display in spec mode to correctly reflect the actual reasoning effort being used**
- **Fixed OpenAI chat completions streaming for tool calls**
- **Improved Gemini's usage of the todo tool with better prompting**
- **Fixed model warmup for GLM-4.6**
- **Fixed `/install-github-app` command issues**

## CLI v0.27.2 (November 25, 2025)

Project-level MCP configs, IDE command, and custom model improvements

### New features

- **Project-level MCP configs** - Configure MCP servers at the project level using `.factory/mcp.json`
- **`/ide` command** - New command to manage VS Code, Cursor, and Windsurf IDE integrations. Shows current extension version or prompts to install
- **Extra args in custom models** - Pass additional arguments to custom model configurations e.g. service_tier, temperature, top_p, etc

### Bug fixes

- **Fixed task tool infinite wait when running subagents**
- **Fixed expanding tilde (~) paths when loading sessions**
- **Improved `@` search rankings - exact filename matches now appear at the top with VSCode-style two-column display**
- **Removed automatic creation of `.factory/skills` folders**
- **Show compacting state when triggered**
- **Consolidate markdown rendering (fixes missing character in spec mode)**
- **Parallelize loading certificates on Windows**

## CLI v0.27.1 (November 24, 2025)

New model support, persistent session settings, and auto-update improvements

### New features

- **Improved rewind functionality** - new `/rewind` command, plus speed and UX improvements.
- **`/install-github-app` command** - New command to install the Factory GitHub app directly from the CLI.
- **Images in MCP tool responses** - MCP tools can now return images that are properly sent to the LLM.

### Bug fixes

- **Upgraded to bun 1.3.3**
- **Safer mechanism to check if ripgrep is installed**
- **Fixed gpt-5.1-codex reasoning**
- **Shift+Backspace deletes single characters like Backspace**
- **Fix GLM4.6 as a spec mode model**
- **Fix exitSpecMode prompt**
- **Fix custom models for subdroids**
- **Prevent console logs during startup**
- **Fix spec mode for Gemini**

## CLI v0.26.12 (November 22, 2025)

Eval tooling upgrades, model catalog refresh, and reliability-focused TUI fixes

### New features

- **`/review` command** - Provides an interactive code review workflow. Review code changes in different ways: comparing against a base branch, reviewing specific commits, examining uncommitted changes, or providing custom review instructions.

### Bug fixes

- **Gemini 3 Pro now uses the updated 0.8× pricing multiplier - replacing introductory pricing**
- **MCP navigator now fills the terminal**
- **Update routing for /resume to filter correctly to /sessions**
- **Position cursor at start when navigating history**
- **Make all views in the mcp navigator full width**
- **Fixed garbled character rendering on Windows**
- **Unify LLM retry logic and do more retries in exec mode**
- **Removed the deprecated Figma MCP server**

## CLI v0.26.10 (November 21, 2025)

Expanded MCP registry and improved session reliability

### New features

- **MCP Registry Expansion** - Added 30+ new MCP server integrations including development tools (Playwright, Braintrust, Honeycomb), databases (Supabase, MongoDB, Prisma, Neon), security scanning (Snyk, Semgrep), and more

### Bug fixes

- **Fixed race conditions where model changes mid-turn**
- **Fixed bug report command**
- **Fixed support for duplicate model IDs in custom model configurations**
- **Fix PowerShell command execution on Windows**

## CLI v0.26.8 (November 20, 2025)

Background processes, MCP search, and TUI stability improvements

### New features

- **Background Processes Support** - Added support for running and managing background processes in the CLI. Includes a new `bg-process` command to list, kill, and clean up processes, with persistent process state tracking.
- **MCP Registry Search** - Added search functionality to the MCP registry list view (`/mcp`). Filter available MCP servers by typing directly in the list interface.

### Bug fixes

- **Fixed race conditions and rendering issues when suspending/resuming the TUI (e.g., when opening an external editor).**
- **Fixed circular dependency issues in grep tool logging.**

## CLI v0.26.7 (November 19, 2025)

Directory-specific sessions, MCP image support, and Gemini fixes

### New features

- **Directory-Specific Sessions** - Sessions are now stored per directory and automatically switch to the correct working directory when loaded. The `/sessions` command shows only sessions created in your current directory plus favorited sessions
- **MCP Image Support** - MCP tools can now return images that are sent to the LLM for analysis
- **Custom Models for Subdroids** - Subdroids can now use custom models instead of inheriting from parent session

### Bug fixes

- **Fixed console output issues in exec mode**
- **Fixed spec mode for Gemini models**
- **Fixed exit spec mode prompt behavior**

## CLI v0.26.3 (November 18, 2025)

Claude Code hooks migration, improved suggestions, and GLM support

### New features

- **Skills Enabled by Default** - Skills command now enabled for all users
- **Claude Code Hooks Auto-Migration** - Automatically detects and imports hooks from Claude Code CLI with interactive prompts. Smart translation converts `bash_tool` to `Execute` and `CLAUDE_CWD` to `DROID_CWD`, preventing duplicates and tracking migration state
- **@ Suggestions Improvements** - Now includes folders in addition to files with better UI and performance

### Bug fixes

- **Fixed GLM4.6 configuration issues preventing it from working in spec mode**
- **Fixed warmup API calls**
- **Shift+Backspace now deletes single character like Backspace**

## CLI v0.26.0 (November 14, 2025)

Skills system, session favorites, and improved git integration

### New features

- **Skills System** - Claude Code-compatible `.factory/skills` support for modular, prompt-based capabilities. Use the `/skills` command to manage skills and import from `.claude/skills` directories
- **Session Favorites** - New `/favorite` command to pin/unpin sessions, keeping your active projects at the top of the session list
- **Enhanced Bug Reporting** - The `/bug` command now zips session context, uploads it to Factory, and returns a shareable report ID automatically
- **Cleaner Diff Viewer** - Improved UI with horizontal lines instead of borders

### Bug fixes

- **Always prompt to accept or reject generated specs and pass the correct labels to the UI flow**
- **`droid spec` now writes files to the expected default path without manual overrides**
- **Fixed autonomy handling so MCP tools respect the configured confirmation level in every session**
- **Better error handling in pre-update logic**
- **Added Axiom MCP server to the registry**

## CLI v0.25.0 (November 13, 2025)

Execute tool streaming, enhanced hooks system, and MCP autonomy controls

### New features

- **Enhanced Hooks System** - Added 7 new hook types for complete lifecycle control:
  - UserPromptSubmit - Modify or validate prompts before they're sent to the agent
  - Stop - Execute custom logic when the agent completes (e.g., metrics collection)
  - SubagentStop - Track and log subagent task completion
  - PreCompact - Run custom logic before conversation compaction (can block compaction if needed)
  - SessionStart - Initialize sessions and inject environment variables
  - SessionEnd - Cleanup tasks when sessions end (triggered on logout, quit, Ctrl+C)
- **MCP Tool Autonomy Levels** - Granular control over MCP tool confirmations: low autonomy requires confirmation for read-only MCP tools, high autonomy requires confirmation for all MCP tool calls
- **Execute Tool Streaming** - Long-running commands now display the last two non-empty lines of output in real-time. No more wondering if Droid is stuck or slow.

### Bug fixes

- **Fixed paste handling in hooks UI - no more escape sequence artifacts when pasting commands**
- **Fixed message ID alignment after conversation compaction**
- **Fixed unfinished tool uses being cleared when switching providers to retry**
- **Fixed markdown prompt usage for GPT models**
- **Fixed /mcp rendering for narrow terminal windows**
- **Fixed bracketed paste handling when suspending TUI**
- **Authentication errors now appear directly in the CLI with clear error messages**

## CLI v0.24.0 (November 12, 2025)

Hooks system, interactive spec editing, and major performance improvements

### New features

- **Hooks** - Introduced a powerful hooks system allowing you to run custom scripts before/after tool executions with configurable exit codes for different behaviors (success, warning, block, abort) - [Experimental - turn on in /settings]
- **Interactive Spec Editing** - Added ability to interactively edit specs before execution
- **Prompt Cache Warmup** - Added prompt-cache warmup while you're typing for faster responses

### Bug fixes

- **Fixed model switching to correctly handle conversation compaction when needed**
- **Fixed spec mode tab cycling for reasoning levels**
- **Fixed bracketed paste when suspending TUI**
- **Corrected line numbers in ApplyPatch tool diff display**
- **Eliminated race condition in ripgrep path resolution**
- **Various agent loop stability improvements**
- **Tool execution now correctly respects autonomy mode**
- **Applied workaround for Figma MCP server compatibility**

## CLI v0.23.0 (November 10, 2025)

Markdown tables, pinned todos, and MCP improvements

### New features

- **Markdown table rendering** - CLI now properly renders markdown tables for better display of structured data and documentation
- **Pinned todo plans** - Pin important todo items to keep them visible and track tasks during long-running sessions
- **MCP tool result formatting** - Improved formatting for MCP tool results with cleaner, more readable output

### Bug fixes

- **Fixed thinking block support for chat completion APIs to enable extended reasoning in compatible models**
- **Fixed issue with baseline versions reverting back to non-baseline builds on update**
- **Fixed autonomy mode handling in `droid exec` command for more reliable execution**
- **Restored Ctrl+T keyboard shortcut functionality on Windows**

## CLI v0.22.14 (November 7, 2025)

Reasoning controls, bash output expansion, and MCP improvements

### New features

- **Tab to cycle reasoning levels** - Navigate through different reasoning levels using the Tab key for better control
- **Expanded bash mode outputs** - Transcript view now expands and displays bash command outputs for better visibility

### Bug fixes

- **Fixed MCP tool discovery for droid exec so tools appear correctly in --list-tools and pass validation**
- **Fixed diff view to line wrap for better readability of long lines**
- **Fixed OAuth refresh for MCP servers**
- **Fixed markdown rendering bug in transcript view**
- **Fixed message cancellation handling in TUI**
- **Fixed prompt cache key handling in completions**
- **Brought back Ctrl+T keyboard shortcut on Windows**

## CLI v0.22.12 (November 6, 2025)

Console improvements and enhanced reliability

### New features

- **Quit/exit aliases** - type 'quit' or 'exit' commands for exiting sessions

### Bug fixes

- **Collect all AGENTS.md and CLAUDE.md files for system reminders**
- **Fixed MCP server argument parsing when adding servers through the UI**
- **Improved system diagnostics utilities for better troubleshooting**
- **Cleaning and dynamic rendering of the pending tools to make it clear Droid is not stuck**

## CLI v0.22.11 (November 5, 2025)

Model support, tool permissions, and MCP improvements

### New features

- **Context7 MCP server** - Added Context7 MCP server to the MCP registry

### Bug fixes

- **Improved droid exec run type tracking**
- **Improved MCP client info handling**

## CLI v0.22.10 (November 4, 2025)

OAuth discovery, interrupt support, and stability improvements

### New features

- **OAuth Discovery** - Automatically discover OAuth providers to streamline authentication setup for MCP
- **OpenAI Reasoning Summaries** - Display OpenAI's extended reasoning summaries in expanded session view

### Bug fixes

- **Fixed copy-pasting behavior in terminal sessions**
- **Improved timeout handling for more reliable operations**
- **Enhanced Windows compatibility**
- **Enable custom droids by default**
- **Improved error logging and diagnostics**

## CLI v0.22.9 (November 1, 2025)

MCP Registry, tool permissions, session resume, and multiple bug fixes

### New features

- **MCP Registry** - Added a curated selection of MCP servers for easy discovery and setup

  [MCP Registry interface showing curated MCP servers](/docs-assets/images/mcp-registry-2.mp4)
- **Tool Permissions Support** - Implemented request tool permissions flow in stream-jsonrpc mode with support for multiple concurrent tool confirmations
- **Session Resume** - Show resume command on exit (Ctrl+C or /quit) with new `-r, --resume` flag to continue sessions
- **Thinking Traces Display** - Added UI component to show thinking blocks in expanded session view

### Bug fixes

- **Fixed CLI completion sounds by extracting embedded sound files to host filesystem, making them accessible to external shell commands**
- **Fixed tool use in user message after tool cancellation**
- **Added baseline builds for x64 CPUs (pre-2013) that don't support AVX2 SIMD instructions**
- **Updated static split logic to use text messages as stable checkpoints, reducing flickering during rendering**
- **Fixed storage and sending of Gemini thinking content from delta.extra_content.google**
- **Removed MultiEdit tool due to low success rate (`~80%`)**
- **Added recovery from malformed optional arguments using optimistic JSON parsing**

## CLI v0.22.7 (October 31, 2025)

Reasoning field support, Import from Claude, and bug fixes

### New features

- **Reasoning field support in streaming responses** - Added support for displaying reasoning fields in chat completion streaming chunks for models that provide extended reasoning
- **Import from Claude restored** - Re-enabled the "Import from Claude" option in the droids menu for easier conversation migration

### Bug fixes

- **Fixed MCP status indicator to only show when MCP servers are actually configured**
- **Fixed message list flickering**
- **Added support for custom headers when adding MCP servers**
- **Fixed sound files not being included in SEA binary releases**
- **Fixed Ctrl+C interruption messages to only display to users and not appear in logs for cleaner output**
- **Resolved issue where tool use would incorrectly appear in user messages after tool cancellation**

## CLI v0.22.6 (October 30, 2025)

MCP Revamp and OpenAI organization field fix

### New features

- **MCP Revamp** - Complete overhaul of Model Context Protocol implementation ([docs updated](/cli/configuration/mcp))

### Bug fixes

- **Fixed issue with OpenAI organization field**
- **Restore Import (I) options in Droids (subagents) menu**

## CLI v0.22.5 (October 29, 2025)

Default model behavior improvements

### Bug fixes

- **Default Model Behavior** - Improved default model behavior

## CLI v0.22.4 (October 28, 2025)

Report previews and help text fixes

### Bug fixes

- **Restored Report Previews** - Re-enabled HTML preview for reliability reports so you can view them directly in the web
- **Fixed --help text** - Running droid exec --help was previously giving incorrect info for using droid exec in streaming mode. This has now been updated to include the correct flag name with correct instructions.

## CLI v0.22.3 (October 21, 2025)

Detailed transcript view, customizable sounds, terminal setup support, and model upgrades

### New features

- **Detailed transcript view (Ctrl+O)** - Press Ctrl+O to view comprehensive tool execution details with complete breakdowns for all tool types including Execute, Edit, MultiEdit, Create, and more
- **Customizable completion sounds** - Configure sound notifications when commands complete, with support for different sounds in focus mode and custom sound file paths
- **Terminal setup support** - Added automated setup support for Warp, iTerm2, and macOS Terminal with automatic terminal indicators for improved integration
- **PowerShell update** - Now uses `pwsh.exe` for better PowerShell compatibility and reliability on Windows systems
- **Drag-and-drop image support** - Attach images to CLI sessions via drag-and-drop for easier multimodal interactions
- **Custom models in subagents** - Added support for using custom models when executing subagents via Task tool
- **Custom droid descriptions** - Moved custom droid descriptions to Task tool for better organization and usability
- **`droid exec` custom model support** - Added support for custom models in droid exec sessions

### Bug fixes

- **Resolved issues with prompt caching to improve performance and reduce costs**
- **Added model ID logging on CLI tool execution for better observability**
- **Limited messages rendered in Ctrl+O view to improve performance with large transcripts**
- **Fixed sound files not being included in SEA binary releases**
- **Fixed readonly value change issues that caused unexpected behavior**
- **Fixed ExitSpecMode flickering issues for smoother user experience**
- **Removed duplicate custom models header in settings**
- **Improved session persistence to legacy sessions to maintain backward compatibility**
- **Fixed infinite render issues on Windows systems**
- **Fixed 400 error handling and validation**
- **Added model validation error messages for better debugging**
- **Fixed certificate loading timing to occur after logging initialization**

## CLI v0.21.3 (October 14, 2025)

MCP OAuth, system certificates, fuzzy search, and session management improvements

### New features

- **MCP OAuth support** - Added OAuth authentication support for Model Context Protocol in TUI for secure server connections
- **System certificates support** - Added support for loading system certificates on Windows and macOS, with additional Windows system certificates support
- **Fuzzy search implementation** - New fuzzy search for improved CLI command and option discovery
- **Rewind fork workflow** - Added ability to rewind and fork from previous points in conversation sessions
- **Bug report enhancements** - Added version, OS, and shell information to bug reports for better troubleshooting
- **Live updates for subagent tool** - Added real-time progress updates when using the Task tool
- **Enhanced custom droid prompts** - Improved prompts to encourage more proactive usage of custom droids
- **Droid Shield optional setting** - Made Droid Shield an optional configurable setting with toggle support

### Bug fixes

- **Added session_id to stream-json output format for better tracking and debugging**
- **Enhanced authentication flow for smoother onboarding**
- **Streamlined first-run experience by removing redundant onboarding steps**
- **Fixed OAuth callback server port collision issues that prevented authentication**
- **Fixed certificate loading timing issues causing TLS errors**
- **Improved error metadata logging for better debugging**
- **Fixed terminal setup issues across different shell environments**
- **Better error messages when ripgrep (rg) isn't available in PATH**
- **Improved handling of corrupted unicode normalization in file paths**
- **Fixed impact level default value handling**

## CLI v0.19.8 (September 30, 2025)

Droid exec enhancements, custom model support, streaming JSON, and stability improvements

### New features

- **`droid exec` Slack integration** - Added `slack_post_message` tool to droid exec for posting updates to Slack channels
- **`droid exec` streaming JSON input mode** - Added streaming JSON input mode for multi-turn exec sessions for better automation workflows
- **`droid exec` tool configuration** - Added ability to enable/disable specific tools in droid exec sessions
- **`droid exec` pre-created session IDs** - Added support for pre-created session IDs in droid exec for better session management
- **Initial prompt support** - Added support for launching TUI with an initial prompt via command line
- **GLM-4.6 support** - Added LLM proxy support for GLM-4.6 with Fireworks, Baseten, and DeepInfra providers
- **Azure OpenAI for GPT-5** - Added Azure OpenAI support for GPT-5 Codex in TUI
- **Custom droid generation** - Added auto-generation of custom droids using LLM for faster setup
- **MCP streamable HTTP servers** - Added support for streamable HTTP MCP servers
- **Model selector refresh** - Updated model selector UI with improved organization and image support warnings
- **Tab key auto-complete** - Tab key now auto-completes custom commands without submitting for better UX

### Bug fixes

- **`droid exec` session continuation fix** - Fixed droid exec to correctly continue an existing session instead of overwriting session data
- **Dynamic reasoning label for Codex models in UI**
- **AGENTS.md source paths now shown in settings for better transparency**
- **Better error messages when custom model JSON configuration is broken**
- **Manual update instructions when auto-update isn't available**
- **Fixed task subagents to properly terminate on abort**
- **Fixed file rename retry logic on Windows systems**
- **Fixed backslash rendering issues on Windows**
- **Major improvements to custom subagents reliability**
- **Fixed task tool subagents prompt for better execution**
- **Don't stop agent on cancelled file edits in spec mode**
- **Validated working directory exists before executing ripgrep**
- **Fixed subagents to inherit model from TUI parent session**
- **Truncated large MCP tool results to prevent context overflow**
- **Fixed /cost command with Fireworks cached input**
- **Added user-agent header to LLM requests for better tracking**
- **Locked down file system permissions for better security**
- **Fixed rendering for failed edit calls in spec mode**
- **Fixed compaction logic and retry without tool results**
- **Applied output transforms before compaction/caching**
- **Persisted session usage for accurate cost tracking**
- **Fixed /new command to reset timer and sessionId properly**
- **Fixed compaction retry without tool results**
- **Fixed screenshot reading with unicode normalization fallback**
