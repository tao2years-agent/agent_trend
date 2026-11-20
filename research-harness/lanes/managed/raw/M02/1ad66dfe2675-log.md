> ## Documentation Index
> Fetch the complete documentation index at: https://docs.devin.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 2026

> Devin release notes for 2026: new features, improvements, and bug fixes across the product, organized by release date.

**November 16, 2026**

### Sessions & Workspace

**Subscribers and Mark done**

Your sidebar now shows the sessions you are subscribed to. Mark done replaces Archive: it moves a session to your Done folder while it keeps running and stays in the sidebars of its other subscribers, so you can clear your sidebar without stopping work others depend on.

**Phonebook: one identity across your connected services**

Devin now keeps a phonebook of each member's linked identities across Devin, Slack, Microsoft Teams, your git providers, Jira, Linear and Pylon. Devin has a tool to match a person to their connected identities, and it tags people by those linked identities: a mention in Devin now tags the person in Devin and in Slack at the same time.

**Slack channel picker in the composer**

Type # in any cloud session composer to pick a Slack channel.

**Session event search matches words separately**

Searching a session's events now matches each word on its own, so a query finds events that contain the words in any order.

### Security

**CSV export of Security Findings**

Export the Security Findings table to CSV.

**Configure is now Customize**

Security > Configure is renamed Customize. Manage security-profile plugins there, let a profile's skills set scan paths and include/exclude globs, pick the repositories a threat-model rule applies to, and keep skills and rules writable when shared uploads are off.

**Findings polish**

The browser tab is named after the open finding, severity is spelled out in the finding title, and the finding sheet crossfades between findings.

### Enterprise & Settings

**Enterprise Knowledge managers maintain migrated skills**

Enterprise Knowledge managers can read and maintain skills migrated from Knowledge.

**Skills layers page in Customize**

Customize > Skills has a page listing the layers you can write skills to, and malformed plugin content says what is wrong in the catalog.

### Slack & Microsoft Teams

**Tagging Devin in an old Slack thread starts a new session**

When Devin is tagged in a Slack thread whose session is too old to resume, it starts a new session instead of failing. !ultrafast is accepted as an alias of !fastultra in Slack and Teams.

**Mentions on Teams and in quotes**

On Microsoft Teams, @user mentions are written back as native mentions. The quote of a user's message names the mentioned person, and message headers name Slack or Teams.

**November 13, 2026**

**German UI Language**

Deutsch can now be selected as the display language in Preferences, using the terms engineers use for session, merge, push, prompt, logs, service user and secrets.

**Session File Editor Saves on Cmd/Ctrl+S**

The session file editor no longer saves automatically: press Cmd/Ctrl+S to save, a dot on the tab marks unsaved files, a cloud icon in the editor header confirms each save to Devin's machine, and closing a tab or leaving a session with unsaved edits asks first. Devin is told which files you saved so it can take your edits into account.

**Sidebar Filter Menu Simplified**

The sessions sidebar Filter menu no longer has the Machine type and Skill filters; both remain available on the Sessions page. The session title menu now lists the sessions above the current session's parent.

**Artifacts Rail Beside the Chat**

Workspace tabs no longer open on their own as Devin works. What a session produces — pull requests, Changes, previews, the Desktop and Agents views, Plan, citations and attachments — is listed in a compact rail to the right of the chat; hover to see the labels, click a row to open it. The workspace pane remembers per session whether it was open, and a session starts with it closed. Tabs that are not artifacts (Findings, Inbox, Todo…) stay in the add-tab menu, and `?tab=` links still open the tab they name.

**Agent / Ask Moves Into the Composer**

The Agent / Ask switch moves from the header into a dropdown inside the composer. The same dropdown holds the modes for each side — Agent modes (Code, Data) or Ask modes (Auto, Q\&A, Plan) — and switching Agent/Ask flips the composer immediately with that side's default mode selected.

**Review Analytics**

Analytics > Review now shows what became of Review's findings (fixed, rejected, ignored) for the built-in review and for each custom reviewer, and how each version of a custom reviewer's instructions performed.

**GitLab Merge Trains**

Devin Review can now add GitLab merge requests to their project's merge train. Editing a pending inline comment on a GitLab merge request keeps it at its original location.

**Find Skips Collapsed Files**

Find in Devin Review now skips collapsed files by default. Turn off "Skip collapsed files" in the find filter menu to search them; the choice is remembered.

**Chapter Guide File Cards**

Review's chapter guide lists changed files in chapter order with clearer filenames and directory paths; mark individual files or entire chapters as viewed without leaving the guide. Selecting "View as sections" restores the guide's chapters even if you previously saved File tree view.

**Keyboard: Auto-merge Shortcut and Shortcuts Dialog**

Pressing `m` in standalone Devin Review now enables auto-merge when the button offers it, and the Review keyboard shortcuts dialog no longer repeats identical key combinations.

**Clearer Status When a PR Updates or a Code Host Is Slow**

Devin Review distinguishes a newly pushed commit from an existing commit that is ready to view and from analysis updates that leave the code unchanged. When GitHub will not accept a Review comment because the file or line is no longer in the diff, Review says so instead of a generic error. When a code host is slow or not answering, Review and the session's pull request tab say the code host did not respond and keep retrying (after one attempt, not three) instead of saying you have no access to the repository.

**Unlink Devin from a Finding**

You can unlink Devin from a security finding from the findings table or the finding's details, so it can be fixed again.

**Copy as Markdown Includes Validation and Review Reasons**

Copy as Markdown on a finding now includes the sandbox validation result and evidence, and the reason the finding was reviewed or dismissed. A board-backed sealed finding can be edited through the content tool, with the changes shown in Activity.

**Security Sidebar**

Fix sessions are listed in their own Sessions section below Scans instead of nested under each scan or connection, with Scans showing 5 rows at a time; the empty Sessions list matches the main sidebar's wording; and the "Introducing Devin Security" dialog no longer appears over a session page.

**Turn Off Automatic CI Follow-up for your Organization**

Org admins can turn off Devin's automatic CI follow-up under Settings > Customization > Pull requests, and reach the switch from the CI checks tile on Cost Breakdown. It stays on by default, and asking Devin directly still works.

**Session Details in PR Descriptions Can Be Turned Off**

Admins can turn off the automatic session links and requester details in Devin-generated PR descriptions from Devin Sessions settings. The setting is on by default and takes effect when sessions start or resume.

**Organization Picture for Every Organization**

Admins of non-enterprise organizations can now upload or remove an organization picture in Settings > General.

**Plugin MCP Server URLs: Region Choices and Readable Settings**

A plugin can now offer a choice of regions for its MCP server (Datadog uses this for its sites), and that choice is shown before the first sign-in instead of defaulting to one region. The Server URL field shows the part you type as its own input and lists long query parameters one per row. When a plugin moves its server to a new URL, existing installations connect at the new URL without reconnecting.

**Enterprise MCP Editor Asks for a Required OAuth Client**

When adding an MCP server from the catalog that needs your own OAuth client (such as Google Calendar) for the whole enterprise, the form opens the OAuth credentials section, shows the setup steps and asks for the client ID before the server can be created, instead of failing silently.

**November 12, 2026**

### Sessions & Workspace

**Same-kind requests merge into one card**

When Devin asks for several things of the same kind at once (credentials, approvals, network access), they appear together in one compact card instead of a stack of cards.

**"Reminder set" row**

When Devin sets itself a reminder, the session shows a "Reminder set" row with the time or schedule and a link to the reminder.

**Repo file links show as pills**

Bare links to a file on github.com or gitlab.com appear in chat as a short pill naming the file, lines and commit instead of the full URL.

**Drag an open session by its header**

Drag an open session by its pane header onto a sidebar folder, Recent or another session, with the same result as dragging its sidebar row.

**Clearer upload and folder-attach errors**

Attaching a folder no longer fails when one file cannot be read (the rest is attached and you are told what was left out), and uploads blocked by your network's security policy say so with the reason.

### Devin Review

**Redesigned Devin Review page**

The redesigned Devin Review page is now available to all organizations: merge controls, the actions menu and the diff-size pill live in the top bar, the sidebar collapses out of the way, and findings are presented in the redesigned cards and panels.

**"Automatically fix Devin Review findings" setting**

Whether Devin fixes Devin Review findings on pull requests from its sessions is now its own setting, separate from Responding to bots. Each organization's default is in Settings > Devin, under Pull requests, and each person can change it for their own sessions in Settings > Preferences, under Devin sessions.

### Security

**Scan syncs with several connections**

When starting a Security scan you can pick several connections so its findings sync to more than one external destination.

**Source filter lists each connection**

The Source filter on the Findings page lists each connection separately, so findings can be filtered to a single scanner connection.

**Named Custom connections**

A Custom security connection now asks for a connection name (for example "Semgrep"), which is the name it is shown under.

**Delete a finding tag org-wide**

Hover a tag in the Findings filter and click the X to delete it from every finding at once.

**Each finding has its own chat**

The chat button on a finding opens that finding's own chat; the Findings page launcher keeps its general chat.

**Finding status changes can be undone**

Dismissing a finding or marking it reviewed shows exactly what changed, with an Undo button (or Cmd/Ctrl+Z).

**Veracode and Black Duck findings sources (closed beta)**

Security connections can import findings from Veracode (Static, Dynamic, Manual and SCA findings) and Black Duck (vulnerable components of a project version). Dismissing or reopening a finding writes back as a Veracode mitigation or Black Duck remediation status. Available as a closed beta.

### Enterprise & Settings

**Seven more optional GitHub permissions**

Enterprise admins can stop Devin from using the GitHub code quality, deployments, pages, discussions, repository projects, repository hooks and packages permissions under Optional GitHub permissions.

**Approve personal secrets shared with service users**

Anyone who can write to a session can approve a request to use a personal secret they shared with a service user.

**Enterprise-disabled agent modes are shown**

Organization settings show agent modes disabled by your enterprise and explain who can enable them.

**Login page explains IP allowlist denials**

Users signing in from outside their organization's IP allowlist see why on the login page, including their current IP, instead of a blank login page.

**Multiple installations per MCP in Customize**

MCPs signed in with several accounts list each installation separately with its own settings; add another installation from the marketplace card; every installation offers Disconnect and Uninstall with a short explanation. Supabase can switch between read-only and full access from its settings.

**Pylon EU region**

Admins can connect a Pylon workspace hosted in Pylon's EU region, and Pylon issue links open the EU app for those workspaces.

**Bitbucket Data Center clone fixes**

Clones through Devin's git proxy work with Bitbucket Data Center `/scm/` clone URLs and on instances with Basic authentication disabled (the default in version 10).

**MCP tool permissions**

Set each MCP tool to Allow, Needs approval or Block from Customize. Enterprise admins can also limit individual tools to specific organizations.

### Integrations

**Mention-only Slack thread mode**

New Slack thread mode "Reply in the same thread, only when mentioned": Devin stays in the thread but only responds to messages that tag it. Available as the org default and as a personal override.

**Archiving a session archives its Slack code channel**

Archiving a Devin session also archives its dedicated Slack code channel.

**Teams: Devin edits messages in place**

In Microsoft Teams, when Devin edits a message it is updated in place, and a replaced message collapses behind "Show earlier".

**Slack working status for @mentions**

In Slack threads with several people, Devin shows its working status right away when you @mention it, and after it starts acting on an untagged reply.

### Automations & Oncall

**Readable schedules on automation cards**

Automation cards show a readable schedule ("Weekly on Thursday at 6:00 PM...") for schedules that previously showed raw RRULE text.

**Oncall report notifications and PR panel**

Oncall report notifications in Slack open with the report period and list action items as bullets; the report's pull requests panel shows each PR's state, repository and date (GitLab orgs see "Merge requests").

**November 11, 2026**

**Customizable Sidebar Navigation Shortcuts**

The keys for Option-hold sidebar session navigation can be changed in Settings › Keyboard shortcuts.

**Filter Sessions by Service User**

The sessions list's Created by filter includes service users, and sessions created by a service user show its name in Properties.

**Improved Visibility of Stacked PRs**

Improved visibility of stacked PRs within the UI, with an option for stack order preference (shared with Devin Review).

**Design Mode**

Selecting an element in Design Mode opens a compact prompt bar with per-property editing. Draw spotlight boxes or pencil annotations in five colors and send the annotated page image with a note; pick colors from the preview with the eyedropper; and search and use your page's CSS variables in property controls.

**Grouped Repository Setup Suggestions**

You can approve adjacent repository setup suggestions together, or review each diff and approve it separately.

**Mark the Open Session Unread**

Mark unread is available in the sidebar menu for the session you currently have open.

**Bulk Add Secrets Accepts Shell-style Lines**

Bulk add secrets accepts `export KEY=value` lines and keeps a `#` that is part of a value (put a space before `#` to add a note).

**Devin Can Set Itself Reminders**

Devin can set itself reminders to wake up in the future, including in sessions started by automations or service users.

**Link Findings and Threats**

Create a threat directly from a finding's Threat menu, remove a finding from the threat it is linked to, and find saved threats by title or number when filtering findings or starting a scan.

**Start Scan Page with Threat Focus**

Start scan opens as its own page (links can preselect a repository or threat) and includes a Focus on threats section with a searchable table.

**Severity Letters**

Findings use C/H/M/L letter badges instead of severity icons, and Repositories show medium and low counts separately.

**Dismissal Reasons**

Record a reason or note when dismissing a finding from its row, from the finding's PR view, or across a selection; the reason is shown in the finding detail sheet.

**Auto-scan Schedules**

New auto-scans show their schedule before launch and keep their local time when daylight saving time changes.

**Failed Scans Explain Themselves**

When a scan fails before finding anything, the scan page, the session's Findings tab and the per-scan history say why and offer Recover scan or Start new scan.

**Findings and Repositories, Smaller Changes**

Open a repository's scan history from its row; scan summaries show medium and low findings; dragged column widths are remembered; drag a CSV report into a Security connection; remediation sessions link to their assigned finding.

**Ask Before Loading External Content**

Session security profiles gain an Ask before loading external content option. In sessions it governs, images from other sites and HTML/PDF attachment previews load only after you click them.

**Guided Perforce Setup**

Perforce setup guides you through server details and depot selection, reusing known details from a saved connection or importing the server address from your local Perforce configuration.

**Edit Enterprise Plugin MCPs in Place**

Enterprise admins can edit an active plugin MCP's Access, OAuth client and secrets in place.

**Improved In-app UI for Grouped Oncall Alerts**

Oncall alerts with many occurrences can load older ones, and the events view shows whether each event was investigated, forwarded, grouped or skipped, with a link to the session.

**November 9, 2026**

**"Redacted Secret" Pills Link to the Secret**

When a transcript shows a redacted secret, the pill links to the matching entry in Settings › Secrets.

**Forwarded Messages Show the Original Sender**

Messages forwarded into a session show who originally sent them, with a "Forwarded by / via" label.

**Stacked PRs Show "In Merge Queue"**

PRs in a stack that are waiting in the merge queue are labeled as such in Devin Review.

**One Source Filter for Findings**

A single **Source** filter (Connections / Scans) replaces the old Scan type filter on Security findings pages.

**Scan Findings Tab: Real Columns and Easier Navigation**

The Findings tab on a scan uses proper columns with horizontal scrolling, breadcrumbs lead back to the finding you came from, and you can open scan runs directly after a split scan.

**Unlink a Finding from Its Remediation Session**

Findings can be unlinked from a remediation session via the API and MCP tools, and batch remediation now paces sessions to avoid overloading repositories.

**My Analytics for Every Member**

All members, including Teams users, can open **My Analytics** to see their own usage and limits and request more usage.

**GitHub User Tokens Refresh Automatically**

For GitHub Enterprise Server and GitHub apps that issue expiring user tokens, Devin refreshes the token automatically; relink once and you won't be asked again.

**Enterprise Environment: Active Build Queue**

Enterprise admins can see the queue of environment builds currently running or waiting.

**Daily Session Consumption API**

New endpoint `GET /v3/enterprise/consumption/daily/sessions` returns per-day session consumption for an enterprise.

**Incident Reports**

Oncall incident reports open in a dedicated view with a timeline, a UTC/local time switch and copy buttons; summaries are shorter.

**Custom Plugin Logos**

Plugins that declare a `logo` in their manifest show it in the plugin list and overview.

**Deny Button on Slack Permission Cards**

Permission cards in Slack now have a Deny button alongside Approve.

**PR Cards Update When a PR Is Reopened**

Slack and Teams PR cards turn green again when a closed PR is reopened.

**Devin's Slack Posts Keep Their Session Link**

Posts containing tables or headings keep the session link, and messages that fail to format are retried as plain text.

**Teams: Suggestions After Linking**

After linking your Teams account, Devin suggests recent work to pick up.

**November 6, 2026**

**"Reveal Child Sessions" Switch in the Sidebar**

The sidebar's Properties menu has a "Reveal child sessions" switch; turn it off to keep child sessions hidden under their parent until you expand it.

**Side Chats: Queue or Interrupt, and the List Persists**

You can now send messages while a side chat is working: send to interrupt it or queue to run after it finishes, as in the main chat. Older side chats stay in a session's side chat list after a reload or reconnect.

**Setup Steps on Secret Request Cards**

When Devin needs an API key from you, its request card now shows step-by-step instructions for getting it.

**Redesigned Share Artifact Dialog**

The Share artifact dialog has a new layout: set the link name and publish, then see the link name and URL with an inline copy button, sharing options and a "General access" row showing who in your organization can view the artifact.

**Ask Screenshots Carry into the Agent Session**

Screenshots attached in Ask now carry over automatically when you create an Agent session from the thread.

**Customizations Tabs in Settings Search**

Settings search now finds each Customizations tab (Plugins, Skills, MCPs, Hooks, Rules, Memory) and opens that tab.

**Gerrit Changes in "PRs Needing You"**

Gerrit changes you own or review now appear in Devin Review's "PRs needing you", matched to your Gerrit account by verified email.

**Repository Shown on Findings and in Scan Details**

The finding detail sheet names the finding's repository with a link to it, and the Scan details popover lists every repository in a multi-repo scan.

**Sort the Security Repositories Table**

Sort the Security Repositories table by repository name, number of open findings, or last scan time from the column headers; the sort is kept in the page URL. Long repository names show in full on hover.

**Session Sharing: Account Defaults and an Organization Cap**

Admins can set the default visibility for new sessions to "Account, read-only" or "Account, read and write", for the enterprise or per organization, and can limit session sharing to the session's organization.

**Pylon Connection: Allowed Organizations**

Enterprise admins can limit which organizations can use the Pylon connection.

**Gerrit Permission Sync**

Gerrit connections can now sync Gerrit group membership and project access into Devin repository access, like GitHub and GitLab member sync. New Gerrit connections use a long-lived service account password that Devin exchanges for short-lived tokens (requires Gerrit 3.13+).

**Jira Admin Connection Finishes in the App**

Connecting Jira as an admin now finishes inside the Devin app for the person who started it, and any problem during the connection is shown on the Jira settings page in your language.

**Machine Catalog and Machines Tab**

The enterprise Machine catalog settings show OS icons per platform and tier names with slot counts, and the Machines tab shows one row per platform with a dropdown to pick the machine.

**Enterprise Environments Page Loads for Large Enterprises**

The Environments page for large enterprises no longer times out; the organization list sorts by name only.

**Log Out of All Devices**

Log out of the web app, Devin Desktop, the CLI and the mobile apps on every device at once from Settings → Connections.

**Enterprise Multi-organization Incidents**

Enterprise admins get an Oncall tab in Enterprise Settings to enable incidents across multiple organizations and route PagerDuty incidents to the right organization; incidents turn on there automatically.

**PagerDuty Incidents Start from the PagerDuty Slack Channel**

PagerDuty incidents now start from the Slack channel PagerDuty creates, with no time limit on how late the channel appears. The PagerDuty incident source now requires a Slack channel name prefix matching the channel names set in PagerDuty. New PagerDuty responder triggers start with an empty filter.

**Service User Slack Apps: Watch Channels, DMs, Icons, Enterprise Setup**

Automations and oncall responders that run as a service user with its own Slack app can watch channels that app is in (including private channels you're in), reply in DMs when the responder allows them, and post answers when installed org-wide on Enterprise Grid. You can upload an icon for the app, and enterprise admins can set up Slack apps from the Enterprise service users page.

**Manage Oncall Role Can Edit Responders**

Members whose role grants Manage Oncall (without Manage Automations) can now fully load and save the Oncall responder editor and incident settings.

**Devin MCP: Run Automations and Oncall as a Service User**

Devin can now create automations and Oncall responders that run as a specific service user. Terraform devin\_automation and devin\_oncall\_responder resources with run\_as = "organization" no longer show drift on every plan.

**Plugins Show an Installing State**

Plugins show "Installing" on the Marketplace card, in Customize and in the / menu until indexing finishes, and refresh their resources automatically when done.

**Plugin MCPs Honor oauthResource**

Plugin MCP declarations now honor oauthResource, so a web plugin can omit the OAuth resource parameter for authorization servers such as Microsoft Entra that reject it.

**GitLab Fine-grained Personal Access Tokens**

Viewing merge requests and Devin Review now work with GitLab fine-grained personal access tokens, and repo permissions set by GitLab group list their repositories with these tokens. Line counts and reactions are not shown until GitLab adds GraphQL support.

**Slack-synced Sessions Start with the Session Title**

Sessions synced to Slack from the composer now start with a top-level message showing the session title and link (updated on rename), with your prompt and all replies in its thread. Sessions linked to Slack later use the same format.

**Teams Messages Retried on Connection Failures**

Devin's messages in Microsoft Teams are less likely to be lost during a brief connection failure.

**V3 API: Memory\_enabled on Session Create**

The v3 create session API accepts memory\_enabled: false to keep memory off for that session and its child sessions. The grants API no longer lets anyone change or remove a secret owner's own access to that secret.

**November 2, 2026**

**Clearer Read-only Access in the Composer**

Viewers who can read but not write to a session now see that they lack write access in the composer, and "Continue in a new session" is offered only when the new session will be able to read this one.

**"Fix with Devin" Links to the Session**

On a blueprint build page, the "Fix with Devin" toast links straight to the session handling the fix when the batch lands in one session, and points at the rows otherwise.

**Multi-repo Scans up to 1,000 Repositories**

The per-scan repository cap for code scans is raised from 500 to 1,000 in the UI and the API.

**Auto-scan Controls and Schedules**

Auto-scan can be turned on or off from a session's Findings tab, a scan's auto-scan schedule is shown in the scan detail and the Devin MCP `get_scan` tool, and the threat-model lead offers weekly or monthly incremental scans when it finishes.

**Findings Improvements**

The Findings tab's quick-wins card shows a carousel of recommended findings' summaries, and the organization Findings page opens as a session tab with a "Chat with Findings" entry point.

**"Not in" Slack Channel Conditions**

Slack channel conditions in Automations accept "not in", so a trigger can exclude a list of channels.

**Automations Settings Refresh**

The Automations settings page gets an Automations icon, empty states, a default-policy setup flow and consistent row actions; the intro dialog adds a Preflight checks step; and network-policy edits now apply to the automation's already-running sessions.

**Multiple Files in One Slack Post**

Devin's Slack tool can attach several files to a single `post_message`.

**OAuth Discovery from the Server's 401**

When an MCP server answers 401 mid-session, Devin starts OAuth from the `resource_metadata` it advertised, including servers whose handshake is public; a URL installation saved without auth asks the server how it authenticates; and OIDC locations are tried after a non-404 at the RFC 8414 URL.

**Filter Repositories by Provider ID in the API**

The v3 repositories endpoint accepts a `provider_repository_id` filter.

**October 30, 2026**

**Rendered Previews for Markdown and Patch Files from Devin's Machine**

Markdown and .patch/.diff files opened from Devin's machine now open as a rendered preview, like attachments do, with a toggle back to the source.

**Files Tab Improvements**

Folders that contain only a single sub-folder open all the way down in one click (shown as parent / child), and each session's expanded folders are kept when you switch between sessions.

**Multi-line Secret Values**

Editing an existing secret now accepts multi-line values (for example private keys or JSON files) without collapsing them to a single line.

**GitHub File Anchors Open the Review at That File**

GitHub pull request links that point at a specific file (#diff-…) now open Devin Review at that file in the web app and Devin Desktop.

**Header Scripts for MCP Servers on the Session Machine**

MCP servers pinned to the session machine can set a header script: a command run before each call that prints the headers to send, for servers that need short-lived tokens. Admins set it on a plugin's server in Settings.

**Personal Plugins Live-Reload into Running Sessions**

Personal plugins (and their MCP tools) that you install or edit now show up in your running sessions without starting a new one. With "Auto-approve actions on your behalf" on, Devin can save, install and update your personal plugins and skills without an approval card, and reinstalling a plugin updates it in place.

**New Security Connections: SonarQube, Linear and Vanta**

Security connections can now ingest findings from SonarQube, a Linear team (with two-way state and priority sync) and Vanta. Dismissing, reopening or resolving a GitHub Advanced Security finding in Devin updates the alert in GitHub, and issues Devin creates in Linear link back to the finding.

**Typed Finding Tags**

Threat-model profiles can define tag kinds (for example CVE); scans and connection imports report each finding with a value per kind, shown as key/value tags on the finding, filterable under Fields in the findings list.

**Findings Workflow Improvements**

Dismissing a finding now lets you pick a reason (Duplicate, False positive, Not actionable, Accepted risk, Mitigated, Other); findings can be copied as Markdown from the detail panel; and the Findings table columns can be resized.

**Remediation and Search in the API and Devin MCP**

The findings API and Devin MCP can search findings by text, remediate every open finding of a scan in one call (select\_all), and target remediation PRs at a chosen base branch.

**Code Channel as the Default Thread Mode**

Slack admins and individual users can pick "Code channel" as the default for where Devin starts new sessions, and Devin now reads replies inside threads in code channels, not just top-level messages.

**Opt Out of Access-Request DMs**

Slack admins can opt out of the DMs Devin sends for organization access requests.

**Share a Private Reply with the Chat**

In Teams private group chats, each Devin reply has a Share with chat link that posts just that reply to the whole group chat.

**Reaction Trigger for Teams Automations**

Teams automations can trigger when someone reacts to a channel message, with a reaction picker in the trigger conditions.

**Network Access Request Outcomes in Teams**

When a network access request is approved or denied from the web app, the card in the Teams thread shows the outcome and the requested domains instead of disappearing.

**Azure DevOps Webhooks Are Removed on Disconnect**

Disconnecting an Azure DevOps connection now removes the service hook subscriptions Devin installed for it.

**Pylon Setup Dialog**

After connecting Pylon, a setup dialog asks which Devin capabilities to turn on and reminds you to review the Pylon security profile.

**Self-serve SSO Connections**

Enterprise admins can verify ownership of their email domains with a DNS record, then create, name, edit and delete their own OIDC or SAML SSO connections from Settings > Authentication without contacting support.

**Personal Access Tokens Default to Approval Required**

Enterprises that have not configured a PAT policy now default to approval required: members can request a PAT and an enterprise admin approves it. Admins can still switch to self-serve or disable PATs.

**Budgets**

Launching budgets, allowing enterprises to organize user spend and organization spend in a budget hierarchy, and enterprise admins can grant granular permissions to manage a budget with sub-budget limits.

**October 28, 2026**

**Progress Tab Shows Your Tasks Live**

The Progress tab now shows the session's task list as a live drawer; clicking a task filters the Activity stream to the work done for it. Each session has a single Progress tab, and the separate Tasks tab is retired.

**Transcript and Composer Refinements**

End / Cmd+Down jumps to the end of the transcript in one press. Shell cards for chained commands show the whole command and each step's output. Attached .diff/.patch files render as a Changes list, and you can quote a selection from an attachment's code view. Error toasts auto-dismiss by default, with a preference to keep them. Text typed in the composer is kept while the session's organization loads. Images open in a Slack-style zoomable lightbox, people Devin mentions are drawn as avatar pills, file trees use Seti file icons, and the Explorer remembers whether it was open per session. Redaction markers name the secret they matched, plugins that failed to install are listed in session info, and accessibility computer-use actions appear in the worklog.

**Pull Request Tabs**

The add-tab Pull requests menu separates the session's own PRs from mentioned PRs.

**Plugin Item View and User-only Skills**

A plugin's skills, rules, hooks and MCP servers open in one item view. The composer's @ Skills category lists your user-level skills, and mentioning one invokes it.

**Azure DevOps and Bitbucket**

Azure DevOps PR feedback (comments, CI, merge conflicts) is routed to the session that owns the PR, as on GitHub, and webhook setup checks build access before subscribing to build events. On Bitbucket Data Center, Devin can decline pull requests and keeps reviewers when updating one; Bitbucket Cloud webhook setup reports missing scopes and asks you to reconnect.

**Automations**

Channel-only Slack "Reaction added" triggers can be edited, and a refused LLM check shows a clear error.

**Devin Oncall**

Responder writes are rendered as automation-style session cards, and a banner offers to migrate an auto-triage automation to Oncall.

**October 26, 2026**

**New Activity Tab Replaces Progress and Shell**

The Progress and Shell tabs are merged into a single Activity view: one stream of everything Devin did, with search, type filters and a pinnable details drawer. Rows fold under the user message they respond to, and shell commands list the files they edited inside their card.

**Richer Artifacts, Shown Inline**

Devin builds HTML artifacts (reports, dashboards, tables, charts) on a new component kit that matches the app's design system, and can embed an artifact directly in its message instead of only attaching it.

**Transcript and Composer Refinements**

Blocked prompts show a blocked card under the message explaining why. A long shell command is clipped to a preview that opens on click. The browser tab is labelled with the preview's name until the page reports a title. "Keep Devin awake" stays available while a sleeping session wakes. You can star a mode as your default from the capability picker in an existing session, and copy a Devin's link from its rail menu.

**Recording Viewer Opens on the Video**

Session recordings now open on the video by default.

**Edited Slack Messages Are Marked**

When Devin edits a Slack message, its footer says (edited). The "Channel for repository updates" dropdown in Slack settings is now searchable.

**PR Cards and Hovercards in Devin Review**

Hovering a PR link shows the PR card even when no session you can view owns it, with a one-click Devin Review action. The session header's PR chip lists the PRs the session references, and PR pills are coloured by PR state.

**Terraform Oncall Responder Resource**

The Terraform provider adds a `devin_oncall_responder` resource and `devin_oncall_schemas` data source.

**October 23, 2026**

**Choose Your Own Default Agent**

Settings > Preferences now has a Default agent setting: pick the Devin mode new sessions you start in the web app use, or keep following your organization's default. You can also star a mode in the agent picker to make it your default, and it applies to sessions you start from Slack too.

**Quote Elements from HTML Attachments**

You can now quote part of an HTML file Devin attaches: pick an element in the rendered preview, add a note and send it, the same way as in the browser Preview tab.

**Prompt to Switch the Interface Language**

Users whose browser is set to Japanese, Spanish or Portuguese are asked, in that language, whether to switch Devin's interface to it.

**GitHub Issue Assignment Triggers and @Devin-prefix Filter**

GitHub issue automations can trigger when an issue is assigned or unassigned and filter on the assignee. GitHub triggers can also filter on whether a comment, issue, pull request or review starts with an @Devin mention.

**LLM Filter in the v3 API and Terraform Provider**

An automation's LLM filter (llm\_check) can now be configured through the v3 automations API and the devin\_automation Terraform resource.

**Turn on Automatic Reviews from a Pull Request**

On a session's PR card, Analyze now reviews the pull request and keeps reviewing it on every push, with a one-time analysis available from the arrow next to it. On a pull request Devin has not reviewed yet, Review PR lets you turn on auto-review for that PR, for all your pull requests or (admins) for every pull request in the repository. When an earlier commit was reviewed but not the latest, the review page says which commit was last reviewed and offers to review again once or on every push.

**Suggest a Change from the Diff**

Selecting lines of a diff on a GitHub or GitLab pull request in Devin Review now offers Suggest change, which opens a review comment prefilled with a suggestion for those lines.

**Finding Status Updates in the v3 API**

The code scan finding status API (dismiss, resolve and reopen findings, single and bulk) is now part of the public v3 API.

**Scan-complete Summaries by Slack DM or Email**

The scan-complete summary is announced and delivered as a Slack DM when Slack is connected, and by email otherwise.

**Private Sessions from Microsoft Teams Channels**

Messaging Devin privately in a Teams channel now starts a session and sends you a private card with the session link. You can move the conversation into a channel thread, where Devin quotes your message and summarizes what it has done, or keep it private and follow it in the web app.

**Sensitivity-label Policy: Unlabeled Files and Files MCP**

Enterprise admins can let Devin read images and other files that cannot carry a sensitivity label while the Microsoft Teams attachment sensitivity-label policy is on, and can open a short visual guide to what people see in Teams for unlabeled, allowed and blocked files. The policy now also applies to file reads through the Microsoft 365 Files MCP.

**Playbooks Are Moving to Skills**

Playbooks are becoming Skills, and accounts move one at a time. When your account moves, each playbook becomes a skill with the same instructions, the Playbooks pages become read-only with a link to the skill each playbook became, and the Playbooks API reads and writes the skill, so automations, @playbook mentions and !playbook macros keep working. New accounts created from October 24, 2026 start with Skills and have no Playbooks.

**SharePoint Support in the Microsoft 365 Files MCP**

The Microsoft 365 Files MCP can now find SharePoint sites, list their document libraries, and browse, read and write files in them using the scopes you already grant. The Microsoft 365 skills cover SharePoint document libraries, batched mail reads and a clearer confirmation flow for writes.

**Redesigned Customize Page**

The Customize page has been redesigned. You get a page for each layer you administer (yourself, your organizations, your enterprise) with one search across its skills, rules, hooks, MCPs and plugins. A layer's plugin list now includes everything a wider layer installs for it, plugins that still need an MCP connection are listed first and can be connected from their row, a plugin's details list its Required and Optional dependencies so you can install or connect them from there, and items from a layer you manage can be edited in place.

**Download and Read Blueprint Files**

Blueprint files can be downloaded from Settings > Blueprints > Files, and their contents read through the v3 API for organization and enterprise blueprints. Saved browser profiles are excluded.

**Blueprint Schema Errors Shown Inline**

When you save a blueprint that is valid YAML but does not match the blueprint schema, the editor shows the error directly under the YAML, naming the field and the problem.

**October 21, 2026**

**"Received Feedback" Rows Open the PR Comment**

Clicking a "Received feedback from …" row in a session opens that pull request comment, following your PR link preference. Rows covering several comments expand to show each one.

**Quote a Devin Review Finding into the Chat**

In a session's PR review, each Devin Review finding has a "Quote in chat" button on its inline comment and in the findings list, and Cmd+I quotes the open inline finding into the chat.

**Devin Review Supports Bitbucket Cloud**

Devin Review now supports Bitbucket Cloud. Connect a Bitbucket Cloud workspace under Settings > Connections: review webhooks are installed automatically, with the install status and a Refresh button in the connection's details, and members can link their personal Bitbucket Cloud account so Devin Review posts as them.

**Merge Past Repository Rules You Are Allowed to Bypass**

Users whose GitHub account may bypass a repository's merge requirements can now merge a blocked pull request directly from Devin Review, after confirming.

**Reactions on /devin Review Comments**

Commenting /devin review on a GitHub pull request now gets a 👀 reaction when the review starts and a 👍 when it completes.

**Resolved Counts in Analytics Only Include Findings Fixed in Code**

Devin Review analytics now count a finding as resolved only when it was fixed in code, by a later push or by Devin. Findings dismissed by a reviewer and duplicates no longer count, so resolved numbers will be lower.

**Support Lite Mode in Devin Oncall**

Oncall responders and incident investigations can now be configured to run in Lite mode.

**Request-access Link for Repositories Not Yet in Devin**

Enterprise admins can set a "Request access link" under Settings > Connections, with an optional separate link for GitHub and for GitLab. Members see it next to repositories that are not connected to Devin yet when picking a repository.

**Gerrit Webhooks Installed Automatically**

Connecting a Gerrit server now sets up Devin's webhook on the projects the service account is allowed to configure, when the server has the webhooks plugin. Projects where it cannot are reported with the reason.

**Hook Matchers Written as a List**

A hook matcher written as a list of strings now matches any of them, not only the first.

**Non-Latin Organization Names**

Organizations can now be created with names in Japanese and other non-Latin scripts.

**October 19, 2026**

**Clearer Work Log While Devin Works**

The current step in the work log shows what Devin is doing as soon as that summary is ready instead of "Deciding action", and status lines no longer narrate internal housekeeping.

**Devin Oncall Is Now Generally Available**

Devin Oncall is now available to all organizations. Responders watch your Slack or Microsoft Teams channels and PagerDuty incidents, triage new alerts, bug reports and support requests, and investigate them using your telemetry tools, code, deployments and runbooks to post a likely root cause and recommended next actions. Devin can also join incident channels to keep investigating and maintain a self-updating incident report, and recurring Oncall reports summarize incidents investigated, issues identified and fixes shipped. Find it under Oncall in the sidebar; organization admins connect tools and manage responders.

**Rules Editor for Devin Review**

Review settings has a new rules editor: exclusions and review rules sit in one list of expandable rule cards, and their targets are picked inline.

**Clearer Notice for Unreviewed Changes**

When a pull request was reviewed at an earlier commit and newer commits have not been reviewed, Devin Review now says "Latest changes haven't been reviewed" instead of "Devin hasn't reviewed this pull request", and offers "Review now" to run a one-off review of the latest commit without turning on automatic review for the pull request.

**CI Status for Commits, Branches and Tags**

Devin can now check CI status for a commit, branch or tag (for example a post-merge run on main), not only for a pull request, on GitHub, GitLab, Azure DevOps and Bitbucket Cloud and Data Center. Bitbucket build statuses are now visible to Devin on pull requests and commits.

**Webhook Auto-install Results for GitLab and Bitbucket Data Center**

The webhook settings for GitLab (with automatic webhook install enabled) and Bitbucket Data Center now show what the last automatic install did for each project or group and flag hand-made Devin webhooks that would cause duplicates.

**Propose Edits to Shared Plugins and Skills**

Devin sessions can now propose edits to organization and account plugins and skills even when the session's creator can't edit them. An admin with the right permission approves the change.

**Attachment Classification by Sensitivity Label**

Enterprise admins can configure Microsoft Teams attachment classification once per enterprise; it applies to every organization in the enterprise. Files with an allowed Microsoft sensitivity label are shared with Devin and files with a blocked label are rejected; unlabeled files and SharePoint or OneDrive links ask the sender to classify them before Devin receives them, and the card explains when a file was not shared and why.

**Recover a Crashed Session from Teams**

When a Devin session crashes, Microsoft Teams posts a message in the thread saying so, and replying in the same thread retries the session.

**Teams Admin Alerts**

Settings → Microsoft Teams warns when a Teams admin has blocked the Devin app and explains how to allow it. Admins who manage Teams get a Notification Inbox alert when their connection needs attention or when a Teams automation stops receiving messages from its channel.

**Teams Tag Mentions**

Devin can mention a Teams tag (for example @Design Reviewers) when it posts to a channel through the Microsoft 365 MCP, so everyone in the tag is notified.

**Clearer Group-chat Permissions**

In Teams group chats, members who can't message the chat's existing Devin session now see why.

**Turn Off Nightly Memory Dreaming**

You can now turn off nightly memory dreaming from the Memory tab while keeping personal memory on in your sessions.

**October 16, 2026**

**Multiple Side Chats from One Message**

A message that already has a side chat can start another: its side-chat button opens a menu of the message's threads with a "New side chat" option.

**Command Palette Finds Archived Sessions**

Cmd+K session search now includes archived sessions, marked with an icon.

**Queued Messages Stay Editable While Devin Is Idle**

Queued messages can be sent, edited, removed or reordered after Devin stops or the session goes to sleep, instead of being locked until the next turn.

**Open Chat Images in a Tab**

Images in the chat can be opened as a tab from the image viewer, so you can view an image alongside the conversation.

**Numbers Follow Your Display Language**

Numbers across Devin (usage, dashboards, counts) now use the thousands separator and decimal mark of your selected display language instead of the browser locale.

**Browser Previews Wake Sleeping Sessions**

Opening a browser preview of a sleeping session restarts the servers behind the preview automatically, without a chat message. The visitor may need to reload once the server is back.

**/devin Commands on GitLab Merge Requests**

`/devin review` and `/devin <prompt>` comments now work on GitLab merge requests.

**Bitbucket Cloud Merge Readiness**

Devin Review shows merge readiness for Bitbucket Cloud pull requests: ready, or blocked by required approvals, default-reviewer approvals, builds or requested changes when the branch enforces its merge checks.

**Word-level Highlights for Edited Lines**

In Devin Review diffs, an edited line shows which words changed even when lines were added or removed right next to it.

**List and Search Pull Requests**

Devin can list and search a repository's pull requests by state, author, branch or title on GitHub, GitLab, Azure DevOps, Gerrit and Perforce Swarm, instead of opening PRs one at a time.

**Git Tools for Issues, Labels, Assignees and Branch Protection**

Devin has built-in tools for issues (view, list, create, comment, edit), repository labels, PR assignees, repository info and branch protection rules on GitHub. Repository info and branch protection also work on GitLab, Azure DevOps, Bitbucket and Gerrit, and the issue and label tools on GitLab.

**Bitbucket Data Center Webhooks Installed Automatically**

Bitbucket Data Center connections now set up their own webhooks: one per project the access token administers, covering every repository in it. Projects created later are picked up within a day.

**Explain and Search Missing Repositories on GitHub**

When a repository is missing from the repository picker, Devin can explain why and search your repositories by name on GitHub and GitHub Enterprise Server as well as GitLab, and points you to linking your personal account when that is the cause.

**Personal Azure DevOps Connections per Tenant**

Linking a personal Azure DevOps account now works when it belongs to more than one tenant: Personal connections lists one entry per tenant, and a failed connect shows an error.

**Microsoft Teams: Separate Direct Messages and Group Chats Access Settings**

Teams Default Access now has separate "Direct messages" and "Group chats" settings, so admins can control them independently of channel access.

**Microsoft Teams: Forwarded Messages as Context**

Devin now sees the content of messages forwarded to it in Teams as quoted context, separate from your comment.

**Enterprise Setting to Hide the Legacy MCP Marketplace**

Enterprise admins can turn off "Show legacy MCP marketplace" in Enterprise settings → Plugins to hide the legacy MCP marketplace and custom MCP entry points and stop Devin from adding such MCPs itself. MCPs already added keep working.

**Google Calendar: Suggest Meeting Times**

The Google integration can suggest meeting times, ranking slots by how many attendees are free and showing who can't make each one. Google MCP installs that grant only some permissions now work for the services granted.

**SAML Single Logout on Sign-out**

Signing out of an enterprise SAML SSO login can also end the session at the identity provider, when a sign-out URL is configured for the connection.

**October 14, 2026**

**Chat Width Preference**

A new Chat width preference (Preferences → Appearance, or the command palette's Accessibility menu) widens the session chat and composer on large screens, so code blocks and tables need less horizontal scrolling.

**Interrupting Devin Keeps the Partial Reply**

When you send a message while Devin is still writing a reply, the part of the reply you already saw stays in the chat instead of disappearing.

**Virtual Environment Picker Uses Your Starred Default**

New sessions use your starred virtual environment default unless you pick another one in the composer; the picker resets your selection across reloads.

**Session Links in Devin's Messages Render as Chips**

Links to another Devin session inside Devin's messages now show as a chip with the session's ticket key and title (or the session title), styled like other inline chips.

**Child Sessions Show in the Sidebar Across the Archive Split**

A child session now appears in the sidebar on its own when its parent is on the other side of the archive: an unarchived child of an archived parent shows in Recents, and an archived child of an active parent shows in Archived.

**Filenames on Diff and Patch Attachments**

Diff and patch attachment chips in a session now show their filename, so multiple patches in one message can be told apart.

**Browser Previews Shared to Slack**

When Devin opens a browser preview in a Slack-started session, the thread gets an "Open preview" link, and Devin no longer repeats the link in chat.

**Manage Devin Review Permission**

Anyone with the "Manage Devin Review" permission can now edit Devin Review settings and review rules and search repositories in Settings > Review without also being an account, org or Git integrations admin. The org-level "Manage review rules" permission grants the same for that organization's review rules and custom reviewers only, not the account's Review settings. Admins can add the permission to an existing role or create a role with Member permissions plus "Manage Devin Review".

**Merge Method Remembered per Repository and Branch**

Devin Review remembers the merge method you last picked for each repository and target branch, so you don't have to reselect "Squash and merge" on every PR.

**Export Findings as SARIF**

Code-scan findings can now be exported as SARIF 2.1.0 — from the scan page's export menu and from the findings export API — in addition to CSV.

**Microsoft Teams**

Saving a Teams message automation now fails with a clear explanation (and a docs link) when Devin can't watch the channel, for example when the Devin app isn't added to the team; previously the automation saved but never triggered. The channel picker no longer offers private and shared channels, which message triggers don't support. Automation replies always link to both the session and the automation. When several Devin accounts share one tenant, a thread reply reaches every automation that answered it, and Devin explains when a chat or thread belongs to a different Devin account than yours. Enterprise customers on a devinenterprise.com domain sign in to Teams through their enterprise API host.

**GitHub Enterprise Server App Permissions**

Newly registered GitHub Enterprise Server apps request the same permissions as the github.com app: code scanning, secret scanning and code quality (read), Actions (write) and repository creation, plus the `team_add` webhook.

**New Observability Plugins**

Splunk, Elastic, Dynatrace, Chronosphere and Google Cloud Monitoring are now available as plugins.

**Clearer MCP Server and Plugin Approval Cards**

MCP server requests in a session now say which action is requested (delete, enable, disable) and keep showing the server's name after you approve or deny; plugin approval prompts in organizations without an enterprise say "organization" instead of "enterprise".

**Repositories and Blueprint APIs Promoted to V3**

The repositories and snapshot-setup (blueprint/build) endpoints are now part of the stable v3 API at `/v3/...`; the `/v3beta1/...` paths continue to work.

**Terraform Provider: Repository Indexing, Blueprints and Repositories**

The Devin Terraform provider now has resources for repository indexing, blueprints and blueprint files, and a repositories data source.

**SSO-only Enterprise Members are Routed to Their Enterprise Sign-in**

Members of SSO-only enterprises on a dedicated domain who also have an old personal account are now sent to their enterprise sign-in page instead of looping back to the login screen.

**October 9, 2026**

**Memory and dreaming**

Devin now remembers what it learns about you and your work across sessions. Memory is personal to you and not shared with your organization; you can review its files and turn it on or off from Settings > Customization > Memory. Each night Devin reviews your recent sessions and refines what it remembers under Recent dreaming sessions in the Memory tab. Org admins can turn memory on or off for their organization, and enterprise admins can force it on or off for every organization.

**Session resume window is now 14 days**

Sessions can be resumed for 14 days after they go to sleep (previously 30 days). Session history remains available after that; starting new work from an older session requires a new session.

**Font family and size settings**

Settings > Appearance now lets you choose the font family and font size used in the session transcript and editor.

**Command palette and Find**

Command palette actions now show their keyboard shortcuts, and Cmd/Ctrl+F in a session reaches more content, including collapsed tool output and PR descriptions.

**Transcript diff cards for large edits**

When Devin rewrites a large file, the transcript now shows a real diff instead of a 'file replaced' summary; edits above roughly 5,000 lines show line counts only, and temporary files created and deleted within one step no longer appear as changes.

**Notification settings and inbox**

Settings > Notifications now gives every notification type its own switch, and the inbox adds All/Unread tabs, a mark-as-read icon, muting a notification type directly from a row, and a hover preview from the bell icon.

**User preferences sync across apps and devices**

Most user preferences (dismissed banners, Review scope, sidebar and wiki toggles, last repository selection, and more) are now stored on the server, so they follow your account across the web app, Devin Desktop, and devices instead of being saved per browser.

**Hide Microsoft Teams sessions from your team**

The "Hide from team" session action now also works for sessions started from Microsoft Teams, so teammates won't see them in team views like All Sessions.

**Repository AGENTS.md loaded on setup**

When Devin sets up a repository, it now reads the AGENTS.md at the repository root and follows its instructions for the session.

**Attachment links in PRs**

Attachment URLs Devin posts into PRs use your tenant domain on dedicated tenants, and on Enterprise plans they no longer expire after 7 days.

**Devin Ultra available regardless of data retention setting**

Devin Ultra is now available to all enterprises with the Ultra preview enabled, including those with zero data retention; previously Ultra was unavailable when a data-retention restriction was in place.

**Manage findings permission**

A new Manage findings permission for code and security scans lets admins control who can change finding status or dismiss findings, separately from who can run scans.

**Create scan and Create profile with Devin**

The Security page's Create scan and Create profile buttons offer Generate with Devin (describe what to scan and Devin drafts the configuration) or Manual, and the scan and profile sheets use the updated form layout.

**Scan findings in the session language**

Scans started from a session via /scan write their findings in the language of the session instead of always English.

**Failure notification backoff**

When an automation keeps failing, failure notifications are sent on a backoff (after the 1st, 3rd, 9th... consecutive failure) instead of on every run, and resume on the next success.

**Slack write-back posts attachments inline**

Automations that reply to Slack now post images and files Devin produces inline in the Slack message, and Devin's Slack tool embeds images directly instead of linking.

**Microsoft Teams**

DM sessions are private by default; non-enterprise connections default to all channels of teams where the app is installed (adjustable in Settings > Connections); and the note posted when an archived session is disconnected includes a reconnect link.

**Team sync**

Group and team sync from identity providers is more reliable: removed members are purged from preview on the same run, and sync no longer stalls on groups that fail to resolve.

**Only allow connecting admin-configured MCPs**

The enterprise setting that stops members from connecting their own remote MCPs is now called 'Only allow connecting admin-configured MCPs'. Admins can add an MCP with Access set to Personal so each member signs in with their own account, including URL-only MCPs.

**Microsoft 365 MCP**

Microsoft 365 MCP sign-in uses account selection instead of forcing re-consent, no longer sends users to 'Approval required' after admin approval, and guest users can't be DMed through the connector.

**Atlassian MCP v2 endpoint**

The Atlassian (Jira/Confluence) MCP connector uses Atlassian's v2 MCP endpoint.

**Org-level Agent capabilities**

Admins can enable agent capabilities for specific organizations, instead of these being set only at the enterprise level.

**Secrets sheets**

New secret and Bulk add in Settings > Secrets use the updated sheet layout with clearer scope selection.

**Devin Wiki in Thai**

Devin Wiki can now be generated in Thai. Enterprise admins can enable it under Settings > Code Indexing > Languages.

**October 7, 2026**

**Notification Inbox**

Devin now has a notification inbox. The bell in the sidebar collects notifications about your sessions, such as when Devin finishes working or needs your attention, and opening a session marks its notifications as read. A new Settings > Notifications page lets you choose which notifications you receive in the inbox and which are also pushed to your phone. On mobile web, the bell opens your notifications full-screen.

**Command Palette Refinements**

The ⌘K palette lists the same navigation pages as the sidebar, with the same names and icons, lists settings pages directly (not individual settings), and when a pull request's review is open in a session's workspace pane its actions (copy link or branch, open in Devin Review or GitHub, convert to draft, close) are available from the palette. The C then L / C then B copy shortcuts also work in the review tab.

**Sidebar Polish**

Right-clicking a session opens its menu next to the row; the Automations filter is a single choice; the list refreshes sooner after clearing a search; and on mobile web the session list keeps its order while the sidebar is open.

**Transcript Layout Fixes**

Message bubbles and wide tables no longer overlap the timeline ticks on the right edge, and wide tables no longer jump sideways shortly after a session opens. File reference chips for same-named files show enough of the path to tell them apart, with the full path on hover.

**Preview Chips Are Links**

Browser preview chips in the worklog are now links: Cmd/Ctrl-click or middle-click opens the session's preview in a new tab.

**Issue Card Titles Link to the Issue**

Clicking the title on Linear, Jira and Pylon issue cards now opens the issue.

**Merge Queue Status Across the App**

The PR header shows an orange "Queued" state while a pull request is in the merge queue; Devin Review has a "Remove from queue" button; the "Re-queue PR" prompt clears once the PR is queued; the "In merge queue" session status is grey; and a session with a stack of PRs shows "Stack is approved" only when every open PR in the stack is approved.

**Private Key Strings Are Redacted More Aggressively**

When a saved secret contains a private key, Devin now redacts each line of the key in command output, so the key stays hidden even when only part of it is printed.

**Microsoft Teams**

Teams notifications and chat previews for Devin's card messages now say what the card is about instead of "Card"; after you link your Devin account, the "account isn't linked" notice confirms the connection, offers the organization picker and lets you resend your message with one click; messages you send from the web app into a Teams DM with Devin appear as sent by you; and Devin can see existing reactions when it reads Teams channel, thread and group chat history.

**Slack**

Files you asked for are uploaded into the thread while supporting documents are linked to the session, so threads stay compact; the first message of a session started from Slack shows @Devin instead of the bot's user id; and clicking a Devin button in Slack without access to the organization now shows a short message instead of failing silently.

**Refreshed Plugin Rows and Logos**

Plugin rows in Customize and the marketplace have a more compact look with app-style logo tiles and say whether a plugin is installed or recommended; the plugin details panel lists skills in two columns and leads with example prompts when a plugin provides them. MCP and plugin logos use one consistent tile and stay visible in dark mode.

**Devin Review Permissions**

Enterprise admins can grant the "Manage review rules" permission to custom organization roles. Editing an organization's Review rules and exclusions requires that permission (members with only Review use access see them read-only), and applying suggested edits or changing a pull request's auto-review setting requires Devin Review permission.

**Security Profiles: Teams Group Chats**

Security profiles have a Group chats setting under Microsoft Teams that controls whether Devin can read the group chat it was mentioned in, separately from channels.

**Settings Dialogs Use the Updated Form Styling**

Dialogs across Settings (automations, readiness, code review, code scans, sessions, workspaces, credentials and access, outposts, environments, gateway, review, plugins and blueprints) now share one form layout with inline validation. The blueprint Upload file dialog shows the generated environment variable as a read-only field with a copy button, and the webhooks receiver guide matches the API Quick start.

**Analytics**

ACUs per merged PR now counts merged PRs created in the selected period, and "per session user" counts users who started sessions; "previous period" comparisons always cover the same number of days immediately before the selection; trailing averages are weighted by usage; "Active users" on Overview and the Local tab include people whose usage was free; the Review tab's repository usage counts only the period's days; the Local tab has standard drilldowns and no organization filter; drilldown changes are coloured by whether the change is good for that metric; numbers use one format with one decimal place; tooltips match the calculations; and failed charts show an error with Retry. Oncall appears only for organizations that have Oncall or Oncall usage.

**October 5, 2026**

**Terminal Tab in the Session Workspace**

The session workspace has a new Terminal tab for running commands on Devin's machine. The Files tab can now be opened while Devin is asleep, and opening Files or Terminal wakes Devin.

**Keyboard Shortcuts and Command Palette**

The Settings → Keyboard shortcuts page is now available to everyone. Mark the current session done (or not done) with ⌘⇧E / Ctrl+Shift+E, and actions from a session's … menu can be found by typing in the command palette (⌘K).

**Open HTML, PDF and SVG Attachments in a New Tab**

HTML, PDF and SVG attachments have a new "Open in new tab" action that opens the file on a page of its own, with the filename as the tab title, instead of downloading it.

**PR Hover Cards in the Owning Session**

Hovering a pull request link shows its PR card even in the session that created or took over it.

**Preview Quote Box Stays on the Picked Element**

In Preview, the element highlight and quote box stay on the picked element when the pane is resized or the page scrolls, and the quote caption box is fully visible near pane edges.

**Preview Loads Straight In After Wake**

Opening a preview for a sleeping Devin session now loads straight into the app when the session resumes within a few seconds, instead of flashing a loading screen.

**Side Chat Attachments**

Files attached by a side chat reply now show as attachments.

**Slack User-Group Mentions**

Slack user-group mentions in Devin's messages now show up in the webapp as named `@group` mentions instead of raw text.

**Devin Review Effort Levels**

Trigger actions can set a Devin Review effort level, and enterprise admins can choose the default effort level in enterprise Review settings.

**Repository Access Without Devin Review Permission**

Users with repository access can open PRs, inspect diffs and read existing Devin Review findings even without permission to run Devin Review. AI review actions are hidden for them, and the Bugs tab explains how to enable Review.

**Azure DevOps Review Summary Threads Are Posted as Closed**

On Azure DevOps, Devin Review's summary comment (including "No Issues Found") is posted as a closed thread, so it no longer blocks PRs under the "Comments must be resolved" branch policy. Inline findings are still posted as active threads.

**PR Links in Devin Review Follow Your Preference**

Links to other pull requests inside a PR description or comment in Devin Review follow your PR link preference, so with "open in session" they open as a tab in the session.

**Code Scan Findings Page**

Severity section headers stay pinned while you scroll, and once you check a finding each header shows a checkbox that selects or clears the whole severity. The select-all checkbox in the bottom bar selects every finding in the current tab, not just the loaded rows. The scan usage card shows how long the latest run took.

**Fetch a Single Code Scan via API and MCP**

API users can fetch a single code scan by id, including its attachment URLs, through `GET /v3/organizations/{org_id}/code-scans/{scan_id}`; the Devin MCP code-scan tool has a matching `get_scan` action.

**Microsoft Teams Improvements**

The "Devin is working" status is a compact single line showing the current step; click it to see the full worklog. With "post as yourself" enabled, messages that quote another message are posted under your name too. When a file shared in Teams can't be opened, Devin recommends connecting the Microsoft 365 OneDrive & SharePoint MCP. Automations can grant Teams direct messages.

**Bitbucket Data Center PR Reviewers**

Devin can now assign pull request reviewers on Bitbucket Data Center, by username, email address or display name.

**Customize Points to the Right Tab**

Opening an organization or enterprise skill, rule or uploaded plugin from the Personal tab shows which tab to edit it from with a button that takes you there.

**Analytics Date Ranges Include Today**

The "Last 7 / 30 / 90 days" ranges include today instead of ending yesterday; custom-range calendars match the reporting dates, and dashboard tooltips were rewritten for clarity.

**October 2, 2026**

**Sidebar Search and Filters**

Sidebar search now shows matching sub-sessions and workflow sessions even when their parent is collapsed; the Updated-time filter no longer defaults to the last month, and the Filters menu uses the available screen height. The session status no longer keeps asking you to review, approve or merge a PR once that step is done.

**Transcript Polish**

Edit cards show the changed lines even when the edit is far down the file and stream the newest lines while an edit is being written; chained shell commands keep their per-step rows while output streams and when a command fails; large scripted-tool and subagent runs expand instantly; and closing a screenshot viewer keeps your transcript position.

**Code Citations Link to the File at the Cited Commit**

Cited files show the repository host's icon, which opens the file at the cited commit on your git provider, including for clones in custom-named folders.

**Reliability Fixes in Long Sessions**

Fixed the transcript flickering or going blank when returning to a background tab, the transcript scrolling by itself while you read older history, syntax highlighting flashing to plain text when a diff remounts, and skill content not loading when clicking an "Activated skill" entry.

**Display Settings Follow Your Account**

Settings-table sort order, session list display options, PR review display toggles and the Devin Desktop release channel now follow your account across browsers and devices instead of staying on one machine.

**Test Recording Viewer Fullscreen**

The test recording viewer has a fullscreen button again.

**Perforce Environment Builds**

Snapshot builds for large Perforce depots now have up to 3 hours to sync instead of failing after 10 minutes, and builds no longer fail when a blueprint step installs the Perforce CLI itself.

**Blueprint Links for Non-GitHub Repositories**

The "Open settings" link on blueprint cards now works for repositories hosted outside github.com, and repository setup status is reported correctly when the repository is referenced as `github.com/org/repo`.

**Find Matches File Names and Authors**

Find (Cmd/Ctrl+F) in Devin Review now matches file names and folder paths in the diff, including a renamed file's previous path, and comment authors' usernames in the Discussion tab.

**Azure DevOps, Bitbucket, Gerrit and Perforce**

Review comments on Azure DevOps, Bitbucket, Gerrit and Perforce no longer ask for a 👍/👎 reaction. Azure DevOps Server PR URLs that include the server's port now work even when the connection was registered without it; ADO links with spaces in project or repository names resolve consistently; and ADO/Bitbucket access failures point to the correct provider integration.

**Select All Findings of a Severity**

On a security scan, after checking a finding you can click "+ Select all Critical" (or High, Medium, Low) in that section's header to select every finding of that severity, including ones not loaded yet, and resolve, dismiss or fix them in one step. The v3 API's bulk status update accepts the same `select_all` filter.

**Compact Automation Cards in Chat**

The "automation created/updated" and approval cards in chat now show a compact, collapsible summary of the automation, expanding to the full details on click. Schedule triggers in the editor no longer break mid-phrase.

**Microsoft Teams Access Settings Are Enforced**

Microsoft Teams access settings (allowed channels, group chats, direct messages) now take effect: Devin won't start sessions, reply or post in blocked conversations, and tells the user why. The channel allowlist picker supports searching across all teams or browsing team by team, and Save is enabled only when something changed.

**Microsoft Teams Polish**

The Teams sync toggle shows which channel a session posts to; Devin can read the group chat it was @mentioned in for context; "Enable posting as you" opens a one-click dialog; Teams-bound sessions no longer see the Sync to Slack prompt and web sessions in Teams-connected workspaces get a one-time Sync to Teams prompt; and the channel picker stays responsive with thousands of channels.

**Slack**

Slack PR cards turn yellow while a PR is in GitHub's merge queue; sessions running longer than 30 days keep posting to their Slack thread; and plugin/skill approval requests in Slack, Teams and Linear say what Devin wants to do instead of showing the raw tool name.

**GitHub Comments That Start Sessions Get an 👀 Reaction**

GitHub PR comments that start a new Devin session now receive an eyes reaction alongside the session link.

**Jira: Invalid Webhook Connections Surface Immediately**

Invalid Jira webhook connections now show an immediate reconnection reason instead of repeatedly retrying; temporary Jira outages continue to retry automatically.

**Bitbucket Data Center OAuth Apps**

Enterprise admins can register Bitbucket Data Center OAuth applications in Bitbucket settings (also findable in settings search), letting users link their own Bitbucket Data Center accounts. Create PR from suggested skills and environment suggestions can now commit multiple files to Bitbucket Cloud repositories.

**MCP Settings Show Only the Controls You Can Use**

Members see a shared MCP's connection status instead of a Connect button they cannot press; a shared installation is managed only from the tab that owns it (Personal/Organization show your own connection with a link to where it is managed); per-member shared MCPs appear once under Personal; API-key installations no longer offer OAuth sign-in; and "New MCP" on the Personal layer adds the server to your personal plugin.

**MCP Connect Card in Sessions**

The MCP connect card now stays on screen after you connect, shows the server logo, says whose account a Shared or Personal connection acts as, and can retry a failed connection. Connecting a Shared Google MCP always shows Google's account chooser so you can pick a service account.

**Organization and Enterprise MCP Authentication Editors**

Organization and enterprise MCP editors show editable authentication header templates separately from write-only secrets, with safe handling of pasted Bearer prefixes.

**Plugin Previews Before Install**

Plugins offered to you but not yet installed show their skills, MCPs, hooks, rules and dependencies before install, and managed plugin bundles can contain up to 10,000 files.

**Outposts**

Opted-in Outpost containers start their browser automatically so browser-opening commands work without manual startup, and Outpost sessions can open the built-in IDE tab.

**September 30, 2026**

**Devin Mono for Code and Terminals**

Code blocks and terminals in the app now render in Devin Mono, a new monospace typeface designed to pair with the app's UI font. Shell output in the Progress tab uses the same character spacing as the rest of the app.

**Read-Only Live Shell Preview**

The streaming terminal preview in the worklog is now a read-only text view: clicking it no longer places a cursor or captures keyboard input, text can be selected and copied normally, and multi-line progress bars redraw correctly.

**Messages Are No Longer Lost When the Connection Drops**

Messages sent to Devin from the browser, Devin Desktop or mobile right before the connection drops (closing the tab, backgrounding the app, a reconnect) are now saved by the server instead of being lost.

**Session Preview Cards in the Sidebar**

Hovering a session in the sidebar opens a preview card showing the session's title and status, the last few lines of Devin's latest response (updating live while Devin is working), the session's pull requests with their status, and its working directory. PR rows in the card follow your "Pull request links open…" preference.

**Sidebar and Command Palette**

The sidebar now names the approval a session is waiting on ("Approve skill", "Approve playbook", "Approve sessions") instead of a generic "Approval required". The Pinned folder has a "+" button to start a new, already-pinned session, the Filter menu search also matches filter values (typing "cloud" finds the Agent filter), and sessions in the command palette show the same working / unread / attention indicators as the sidebar.

**Context Tab**

The Context tab now shows the session's reports and images first; other files fold into one row, and memory opens from a single row.

**Session Menu Polish**

Unavailable session menu actions are hidden or explain why they cannot be used, and the explanation for Mark done / Stop session appears when hovering the info icon rather than the whole row.

**Voice Call Bar Follows the Composer**

The voice call bar fills the composer row correctly, including in a narrow pane.

**Sharper Testing Recordings and Screenshots**

Devin's testing recordings and screenshots are captured at 2× resolution, so zoomed-in footage stays sharp.

**Hardware-Accelerated Emulators in Sessions**

Android emulators and other KVM-accelerated tools now start with hardware acceleration on the first try in Devin sessions, with no permission workaround needed.

**Ask Devin Recognizes Commented-Out Code**

Ask Devin now recognizes when code in its search results is commented out, so it no longer describes commented-out routes, features or settings as if they were active.

**Devin Fixes Its Own PRs' Review Findings Before They Are Posted**

When Devin Review reviews a pull request that a running Devin session opened, the findings are no longer posted as review comments right away. They go to that session first: with Auto-fix on Devin fixes what it can, with Auto-fix off it only reports back. While this happens the PR shows a "Devin is addressing Devin Review findings" status. Once Devin is done, only the findings it could not fix are posted as review comments, and the status lists what was fixed; the Devin Review badge and "No Issues Found" summary still appear as before, and code-quality findings stay on the Devin Review page. PRs that no running session owns are reviewed exactly as today.

**Resolved Findings Keep the Original Finding**

Findings that Devin marks as resolved keep showing the original finding, with Devin's resolution explanation as a reply underneath.

**Remembered Comment Action**

Choosing "Comment" or "Start a review" from the comment button's dropdown in Devin Review makes it the default action for future comments.

**Reliability and Navigation Fixes**

Returning to a session's Devin Review tab after a new commit opens the latest analysis, reopening a collapsed session pane keeps your reading position, clicking another PR in a stack follows your PR-link preference, CI check names are no longer cut off by long descriptions, and expanding an "Asked DeepWiki" step in Review chat no longer shows raw snippet markup. Sessions also no longer get spurious "Rate limit exceeded" errors from the Devin Review tools when many sessions run at once.

**Scan Finding View Polish**

Scan finding summaries no longer show a duplicate "Overview" heading, finding details are left-aligned, and dismissed or resolved findings have a "Reopen finding" button in the footer.

**Preflight Checks for Automations**

An automation can now run a script after each trigger, before Devin starts. Use it to further validate the event, transform or enrich its data for the session, or skip runs you don't want. Turn it on under "Before the agent runs" in the automation editor; the script runs in an isolated environment with a configurable timeout, and each run's preflight result is shown in the run details.

**Oncall Lists and Settings**

The Oncall Reports tab lists reports in the same format as responder issues, ordered by most recently updated, with a short summary of each report's latest run. Responders and Incidents lists show relative times with the exact date on hover, and Oncall Skills & Context now opens from a settings gear in the Oncall header and matches Customize.

**Devin as a Native Jira Agent**

Devin is now available as a native agent inside Jira. A Jira admin installs the Devin for Jira app on the site and links it to your Devin account from Settings → Integrations → Jira. Once linked, assigning a work item to Devin or @mentioning it starts a session, and Devin's progress and replies appear in Jira's agent panel; if Devin can't start (no default organization, missing permission, usage limit), Jira shows Devin's explanation instead of a generic error.

**Microsoft Teams: Sync from the Session Menu and Clearer Setup Messaging**

You can now sync a session to Microsoft Teams from the session's menu in the sidebar, and sessions synced to a Teams channel or group chat show a simple "Sync to Teams" switch, matching Slack. Links from Devin in Teams open your organization's dedicated Devin domain when it has one, and "link your account" links open a one-click dialog. If your organization hasn't connected Devin yet, Devin's Teams welcome messages, replies and `help` say so with a Connect Devin link and update automatically once Teams is connected; users whose Teams email matches their Devin account are connected automatically on install.

**Slack: Buttons Work Across Organizations**

Slack buttons on a session thread (network access, environment suggestions, approvals) now work when the session belongs to a different Devin organization than the Slack channel, as long as both are in the same account and you are a member of the session's organization. Looking up a channel with `refresh_cache: true` right after inviting Devin to it picks up the new access immediately.

**GitHub Team Sync: Managed Repository Access**

On connections where repository access is synced from GitHub, the access list shows which GitHub team or role grants each person's access, manual grants that no longer apply are marked inactive, and blocked users are told that access is managed by GitHub and how to fix it (link their GitHub account or request access on GitHub) — including in the new-session composer. Admins can grant access to playbooks, secrets, budgets, connections and other resources to GitHub teams synced from their organization, git-provider teams in the access dialog are grouped by provider and host, and synced access follows changes to the GitHub org's default repository permission. Removing a GitHub connection now also removes the group memberships and repository access synced from it.

**Skills-Only Repositories Install as Plugins**

Plugins → From repository and `devin plugins install owner/repo` now accept skills-only repositories (`skills/<name>/SKILL.md`) that have no plugin manifest.

**Outposts**

Sessions on an outpost now wait for the outpost's machine to come online instead of failing, with a banner explaining that the session is waiting on your organization's outpost. Enterprises using Git Manager on Outposts can configure a dedicated IP allowlist for outpost git traffic; if it isn't set, the existing IP allowlist applies. Admins can also read and set their organization's default platform through the v3 API (`GET`/`PUT /v3beta1/organizations/{org_id}/default-platform`).

**Environments and Analytics**

Enterprise → Environments shows the latest build status of each platform an organization builds, with a per-platform breakdown on hover. Analytics drilldown tables list every user, organization and repository with paging instead of grouping everyone past the top 500 into "Other".

**September 25, 2026**

**Sidebar Status Groups: Working / Ready / Blocked / Inactive**

The sessions sidebar's "Group by status" now uses Working / Ready / Blocked / Inactive, so sessions with a PR awaiting review and sessions that need your input are listed separately.

**View Preferences Follow You Across Devices**

Your search mode, changed-files tree layout, sidebar Review/Ask filters and grouping, and wiki language/view choices now sync across browsers and devices instead of staying on one machine.

**Keyboard: Next/Previous Session and Cmd+Enter to Submit Dialogs**

Press Option+J / Option+K (Alt+J / Alt+K on Windows and Linux) to move to the next or previous session in the sidebar. The feedback, Invite members and New ticket dialogs can be submitted with Cmd+Enter (Ctrl+Enter).

**Command Palette Finds Child Sessions by Their Own Title**

Session search in the command palette (Cmd+K) now matches sub-sessions on their own title, not only when the parent session matches.

**Child Sessions Start with Their Parent's Context**

Starting a child session now carries a short summary of its parent, shown as a removable chip in the composer, so the child begins with the parent's context.

**PR Link Hover Card Opens the Owning Session**

Hovering a pull request link in a session shows a card with the session that owns the PR — its status, PR badges and integration icons — and opens that session directly on the PR. If the PR was taken over, the card points at the session that currently owns it.

**PR Links Respect Your PR-Link Preference Everywhere**

The pull request menu in a session has a new "Copy link" option that copies the link matching your PR-link preference (Devin Review or the git provider), and PR URLs you paste into a message now open the same way PR links in Devin's replies do instead of always opening GitHub.

**PDF Attachments Are Versioned**

When Devin shares an updated PDF with the same name, it opens in the same tab with a version picker so you can view any earlier version.

**Progress Tab Names the Sender**

The Progress tab now labels messages by who sent them ("Alice said") instead of "You said" for every message, including messages that arrive from Slack or Teams.

**Sleeping Sessions Wake on Preview or SSH Traffic**

Opening a preview URL or SSHing into a session whose machine has gone to sleep now wakes the machine and completes the request instead of showing "not running". Browser previews come back automatically after a session wakes, and the "Wake Devin up" button on a sleeping preview now shows live progress.

**Clearer Notices: Failed Sends, Dismissible Toasts, Incomplete Builds**

When a message can't be sent because the connection to Devin is down, the app shows a "Message failed to send" notice and puts your text back in the composer. All notifications can be dismissed with the ✕ button. The "Environment build incomplete" notice at the start of a session expands into a warning card listing the blueprints that failed, with a link to the build.

**Performance Improvements**

Streaming replies in long sessions update the transcript without re-processing the whole conversation on every chunk, and large PR diffs open and switch tabs faster.

**Interactive HTML Reports**

When you ask for a report that would benefit from interactivity (charts, tables, diagrams) without naming a format, Devin now produces an interactive HTML report.

**Devin Updates Only Its Own Section of a PR Description**

When updating a PR description, Devin now replaces only its own section and leaves sections added by other tools (review bots, CI preview links) or people intact, instead of skipping the update or offering to overwrite them.

**"Test the App" Offered in Automation and Triage Sessions**

Sessions started by automations or triage now offer the "Test the app" button after opening a PR instead of skipping end-to-end testing.

**Large File Copies with a Connected Local Machine**

Large files can now be copied between a connected local machine and a Devin session VM without manual splitting.

**Status Comment Is Cumulative Across Commits**

The Devin Review status comment on a PR now keeps listing the findings Devin fixed on earlier commits instead of resetting on each push.

**Required Checks That Haven't Reported Show as Pending**

Devin Review now shows required GitHub checks that have not reported a status as pending instead of saying all checks passed.

**Bitbucket Data Center: Automatic Reviews and Comment Threads**

Bitbucket Data Center repositories now appear in the Devin Review repository picker and can be enrolled for automatic PR reviews. Devin can read the comment thread on Bitbucket Data Center PRs and reply in-thread to (or edit/delete) its comments, and rotating the access token on connections created before February 2026 works again.

**Azure DevOps: Pipeline Logs and Self-Hosted Servers**

Devin can now read Azure Pipelines job logs for failed checks on Azure DevOps PRs and (with a "Build completed" service hook) is notified when a pipeline on its PR fails. Azure DevOps Server and Bitbucket Data Center instances hosted under a virtual directory (e.g. `https://host/tfs/Collection`) are supported, with correct provider logos and PR/commit/file links throughout the app, and the Review "not available" prompt now names the actual provider instead of offering to connect GitHub.

**Finding Update Times and Filters in the API**

Code scan findings now include their last-updated time, and the webapp and v3 APIs can filter findings by creation or update time.

**Resolved Tab Shows Only Merged Fixes and Dismissals**

The Findings "Resolved" tab now lists only findings whose fix PR was merged or that a user dismissed; findings Devin closed on its own are no longer listed there.

**Runtime-Validation Evidence in Scan Reports**

Security scan reports now include recorded runtime-validation results and supporting artifacts for open and dismissed findings at every severity, with dismissed false positives summarized separately. The findings API exposes these results so integrations can distinguish recorded validation from missing information.

**Create Code-Scan Automations via the API**

Code-scan automations can now be created and updated via the API with a service-user API key (the service user's role needs the relevant scan permission), not only from the Automations UI.

**Structured Questions in Automation Sessions**

Automations can now ask questions with clickable choices in their sessions.

**Run Sessions on a Shared Outpost**

Automations can now run their sessions on a shared Outpost you choose in the automation editor.

**Plain-Language Schedules**

Schedules with a start or end date, several times of day, or a bare hourly cadence now display in plain language (e.g. "Every 6 hours, from 9/19/2026 until 9/22/2026") instead of raw RRULE text.

**Linear-Triggered Sessions Can Start Child Sessions**

Sessions started by Linear automations or allowlisted Linear bots can now start and manage child Devin sessions (for example, orchestrator playbooks).

**Microsoft Teams: Simpler Channel Routing**

Enterprises with a single organization no longer need to configure channel mappings — Devin routes every channel in the Team to that organization automatically. Enterprises with several organizations can map a channel (or all unmapped channels in a Team) directly from a card in the Teams thread, and the "channel not mapped" message links to the mapping settings.

**Microsoft Teams: Approve Network Access from the Card**

Teams users can approve or deny Devin's network access requests directly from the Teams card — for the session or, when applicable, in the governing security profile or automation — instead of opening the webapp.

**Microsoft Teams: One-Tap Answers and Reactions**

When Devin asks a simple question with up to three options, they appear as one-tap reply buttons, and the question stays in the chat with your answer shown underneath. In channels, Devin reacts 👀 to your message while it works and 🚫 when it can't act on an @mention (for example, the channel isn't connected).

**Microsoft Teams: Group Chats**

In Teams group chats, Devin now only replies to messages that mention it or ask it for something, stays quiet on statements that aren't requests, keeps its answers chat-sized, and only shows a typing indicator when it is actually writing a response.

**Microsoft Teams: Attachments, Links and Defaults**

Files Devin shares in Teams now include a link that opens the attachment in the Devin web app alongside the download link, and messages with many attachments are delivered as multiple cards. Links you share with Devin keep their URL so Devin can open them. New Teams connections reply in the existing thread by default (switchable in Settings → Connections → Microsoft Teams). Sessions started from a private channel note that follow-ups need to @mention Devin, the welcome card is simpler, and dedicated-tenant customers get session links on their own Devin domain.

**Slack: Canvas and User-Group Permissions**

Devin's Slack app now requests canvas read/write and user-group read permissions on install, so those features work for every workspace. Existing workspaces may be asked to reconnect Slack.

**Slack: Thread Replies Reach the Session That Posted**

Replying with `@devin` in a Slack thread that a Devin session already posted to now reaches that session (or shows a no-access notice) instead of starting a second session.

**Slack: Long Answer Options, Markdown Attachments and Mentions**

When one of Devin's suggested answers is too long for a button, the options render as a selectable list with a Submit button so the full text is visible. Markdown attachments are shared as a link that opens the file in the session instead of being uploaded to the thread. Devin @-mentions people correctly in Slack-connected sessions, including in workspaces with over \~1,000 members.

**Microsoft 365 MCP Requests Write Scopes by Default**

Microsoft 365 MCP connections now request all read/write permissions that don't need admin approval by default, so Devin can send mail, create events, post in Teams, etc. without reconnecting.

**57 New Hosted MCPs in the Marketplace**

57 new hosted MCP integrations are available in the Marketplace, including Buildkite, Brex, Expo, Resend, Statsig, Todoist, Vanta, WorkOS, Wix and Strix. Hosted MCP servers that publish their OAuth metadata at the server root (e.g. Codspeed, You.com, Datadog) now connect via OAuth.

**Customize → MCPs: Clearer States**

MCP switches that only org admins can change now show a lock icon, and disconnected MCPs on the Personal tab show a Connect action instead of appearing enabled.

**Devin Can Target a Specific Uploaded Plugin**

Devin can now save a skill, rule, MCP server or hook into a specific uploaded plugin (personal, organization or enterprise) by naming it, instead of only the default one. When installing a plugin from a directory, the approval says whether it creates a new plugin or replaces an existing one, and Devin must ask explicitly to replace.

**Reinstall an Uploaded Plugin as a New Revision**

Devin can update all files of an already-uploaded plugin (including companion scripts) by reinstalling it, keeping the plugin's version history. Plugins between 16 and 20 MiB can be edited and reinstalled again.

**Org Admins Can Change Access on Plugin MCPs**

Org admins can now change the Access level (Organization or Personal) of MCP servers installed by a plugin — and the OAuth client where the provider takes one — from the plugin's connection settings.

**Enterprise Plugins Settings Page**

Enterprise admins can now find plugin policies — allowing uploaded organization/enterprise plugins and showing the official marketplace — on a dedicated Enterprise › Plugins settings page.

**Snapshot Builds Fail Early When Disk Is Short**

Snapshot builds that leave less than 2 GiB free on the root filesystem now fail with an explanatory message instead of publishing an image that runs out of disk shortly after a session starts.

**GitHub Enterprise Server: Role Mirroring and Team Sync**

Newly registered Devin GitHub Apps on GHES request Organization Administration: Read and Custom organization roles: Read so Devin can mirror your GitHub organization's roles and default repository permission into Devin access groups. Team sync now grants members of one synced organization read access to sibling organizations' internal repositories right after the first sync.

**September 23, 2026**

**Session Tree from Parent Sessions**

Parent sessions now show the session-tree icon in the header. Click the title to see and open the child sessions, as you already could from a child session.

**Rename Sessions You Can Edit**

Teammates with edit access to a session can now rename it, not just the person who started it.

**Devin Resumes Right After Permission Responses**

Devin now resumes promptly after you approve or deny a permission request while it is waiting, instead of sitting until its wait timer expires or you send another message.

**Capability Picker Names the Models**

The Ultra and Normal cards in the capability picker now name the models they use: Ultra reads "Highest intelligence available with Fable 5.1 and GPT-6 Astra", and Normal lists Fable 5.1, Opus 5 and GPT-6 Astra.

**Performance Improvements**

Streaming shell output and code blocks no longer stutter in Safari, and CPU use while Devin streams messages is lower. On phones and tablets, session tabs you are not looking at are unloaded to reduce memory use and crashes.

**Organization Admins Can Manage Autoreview**

Organization admins with the relevant permissions can now manage automatic review settings for their organization.

**Richer Autoreview Triggers**

Automatic reviews can now be triggered by a composable set of custom rules. In Settings → Review, enroll a whole account, an SCM organization, a repository, a repository prefix or an individual member, then narrow each trigger with advanced filters on PR author, reviewer, label, title, source or target branch, changed files, author type (human, bot or Devin) and diff size, combined with all / any / not. Each trigger also sets when Devin reviews (when the PR is created, when it is marked ready, on every push, or once), and exclusions override triggers so matching pull requests are never reviewed automatically.

**Self-Hosted Git Servers on Non-Default Ports**

Devin Review now loads pull requests from self-hosted GitHub Enterprise, GitLab and Bitbucket Data Center instances that run on a non-default port (e.g. `https://bitbucket.example.com:8443/...`), and the Recent list no longer hides a PR when another PR on the same server shares its repository path and number.

**Helix Swarm (Perforce) Reviews**

Devin Review can now be triggered from Helix Swarm reviews (via a Swarm test definition or, on Swarm 2026.3+, an outbound webhook) and reviews the shelved or submitted changelist directly from the Perforce depot. Swarm reviews open in Devin Review with links back to Swarm for the review, author and stream, and Swarm test runs close with the review's verdict.

**Bitbucket Data Center: Comments, Reviewers and Decline**

Bitbucket Data Center users who linked their account can now post and edit Discussion comments, add or remove reviewers, and decline a PR from Devin Review as the linked user. Controls Bitbucket Data Center does not support (labels, assignees, reactions) are no longer shown.

**A Findings Tab for Every Scan**

Each code scan a session starts now has its own Findings tab, so earlier scans' findings stay reachable, and a session's scan findings are one click away in the header links, even after the scan card scrolls out of view.

**Scans Fail Clearly When a Repository Can't Be Fetched**

Code scans that cannot fetch a repository's latest commits now end as failed with the fetch error instead of reporting "no changes" on outdated code, and scheduled scans no longer start when Devin can't access the repository.

**Dismissal and Resolution Notes in the Finding Status API**

The v3 code scan finding status endpoint now accepts an optional `dismissal_reason`, `dismissal_note` and `resolution_note` when dismissing or resolving a finding.

**Microsoft Teams: Commands, Context and DM Cards**

In Microsoft Teams you can now type `ask` or `deep` (no `!`) after mentioning Devin, or in a direct chat, for a quick codebase answer; start a message with `aside` to have Devin ignore it; and add `!windows` or `!mac` to start the session on a Windows or macOS machine if your organization has those enabled. Replying to a quoted message passes the quoted text to Devin as context. Sessions started from a Teams DM show a "Microsoft Teams message · DM" card, and the Teams item in the session header links back to the Teams thread or chat.

**Microsoft Teams Without Tenant-Wide Admin Consent**

Connecting Microsoft Teams now uses a single Connect button and no longer requires a Global Administrator by default. Devin can send Teams direct messages and look up people in teams where it is installed without tenant admin consent; people outside those teams are no longer searchable.

**Teams MCP Can Read Channel Messages**

The Microsoft Teams MCP can now read channel posts and their replies when the connected Entra app grants `ChannelMessage.Read.All`, which admins can select in the Teams MCP scope picker.

**Bring-Your-Own OAuth Setup Guides for Microsoft 365 and Google Workspace MCPs**

The Microsoft 365 and Google Workspace MCP settings now include step-by-step instructions for setting up your own OAuth app, plus clearer field descriptions and error messages.

**Slack: Tables Render Natively**

Markdown tables in Devin's Slack messages now render as real Slack tables instead of raw pipe-delimited text.

**Linear: `!mac` / `!windows` Platform Directives**

You can now pick the machine for a Linear-triggered session by adding `!mac` or `!windows` to the comment that mentions Devin, just like in Slack.

**Plugin MCPs Appear in Customize → MCPs**

On the Customize → MCPs tab, an MCP provided by an installed plugin now appears under "From plugins" as soon as the plugin is installed, with a Connect button, instead of only after it has been set up.

**Plugin Change Approvals Show the Proposed Diff**

Clicking a plugin change approval card now opens the proposed change in the Progress tab as a diff against the saved plugin, with a link to the plugin; after approval it shows exactly what was written. Single-file plugin edits preview the file directly.

**Settings Search Shows Only What Applies to You**

Settings search now only shows settings that exist for your plan, configuration and connected integrations, and results open the right tab and highlight the setting.

**GitHub App Permissions Update**

Devin's GitHub App is requesting additional permissions: Organization Administration: read, Custom Organization Roles: read, Code Scanning Alerts: read, Secret Scanning Alerts: read, Members: read (for GitHub team sync), and Actions: write (so Devin can rerun workflows). GitHub organization admins will receive an email and should approve the updated permissions in their installation settings. Devin keeps working with the current permissions until then.

**Security Profiles for Snapshot Builds**

Enterprise and organization admins can now bind a security profile specifically to snapshot builds (or opt builds out) via the API.

**Blueprint Knowledge from Organization and Enterprise Environments**

Knowledge defined in organization- and enterprise-level environment blueprints now reaches Devin sessions.

**Outposts Permissions**

Custom roles with the Outposts read or write permission can now view or administer Outposts in Settings → Environment without also needing Manage enterprise settings.

**September 21, 2026**

**SWE-2 Research Preview in the Agent Selector**

SWE-2, Cognition's next-generation software engineering model, is rolling out as a research preview in the agent selector under the "Research preview" section. Choose SWE-2 and a reasoning effort (Medium, High, or Max) when starting a session, or switch to it mid-session with the agent toggle next to the message input; in Slack, use `!swe2`. Enterprise admins enable SWE-2 (Preview) for their enterprise in Settings, and organization admins can then turn it on or off for their organization under Agent capabilities. As a research preview, behavior and availability may change.

**Attach a Folder to a Message**

You can now attach a whole folder to a Devin message by dropping it on the composer or choosing "Upload folder". The folder is compressed in your browser and attached as a single zip file.

**More Automatic Merge-Conflict Fixes**

Devin now fixes merge conflicts on its PRs automatically more often: within 12 hours of session activity (36 hours if the PR is approved), including conflicts that reappear after an earlier one was fixed.

**Shell Command Durations in the Worklog**

Finished shell commands in the session worklog now show how long they took, so slow commands are easy to spot.

**Full Links for PRs, Issues, and Commits**

Devin now links PRs, issues, and commits it mentions instead of writing bare numbers like #123.

**File Tree, Smart Diffs, and Open in Editor in the PR Tab**

The PR tab now has a file tree alongside the diff that highlights the current file as you scroll, a Smart diffs toggle in the diff settings to view a PR as a flat list of files, an "Open in editor" button, and a "File tree on left" option to move the changed-files tree to the left of the diffs.

**Checks Tab and Faster Diffs**

The PR tab has a new Checks tab showing CI status, with tabs ordered Changes, Description, Discussion, Commits, Checks, Bugs. Diffs highlight faster and scrolling large PRs is smoother, and the embedded editor now matches the diff viewer's fonts and colors.

**Devin Review in Spanish and Portuguese**

Devin Review's interface is now available in Spanish and Portuguese for users whose display language is set to Español or Português.

**Devin Review for Bitbucket Data Center**

Devin Review can be enabled for Bitbucket Data Center repositories, including automatic reviews when pull requests are opened or updated. Bitbucket Data Center projects and repos can be selected on the Devin Review home page, the merge bar shows merge, approval, and build status, and admins can configure a webhook (Settings › Integrations › Bitbucket) so Devin updates pull request status and comments in near real time.

**npx devin-review CLI Retired**

The standalone `npx devin-review` command-line tool and its unauthenticated review page have been removed. Use Devin Review on the PR tab or in the Devin Review home instead; existing installed copies of the CLI will no longer work.

**Azure DevOps Improvements**

Devin can now add and remove pull request labels (tags) on Azure DevOps and Azure DevOps Server. In Settings, Azure DevOps connections show the organization name, and organizations or Server collections with more than 100 projects now list repositories from every project.

**Rotate Bitbucket Data Center Tokens**

Admins can rotate a Bitbucket Data Center connection's HTTP access token from Settings → Bitbucket or the enterprise API without disconnecting; the new token must belong to the same Bitbucket user.

**Link Your Bitbucket Data Center Account**

Once an admin registers an OAuth application for a Bitbucket Data Center host, you can link your own Bitbucket account from Devin Review or Profile → Linked accounts. Review approvals and comments Devin posts on that host are then attributed to you rather than the shared connection.

**Microsoft 365 MCP Servers and Plugins**

Microsoft 365 Mail & Contacts, Calendar, To Do, OneDrive & SharePoint, Teams, and Directory (Entra ID) are now available in the MCP marketplace and as plugins that bundle each MCP server with a usage skill. Connect them with your own Microsoft Entra app registration, pick OAuth scopes from a list that explains what each permission is for, and Devin connects with read-only permissions by default when no scope is configured. The Files MCP can return files converted to PDF or JPG.

**Google Workspace MCPs Through Plugins**

Gmail, Google Drive, and Google Calendar MCPs installed through a plugin can now be connected with your own Google OAuth client ID and secret, including custom OAuth scope and resource. On plugin MCPs that need your own OAuth client, the client ID and secret fields now appear first.

**Personal MCP Servers Are Private**

MCP servers you add or install from the Personal tab in Customize are now private to you instead of being shared with your organization, and editing a personal MCP server more than once no longer fails.

**Devin Can Manage Org and Enterprise Plugins**

Org and enterprise admins can have Devin create, update, remove, and install plugins for their whole organization or enterprise, approving each change. Devin can also create, update, and remove skills, rules, MCP servers, and hooks in your uploaded personal plugins through a single tool, including plugins that use a root mcp.json.

**Required and Available-to-Install Plugins**

Org and enterprise admins can make uploaded plugins "Available to install" so members choose whether to add them, or "Required", from the plugin's card or details panel. Renaming a plugin updates its name across Customize, Marketplace, and the session plugins menu, plugin indexing errors on the Customize page now say what actually failed, and plugins can be up to 5x larger (20 MiB, 2,500 files).

**Simpler Create Automation Menu**

The Create automation menu is reordered, "Manual" is now "Create", and "Suggest automations" is now "Suggest for me".

**Reactivated SCIM Users Keep Their Groups**

SCIM users who are deactivated and later reactivated by the identity provider now keep their IdP group memberships, including group changes made while they were inactive.

**September 18, 2026**

**Knowledge Is Moving to Skills**

Knowledge is being migrated to [Skills](https://docs.devin.ai/product-guides/plugins.md). Your existing Knowledge notes are converted automatically into skills in a `knowledge` plugin for each scope (organization, enterprise, or personal), with their content unchanged and their folder structure preserved; Devin uses them in sessions the same way it used the notes. Once an organization is migrated, its Knowledge page shows the legacy notes read-only and points to Customize → Skills, where you can view and manage them. No action is needed; the migration is rolling out gradually.

**Filter Sessions by Origin**

The sidebar session filters now include Origin, so you can show or hide sessions by where they were created: Slack, Web, API, Jira, or Linear.

**Command Palette: Open Devin Review from a PR Link**

Paste a pull request link into the Cmd+K palette and press Enter to open that PR's Devin Review.

**Smoother Screen Recordings**

Ask Devin to record at a higher frame rate and its screen recordings capture at up to 60 fps, so animations and scrolling look smooth in demos while keeping Devin's test-case annotations. Default recordings are unchanged.

**Email Notifications for Enterprise and Security-Profile Organizations**

Devin can now send email notifications to members of the same organization for enterprise organizations and organizations with a security profile.

**Enterprise API: Audit-Logs Pagination**

The `total` field in the Enterprise API audit-logs list response is no longer populated (returns `null`). Use `has_next_page` / `end_cursor` to paginate.

**Azure DevOps Server Support**

Organizations can connect Azure DevOps Server 2020/2022 collections with a personal access token from the Azure DevOps settings page.

**"Require Session Access for PR Comments" Org Setting**

Org admins can require that PR comments only reach Devin sessions the commenter has access to, under Settings → Devin → Pull requests. Enterprise admins can enforce it for all organizations.

**Perforce: Workspace Follows Connection Changes**

When a Perforce depot path is removed from an organization's connection, running Devin sessions lose access to it on their next Perforce command; the session's workspace is narrowed automatically and the command is retried.

**@-Mentions and Session Links in Microsoft Teams**

Devin can now @-mention people in its Microsoft Teams replies so they get notified. Sessions linked to a Teams thread show a Teams indicator in the session header, and "connect your account" messages take you to your Connections settings.

**Plugin Management in Customize**

Plugin version history shows readable diffs and a file tree for every version. You can download a plugin you uploaded as a .zip, edit skills and rules from organization plugins directly on the Skills and Rules pages, and share a direct link to a plugin from the address bar.

**MCP Connection Status and Reconnect**

Each MCP server now shows how it is authenticated, with a Reconnect action to redo authentication without uninstalling. Public MCP servers that offer optional sign-in (such as Context7 or Clerk) are marked ready instead of asking you to sign in, and org-owned MCPs where each member connects their own account also appear under Organization so admins can manage them.

**Connect Enterprise MCPs with Your Own Account**

Developers can authenticate enterprise MCPs that use individual OAuth from All organizations → Customize → MCPs → Personal, then use that connection across the applicable organizations.

**New in the MCP Marketplace: ActiveCampaign**

ActiveCampaign lets Devin manage contacts, campaigns, automations, and deals in your account.

**Grafana (OAuth) Plugin Support**

Grafana (OAuth) connects to Grafana Cloud's hosted MCP server with no API key or Docker setup; the Docker-based integration remains available as Grafana (stdio).

**September 16, 2026**

**Live Voice Mode**

Voice calls with Devin now run on a live speech model. Starting a call drops you straight into the call controls (with a ringtone while connecting), holding Space to talk works right after muting, and Devin's spoken replies stay in order in the transcript. When a session is connected to Slack, the thread shows who is on the call and how long it lasted instead of Devin's internal voice notes.

**Sessions Wake as You Type**

A sleeping session starts waking up as soon as you begin typing in its composer, so Devin is usually ready to work the moment you press send.

**Copied Messages Keep Their Formatting**

Copying a Devin message now preserves formatting when pasted into email or documents, still pastes as Markdown into code editors, and keeps bullets and links when pasted back into the Devin composer. Transcript copies include each speaker's name.

**Configurable Send Shortcut**

Choose whether Enter or Cmd/Ctrl+Enter sends a message under Settings → Personal → Send shortcut. The preference applies across Devin's composers.

**Skipped Questions Are Shown as Skipped**

When Devin moves on from a question before you answer, the transcript (and the Slack thread, for Slack-connected sessions) now shows the question as skipped, with what was asked, instead of "User answered: (no answer)".

**Reboot VM from the Sidebar**

Sessions that lose their VM now show a "Reboot VM" action in the sessions sidebar instead of a generic blocked or finished state.

**Agent Mode Icons in the Sidebar**

You can show each session's agent mode as an icon in the detailed sidebar. Enable Agent mode under Properties → Property visibility; it is off by default.

**Redesigned Session Dialogs**

Session dialogs — including the confirmations for stopping a session or closing its PRs — have been restyled to match the rest of the app.

**Security Bugs Are Always Checked in Devin Review**

Devin Review now always checks for security bugs in every review; the "Security scan" toggle has been removed from Settings › Review. Whether security bugs are posted to GitHub remains toggleable.

**Slack User-Group Mention Triggers for Automations and Oncall**

Trigger automations and oncall responders when a Slack user group is mentioned. Select a group or enter its Slack ID manually, and optionally restrict matching to specific channels.

**Admins Can Opt into Allowing Automations on Public GitLab Repos**

GitLab connections now have an "Automation scope" setting. Org admins can choose "All connected repos" to let automations access public-visibility GitLab projects on that connection.

**Install a Personal Plugin from a Directory**

Devin can now install a plugin from a folder on its machine (for example an attachment you sent it, once unpacked), not only from a GitHub repository URL.

**Read-only Customize View**

Members who can view Customize but have no layer of their own to install into see a read-only view of what's configured. When no plugins are available to browse, the Browse view explains that admins can add plugins instead of showing a blank list.

**MCP Secrets Are Now Managed in the MCP Page**

Settings → Secrets shows a banner explaining that MCP server credentials moved to each server's page, with a button to the right surface and a docs link.

**Teams Improvements**

Devin sessions attached to Microsoft Teams format replies for Teams (tabular data is sent as file attachments), include images pasted earlier in a thread when Devin is mentioned, and respond faster to new conversations. Picking new or org from the / command menu now works in personal and group chats, and the first-session welcome card suggests tagging @Devin in Teams when your organization has Teams connected. When Devin isn't connected to your Teams organization or a team wasn't fully set up, the bot now explains how to fix it.

**Connection Page Titles**

Browser tab titles on Settings → Connections detail pages show the integration name (e.g. "Microsoft Teams") instead of "Settings".

**Blueprint Source in the v3 API**

The v3 blueprint API lets you choose whether a repository blueprint is managed from .devin/blueprint.yaml in git or from Devin's database (source: "git" | "database" on create/update) and reports the current mode in blueprint responses.

**September 11, 2026**

**Clearer Machine Startup in the Computer Tab**

The Computer tab now says the machine is being provisioned while a session's VM is starting, instead of showing a connection failure, and waits up to roughly five minutes for slow-starting machines.

**Sidebar Keyboard Navigation**

Arrow keys now move between every sidebar navigation row, including items in the More menu, and screen readers announce them as a single menu.

**Nested Sidebar Groups Stay Expanded**

Expanded nested session groups in the sidebar stay expanded after you refresh the page.

**Neutral Primary Buttons**

Primary buttons across the app now use a neutral style instead of blue.

**Teams Parity Improvements**

Emoji reactions on Devin messages in Teams (including channel threads) are now forwarded to the session. Devin sees the recent Teams conversation when you reply in a thread or chat that already has a session. PR links in Devin's messages include a Devin Review link for organizations with Devin Review enabled. When a conversation moves from Teams to the Devin webapp or Desktop, the Teams thread shows a notice linking to where it continued. Devin no longer posts a "went to sleep due to inactivity" message, and shared-channel threads note that Devin can only see messages that @mention it.

**PagerDuty Integration for Oncall and Automations**

Connect PagerDuty to Devin to trigger automations on incident events (triggered, acknowledged, resolved, and updated) and to let Devin act as an oncall responder that triages PagerDuty incidents and posts its investigation as incident notes.

**Jira Site Picker**

Connecting Jira with an Atlassian account that belongs to more than one Jira site no longer fails; after signing in, Devin shows the sites you can access and lets you pick the one to connect.

**Datadog MCP on the Stable Endpoint**

The Datadog MCP integration now uses Datadog's stable `/v1/mcp` endpoint. Existing installations can adopt it via "Update from marketplace" in MCP settings and keep their region; users of the OAuth-based Datadog server need to reconnect once after the update.

**21 New Zero-Config OAuth MCP Servers**

21 new one-click integrations in the MCP marketplace — including Dropbox, ClickHouse Cloud, Lucid, Typeform, Coda, GitBook, Railway, Retool, Smartsheet and Make — each connecting through OAuth with no API keys or setup steps.

**Unified Plugin Marketplace**

Browse marketplace now lives in the Customize page's tab bar and shows one list across your scopes: Install lets you pick which scope to install to, cards say where a plugin is already installed, and a "+" adds it to other scopes you manage. The official marketplace loads without separately granting your organization access to its public repository, and a short introduction appears the first time you visit Customize.

**Customize Editor Improvements**

Skill and rule rows open an editor with Preview, Edit, and Version history tabs; removing or uninstalling a plugin asks for confirmation first. Customize shows only the configuration layers you can edit, with plugins your organization or enterprise requires shown as read-only "Required by organization" / "Required by enterprise" sections. Skills from plugins not activated in a session appear greyed out in the `/` and `@` menus.

**Devin-Managed Personal Plugins**

Plugin install approval cards in the worklog now show the plugin's marketplace name, contents summary, and logo, distinguish approval from successful saves and installs, and offer a "View plugin" link to open the item in Customize. Devin can install a plugin from a bare GitHub repository URL and save personal skills, rules, MCP configurations, and hooks from files.

**Effective Membership in Member Lists**

Enterprise admins now see everyone who effectively belongs to an organization — including users granted access through IdP/SCIM group mappings — in the enterprise Members page and each organization's Members page. Group-derived access is labeled with the granting group.

**Safer Secret Defaults**

New secrets default to Personal for non-admins, and creating or importing organization secrets asks you to confirm that everyone in your organization can use them.

**Idempotent Session Creation**

The v1 Sessions API accepts an optional `idempotency_key`; repeating a key returns the original session, and if creation with that key is still in progress the API returns 409 so the caller can retry shortly. The legacy `idempotent` boolean is deprecated.

**Azure DevOps Citations**

Source citations in Devin Wiki for Azure DevOps repositories now open the correct file, linking to the exact commit the wiki was built from.

**September 9, 2026**

**Archiving Closes Child Sessions' PRs**

Archiving a session now also closes the open pull requests of the child sessions archived with it; they are listed in the archive prompt so you can choose which to close.

**Multi-PR Dropdown in the Sidebar**

Sidebar sessions with several pull requests in the same state now show a dropdown listing each PR, with the same details as the session header's PR popover.

**Open Changes and PR Files as Diffs**

In a session's Changes and PR tabs, file paths are clickable while Devin's machine is online: clicking opens the file's diff in the embedded editor, with a button to view the full file.

**Desktop Tab on Touch Devices**

The Desktop tab now works like a remote desktop on iPad and other touch devices (tap to click, drag, long-press for right-click, two-finger scroll). When Devin is asleep, the last screenshot fills the pane and hovering it offers a one-click "Wake up Devin" action.

**Continue in a New Session after a Machine Failure**

Hard-blocked machine-failure cards now offer "Continue in a new session" alongside "Try restart", with a note that machine-local files and running processes do not transfer.

**Composer Code Chips**

Typing `` `code` `` in the message composer reliably turns the text into a code chip, Undo turns the chip back into plain text, and a backtick typed inside a chip becomes part of the code.

**Cleaner Chat Rendering**

A question you or a teammate answered now shows as that person's normal chat message. In sessions where you are the only participant, Devin's avatar and name header are hidden (hover a message to see its time) and appear once someone else joins.

**Faster Tab Switching**

Switching between the Progress, Diff, and PR tabs inside a session is roughly twice as fast, the Progress tab keeps your selected step, and switching no longer slows down as more pull-request tabs are kept open.

**Queued Messages Survive Idle/Resume**

Messages queued in a session are no longer lost when the session goes idle and resumes.

**Simplify Devin Review PR Summaries**

Devin Review's top-of-page analysis is now a short, behavior-focused summary (one to two sentences plus up to five bullets) instead of a long implementation walkthrough.

**Improve Progressive Disclosure of Review Findings**

Review findings keep concise summaries while offering an optional "Learn more" section with a plain-language explanation, a concrete example, and a recommended fix; whole findings can be copied.

**Re-scan New Commits and Bulk Remediate via MCP**

Devin can re-run an existing code scan on just the new commits and fix several findings in one go, from a session or any Devin MCP client.

**Webapp Answers Mirrored to Slack**

Answers to Devin's questions given in the web app now appear in the linked Slack thread.

**Slack Controls in the Sidebar**

Link a session to Slack, or turn Slack sync on and off, from the session's "..." menu in the sidebar without opening the session.

**Sync to Teams from the Webapp**

Sessions connected to a Teams chat can turn syncing on and off from the composer, the sidebar, and the command palette, the same way Slack sync works.

**Teams Improvements**

`mute` now fully disconnects a session from the chat and `unmute` or mentioning @Devin reconnects it; a "Detach session" card appears when Devin goes to sleep in DMs and group chats; Devin shows an "Approve deployment" button when it asks to deploy; and the Teams settings page includes the keyword tutorial and thread-mode setting.

**Regex Matching in Text Fields**

Automation text fields can use case-sensitive regular expressions (Google RE2 syntax).

**Grayed-Out Templates**

Templates that need an MCP server or integration your organization hasn't set up stay visible but grayed out, with a hint explaining what to connect.

**Update Approvals Show a Diff**

Approving an automation update now shows exactly what changes: added, removed and modified triggers and actions, settings as old → new, and prompt edits as a line diff.

**Automations Page Refresh**

The Automations page opens on a "Mine" tab by default, empty tabs show the creation options in place, creating an automation or on-call responder opens in a side panel, and the preflight-check card and script editor have been redesigned.

**Marketplace Updates**

The Meticulous MCP server is out of beta, and Intercom now connects with an access token.

**Plugins**

Plugins bundle skills, rules, hooks, and MCP servers into a single installable package so you can customize how Devin works and share that setup across your team. Install plugins from the marketplace in Settings → Marketplace or from a repository, for your organization or your whole enterprise; plugin details show where a plugin comes from (pinned commit or tracked ref and folder) and which scopes have it installed, and skills from a newly installed plugin are available in the `/` and `@` menus right away. Every install shows a security notice describing what the plugin can do and asks you to confirm you trust its source. Org and enterprise admins can mark plugins as required or available, and organizations inherit enterprise-managed plugins automatically.

**Environment Build Attention**

Enterprise admins can see which organizations need attention on the Environment page — consecutive failed builds, no usable snapshot, and a "Needs attention" filter — plus a "Last build failed" filter for repositories in an organization's environment settings.

**Roles and Access**

Roles whose only remaining assignments are expired service users can be deleted. Members with an Ask-only role (such as "DeepWiki Only") can see their past Asks in the sidebar, and view-only roles' session lists are restored.

**Git Bash on Windows**

On Windows machines, Devin runs commands under Git Bash by default (PowerShell remains available on request, and is used when Git Bash is not installed).

**Blueprint Suggestions**

Devin validates proposed repository blueprints (YAML and schema) before suggesting them, and the setup guide lists the optional Clone step.

**September 4, 2026**

**Lightbox Keyboard Navigation and Mermaid Diagrams**

Use the arrow keys to move between images in the lightbox carousel, and Mermaid diagrams now join the carousel alongside images.

**Single Devin PR Comment**

Devin's PR intro comment and the "Original prompt" details block are now a single comment, with the prompt shown below the intro.

**Code Scan Multi-Select Findings**

Select several findings at once to assign them to a single Devin session (one branch/PR) or to bulk-update their status (reviewed or dismissed).

**Code Scan No-Op Runs When There Are No New Commits**

Scan-new-commits runs (including scheduled runs in Automations) now skip starting a session when the repository has no new commits since the last scan; the run is recorded as completed with no ACU usage, and the webapp shows a "No new commits" toast.

**AWS and Braintrust MCP Servers in the Marketplace**

The MCP marketplace now includes AWS and Braintrust servers.

**Google Workspace MCP Setup Guidance**

The Google Drive, Gmail, and Calendar MCP configure pages now warn that the Google Cloud project must be enrolled in the Developer Preview and explain the bring-your-own OAuth client setup.

**Security Profiles Can Allow Orgs' Custom MCP Installations**

Enterprise admins can now let an enterprise security profile permit organizations' own custom MCP server installations.

**Microsoft Teams Improvements**

Files shared via SharePoint render as file attachments, Devin shows a typing indicator while working, /new is supported in group chats, and outgoing attachments are sent as their own activity.

**Partial Snapshot Builds on Clone Failures**

A new enterprise setting lets snapshot builds finish as partial when a repository cannot be cloned, instead of failing the whole build.

**September 2, 2026**

**New Sidebar Grouping and Filters**

The session sidebar can now group sessions by pull request status or by repository, and session filters now include Devin mode.

**Cleanup Scan Type**

A new cleanup scan type finds dead code and cleanup opportunities in your repositories.

**/scan Composer Command**

You can now start a code scan directly from the composer with the /scan command.

**Scheduled Scans in Automations**

Automations now support a code scan agent type, so you can schedule recurring scans or re-scan new commits automatically.

**Redesigned Findings Tab**

The scan findings tab has been redesigned for easier triage.

**Richer Trigger Event Details**

Automation runs now show richer event details for GitLab, Jira, incident.io, and GitHub triggers.

**Clearer Reply Delivery**

Slack users who are not members of the session's organization are now warned when their replies cannot reach Devin.

**August 28, 2026**

**Multi-Select Tag Filters**

The session sidebar now supports multi-select metadata tag filters with per-tag counts, plus a machine-type filter.

**Split Editor Groups in the Session Workspace**

The session workspace editor now supports VS Code-style split editor groups.

**Code Scan History**

The scan detail page has a scan history sheet, and redesigned history rows show each run's profile and cost.

**Code Scan Validation Severities**

Code scan profiles can now configure which finding severities require validation, with a threshold meter in the profile editor.

**New MCP Marketplace Servers**

Gmail, Google Calendar, Gamma, and Supabase MCP servers are now available in the marketplace, and marketplace entries now show icons.

**Clearer MCP Install Approvals**

MCP install approval cards now show the server's identity, source, and resolved scope before you approve.

**Authentication**

We are upgrading our authentication platform and login page.

**New Org Permission: Manage Personal Automations**

Org admins can control who can manage personal automations independently from who can manage system user automations. Account-level automation permissions are also now more granular.

**August 26, 2026**

**Queued Message Improvements**

Queued messages are now delivered while Devin is in a long-running wait, and pressing Cmd/Ctrl+Enter while editing a queued message sends it immediately.

**Waiting Activity Status**

Sessions now show a dedicated "Waiting" activity status while Devin is intentionally sleeping in a wait.

**Undo for Folder Moves**

Moving sessions between folders now shows an undo toast, and Cmd/Ctrl+Z triggers the newest toast's Undo action.

**Accessibility Improvements**

Reduced-motion users now get static/text equivalents for animated elements, and high-contrast support has been improved.

**Redesigned GitHub Link Badges**

Devin's GitHub link badges (PRs, branches, commits) have a refreshed design.

**Smarter @mention Routing in Slack Threads**

@mentioning Devin in a thread now routes your reply to the session you're subscribed to.

**Default Working Org for Slack Channel Sessions**

New Slack channel sessions are routed using the mentioning user's default working organization.

**Finer Automation Schedule Controls**

Hourly schedules now have a minute selector, and run-once schedules use a date picker.

**Multiple Slack Channels in Automation Triggers**

Automation triggers can now select and edit multiple Slack channels.

**Improve Existing Automations with Devin**

A new "Improve with Devin" action lets Devin iterate on an existing automation for you.

**Linked Triggering Events**

An automation run's triggering event source now links to its origin (e.g. the Slack message or issue).

**Support Jira previous\_status Automation Triggers**

Jira status\_changed triggers can now filter on the previous status, and the new status is optional.

**Security Section**

Code scan pages moved from /code-scan to /security (old links redirect). Scan sessions are listed for the user who triggered them, and archiving a scan's root session cancels the scan.

**Scan Now**

A "Scan now" button in the Auto Scan configure dialog starts a scan immediately.

**Batch Remediation via v3 API**

New v3 API routes support batch remediation of findings at the org and enterprise level.

**Allow PRs to Be Opened by Session Participants Configuration**

A new org setting, "Allow PRs to be opened by session participants", lets sessions open PRs as a validated session collaborator.

**Streamlined MCP Marketplace Install and OAuth Connect**

Installing an MCP server from the marketplace is now a single streamlined flow: install cards stay visible through approval, and the OAuth screen opens directly from the card.

**August 21, 2026**

**Redesigned Session Page Header**

The session page header is more compact, with tags and session hierarchy built in.

**Redesigned Sessions Sidebar**

The sessions sidebar has been redesigned with customizable nav tabs, grouping, richer filtering, and a cleaner session list.

**Refreshed Chat Visual Design**

The chat interface has a refreshed visual design.

**Nested Sub-Devin Sessions**

Sub-Devin sessions are now shown as a nested tree in the sidebar.

**Hideable Sidebar**

The sidebar can be fully hidden and peeked on hover.

**Session Subscribers**

Follow and view others' sessions, with subscriber-based sidebar organization and filtering.

**Inline Session Rename Shortcut**

Press Cmd/Ctrl+Option+R on a session page to rename the session inline.

**Stop Devin Shortcut**

Press Cmd/Ctrl+Shift+Backspace to stop Devin while it is working.

**Default Org Picker in Slack DMs**

In Slack DMs with Devin, you can now set your own default organization with the !org picker.

**Bearer Secrets for Automation Webhooks**

Automation webhooks can now authenticate with an Authorization: Bearer secret.

**Duplicate Findings Fix**

Resolved a regression in Devin Review that led to findings being reported multiple times.

**Clearer Findings**

Improved clarity and conciseness of Devin Review findings.

**Change a Scan's Profile**

You can now change a code scan's security profile from the UI.

**Scan Effort Selection**

Choose a scan effort (normal/deep) on the ingest scan form, and set it via the v3 API.

**New v3 Scan API Endpoints**

The v3 API can now trigger an incremental (diff) scan immediately and accepts multiple repos on ingestion scan start.

**Finding Resolution Notes**

A finding's resolution note is now shown in the UI, and a one-time "Scan new commits" action is available when automations are unavailable.

**Enterprise MCP Servers Support**

Enterprise admins can now configure an MCP server once at the enterprise level and make it available to the organizations they choose, in Settings → Connections → MCP. An organization's own installation of the same server overrides the enterprise version.

**Private Network MCP Servers for Dedicated Deployments**

For dedicated deployments, Devin can now use MCP servers that are only reachable inside your own network: both the OAuth authorization flow and Devin's calls to the server travel through your private network tunnel instead of the public internet. Enterprise admins can also upload the private certificate authority bundle that Devin should trust for that traffic.

**Replace Secret Values in Place**

Enterprise-scoped secrets can now have their values replaced in place.

**New MCP Marketplace Entries**

The New Relic MCP is now available in the MCP marketplace, and the Mintlify Index MCP is out of beta.

**August 19, 2026**

**Model Degradation Notifications**

In Ultra sessions, Devin now notifies you when the lead action model degrades or recovers.

**Lightbox Improvements**

Image lightboxes now show filename captions, an image counter, and clickable prev/next arrows; review comment images open in a lightbox on click.

**Attachment Preview Actions**

Attachment previews now offer both copy link and copy content.

**Faster PR Tab**

PR diff files are now virtualized, speeding up session switching with the PR tab open.

**CI Failure Shortcuts**

Worklog "CI failed" rows now open the PR review tab with checks expanded.

**Preview Tab Renamed to Browser**

The session preview tab is now labeled "Browser".

**Slack Mute Moves the Session to the Webapp**

Muting a Devin session in Slack now disconnects it from the Slack thread and continues it in the webapp.

**Automation Schedule Timezones**

Automation schedule triggers now store their timezone.

**Scan Mode Filter in Code Scan**

The scans list can now be filtered by scan mode (discover/ingest).

**Group(s) Column in User Metrics Export**

The user metrics CSV export now includes a Group(s) column.

**Git Provider Connection Details**

On the git provider settings pages (GitHub, GitLab, Bitbucket), clicking a connection now opens a detail sheet with connection info and management actions in place.

**New MCP Marketplace Entry**

The Cello MCP is now available in the MCP marketplace.

**August 14, 2026**

**Devin Coach Suggestions in the Input Box**

Introducing Devin Coach, a new feature that surfaces suggestions directly in the session input box as you write, helping you improve prompts before sending.

**Smarter Re-Review Behavior in Devin Review**

Devin Review now skips re-reviewing a PR when its diff against the base branch is unchanged (e.g. stacked PR restacks).

**Slack Thread Follow-Ups**

Devin sessions now subscribe to Slack threads they post in and route replies back to the session, so follow-ups in the thread reach Devin without re-tagging.

**Teams Polish**

Microsoft Teams user mentions now render as mention chips, emoji render inline, and channel-mention threading behavior now matches Slack.

**High Contrast Mode: System Option**

High contrast mode adds a "system" option that follows your OS preference, alongside broader accessibility improvements including a new accessibility submenu in the command palette.

**Sidebar Improvements**

The sidebar now reveals the active session when navigating via the command palette or a URL, newly created folders appear at the top of the list, and right-clicking a folder opens its options menu.

**Command Palette Improvements**

"Start session with a prompt" now supports multiline prompt editing, and "Search sessions" is pinned under Start session.

**Preview Toolbar Improvements**

Open-in-new-tab is now promoted to the preview toolbar, exposed ports moved into an overflow menu, and share/open-in-new-tab now follow the page currently being viewed.

**Platform Filter for Sessions**

The sessions list can now be filtered by platform.

**Ingest Scan Mode in Code Scan**

Ingest is now available as a scan mode directly in the new-scan sheet.

**Auto-Scan Schedules API**

Code scan auto-scan schedule routes are now generally available in the v3 org and enterprise APIs.

**Devin Local On by Default for Enterprise**

Devin Local is now enabled by default for enterprise customers.

**In-Page Search in Automations**

Automations pages now support in-page search via Cmd/Ctrl+F.

**Unified Workflow Permission Preview**

In Automations, the workflow permission preview pane now matches the live run pane.

**August 12, 2026**

**Side Chats**

Start a side conversation anchored to any point in a session to ask questions and dig into details without interrupting Devin's main work. Side chats open in a panel next to the worklog and support stopping in-flight responses.

**Syntax-Highlighted Code Blocks in Chat**

Fenced code blocks in chat messages now render with syntax highlighting.

**Command Palette Session Search Pagination**

Session search in the command palette is now paginated with an explicit "See more" option.

**Sidebar Organization Improvements**

The sessions sidebar now supports a "None" option in the Group by menu for a flat session list, a "New session in folder" action on folder menus, and a Cmd+K "Move to folder" command for the current session.

**Slack Improvements**

Users can now request channel access directly from Slack DMs, Slack-spawned sessions automatically get read access to their origin channel, and Devin posts a notice when a session is waiting for machine capacity. Workspace members beyond the first page no longer show as "Unknown User".

**Slack Connection Management**

The Slack integration settings now include a Reconnect option, with integration Manage menus aligned on a consistent Reconnect/Disconnect component.

**Playbook Mentions from Slack**

Playbooks mentioned in messages are now resolved when forwarding user messages from Slack.

**Agent Mode Selector Improvements in Automations**

The agent mode selector in Automations and On-Call now shows the resolved organization default (e.g. "Org default (Fusion)") and a description for each mode.

**Negated String Operators in Automation Conditions**

Automation conditions now support "not contains", "not starts with", and "not ends with" operators.

**Security Profile Safeguards in the Automation Editor**

The automation editor now warns when selected MCP servers or network-policy entries fall outside the governing security profile, and confirms security profile changes with a warning popup.

**Perplexity MCP in the Marketplace**

Perplexity is now available as an MCP server in the connectors marketplace.

**August 7, 2026**

**Queueing Support for Automations**

Automations now support queueing: set the maximum number of concurrent runs and queue depth per automation, see queue lifecycle states in the events table, and view an activity chart sourced from automation events. Concurrency groups are also available in the public v3 API.

**Automations API and Terraform Provider**

The automations API has been promoted from beta to the production v3 API spec, sessions can now be filtered by `automation_id`, and a `devin_automation` resource is available in the Devin Terraform provider.

**GitLab Support in Automations**

Automations now support GitLab triggers (issues, issue notes, pushes, and pipelines) with reply support on issue triggers, plus support for a GitLab service-account connection to automatically manage webhooks.

**Request Channel Access from Slack**

When Devin can't access a Slack channel, users now see a specific reason and can request access directly from Slack, with admin approval.

**Command Palette Improvements**

The command palette now surfaces session search results in top-level search, keeps rows on a single line, and nests navigation commands under a "Go to" command.

**Figma Live Embeds in Link Previews**

Figma links shared in chat can now render as live embeds in link preview cards.

**Accessibility Improvements**

A broad accessibility (WCAG 2.1 AA) pass across the webapp: proper labels and accessible names on controls, keyboard-accessible sortable tables and toggles, skip links, distinct navigation landmarks, document titles, and assertive error toast announcements.

**Security Profiles**

Security profiles are now generally available. Admins can define security profiles governing network access and apply them across sessions and automations, including an org-wide default and per-automation profile selection.

**Legacy Cascade Disabled by Default for Enterprises**

Legacy Cascade now defaults to disabled for enterprise tiers, with clarified settings copy.

**Personal Access Tokens**

Personal access tokens are now generally available for authenticating with Devin programmatically. Tokens are automatically revoked when a user loses account membership.

**MCP Connection Improvements**

MCP sessions resume automatically after completing OAuth, personal MCP connections are account-wide with OAuth scoped to the installation's organization, and marketplace MCP installs support custom server URLs.

**August 5, 2026**

**Easier Recovery from Failed Snapshot Builds**

Failed environment snapshot builds are now easier to find and fix in fewer clicks.

**Linear Reconnect Action**

The Linear connection manage menu now includes a Reconnect action.

**July 31, 2026**

**Redesigned Changes Tab**

The Changes tab now has a persistent file tree sidebar with a tree or flat list toggle, and full-width diffs with language icons.

**Session Sidebar Improvements**

A new "Empty folder" action archives all sessions in a sidebar folder, session menus are reorganized into submenus, and archived sessions have clearer indicators.

**Session Renames in the Timeline**

When a session is renamed, the change now appears in the session timeline.

**Approval Progress at a Glance**

The pull request merge status bar now shows approval progress as a count of received versus required approvals.

**Slack Access Defaults**

Devin's Slack channel access is now configurable for all accounts, including a default of all public channels plus direct messages and an account-level setting for DM access.

**MCP Execution from Devin's Servers**

MCP tools now run from Devin's servers rather than the session's remote machine.

**Connectors Page Improvements**

Plugin-provided MCP servers are grouped into their own section, organization marketplace installs are always organization-scoped, and MCP installations without a configured auth method can fall back to dynamic OAuth.

**Control Where Legacy Cascade Is Available**

The enterprise Cascade setting is now a scope choice — enabled everywhere, JetBrains plugin only, or disabled — so admins can move users to Devin Local while keeping Cascade in the JetBrains plugin.

**Opt-In Public GitHub Repo Support in Automations**

Admins can now opt a public GitHub repo into automation triggers.

**Primary Billing Organization Attribution**

All users will be automatically assigned a primary billing org that all Devin Desktop and CLI usage is attributed to.

**IP Allowlists Cover Automation Webhooks**

Account IP allowlists are now enforced on automation webhooks, with support for additive webhook-only ranges.

**Bug Fixes**

This release also includes many smaller fixes and improvements, including Slack and Teams thread cards rendering markdown, queued messages showing slash commands as command chips, quote captions preserved as drafts, smoother streaming in very long sessions, and various UI polish across the webapp.

**July 29, 2026**

**Word-Level Diff Highlights**

Unified diff views now highlight exactly which words changed within a line, making edits easier to scan.

**Link Preview Cards in Chat**

Links shared in your messages and in Devin's replies now render as rich preview cards.

**Remix Keeps the Playbook**

Remixing a session now carries the original session's playbook and rich message content into the new prompt.

**Expandable Knowledge Previews**

Knowledge cards now include an expand toggle so you can read the full note content in place.

**Session Organization Improvements**

You can now remove archived sessions from sidebar folders, and opening an information tab reveals the workspace, including on mobile.

**Slack DMs with Automation Devins**

Automations can now work over Slack direct messages, with a setting to control whether DMs are enabled.

**Simpler Automation Channel Access**

Configuring which Slack channels an automation can access is now a simple two-mode choice.

**Playbooks Scoped to the Right Organization**

Playbook references in Jira and Linear mappings and automation triggers are now validated against the correct organization, with clear removal notices when a mismatch is found.

**SCIM Provisioning Is Generally Available**

SCIM user and group provisioning is now generally available for enterprises, enabling automated user lifecycle management from your identity provider.

**Audit Logging for Devin Local Settings**

Changes to Devin Local settings are now recorded in the enterprise audit log.

**IdP Group Improvements**

The enterprise IdP groups tab now shows member counts, and the group popover is easier to read with middle-truncated names and a copy button.

**Bug Fixes**

This release also includes many smaller fixes and improvements, including clearer Slack channel mapping copy, smoother scrolling in long sessions, fixed lightbox arrow-key navigation, more reliable copying from the shell tab, and various UI polish across the webapp.

**July 24, 2026**

**Redesigned Model Picker**

The model picker has been redesigned into a single organized menu where you can choose a capability, toggle Fusion, adjust speed, and switch modes.

**Slash Commands in the Message Box**

Typing commands like /btw and /queue in the message box is now more discoverable, including a new /ask command that switches the session to Ask mode.

**Playbook Previews in the Message Box**

Hovering over a playbook macro in your message now shows a preview of its contents, with a button to copy the full text.

**Start Windows Sessions from Slack**

A new !windows command lets you start a session on a Windows machine directly from Slack.

**Approve Network Access Requests from Slack**

When Devin requests access to a blocked network destination, you can now approve or deny the request directly from Slack.

**Clickable Finding Counts in Devin Review**

Finding counts on PR cards are now clickable and take you straight to the relevant findings in the embedded review view.

**Required Approvals at a Glance**

Devin Review now shows how many approving reviews a pull request requires.

**Redesigned New-Scan Flow**

Starting a code scan now uses a streamlined flow with support for single-repository, multi-repository, and bulk scans.

**OIDC Identity Tokens**

Devin can now authenticate to cloud services using short-lived OIDC identity tokens.

**API Additions**

The API now supports unarchiving sessions and creating ingestion-mode code scans at the organization and enterprise level.

**Bug Fixes**

This release also includes many smaller fixes and improvements, including faster DeepWiki MCP question answering, links shared from Slack rendering correctly in chat, a clearer Approve button for environment changes, the session "Code files" tab renamed to "Editor", easier text quoting, and various UI polish across the webapp.

**July 22, 2026**

**Smarter Linear Thread Handling**

Replies in different Linear comment threads are now routed to the correct Devin session, and follow-up work on the same issue continues in the original session for better continuity.

**Automations Consumption Visibility**

A new Consumption tab on each automation shows the ACUs used by sessions the automation has started, so you can track the cost of your automated workflows.

**Slack Channel Improvements for Automations**

When configuring an automation's monitored channels, Devin can now automatically join public channels you select, and you can grant access to all public channels at once.

**Safer MCP Access Changes**

Switching an MCP server from personal to Organization access now shows a warning step explaining that your connection will be shared with other members before you confirm.

**Review Usage in Consumption Analytics**

Consumption analytics now shows what triggered each Devin Review run, making it easier to attribute review usage.

**Improved Quoted Attachments**

Quoting text from files or previous messages has a refreshed look, and clicking a quote reopens it on the original surface with the relevant lines highlighted.

**Performance Improvements**

The webapp loads faster and stays responsive in long sessions, including faster boot, smoother work logs, and better handling of large diffs.

**Devin Outposts**

This release introduces Devin Outposts, a new capability for running Devin workloads in your own environment. It is disabled by default — contact your Cognition representative if you are interested in enabling it.

**Quicker Access to Enterprise Settings**

Enterprise admins can now jump to enterprise settings pages, including from a child organization, using the cmd+K command palette.

**Code Scan Profile Filters**

The scan profiles tab now supports filtering profiles by type and mode.

**Snapshot Build History Filters**

Snapshot build history can now be filtered by build status and platform.

**API Additions**

Enterprise member API responses now include each member's enterprise join date, and organization consumption endpoints now report ACUs used by Devin Review.

**Bug Fixes**

This release also includes many smaller fixes and improvements, including icons on the enterprise MCP server list, the ability to switch an automation between session types after creation, clearer error messages, and various UI polish across the webapp.

**July 17, 2026**

**Centralized Skill Management via Plugins**

Skills can now be distributed via Plugins that can be installed and governed centrally, then applied consistently across Devin Cloud, Devin CLI, and Devin Desktop (via Devin Local).

**Enterprise-Grade Plugin Governance**

Admins can configure required, optional, and forbidden plugins in Settings → Marketplace, and organizations inherit enterprise-managed plugin policies automatically.

**Multi-Repository Code Scans**

Code scans can now span multiple repositories in a single scan, with per-repository details and a repository filter on findings.

**Chained Attack Paths in Findings**

Related findings are now linked together as chained attack paths, helping you understand how individual vulnerabilities combine into larger risks.

**Queued Messages Improvements**

You can now set a preference to automatically queue messages while Devin is working, send the next queued message by pressing Enter in an empty composer, and queued messages now default to sending immediately when Devin becomes available.

**Tasks Tab in the Workspace**

A new Tasks tab in the workspace tab picker shows Devin's latest task list so you can follow progress at a glance.

**Inline Link Previews**

Links shared in chat now render inline previews for markdown, PDF, HTML, and CSV content.

**Sortable Tables in Chat**

Tables in Devin's chat messages are now sortable by column.

**Custom Slack Emoji Rendering**

Your workspace's custom Slack emojis now render correctly in synced session message history.

**Instant Slack Unsync Command**

Sending "unsync" (or "!unsync") in a synced Slack thread now immediately stops syncing the conversation.

**Revamped Automations Pages**

The Automations pages have been redesigned with a streamlined editor, clearer trigger configuration, and a new option to create a long-running session that receives subsequent trigger events.

**GitHub Enterprise Server Support for Automations**

Automations can now target repositories hosted on GitHub Enterprise Server.

**Bug Fixes**

This release also includes improved bulk secret import with name validation, expanded keyboard shortcuts, better mobile layouts, a simplified Devin Desktop login button in settings, cleaner Slack send options in the composer, more reliable MCP tool listing for HTTP servers, and many performance improvements to session streaming and PR review loading.

**July 15, 2026**

**Quote Text in Your Messages**

You can now select text in a session — from files, the worklog, or Devin's messages — and quote it directly in your next message, making it easier to reference exactly what you're talking about.

**Filter Sessions by Skill**

The sessions list can now be filtered by which skill was activated during the session.

**Session Sizes Are Now ACU-Only**

Session t-shirt sizes (XS–XL) are now based solely on ACU consumption and no longer factor in the number of user messages sent.

**Promote Playbooks to Your Enterprise**

Admins can now promote a playbook from a single organization to the entire enterprise, making it available across all organizations.

**Interactive ACU Chart Legends**

Legend entries on the enterprise ACUs-by-product chart are now clickable, letting you toggle individual series on and off.

**July 10, 2026**

**Redesigned Account Switcher**

A redesigned account switcher makes it easier to move between your organizations, with a clearer two-pane layout for people who belong to an enterprise.

**Copy Commands from the Worklog**

Shell commands in the session worklog now have a copy button that copies the full command to your clipboard.

**Streamlined Copy Actions**

Copy actions in the command palette are now grouped together under a single "Copy…" menu.

**Lists That Load as You Scroll**

Long lists such as repository and snapshot pickers now load automatically as you scroll, instead of requiring a "Load more" button.

**Fullscreen Devin Desktop**

The Devin Desktop VNC viewer now supports native fullscreen.

**Clearer Bulk Secret Imports**

Importing multiple secrets at once now reports errors per line, so you can see exactly which entries need fixing.

**Bug Fixes**

This release also includes a working organization filter on the enterprise sessions view, self-serve removal of GitHub Enterprise Server app configurations, and various other UI improvements throughout the app.

**July 8, 2026**

**Redesigned Review Comment Composer**

The Devin Review comment composer now uses GitHub-style Cancel, Comment, and Start a review buttons, with Cmd+Enter to submit and Escape to dismiss. In the pull request view embedded in a session, a new Commits tab lets you browse the changes commit by commit.

**Apply Environment Config Suggestions from Slack**

When Devin suggests an environment configuration change in Slack, the message now includes a diff of the proposed change and an Apply button, so you can accept it without leaving Slack.

**Mobbin MCP Server**

The Mobbin MCP server is now available in the integrations marketplace.

**Reorganized Settings Navigation**

Skills & Rules and Plugins now live together under a new Resources section, the Plugins page has a wider and clearer layout, and your personal analytics have moved into your personal settings.

**July 3, 2026**

**Diff Line Permalinks**

You can now share direct links to specific lines in a Devin Review diff via the URL hash — useful for pointing teammates to exact code locations.

**Slack !agent Renamed to !normal**

The `!agent` Slack bang-command has been renamed to `!normal` for consistency with the standard Devin mode naming.

**Slack Sync Toast Improvements**

The Slack sync notification toast now has clearer copy, can be dismissed per-tab, and includes a "don't remind me" opt-out.

**Service User Automations**

Service users can now create and manage automations via the API, enabling programmatic automation workflows.

**Snapshot Build Trigger**

`snapshot_build:completed` is now available as an automation event trigger, letting you kick off workflows when a new environment snapshot finishes building.

**MCP Run-As-Creator Warning**

Automations now display a warning when a user-scoped MCP server is selected but run-as-creator is turned off, helping avoid permission mismatches at runtime.

**Code-Snippet Telemetry Audit Log**

Changes to code-snippet telemetry settings are now recorded in the customer-facing audit log.

**Security Scan Remediation API**

The v3 API now supports endpoints for remediating security scan findings.

**API Default Devin Version**

API-created sessions can now specify a default Devin version, giving teams programmatic control over which Devin version runs their workloads.

**Git-Backed Blueprints**

Blueprints can now be backed by a Git repository, letting you version-control and collaborate on environment configurations alongside your code.

**Blueprint Permission Descriptions**

Blueprint permission names and descriptions now clearly indicate their scope, making it easier to understand what each permission controls.

**Hover Copy for Tables**

Markdown tables in sessions now display a copy button on hover, letting you quickly copy table contents to your clipboard.

**Bug Fixes**

This release also includes fixes for virtualized Review comments hijacking scroll, diff-viewer partial-expand into file boundaries, collapsed worklog diff-stat clipping in WebKit, desktop VNC reconnection after session wake, terminal LF-to-CRLF conversion on non-PTY flush, PAT-authenticated webhook error comments now being allowed, and various other UI polish improvements throughout the app.

**July 1, 2026**

**No-Access Permission Popover**

When your connected account lacks write permission on a repository, Devin Review now shows a clear "no access" popover explaining what's needed instead of silently failing.

**Auto-Review Scoped to Your PRs**

The auto-review user preference now applies only to PRs you author, so enabling it won't trigger automatic reviews on other people's pull requests.

**PR-Link Preference**

Users can now control whether in-session PR links open in the Devin tab, in GitHub, or in Devin Review.

**Persist Model Selection**

Your chosen default model is now remembered when you select it in the agent picker, persisting across page reloads.

**Network Access Requests**

In network-restricted sessions, Devin can now request access to specific domains. The request surfaces to you for approval, removing the need to preconfigure every domain.

**GitLab Mention-Only Comments**

Devin now respects mention-only PR comment settings for GitLab merge requests, reducing notification noise for teams that prefer targeted mentions.

**Slack Thread Sync**

Sessions can now sync messages bidirectionally with Slack threads. A confirmation prompt appears for busy threads, and global sync is enabled by default for new sessions.

**Unarchive on Mention**

Mentioning @Devin in a Slack thread for an archived session now automatically unarchives it so you can continue the conversation.

**Slack Commands Anywhere**

Slack bang-command macros (like `!ultra` or `!fast`) are now recognized anywhere in your message, not just at the beginning.

**Inline Mute Reminder**

The mute/quiet-mode reminder now appears inline in the session footnote instead of as a separate message, reducing clutter.

**MCP Read-Only Mode**

The secure-mode profile UI now includes a toggle for restricting MCP servers to read-only access.

**Improved Webhook Trigger Setup**

The automation editor now shows the webhook URL and secret inline before you save, so you can configure the external service first.

**Usage Analytics: PR Ratio Chart**

A new weekly Devin PR ratio chart with repository filtering is available on the Repositories analytics tab, along with CSV export and improved number formatting across all analytics tables.

**Skills Analytics**

A new enterprise-level skills analytics page shows skill usage patterns, adoption rates, and performance across your organization.

**ACU Limit Audit Trail**

Organization ACU limit changes are now recorded in the customer-facing audit log, giving enterprise admins full visibility into limit adjustments.

**Read-Only Scan Profiles**

Enterprise-managed scan profiles now render as read-only in child organizations, preventing accidental modifications to centrally managed security policies.

**Analytics Page Improvements**

Analytics time-range and filter selections now persist in the URL for easy sharing, and the organization picker in productivity dashboards supports pagination for enterprises with many organizations.

**Redesigned Environment Page**

The environment page is redesigned with platform filters, an active snapshot grid layout, and platform-specific icons for better discoverability of your build configurations.

**Cross-Platform Repository Cloning**

Organizations can now clone configured repositories on every available build platform, not just the default — enabling consistent environments across Linux, macOS, and other platforms.

**Bug Fixes**

This release also includes numerous bug fixes across the platform — including fixes for the Slate editor crash on mobile, voice recording button visibility on narrow screens, Review header alignment, IDE frame layering over dialogs, MCP OAuth redirect handling, mentions preserving spaces correctly, false "Installation out of date" banners on fresh MCP installs, blueprint drawer state preservation, unsubscribe link routing for enterprise emails, and various UI polish improvements throughout the app.

**June 26, 2026**

**Archive/Unarchive Sessions from Command Palette**

Sessions can now be archived or unarchived directly from the Cmd+K command palette on session pages, without navigating to session settings.

**Run-Once Automation Schedules**

Automations now support a run-once schedule option for one-time executions, in addition to recurring schedules.

**MCP "Installation Out of Date" Banner**

Installed MCP integrations now surface an "Installation out of date" banner with one-click marketplace refresh when an update is available.

**Post-Build Section for Blueprints**

The blueprint editor now includes a Post Build guide item for organization and enterprise blueprints.

**Readable PR Review Label Colors**

PR Review labels now render with readable text in both light and dark themes.

**Usage Analytics Improvements**

The Consumption Dashboard now uses bar charts for the session activity chart, combines active and review users into a single chart with a metric selector, adds a counts/percentages toggle, and normalizes the per-tab export buttons to a consistent "Export" control.

**June 24, 2026**

**Pin/Unpin Sessions from Command Palette**

Sessions can now be pinned or unpinned directly from the Cmd+K command palette for faster access to important sessions.

**Start Session in Background**

A new "Start session in background" button on the home page lets you kick off a session without navigating away from your current view.

**View Latest Version for File Tabs**

File tabs in sessions now include a "View latest version" affordance, making it easy to jump to the most recent version of a file Devin has edited.

**Security Findings in Ask Devin**

When using Ask Devin within PR Review, the AI context now includes security findings, enabling more security-aware assistance during code review conversations.

**"Repo Rule" Badge on Lifeguard Findings**

Lifeguard bugs that were flagged from repository rule files now display a "Repo rule" badge, helping reviewers distinguish rule-sourced findings from general analysis.

**Split View Auto-Disable on Narrow Panels**

The Split view option in PR Review is now automatically disabled when the panel is too narrow to display it usefully, preventing layout issues on smaller screens.

**Usage Analytics — Top 10 Rankings**

Consumption analytics now includes Top 10 ranking charts for repositories (in Reviews usage) and for users and service users (in the Consumption tab), giving admins quick visibility into where usage is concentrated.

**Enterprise Wide Snapshot Build Schedule**

Enterprises can now configure a snapshot build schedule, controlling when environment builds run. Blueprint settings also display drift warnings when the environment is out of sync, with actionable buttons to trigger a re-sync.

**Add Enterprise Members When SSO Is Required**

Org admins can now add existing enterprise members to their organization even when SSO is required for enterprise membership.

**ACU Billing Schedule Warning**

Enterprises consuming ACUs without an active billing schedule now see a warning, helping admins avoid unexpected usage without payment coverage.

**June 19, 2026**

**MCP Marketplace Expansion**

48+ new engineering MCP connectors are now available, including Miro, Mixpanel, Honeycomb, Postman, monday.com, Klaviyo, and many more. 42 previously-beta MCPs have graduated to general availability. New additions include LaunchDarkly (with hosted OAuth), Fathom, Attio, and Calendly. Google Drive MCP is now available to all users.

**Dedicated MCP Management Page**

Enterprise admins now have a dedicated MCP management page with per-server detail views showing organization-wide and per-session usage, replacing the previous side panel.

**GitLab User Identity Linking**

Link your personal GitLab account so Devin creates Merge Requests under your GitLab user instead of the Devin identity. For enterprises with self-hosted GitLab instances, admins can register a GitLab OAuth Application under Advanced settings to enable user linking for self-hosted instances.

**Devin Review for GitLab**

Devin Review now supports GitLab Merge Requests. Intelligent diffs, inline comments, and AI chat all work on GitLab MRs. Your GitLab MRs appear in the sidebar organized by status (Needs your review, Returned to you, Approved, Waiting for reviewers, Drafts). GitLab repos can be added to auto-review in Review settings.

**File Path Visible During Streaming Edits**

The full file path is now shown while the edit tool is actively streaming changes, so you always know which file Devin is modifying.

**Deduplicated File Tabs with Version Switcher**

When multiple versions of the same file exist, they are consolidated into a single tab with a version dropdown instead of cluttering the tab bar.

**Slack Formatting in Webapp Comments**

Bold, links, code, and other Slack formatting now renders correctly in webapp thread comments forwarded from Slack.

**PR Context Visible While Waiting for CI**

PR-ready context is now shown while CI checks are still running, so you can start reviewing before checks complete.

**Improved Feedback Controls**

Both thumbs-up and thumbs-down buttons are now always visible on messages. Session-level feedback and a qualitative feedback modal make it easier to share detailed feedback.

**Incremental Generation Steps in Automation Input**

The AI-assisted automation input now shows incremental generating steps as it builds your automation configuration.

**Public Repos Shown as Disabled in Repo Picker**

Public repositories now appear greyed out in the repo picker instead of being hidden, making it clear they exist but are not selectable.

**"User Only" PR Author Enforcement**

A new "User only" option is available in the "Open PRs as" setting. When selected, Devin will only create PRs under the user's identity and will fail if their Git account is not connected. Automations and service users fall back to the Devin identity. Enterprise admins can enforce this setting across all organizations.

**June 17, 2026**

**Cmd+K: Switch Organization & Copy Org ID**

The command palette (Cmd+K / Ctrl+K) now supports switching between organizations and copying your org ID without navigating to settings.

**Sidebar: Unpin & Remove-from-Folder Quick Actions**

The sidebar archive button has been replaced with context-aware quick actions: pinned sessions show an "Unpin" button, and sessions in a folder show "Remove from folder." Archive remains accessible via the context menu.

**Wiki: Clean Page URLs**

Wiki pages now use cleaner `/page/<id>` routes instead of the previous longer format, making links easier to share and bookmark.

**Automations Sidebar**

Automations now appear in the main navigation sidebar for quicker access to your configured automation rules.

**Japanese Translations: 100% Coverage**

All remaining Japanese translation keys have been filled across the platform, bringing Japanese language coverage to 100%.

**Ask Devin: @repos Picker Scoped to Search Repos**

The @repos file picker in Ask Devin now only shows repositories from your selected search scope, reducing noise when referencing files.

**Suggested Knowledge Visible in Session Worklog**

When Devin suggests a knowledge item during a session, it now appears as a standalone event in the worklog for easier visibility and review.

**Devin Review: Comment Language Selector**

When reviewing PRs in Devin Review, you can now select the language for AI-generated review comments (e.g., English, Japanese, Spanish).

**Devin Review: Security Findings**

All Devin reviews now include a security findings section. The security reviewer respects your repository's SECURITY.md file to tailor its analysis to your project's security policies.

**Devin Review: Code Owner Review Block**

The merge bar now shows when a PR is blocked waiting for code owner approval, making it clear which reviews are still required before merging.

**Devin Review: GitHub Alert Callouts**

GitHub-style alert callouts (note, warning, caution, etc.) in markdown files now render with proper styling in Devin Review.

**Slack: Preceding Thread Messages as Context**

When Devin is mentioned in a Slack thread, it now receives the preceding thread messages as context, enabling more informed responses without needing to repeat background information.

**Slack: !agent Bang Command**

Use `!agent` in Slack messages to Devin to explicitly route your request to a full Agent session instead of Ask mode.

**Default Sync with Slack Per Session**

New sessions can now default to syncing messages with Slack, configurable at the organization level so teams stay in the loop automatically.

**Automations: Slack Channel Updates**

Automation run results can now be posted to a designated Slack channel, keeping your team informed of automated session outcomes.

**Linear: Projects Filter for Triggers**

When configuring Linear-triggered automations, you can now filter by Linear project to scope which issues trigger Devin sessions.

**MCP Server: View Logs on Error**

MCP plugin error cards now include a "View logs" button linking directly to the MCP output channel, plus detailed error information surfaced in the plugin status card for faster debugging.

**Axiom MCP Server**

A new official Axiom MCP integration is available, allowing Devin to query your Axiom logs and observability data during sessions.

**Structured Output Schema for Playbooks**

Playbooks now support a structured output schema, enabling Devin to return results in a defined JSON format for easier programmatic consumption.

**Enterprise Knowledge Limit Increased to 300**

The maximum number of enterprise knowledge items has been increased from 200 to 300.

**June 12, 2026**

**Session Folders**

Group sessions into named folders in the sidebar. Move sessions via drag-and-drop or the three-dot menu. Folders are personal, so each user defines their own layout.

**!ultra and !fast Mid-Session Toggles**

You can now start sessions on Devin Ultra directly from Slack with the `!ultra` command. You can also switch between Ultra and Fast modes mid-session by typing `!ultra` or `!fast` in the Slack thread.

**Smarter Emoji Reactions**

Devin now only adds sleep/archive emoji reactions to messages that are explicit sleep or archive commands, reducing noise on other status messages.

**Custom OAuth for Marketplace MCP Servers**

Marketplace MCP servers that require organization-specific OAuth client credentials can now be configured directly from the integrations page.

**Markdown File Preview in Worklog**

Markdown files created during a session now render with a preview toggle, letting you see the formatted output alongside the raw content.

**Web Search Enterprise Setting**

Enterprise admins can now enable or disable Devin's web search capability via a new toggle in enterprise settings.

**"Users" Tab Renamed to "Members"**

The org membership page tab now reads "Members" for clarity.

**June 10, 2026**

**Devin Review: Pending PR Reviews Canceled on New Commits**

When new commits are pushed to a PR, any in-progress Devin reviews are now automatically canceled. The PR Review API also reflects this with a new `cancelled` status on review objects.

**Large Pastes Automatically Attached as Files**

Pasting large content (10k+ characters) into the composer now automatically attaches it as a file, regardless of existing message length. This keeps your prompt clean and avoids hitting size limits.

**User Mentions Rendered as Styled Links**

@mentions in session messages are now displayed as styled deeplinks instead of the raw "@Name (ID)" format.

**"Sent from Slack/Teams/Linear" Indicator**

Follow-up messages that originated from an integration now show a small badge indicating their source (e.g., "Sent from Slack").

**Echo Message to Slack Toggle**

A new toggle lets you bypass Slack message suppression and echo your webapp messages into the Slack thread, even in quiet-mode sessions.

**Improved Slack Message Rendering**

HTML entities in Slack messages are now properly decoded outside of code blocks, fixing garbled characters in forwarded content.

**Official Figma MCP Integration**

The official Figma MCP server is now available with suggestions enabled. The previous unofficial integration has been deactivated.

**IdP Group Role as First Assignment**

Org-scoped IdP groups can now use a group role as their very first role assignment, removing the previous requirement to set an individual role first.

**Success Confirmation After Org Creation**

Creating a new organization within an enterprise now shows a clear success state, confirming the operation completed.

**June 5, 2026**

**Start a New Session with This Prompt**

The first message in a session now shows a "Start a new session with this prompt" button, replacing the previous "Start duplicate session" menu action. Reuse any prompt for a fresh session in one click.

**Playbook Devin Mode**

Playbooks can now specify a Devin mode (e.g., Fast or Normal). When launching a session from a playbook, the agent picker reflects the playbook's configured mode.

**Configurable Auto-Reload Threshold**

You can now customize the balance threshold that triggers auto-reload in the billing usage modal.

**Jira Webhook Failure Recovery**

When a Jira webhook connection fails, a banner now appears in your Jira integration settings with a one-click reconnect action to restore the connection.

**Devin Review: Action-Required Flags on PRs by Default**

Devin Review now posts orange action-required flags to your GitHub pull requests by default when issues are found that need investigation.

**Webhook URL in Automation Editor**

The automation editor now displays the webhook URL directly under the webhook trigger, so you can copy it without navigating away.

**Improved Slack Message Formatting**

Devin's messages in Slack now use full markdown formatting for all users, providing richer text rendering with proper links, code blocks, and lists.

**Send Messages While Session Is Queued**

You can now send messages to a session that is waiting for capacity. Your messages will be delivered as soon as the session starts.

**Persist Chat Draft Across Panel Close**

Draft messages in the session composer are now preserved when the panel is closed and reopened, so you won't lose work in progress.

**Session Counts on Collapsed Sidebar**

Session counts are now visible on collapsed sidebar section headers, giving you a quick overview without expanding each section.

**Devin Review: Connect Personal Account from Blocked Controls**

In Devin Review, when Review, Merge, or comment actions are blocked because your personal identity isn't linked, you can now connect your GitHub or GitLab account directly from the blocked control without navigating to settings.

**Active Todo in Slack Plan Header**

The collapsed plan header in Slack threads now shows the currently active todo item, so you can see what Devin is working on at a glance.

**Detect @Devin Mentions After Inviting the Bot**

When you tag @Devin in a channel where the bot isn't present and then invite it, Devin now detects and responds to your original mention.

**Lower Minimum Per-Session Limit for Automations**

The minimum per-session limit for automations has been lowered from 3 to 1, giving you finer-grained control over automation budgets.

**Scratchpad Moved Under MCPs in Automations**

The scratchpad section in the automation editor has been moved to the top level under MCPs for easier discoverability.

**Prompt to Reconnect Linear**

When creating a Linear automation with an expired personal token, you'll now be prompted to reconnect before proceeding.

**June 3, 2026**

**Personal Automations**

You can now create personal automations that run under your own identity. Personal automations include a dedicated toggle, permission model, and badge in automation lists. The legacy Schedules page now shows migration guidance to help you transition to the new Automations system.

**Devin Review: Enrolled Users, Spend Limits, and GHES/GitLab Support**

Devin Review now includes an enrolled users management table in settings, a redesigned per-PR spend limit that acts as a soft block (you can re-enable if needed), and pinned section titles above file headers in the embedded review view. "Open in Devin Review" is now available for GitHub Enterprise Server and GitLab PRs.

**Pre-Approve Testing**

A new user preference lets you always approve testing for future sessions, so Devin can test changes without prompting each time. Access it from your profile settings or via the split-button on the "Test the app" action.

**V3 API: Organization Members and Automations**

New org-scoped `GET /v3beta1/organizations/{org_id}/members` endpoint for listing organization members. A full automations CRUD API is also now available via v3.

**SSO/SCIM: JIT Provisioning and Enterprise Redirect**

SSO just-in-time provisioning can now be toggled on or off, with group sync gated separately. SSO-only enterprise users are now automatically redirected to their enterprise webapp host on login.

**Settings Improvements**

The Repositories page now supports pagination. Search results in the settings sidebar are deduplicated with indent guides. A permission-gated "Add repositories" button and empty state have been added to Skills & Rules. Terminology has been updated from "org" to "organization" throughout.

**Child Sessions: Tree Connector**

Child sessions now display with a tree connector in the sidebar, making parent-child relationships visually clear.

**Bug Fixes**

Persisted orange sidebar indicator for quota-suspended sessions. Made question answer submission optimistic, removing click lag. Fixed send button centering at fractional zoom levels. Added email fallback for IdP users without a name in the session list. Fixed cross-org router links dropping query string and hash. Added cost column to scheduled sessions past sessions list. Cleared "Approve session" attention dot once the session is read. Restored question selections when an optimistic submit fails. Pinned bulk-edit bar to viewport bottom centered over content column. Included enterprise members in the session creator filter.

**May 29, 2026**

**New Command Palette**

The redesigned command palette is now available with improved search, keyboard navigation, and settings integration. Access it with Cmd+K (Mac) or Ctrl+K (Windows/Linux) to quickly navigate pages, settings, and actions.

**Automations: Files-Changed Trigger**

The automation builder now supports file-change triggers for GitHub push events. You can configure automations to run only when specific files or directories are modified in a push. Pull request triggers also automatically add the appropriate action filter.

**PR Review Sidebar Restructure**

The in-session PR review sidebar has been redesigned with collapsible sections, portalized toolbar actions, and a new diff settings menu replacing the previous split/unified toggle.

**Raindrop.ai MCP in Marketplace**

The Raindrop.ai MCP server is now available in the MCP marketplace.

**Disable Review/Analysis for Merged and Closed PRs**

The review and analysis trigger is now disabled for already-merged and closed pull requests, preventing unnecessary processing.

**Wake Sleeping Sessions on Retrigger**

Sleeping sessions now automatically wake up when a PR comment retrigger is posted, so you no longer need to manually restart them.

**Devin Review: Respect CI Monitoring Setting**

Devin Review now correctly honors the "Disable automatic comment and CI monitoring" checkbox for merge-conflict notifications.

**Bug Fixes**

Fixed intermittent Recent repos display issue. Fixed diff view flashing two-column layout before snapping to unified view. Added DeepWiki button to repo indexing header. Fixed infinite page spinner when a user is not a member of the resolved organization.

**May 22, 2026**

**Platform Default Settings**

Org admins can now set a default platform (Linux or Windows) for all new sessions, and individual users can star their personal preference. The default platform is honored across all session creation methods, including Slack, Linear, Jira, API, and automations.

**Slack Channel Override**

Type `!channel #channel-name` in Slack to override which channel Devin spawns its response thread in for that session.

**MCP OAuth Resource Parameter**

MCP OAuth flows now forward the RFC 8707 resource parameter, fixing authentication for MCP servers that require resource indicators (such as Snowflake and Runlayer).

**Custom RRULE Schedule Input**

Automation schedules now support pasting raw RFC 5545 recurrence rule strings directly, with validation and auto-detection, for schedules that go beyond the visual editor.

**GitLab Interactive PR Review**

GitLab repositories now support interactive PR review — Devin can post review comments and resolve threads as you — when the read-write GitLab connection is enabled.

**PR Review Status API**

A new `GET /v3/enterprise/pr-reviews` endpoint lets you poll Devin Review status programmatically, with optional commit SHA filtering.

**In-App Support Dialog**

"Contact support" now opens an in-app dialog where you can submit a ticket directly, replacing the previous email link.

**Inline Repo Permission Toggle**

You can now toggle repository permissions between "Read only" and "Read & write" directly from the permissions table, without needing to remove and re-add the repository.

**Enterprise Max Concurrent Snapshot Builds**

Enterprise admins can now set a maximum concurrent snapshot builds limit in enterprise settings, with backend enforcement to prevent build queue overload.

**GitLab OAuth Scope and Token Refresh**

GitLab user OAuth now requests the broader `api` scope for better compatibility, and tokens are automatically refreshed before they expire.

**Network Config Editor Redesign**

The network policy editor has been redesigned as an inline-editable list with multi-line paste support and duplicate detection, fixing the issue where domains typed but not submitted were silently lost on save.

**GitHub Connection No Longer Required for Automations**

GitHub-triggered automations no longer require a personal GitHub connection, allowing teams to rely on the org-level connection exclusively.

**PostHog MCP**

The PostHog MCP server is now available in the MCP marketplace, enabling product analytics integration directly from Devin sessions.

**Other Improvements**

Automation sessions now appear in a dedicated "Automations involving you" sidebar folder instead of being auto-pinned. Session @-mentions in chat are clickable links. A new Cmd+K action copies the session URL to clipboard. Archive undo now restores cascade-archived child sessions. MCP connection errors are surfaced instead of silently swallowed, and a new disconnect action removes stored OAuth tokens. Integration mappings for Linear, Slack, Teams, and Jira are validated at save time. The repo selector shows a Recent section and org labels. Tool calls in Watch Devin Work display timing. Automation-spawned sessions can be renamed by any org member. Integration page actions are permission-gated. File URLs in the timeline link to the correct git provider. GHES installations resolve bot identity per-config and scope webhook processing to the owning account.

**May 17, 2026**

**Collapsible Session Folders**

Sessions in the left sidebar can now be organized into collapsible folders. Click the chevron to expand or collapse a folder, and your preference is persisted per organization.

**Archive All Sessions**

A new "Archive all" option in the sidebar menu lets you archive all sessions or asks at once, with a confirmation dialog and undo support. Child sessions skip the confirmation step for faster cleanup.

**Sub-Devin Session Filter**

The sessions page now includes a "Sub-Devin" filter that lets you view child sessions independently, with support for combined parent and child filtering.

**Default Member Roles**

Enterprise admins can now configure default roles that are automatically assigned to new organization members on join, with badge display in the members list and safeguards against accidental deletion of roles in use.

**GHES App Registration Restriction**

GitHub Enterprise Server app registration is now restricted to one app per account and host combination, preventing duplicate registrations with a clear error message when a conflict is detected.

**Copyable Organization ID**

Your Organization ID is now displayed with a one-click copy button on both the Settings → General and Settings → Devin API pages, making it easy to share with support or use in API calls.

**Admin-Enforced Settings Lock Icon**

Settings that have been locked by an admin now display a lock icon with an explanatory tooltip, replacing the previous banner-style callout for a cleaner interface.

**MCP OAuth Client Credentials**

When installing MCP integrations that don't support Dynamic Client Registration (such as Salesforce), you can now supply your own OAuth client credentials directly in the configuration flow.

**Tavily MCP in Marketplace**

Tavily web search is now available in the MCP marketplace, providing AI-optimized real-time web search and content extraction capabilities for your Devin sessions.

**PR Actions & Auto-Review Settings**

The PR actions menu in Devin Review has been restored with an auto-review toggle and personal settings popover, giving you quick access to review preferences without leaving the review interface.

**Checks Tab Always Visible**

The Checks tab is now always visible in the embedded PR review experience, and the merge-status popover properly restores the checks UI so you can always see CI status at a glance.

**Improved @-Mention Search**

The @-mention search in the chat input now uses fuzzy bag-of-words matching, so queries like "setup-dev" will find "setup-devin-dev". Repositories are also ranked first in the dropdown for faster access.

**Slack Improvements**

This release includes several Slack integration improvements: channel names now resolve correctly even for channels you haven't joined, mentions display as styled blue pill badges, unmapped channel messaging is clearer, the Watch channel option appears at the top of the trigger submenu, stale channel lists are fixed, and duplicate webapp-to-Slack thread posts are suppressed.

**Slack Security Hardening**

Enterprise channel isolation for Slack thread-attach has been hardened with runtime authorization that validates channels against enterprise channel preferences, preventing cross-organization channel access.

**Video Recording Download**

You can now download session recording videos directly from the video player controls.

**Miscellaneous Improvements**

This release also includes: file re-upload fix, archived chip now clickable for non-owners with unarchive permission, network config available for finished sessions, test recording viewer close button visibility fix, settings search improvements, back buttons on MCP marketplace and knowledge detail pages, deep mode callout hidden when disabled, repo name truncation so filter stays visible, mobile agent selection single-tap fix, Devin Review file scroll and merge status fixes, skills link fix, Slack support channel in help popover, and wait tool rendered as standalone worklog event.

**May 13, 2026**

**Snapshot Build Delete**

You can now delete snapshot builds directly from the build history menu or detail page, with a confirmation dialog to prevent accidental removal. This makes it easier to clean up old or failed builds without navigating away from your environment settings.

**MCP Multiline Environment Variables**

When configuring MCP server connections in the marketplace, you can now enter multiline values for environment variables — such as PEM private keys, JSON service account credentials, and Snowflake key passphrases — without needing to escape or flatten them first.

**Sub-Devin Sidebar Improvements**

Sub-Devin sessions spawned by automations can now be pinned and reordered independently in the sidebar, and they appear expanded by default so you can see their status at a glance without clicking to expand.

**Voice Recording While Devin Is Working**

The microphone button now appears alongside the stop button while Devin is actively working, allowing you to record and send voice follow-ups without waiting for Devin to finish its current task.

**Settings Redesign**

Settings pages have been redesigned with a hub-style layout, improved search across all settings, and a streamlined navigation structure. An announcement dialog introduces the new experience on first visit, and legacy settings URLs automatically redirect to their new locations.

**Archive Active Session Warning**

When you archive a session that is still actively working, a warning dialog now informs you that archiving will put both the session and any child sessions to sleep before proceeding.

**Share Session on Mobile**

A new "Share session" action is available in the sidebar session menu on mobile devices, making it easy to share session links directly from your phone.

**Devin Review Mobile Improvements**

On mobile, tapping "Ask Devin" on a comment now opens the chat panel directly, pull-to-refresh is available on the review scroll container, and bug/flag tap targets have been fixed so they open on the first tap and reveal the associated comment.

**V3 API Enhancements**

The V3 API now supports filtering sessions by repository name via the `repo_names` parameter, filtering by archive status via `is_archived`, specifying `devin_mode` when creating sessions, and setting `folder_id` and `is_enabled` when creating or updating knowledge notes.

**Enterprise Member Invite Acknowledgement**

When inviting new members to an enterprise organization from the admin panel, an acknowledgement modal now confirms the invitation details before it is sent.

**Rename Context to Skills & Rules**

The "Context" section in settings has been renamed to "Skills & Rules" to better describe its purpose of managing Devin's skill definitions and behavioral rules for your organization.

**Blueprint Migration Improvements**

The blueprint migration page now displays per-repo session counts, supports filtering by repository, and shows a completed state when all migrations are finished, making it easier to track progress across large organizations.

**Miscellaneous Improvements**

This release also includes: autofocus on confirmation buttons in archive dialogs, plan artifact button polish, configurable CI status in search results, debounced enterprise snapshot builds, server-side event deduplication to prevent duplicate delivery, pinned sessions remaining visible when automations are hidden in the sidebar, removal of the misleading "Action required" label for Python sessions awaiting instructions, schedule list cap raised from 50 to 200, monitor trigger cleanup when adding new Slack triggers, repo setup status fix for Dynamic Repo Setup organizations, "Approve session" visibility in the sidebar even after all PRs are merged, inline image deduplication by URL, streaming scroll stability fix, high-resolution home screen icon for Android, beta Vite mode build fix, fast mode loading indicator reset on session switch, and sidebar hover cards on expanded non-active sections.

**May 8, 2026**

**Devin Review API**

You can now trigger Devin Review programmatically via the REST API. Use `POST /v3/organizations/{org_id}/pr-reviews` with a service user token or PAT to initiate reviews from CI pipelines, scripts, or custom integrations.

**Mermaid Diagram Rendering**

Mermaid code blocks in session messages now render as interactive SVG diagrams with zoom and pan controls, making it easier to explore flowcharts, sequence diagrams, and architecture diagrams that Devin produces.

**Close PRs on Session Archive**

When archiving a Devin session, a dialog now appears where you can optionally close any linked GitHub pull requests, keeping your repository tidy without manual cleanup.

**Per-PR Auto-Review Toggle**

You can now enable or disable automatic Devin Review on a per-PR basis from the PR actions menu, giving you granular control over which pull requests receive automated review without changing your organization-wide settings.

**Sidebar Session Notifications**

The session sidebar now shows persistent status labels, such as "PR created," "Awaiting instructions," or "Approve session," alongside timestamps so you can quickly see what each session needs. Sessions also display read/unread indicators: an orange dot marks sessions with unread updates, and the dot clears once you open the session.

**Service User Permission Management**

Enterprise administrators can now assign the `ManageAccountServiceUsers` permission in custom roles, providing granular control over who can create and manage service users and API keys within the organization.

**Ask Devin in PR Discussions**

The "Ask Devin" button is now available on discussion tab thread comments in Devin Review, making it easy to ask follow-up questions or request changes directly within review conversation threads.

**MCP Secret Scoping**

When adding secrets for custom MCP server connections, you can now choose between personal scope, visible only to you, or organization scope, shared with your team, via a new scope selector in the creation dialog.

**Clickable Diff Stats in Worklog**

Clicking the +N/-M diff stats in worklog group headers now opens a scoped diff tab showing only the file changes from that specific group, making it faster to review exactly what changed at each step.

**Repo Selector Fix**

The select-all checkbox in the repository selector now correctly toggles only the repositories matching your current search filter, rather than selecting all repositories regardless of the filter.

**May 6, 2026**

**Slack Tool Use in Worklog**

When Devin interacts with Slack during a session (sending messages, adding reactions, reading channels), these actions now appear in the worklog and progress UI with a dedicated Slack icon and action details.

**Settings Search Improvements**

Settings pages now use a centralized item registry with keyword-driven search, delivering more accurate and comprehensive results when searching across all settings pages.

**Command Palette Search**

Fixed search ordering in the command palette so results rank correctly, and resolved a scroll view issue in the search results window.

**Review Commit Links**

Fixed commit links in Devin Review to point to the correct URL path, and improved status indicators for review progress.

**Default Branch Detection**

Fixed an issue where repository indexing could use the wrong branch as the primary branch instead of the actual GitHub or GitLab default branch, which could affect DeepWiki and search results.

**May 1, 2026**

**Stacked Review Permissions**

Enterprise admins can now assign tiered PR Review access levels to their organization members: manual-only review, automatic review on PR creation, or automatic review on every push. This gives administrators granular control over how and when Devin Review engages with pull requests across their organization.

**Skill Slash Commands**

You can now invoke skills by typing `/name` in the prompt input, in addition to the existing @mention syntax. Skills are grouped by repository in the dropdown for easier discovery.

**Auto-Attach Large Paste**

Pasting a large block of text into the prompt input now automatically attaches it as a file instead of filling the text box, preserving any message you've already typed.

**Jira Project Mapping Redesign**

The Jira project mapping modal has been redesigned with a fixed header and scrollable content area, making it easier to configure mappings for organizations with many Jira projects.

**Auto-Fix Includes CI Checks**

The "Auto-fix with Devin" button on pull requests now includes failing CI check names in the prompt alongside review findings, giving Devin more context to resolve issues in a single pass.

**Linear Team Mapping Improvements**

The default organization is now optional when configuring enterprise Linear team mappings, and unmapped teams can be explicitly cleared to "None" instead of requiring a catch-all mapping.

**Session Origin in API**

The v3 API session response now includes an `origin` field indicating how the session was created (webapp, Slack, API, or CLI), making it easier for API consumers to categorize and filter sessions programmatically.

**Deleted Orgs in Enterprise Sessions API**

Enterprise session endpoints now support an `include_deleted_orgs` parameter, giving enterprise admins visibility into sessions from organizations that have been removed.

**Snapshot Revert for Declarative Setup**

Users with the ManageOrgSnapshots permission can now revert an organization from declarative environment configuration back to classic configuration, without needing the broader ManageOrgSettings permission.

**April 29, 2026**

**Revamped Blueprint Authoring Experience**

The blueprint editor has been redesigned with a shared layout, per-section play buttons, and a bottom terminal drawer. You can now deep-link directly into a repo's blueprint editor, making it faster to author and test environment setups.

**Enterprise Commit Email Lock**

Enterprise admins can now require all member commits to use the user's primary email. The lock is enforced across snapshot setup, session creation, and PR digest commits, helping enterprises keep commit attribution consistent for audit and compliance.

**PR Auto-Close Removed**

Devin sessions no longer automatically close their pull requests when the session ends. Open PRs now stay open by default so you can manage their lifecycle yourself, with no surprise closures.

**Hybrid Comment Mode in Devin Review**

When Devin Review is opened alongside a Devin session, review comments now default to hybrid mode — anchored to specific lines where possible and falling back to file-level comments otherwise — instead of forcing one or the other.

**Auth-Type Badges in Git Connections**

The git connection filter dropdown on the repository permissions page now shows a PAT, App, or OAuth badge next to each connection, making it easier to disambiguate connections that share a name.

**Slack Trigger Message in Sessions List**

Sessions started from Slack now display the user's triggering Slack message in the sessions list instead of the system prompt, making it easier to identify Slack-launched sessions at a glance.

**PR Digest List Redesign**

The PR digest list has been redesigned with a cleaner layout that matches the sessions list view, making it easier to scan and navigate through pull requests.

**Double-Click File Attachment Picker**

Double-click the plus button in the prompt input to directly open the file attachment picker, skipping the intermediate menu.

**April 24, 2026**

**Sensitive Toggle for Secrets**

When Devin requests a secret, you can now toggle whether the value should be masked (sensitive) or visible, instead of it always defaulting to masked.

**Merged Multi-Edits in Progress Tab**

Consecutive file edits to the same file are now merged into a single entry in the progress tab, showing a combined diff from the original to the final version instead of individual per-edit diffs.

**Session Category and Subcategory in API**

The v3 API session response now includes category and subcategory fields. A new category filter is available on session list endpoints, and session exports also include these fields.

**Wide Markdown Tables in Chat**

Markdown tables in Devin's chat messages can now extend beyond the chat column width, preventing cramped multi-column tables from being unreadable.

**April 22, 2026**

**SSO Connection Picker**

Organizations with multiple SSO connections for the same email domain now see a picker on the login page instead of being auto-redirected to the first match, letting users choose the correct identity provider.

**MCP OAuth Token Expiry Warnings**

Invalid or expired MCP OAuth tokens are now flagged with warning banners in the integrations UI. A reconnect button lets you re-authorize without navigating away from the page.

**Repository Permissions Decoupled from Git Integrations**

Repository permissions are now managed separately from git integration settings with a view/manage split, giving admins finer-grained control over who can modify repository access versus who can manage the underlying git connection.

**View Consumption Permission**

A new ViewAccountConsumption permission separates read access to usage and consumption data from billing write access, allowing admins to grant visibility without full billing control.

**Attachments in Question Answers**

File attachments are now included when you answer Devin's prompts. Previously, attached files were silently dropped.

**MCP Auth Status Feedback**

MCP authentication requests now show success or error status in both the webapp and Slack after completion, so you know immediately whether authorization succeeded.

**Merge Time Reduction in Review**

The Devin Review page now displays the merge time reduction percentage, showing how much faster PRs are merged with Devin Review enabled.

**April 17, 2026**

**PR Digest for Disconnected Users**

The Review page now shows a read-only digest of PRs from your Devin sessions — including open, draft, merged, and closed PRs — even if you haven't connected GitHub yet.

**GitHub Enterprise Server in Review**

GitHub Enterprise Server instances can now be selected in the Review page's Link GitHub flow, and GHES organizations appear in the Devin Review org selector.

**Review Permissions Enforcement**

Repository-level review permissions are now enforced, giving admins control over which repositories Devin Review can access.

**IDP Groups Management**

Enterprise settings now include a management UI for Identity Provider (Okta) groups, letting admins map groups to roles, view group members, and detect user conflicts with existing role assignments.

**Secure Mode Description**

The Secure mode description in enterprise settings has been rewritten to more clearly explain what Secure mode does and when to use it.

**WikiGenerationItem Card**

A new card is now displayed in sessions when the generate\_wiki MCP tool is invoked, giving better visibility into wiki generation progress.

**GHES Links in Integrations**

GitHub Enterprise Server user account links have been moved to the Integrations section of your profile for easier access.

**Minor Bug Fixes and Improvements**

This release also includes a range of smaller fixes and polish: sessions now indicate which are in an "Action Required" state, fixed the playback speed dropdown not opening on click, resolved invisible text in chat inputs on light backgrounds, fixed sidebar glyph flickering, corrected the Context Growth chart x-axis to use continuous datetime, removed checkboxes from combobox options, fixed seat type dropdown clipping, improved seat invitation copy for proper singular/plural phrasing, clarified the "available full seats" invite warning, updated flex seats to show as unlimited on the members page, and hid the Connect GitHub banner for GitLab MRs and during the Review intro overlay.

**April 15, 2026**

**Close PR or Convert to Draft in Review UI**

The PR review merge bar now includes options to close a PR or convert it to a draft directly from the review page.

**Inline Session Rename**

Sessions can now be renamed inline directly in the sidebar without opening a dialog.

**Smart Table Column Sizing**

Tables throughout the app now use content-aware column width sizing for better readability.

**Faster Sidebar Session Loading**

The sidebar now lists sessions faster and more reliably, with improved rendering performance and optimistic updates when creating new sessions.

**Datadog Remote MCP Server**

Datadog is now available in the MCP marketplace as a remote MCP server with OAuth-based authentication, so Devin can query your Datadog dashboards and metrics directly.

**ACP Summarizer**

Agent Client Protocol now supports a summarizer method for generating session summaries programmatically, useful for integrations that need a concise recap of what Devin accomplished.

**Granola MCP Server**

The Granola MCP server is now promoted out of beta, letting Devin access your Granola meeting notes during a session.

**Pagination and Search for Review Settings**

Enterprise review settings now support pagination and search for repository and user lists, making it easier to manage large configurations.

**Minor Bug Fixes and Improvements**

This release also includes a range of smaller fixes and polish, including a proper 404 error page for invalid URLs, frontend performance optimizations, and assorted stability improvements across the webapp.

**April 10, 2026**

**Theme Selector Generally Available**

The theme selector is now generally available, with system theme as the default so Devin automatically matches your OS light or dark mode.

**Wiki Effort Level Descriptions**

When choosing a DeepWiki effort level, each option now shows its expected ACU range so you can pick the right trade-off between cost and depth with confidence.

**DeepWiki Cost Breakdown Modal**

The DeepWiki cost breakdown modal is back, giving you an ACU-level view of where a wiki generation spent its budget.

**Cancel In-Progress Snapshot Builds**

You can now cancel an in-progress snapshot build directly from the snapshot list without waiting for it to finish or fail.

**Snapshot Blueprint Ordering**

Snapshot detail rails and repository-level blueprints now respect your configured blueprint ordering, so the list you see matches the order you set.

**Scheduled Session Failure Email Rate Limiting**

Failure email notifications for scheduled sessions are now rate limited, so a scheduled run hitting the same problem repeatedly will no longer flood your inbox.

**Knowledge Search Auto-Expand**

When you search your knowledge base, any folder containing a matching note now automatically expands so you can see the result in context without hunting for it.

**Profile Integrations Filter**

Your profile page now only shows integrations that are actually connected for your organization, cutting the clutter from services you do not use.

**Browser Tool Parity Improvements**

Devin's browser tool now handles native browser dialogs, intercepts file chooser prompts, respects navigation guards, and restores focus correctly, bringing its behavior much closer to a real user browsing the web.

**Amplitude MCP Server**

Amplitude is now available in the MCP marketplace, so Devin can pull product analytics directly into a session without a custom integration.

**One-Click MCP OAuth Install**

Installing an MCP server that uses OAuth now returns the authorization URL directly, skipping an extra click and getting you connected faster.

**Personal MCP Servers**

You can now connect personal MCP servers, which enable Devin to use MCPs with authorization provided by an individual user rather than shared across an organization.

**Richer ACP Methods and @-Mentions**

Agent Client Protocol now carries @-mentions as structured resource blocks and adds new methods for listing repositories, saving secrets, archiving sessions, approving deploys, and attaching to the interactive browser, giving ACP clients a much richer surface area to work with.

**Devin CLI Polish**

The Devin CLI now preserves streamed shell output alongside exit codes, supports a `/resume` alias, renders plan-mode exits more clearly, and uses focus pings to keep a session from sleeping while you are actively watching it.

**Reconnecting VNC Screen**

The interactive browser now shows a reconnecting screen while its VNC stream is recovering, so you get clear feedback instead of a frozen view when the connection briefly drops.

**Unlink GitHub Enterprise Server OAuth**

You can now unlink a GitHub Enterprise Server OAuth connection from your account, making it easy to rotate credentials or clean up stale integrations.

**Total ACUs Column in Usage Table**

The Users table in Usage analytics now includes a Total ACUs column, so enterprise admins can rank and compare per-user consumption at a glance.

**Bulk Repository Secrets Import**

Enterprise admins can now import multiple repository secrets at once through a new bulk import flow on the repository configuration page, replacing the old one-at-a-time workflow.

**Minor Bug Fixes and Improvements**

This release also includes a range of smaller fixes and polish across the webapp, including repository branch dropdowns that now size correctly, the DeepWiki section hidden when no branches are indexed, a fix for Linear OAuth cancellations returning errors, correct starting numbers on streamed ordered lists, a copy-message button that now copies only the selected message, and assorted other stability and layout improvements.

**April 8, 2026**

**Auto-merge from Devin Review**

You can now enable or disable GitHub auto-merge directly from the Devin Review merge button, so approved pull requests land as soon as checks pass without an extra trip to GitHub.

**Enterprise Review Consumption by Repository**

The Reviews tab on the Enterprise Consumption page now groups Devin Review spend by repository with current-cycle vs previous-cycle columns, a search box, and CSV export, making it much easier for enterprise admins to see where their review spend is going.

**Devin Review Breakdown in v3 Consumption API**

The v3 consumption API now reports Devin Review as its own line item in the product breakdown alongside sessions and indexing.

**Categorization and Subcategories**

Session categorization and subcategories are now generally available for every workspace, giving you a consistent way to organize and filter your Devin sessions.

**Pinned Organizations Sync Across Devices**

Your pinned organizations are now stored server-side and follow you across every device and browser you sign in from.

**Session Message Permalinks**

Every message in a session now has its own shareable link, so you can point teammates directly at the exact moment you want them to see.

**Larger Attachment Uploads**

Session attachments now support files up to 75 MB, up from the previous 20 MB limit.

**Higher-Quality Wiki v2**

Wiki v2 now uses stronger reasoning, subagents, and agentic page writers to produce noticeably better documentation, and shows the ACU cost of the last generation so you can see exactly what each refresh costs.

**Guardrails V3**

Our new pattern-based guardrail prompts significantly reduce false positives while keeping the same level of protection.

**Ask Sub-mode Renamed to Q\&A**

The Ask sub-mode is now simply labeled "Q\&A" to better reflect what it does.

**Consolidated Session Header Menu**

Session header links are now grouped into a single hyperlink menu for a cleaner, less crowded header.

**Faster Syntax Highlighting**

Code blocks across the app now render with an incremental, worker-based syntax highlighter for noticeably faster and smoother highlighting on large files.

**Scroll Restoration**

Navigating back through the app now restores your previous scroll position so you land where you left off.

**Japanese Localization Refresh**

Japanese localization strings have been refreshed across the webapp.

**MCP Marketplace Upgrades**

The MCP marketplace now includes a Recommended section, smarter Figma discovery, and a shared interactive OAuth flow that shows connection status and errors directly in chat as you install servers.

**MCP Audit Logs**

Enterprise audit logs now cover MCP server updates and secret link and unlink events for better visibility into integration changes.

**Session ACU Hard Caps**

Enterprises can now set a hard upper limit on total ACUs per session, with an acknowledgement modal and real-time validation so users always know when a session is approaching the cap.

**Cerebras Now Enterprise-Ready**

Cerebras is now available as an enterprise-ready inference provider for organizations that want to use it for their Devin workloads.

**US Privacy Controls**

Devin now honors Global Privacy Control signals and supports CCPA and CPRA opt-out requests for customers in the United States.

**Refreshed Settings Layout**

Insights, identity provider, and several other enterprise settings pages have been migrated to the new settings layout and design system for a more consistent look and faster navigation.

**Enterprise Secrets Table Polish**

The enterprise secrets table now includes an environment variable column and a build-only toggle, with a simplified layout that removes the Name column and type selector.

**Minor Bug Fixes and Improvements**

Numerous smaller fixes and polish, including sidebar collapse state persistence, sidebar pull requests loading without a GitHub connection, better multi-PR session isolation, deduplicated Slack file forwarding, quota reset on plan upgrade, billing cycle short-month correction, snapshots sorted alphabetically, an auto-organize tooltip explaining when it is disabled, and the Category beta label and Review beta badge retired for paying organizations.

**April 3, 2026**

**Classic Environment Setup Deprecation**

Classic environment setup is being deprecated on June 30, 2026, when all organizations move to declarative configuration (blueprints). Your classic machine configuration stays available as a read-only reference until July 31, 2026. See [Environment configuration](https://docs.devin.ai/onboard-devin/environment).

**Enterprise-Scoped Secrets**

Enterprise admins can manage secrets at the enterprise level, automatically shared across all organizations. Initially only available to users of declarative environment configuration.

**Enterprise ACU Visibility Control**

Enterprise admins can control whether users see ACU usage info.

**Enterprise MCP Registry Enforcement**

Enterprise admins can enforce an MCP server allowlist across their organization.

**Enterprise Build Pinning**

Enterprise admins can pin specific Devin builds and roll back to previous versions. Initially only available to users of declarative environment configuration.

**Devin Review Auto-Fix**

When Devin Review detects bugs in a PR, a new "Auto-fix with Devin" button launches a session to fix them in one click.

**PR Review Chat CI Tools**

Check CI status and view CI job logs directly within the PR review chat.

**Pin Sessions**

Pin important sessions from the three-dot menu for quick access.

**Organization Terminology**

All "team" references updated to "organization" across the product. No functional change.

**Improved Questions UI**

Navigation between questions, inline "Something else" input, cleaner design.

**Auto-Skip Pending Questions**

Devin auto-skips pending questions when you send a new message.

**Cleaner File Paths**

Relative paths with structured format instead of full absolute paths.

**PR Review Polish**

Sticky tabs, bug navigation, copy buttons, chat CTA at end of diffs, empty state for PRs without descriptions.

**Structured Output for Child Sessions**

Child sessions can return structured JSON via schema for automated workflows.

**Smarter Codebase Search**

Recency-based repository ordering for faster, more accurate results.

**/new Slash Command**

Alias for /clear to start a fresh conversation.

**Azure DevOps Service Principal**

Connect Azure DevOps via service principal instead of personal OAuth.

**Linear Assignee Filter**

Rich picker for Linear assignee filtering in automations.

**Linear Token Refresh**

Linear connections now auto-refresh OAuth tokens, preventing disconnection on expiry.

**Minor Bug Fixes and Improvements**

GitLab PAT rotation fix, responsive mobile layouts, startup command display improvements, build log scroll-to-bottom, Ctrl+O expand hint, shell security improvements, automations UI fixes.

**April 1, 2026**

**PR Resuming**

Devin can now take over and work on existing pull requests that weren't created in the current session, enabling continuation of work across sessions.

**Devin Review Improvements**

Added a "lines left to review" counter in the PR review diff viewer, and significantly faster page load times via parallel queries.

**Streaming Terminals**

Terminal output in the session view now streams in real time.

**Connected Accounts Pagination**

GitHub and GitLab connected accounts pages now support pagination and search for organizations with many connections.

**GHES Improvements**

Support for org-level GitHub App registration on GitHub Enterprise Server, with pre-filled app name in the manifest flow.

**Settings Page Redesign**

Multiple settings pages (Schedules, Playbooks, Knowledge, Secrets) have been redesigned with a new unified layout, along with consolidated dialog styles across the product.

**Sticky Sidebar Headers**

Sidebar section headers now stick to the top while scrolling for easier navigation.

**Light Mode Polish**

Multiple fixes for theme-aware colors across modals, dialogs, and components.

**Add or Create Team**

New button in the account dropdown to create a team without going through the GitHub integration flow.

**Auto-open Agents Tab**

The Agents tab auto-opens when child sessions are detected.

**Tab Title Simplification**

Browser tab title simplified to "Devin" with contextual page titles.

**Slack Thread Permissions**

Users without Devin accounts are now blocked from messaging in Devin Slack threads.

**Improved PR Comment Formatting**

Devin's PR comments now include line info and outside-diff context.

**IME Composition Fix**

Fixed an issue where pressing Enter during IME composition (e.g., Japanese input) in Safari would prematurely submit text.

**Ignore Comment Info**

More helpful information shown when Devin Review comments are ignored.

**Environment Setup Cleanup**

Clarified environment description copy and removed redundant buttons.

**Bash Syntax Highlighting**

Terminal output now has syntax highlighting for bash commands.

**Scheduled Session Pill**

Visual indicator for scheduled sessions in the sessions list.

**Minor bug fixes and improvements**

Various bug fixes, performance improvements, and visual polish across the platform.

**March 27, 2026**

**Preview Agent Toggle**

A new "Preview upcoming features" toggle is available in the agent selector, enabling streaming thoughts and faster execution. Stability may be limited as these features are still in development.

**Inline File Previews**

HTML, PDF, and SVG attachments can now be securely rendered inline in the session sidebar, with a code/render toggle and download button in the file toolbar.

**Focus Mode**

A new focus mode hides the sidebar, header, and right panel for a distraction-free chat experience. Access it from the session menu or with the keyboard shortcut Cmd+Shift+F.

**Agents Tab for Child Sessions**

A new "Agents" tab automatically appears when a session creates child sessions, showing their status, todos, and PRs in one place.

![](https://mintcdn.com/cognitionai/RTcVGIV5Ij1tsiWg/images/release-notes/agents_tab_mar27.png?fit=max\&auto=format\&n=RTcVGIV5Ij1tsiWg\&q=85\&s=a85543a0050ddc5a08658f2702775faf)

**Test Recording Viewer**

Devin's test recordings now display as rich cards with pass/fail summaries, playback speed controls, and loop functionality.

**Jira Integration Enhancements**

Jira now supports direct session creation from issues, service account connections, and per-project trigger options for controlling when Devin is activated.

**Redesigned Integration Settings**

The Linear, Jira, and Slack integration settings pages have been redesigned with cleaner layouts for team mapping, playbook management, bot allowlists, and automation rules.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**March 24, 2026**

**Light Mode (Beta)**

Devin now supports a light mode theme. You can switch between dark, light, and system themes from your profile settings.

![](https://mintcdn.com/cognitionai/IKMeVQNNTefx1Aj_/images/release-notes/light_mode_mar24.png?fit=max\&auto=format\&n=IKMeVQNNTefx1Aj_\&q=85\&s=f89454e875c916e651cdc270593ecfa2)

**Streaming Shell Output in Worklog**

Background shell process output now streams inline within worklog items, so you can monitor long-running processes without switching to the terminal.

**Cookie JSON Builder for Secrets**

A new tabbed interface for cookie secrets lets users paste raw JSON (auto-encoded to base64) with validation, parsed previews, and expiration warnings.

**Org-Level Metrics API**

New organization-scoped API endpoints for metrics and consumption data.

**Session Insights UI Redesign**

The session insights modal has been redesigned with a refreshed layout, improved empty states, and updated copy.

**Secrets on Initial Prompt**

Users can now attach secrets when creating a new session from the home page, matching existing functionality for follow-up messages.

**Devin Reviews Analytics**

A new Devin Reviews section has been added to the usage analytics page showing review metrics.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**March 19, 2026**

**Devin Manages Devins**

Devin can now orchestrate Devins and manage your Devin setup directly from any session. This will replace the current Advanced Devin features.

Devin can delegate to a team of managed Devins that work in parallel. Each managed Devin is a full Devin with its own isolated virtual machine. The main Devin session acts as a coordinator — scoping the work, monitoring progress, resolving conflicts, and compiling the results.

New capabilities include:

* Session management – Create child sessions with structured output schemas and playbooks. Search and filter past sessions by tags, playbook, origin, or time range. Analyze past sessions with full search across shell, file, browser, git, and MCP activity.
* Knowledge management – Create, update, delete, and organize knowledge notes into folders. Review knowledge suggestions.
* Playbook management – Create, edit, and delete playbooks.
* Schedule management – Create and manage scheduled sessions including recurring or one-time runs, agent selection, and notification preferences.

![](https://mintcdn.com/cognitionai/LlJfDoruQJVIwKYo/images/release-notes/devin_manages_devins_mar19.png?fit=max\&auto=format\&n=LlJfDoruQJVIwKYo\&q=85\&s=bb5a37d342e6f70ff233efe7fbc703c5)

**Redesigned Integration Pages**

The integration settings pages have been redesigned with a new layout including connection cards, support sections, and pagination.

**Improved Playbook Page**

The playbooks page now shows a table layout. Each playbook page now shows session count, unique users, and merged PRs per playbook, with a weekly activity chart. Playbooks now include a version history.

**Parent/Child Session Grouping**

Parent and child sessions are now grouped together in the sidebar, so child sessions stay nested under their parent regardless of sorting or filtering.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**March 13, 2026**

**On-Demand Session Insights**

Session insights are now generated on demand rather than automatically. You can trigger analysis from the Session Insights button in the UI or programmatically via the new [generate insights API endpoint](https://docs.devin.ai/api-reference/v3/sessions/post-organizations-session-insights-generate.md). Insights will continue to be automatically generated for L and XL sessions.

**New Session Inputs**

* An inline voice recording button is now available for hands-free messaging.
* Devin sessions can be @ mentioned to reference them directly in another session.

**Session List Improvements**

* Important sessions can be pinned to the top of the sidebar for quick access.
* A new sidebar filter hides scheduled sessions from the session list.

**Structured Output Modal**

The structured output from sessions created with the API with this parameter set can now be viewed and downloaded from the "Structured output" option in the session menu.

**Markdown Preview**

Markdown files can now be natively displayed in the right panel.

![](https://mintcdn.com/cognitionai/6rLe9xqH8tl30kzu/images/release-notes/markdown_preview_mar13.png?fit=max\&auto=format\&n=6rLe9xqH8tl30kzu\&q=85\&s=0e1522d5b0c2dcf450c1d500831970e7)

**March 11, 2026**

**Datadog MCP Integration**

Datadog is now available as an official integration in the MCP marketplace.

**Default Branch Management**

Users can set and manage the default branch for repository indexing from the repositories management page.

**Schedule: Run as User**

Schedules can now be reassigned to run as the current user via a "Run as me" button in the schedule detail view, also available via the v3 API.

**IdP Groups in Enterprise Settings**

The enterprise members table now shows IdP group memberships for each user.

**Minor bug fixes and improvements**

Various bug fixes, performance improvements, and visual polish across the platform.

**March 7, 2026**

**Install Devin as an App**

Devin can now be installed as a Progressive Web App on desktop and mobile. On Chrome or Edge, open app.devin.ai and click the install icon in the address bar (or Menu → Install Devin); on iOS Safari, tap Share → Add to Home Screen. Once installed, Devin links open directly in the app.

![](https://mintcdn.com/cognitionai/KW9HnR-CzYk_OnFB/images/release-notes/pwa_install_mar7.png?fit=max\&auto=format\&n=KW9HnR-CzYk_OnFB\&q=85\&s=d5899122826b65c58752dbc8c4e3494e)

**Session Status in Browser Tab**

The browser tab favicon now shows a colored status dot on session pages (green when Devin is working, orange when it's waiting for you) so you can spot sessions that need attention without switching tabs.

**Minor bug fixes and improvements**

Various bug fixes, performance improvements, and visual polish across the platform.

**February 27, 2026**

**AskDevin Upgrade**

Expanded to support Ask and Plan modes. Now has more advanced code search capabilities which produce more detailed and accurate answers. The status of Devin sessions created from AskDevin can now be seen in the conversation.

![](https://mintcdn.com/cognitionai/_dRQes3XKFhFT5iT/images/release-notes/askdevin_modes_feb27.png?fit=max\&auto=format\&n=_dRQes3XKFhFT5iT\&q=85\&s=185d827e8490305032b08e4159f03aed)

**Devin Review: GitHub Commit Status Checks**

Status checks now displayed directly on pull request commits, giving visibility into review progress without leaving GitHub. The status links to the full Devin Review analysis.

To enable this, the Devin GitHub App will request the Commit Statuses and Checks permissions. If these permissions are not granted, all existing functionality is unaffected.

**Repository Selection for Schedules**

Schedules can now be configured with specific repositories that the session will be run with each time the schedule executes.

**February 24, 2026**

**Devin 2.2 Launch**

Devin 2.2 is the culmination of hundreds of improvements both big and small over the last few weeks including:

* 3x faster startup time to immediately see Devin's output and build trust that it's on the right track
* A new UI that connects every step of the dev lifecycle: start sessions from anywhere, review agent output directly in Devin, and jump back into sessions from code review.
* Smoother and faster Slack and Linear integrations to start sessions without having to switch context

See past release notes for the full list of the improvements.

**Full Desktop Testing**

Devin now supports end-to-end testing using computer use and can test any desktop app that can run on Linux. Devin will request to QA its PR, if you approve it, it will run your app, use its desktop to click around, and send you an edited recording of the testing for your review.

Existing users can enable Desktop mode in [Settings > Customization](https://app.devin.ai/customization).

<video autoPlay muted loop src="https://mintcdn.com/cognitionai/h8qwUI43QqmV5C_j/images/release-notes/desktop_testing_feb25.mp4?fit=max&auto=format&n=h8qwUI43QqmV5C_j&q=85&s=d1b61b1bbc16fe6d9777a5cb5e1d48e8" />

**February 20, 2026**

**Devin v3 API Officially Released**

The v3 API is coming out of beta and is now the primary API for all Devin functionality. The new API provides all of the legacy API functionality and additionally provides role-based access control, session attribution, and new capabilities.

The legacy APIs (v1 and v2) will be deprecated in the future. The exact date will be announced in the product and in release notes. We commit to providing at least 30 days notice. During the deprecation period, the legacy APIs will continue to work but all new features will only be available in the v3 API.

**Sessions List Redesign**

The sessions list page has been redesigned with an updated layout featuring inline PR previews, message snippets, and status indicators. Sessions can now also be sorted by creation date.

![](https://mintcdn.com/cognitionai/giTocETit1KrE1tc/images/release-notes/sessions_list_redesign_feb20.png?fit=max\&auto=format\&n=giTocETit1KrE1tc\&q=85\&s=af8e47c95bd885a917a3b14eb88a70b7)

**Merge Conflict Detection**

Devin will automatically notify users when a PR created in a Devin session has merge conflicts. Available on GitHub.com only.

**New Devin Scheduling Options**

Scheduled Devins can now be created as a one-time scheduled event, and existing schedules can be triggered on demand with the "Run now" button.

**Devin Review for GitHub Enterprise Server**

Devin Review now supports GitHub Enterprise Server (GHES) repositories. You can view PR diffs, run analysis, and use the Devin Review chat agent to propose and apply code changes. Some interactions with GitHub such as posting comments, submitting reviews, and merging are not yet supported on GHES.

**Repo Selector Enhancements**

The repository selector now features an "Only" button to quickly isolate a single repository and displays setup and indexed repo counts.

![](https://mintcdn.com/cognitionai/giTocETit1KrE1tc/images/release-notes/repo_selector_feb20.png?fit=max\&auto=format\&n=giTocETit1KrE1tc\&q=85\&s=02dbaec4d88fde1c05a23a1249c9bfab)

**Session Messages API**

A new `GET /messages` endpoint allows programmatic access to session message history.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**February 13, 2026**

**Visual Refresh and Polish**

The overall design has been improved and polished across the product. Some button locations have been minorly adjusted, but these changes do not impact the product functionality.

![](https://mintcdn.com/cognitionai/eb79m3k_19Q1Z7JT/images/release-notes/visual_refresh_feb13.png?fit=max\&auto=format\&n=eb79m3k_19Q1Z7JT\&q=85\&s=2b120f33cf351e2a8ef0519122a13761)

**Devin Fast Mode**

A new "Fast Mode" option is now available in the agent picker, delivering \~2x faster responses with the same intelligence at 4x ACU per session.

**Devin Review: Batch Comments**

When replying to PR review threads, you can now check "Start a review" to batch multiple review comments before submitting them all at once.

**Devin Review: Code Changes from Chat**

The Devin Review chat agent can now propose code edits directly in the conversation. You can review the suggested changes, then apply them as a commit to the PR branch without leaving Devin Review.

![](https://mintcdn.com/cognitionai/eb79m3k_19Q1Z7JT/images/release-notes/devin_review_code_changes_feb13.png?fit=max\&auto=format\&n=eb79m3k_19Q1Z7JT\&q=85\&s=c3fa22770c3519e48e2d30693f52b597)

**Secure Mode for All Organizations**

Secure mode is now available for non-enterprise organizations. When enabled, Devin loses native internet deployment capabilities. You can find this setting under "Security settings" on the Customization page.

**Skills Support**

Devin now recognizes and uses skills defined in your codebase. Skills provide reusable instructions that Devin can activate, search, and invoke during sessions to follow your team's preferred workflows.

**Settings Search**

A search bar has been added to the settings sidebar, making it easy to quickly find any settings page by name or keyword.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**February 6, 2026**

**Schedule from the Input Box**

You can now quickly create a scheduled Devin session directly from the input box. Use the "Schedule Devin" option in the context menu or switch to the "Create schedule" tab in Advanced mode to set up recurring sessions without leaving the home page.

![](https://mintcdn.com/cognitionai/5kC7KOFG99QiDpzy/images/release-notes/schedule_tab_feb6.png?fit=max\&auto=format\&n=5kC7KOFG99QiDpzy\&q=85\&s=5a1be9af185e7b49aead3841d5cdc71f)

**Enterprise Organization Selection**

The enterprise landing page has been redesigned with a cleaner organization list, member counts, and sorting options for easier navigation across your enterprise.

**Devin Review: Auto-Review Settings**

Auto-review configuration is now accessible as a settings popover directly in the PR header, making it faster to enable or disable auto-reviews per repository.

**Devin Review: Hide Comment Highlights**

A new setting in the code diff viewer lets you hide comment highlight boxes for a cleaner reading experience when reviewing code.

**Git Permissions Update**

Removed the ability to index repos in the primary organization for enterprises.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**February 3, 2026**

**Scheduled Devins**

You can now create recurring Devin sessions that run automatically on a schedule. Configure frequency, prompt, and playbook from the new Schedules page in settings, and receive email notifications for schedule events.

![](https://mintcdn.com/cognitionai/bmZeS9ugCdt432TZ/images/release-notes/scheduled_devins_feb3.png?fit=max\&auto=format\&n=bmZeS9ugCdt432TZ\&q=85\&s=9eea264876c694242d828772af338ccb)

**Devin Review: Draft PR Support**

Draft PRs now show a "Ready for review" button, allowing you to mark PRs as ready for review directly from Devin Review.

**Devin Review: File Comments and @Mentions**

You can now add file-level comments from the file header menu and use @mentions when editing existing comments in Devin Review.

**Settings Sidebar Reorganization**

The organization settings sidebar has been reorganized with clearer section headers including "Devin's resources," "Membership," "Settings," and "Integrations" for easier navigation.

![](https://mintcdn.com/cognitionai/bmZeS9ugCdt432TZ/images/release-notes/sidebar_reorganization_feb3.png?fit=max\&auto=format\&n=bmZeS9ugCdt432TZ\&q=85\&s=f65a8a5b3c00f0bb6d9a8a20328a63a3)

**Per-Product Consumption Analytics API**

The v3 analytics API now includes a per-product breakdown of Agent Compute Unit consumption alongside existing totals. See [API Release Notes](https://docs.devin.ai/api-reference/release-notes.md) for details.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**January 22, 2026**

**[Devin Review Launch](https://docs.devin.ai/work-with-devin/devin-review.md)**

Devin Review is a reimagined interface for understanding complex PRs. Devin review groups related changes together logically, detects copied code, detects bugs and security issues, and an embedded PR chat interface.

**Repo Setup AI Suggestions**

The repository setup flow now provides inline AI-powered suggestions for setup commands, helping you configure repositories faster with less manual effort.

**Sessions API Enhancements**

New API endpoints allow you to retrieve session details by ID, send messages to active sessions, and filter sessions by origin (webapp, Slack, Teams, API, Linear, Jira). See [API Release Notes](https://docs.devin.ai/api-reference/release-notes.md) for details.

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.

**January 9, 2026**

**Session Secrets via API**

You can now provide session-scoped secrets when creating sessions via the API, enabling secure credential management for automated workflows without manual intervention.

**Native Linear Integration**

Devin now has a built-in Linear tool for organizations with the Linear integration installed. This means you no longer need to install the Linear MCP separately to interact with Linear issues and projects.

**API Session Filters**

Added new filtering options to the sessions API endpoint, including the ability to filter sessions by user email for better session management and reporting.

**Syntax Highlighting for Kotlin and Protocol Buffers**

Code blocks now support syntax highlighting for Kotlin and Protocol Buffers (.proto files), improving readability when working with these languages.

**Git Settings Reorganization**

Personal git settings have been moved from the "Customization" section to the "Profile" tab in user settings for better organization and discoverability.

**Playbook Visual Distinction**

Playbooks now have a visual badge in the dropdown menu, making it easier to distinguish between playbooks and other options when starting a session.

**Machine Setup UX Improvements**

Small usability improvements to the machine setup flow for a smoother onboarding experience.

**Copy Context Button**

Each PR now has a "Copy Context" button that provides an AI-generated summary of the agent's work, context it found, and decisions it made, which is particularly useful when handing off work to other agents.

![](https://mintcdn.com/cognitionai/4q3bdIh3Bg1UZT5q/images/release-notes/copy_context_button_jan9.png?fit=max\&auto=format\&n=4q3bdIh3Bg1UZT5q\&q=85\&s=204360196ce417fcf11f9a00ee67eeb6)

**Minor bug fixes and improvements**

Various bug fixes and performance improvements across the platform.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.