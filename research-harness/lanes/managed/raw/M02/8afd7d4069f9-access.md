> ## Documentation Index
> Fetch the complete documentation index at: https://docs.devin.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Devin Bot access and security

> Share a Devin Bot and control its access: who can use it, what it can reach, how Bots hold grants, and what changes when you share or connect Bots.

A [Devin Bot](https://docs.devin.ai/work-with-devin/bots) works with its own access, not the access of whoever messages it. So when you share a Bot, everyone you add can use every sign-in, secret, and session the Bot holds, by asking it.

That gives you two things to control, both on the **Sharing** page of the Bot's settings:

* **Who can use** the Bot: the people, groups, roles, and other Bots that can message it.
* **What it can access**: the sign-ins, secrets, sessions, and other Bots it has been given.

## Who can use a Bot

A new Bot is private to its creator. Nobody else can message it, read it, or change it until it's shared with them. Roles with [**Manage Bots**](https://docs.devin.ai/work-with-devin/bots#enterprise-permissions) can also share any Bot in the organization, without access to its conversations.

### Share a Bot

Share a Bot when other people should work with the same Bot: one conversation, one memory, one set of connections. To give people a Bot of their own with the same instructions, [share it as a template](https://docs.devin.ai/work-with-devin/bots/templates.md#share-your-own-template) instead.

**1. Check what the Bot can access**

On the **What it can access** tab, read through **Resources** and revoke anything that should stay yours. For a tool everyone should use through the Bot, give the Bot [its own account](https://docs.devin.ai/work-with-devin/bots/connections.md#sign-ins) in place of your sign-in.

**2. Add people, groups, roles, or Bots**

On the **Who can use** tab, add them under **People**. To share the Bot with everyone in your organization, add the organization's Member role.

**3. Pick an access level**

Each entry starts with **Can use**. Keep **Can configure** and **Can share** for the people who maintain the Bot.

> [!WARNING]
>
> Anyone you add can read everything the Bot has said and remembered so far, and can use every connected account the Bot already holds. If the conversation holds something private, create a new Bot from the same template instead of sharing this one.

### Access levels

Access comes in three levels, so the people who maintain a Bot don't have to be the people who talk to it.

| Access | What it allows |
| - | - |
| **Can use** | Message the Bot and direct its sessions, which run with the Bot's own connections and secrets. This includes reading the Bot's conversation, its memory, and the sessions it started. |
| **Can configure** | Change the Bot's instructions, connections, plugins, and secrets. |
| **Can share** | Decide who else can use, configure, or share the Bot. |

None of the levels includes another. Someone with **Can share** can manage the access list without reading the Bot's conversation, and someone with **Can configure** can't message the Bot unless they also have **Can use**.

### Access requests

Someone who opens a Bot they can't use can request access, and so can another person's Bot. Anyone who can share the Bot grants or declines the request on the **Who can use** tab, and the Bot's creator is notified of new requests.

Granting gives the requester **Can use**. When the requester is a Bot, anyone who can use that Bot can use the access you grant.

### Message sources

People are not the only way a message reaches a Bot. To see everything that can make a Bot act, check **Message sources** on the **Who can use** tab:

* **Slack.** Once the Bot has its own Slack app, the **Who can message** setting decides which Slack members can DM the Bot and whose thread replies it reads. See [Slack permissions](https://docs.devin.ai/work-with-devin/bots/slack.md#slack-permissions).
* **Automations.** Each event source of an enabled [automation](https://docs.devin.ai/product-guides/automations.md) that messages the Bot, such as Slack, a Git provider, or a webhook.

## What a Bot can access

Every Bot can use your organization's [secrets](https://docs.devin.ai/product-guides/secrets.md) and the [connections](https://docs.devin.ai/work-with-devin/bots/connections.md) installed for the whole organization or enterprise. Anything beyond that is a grant.

### How a Bot holds grants

A grant is something a person gave the Bot and can take back, such as a sign-in, a secret, or a session. The Bot holds the grant, not the person who asked for the work, so it applies to every session the Bot starts, whoever sent the message.

| A Bot can hold | What the grant lets the Bot do |
| - | - |
| **An MCP sign-in** | Connect to that MCP server with the giver's own sign-in. The Bot acts as the giver there. |
| **A plugin** | Use the giver's copy of the plugin, with the giver's sign-ins on the MCP servers it declares. |
| **A personal secret** | Use the giver's personal secret with that key. |
| **A session** | Open one of the giver's sessions, at the giver's own level or below. |
| **A personal automation** | Read and change the giver's personal automation the way the giver can. |
| **Another Bot** | Read that Bot and message it. See [Share Bots with each other](#share-bots-with-each-other). |
| **Pull request authorship** | Open pull requests as a person, for work that person asked for. Each person turns this on for themselves. |

Two rules keep a grant tied to the person who gave it:

* **A grant never exceeds the giver.** A Bot gets a session at the giver's level or below, only the secrets the giver has, and only the sign-ins the giver holds.
* **A sign-in lasts only while the giver still has it.** If the member who gave a sign-in leaves the organization or loses access to that connection, the Bot loses it too. If they sign out, the Bot can't use the connection until they sign back in.

### How a Bot gets a grant

1. **You give it in settings.** For example, you connect an MCP server on the Bot's **Connections** page, add a secret, or tick a Bot under **Your Bots**.
2. **The Bot asks, and you approve.** While it works, a Bot can ask in chat for one of your MCP sign-ins, your copy of a plugin, a personal secret, a session, or a personal automation. The card says what approving will share. You can only approve giving your own.
3. **A private Bot takes what its creator already has.** See [Private and shared Bots](#private-and-shared-bots).

### Private and shared Bots

A Bot is **private** while only its creator can use it, and **shared** as soon as anyone else is given the Bot. A private Bot acts for one person, so it can use that person's resources without asking. A shared Bot acts for several people, so each new piece of access needs someone to approve it.

| | Private Bot | Shared Bot |
| - | - | - |
| **The creator's secrets, sign-ins, plugins, and sessions** | Takes what it needs without a prompt. Each one is still recorded as a grant. | Asks the person it is answering, who approves a card to give their own. |
| **The creator's other Bots** | Connects to the creator's other private Bots when it needs them. | Only the Bots the creator ticks under **Your Bots**. |

Giving one of your Bots access to another of your own Bots doesn't make either one shared. But a private Bot that a shared Bot can use also asks before it takes its creator's resources, because the people who use the shared Bot can reach it.

### Review and revoke access

**Resources** on the **What it can access** tab lists every grant a Bot holds, grouped by kind. Anyone who can share the Bot can revoke a grant there.

You can also take back what you gave without being able to share the Bot:

* On the Bot's **Connections** page, remove the sign-ins and plugins you gave it.
* Ask the Bot in chat to remove access. It shows a confirmation card listing what will be removed before anything changes.

## Share Bots with each other

Give one Bot access to another when it needs to read the other Bot's work or send it messages. Giving Bot A access to Bot B lets A read B, including its conversation and sessions, and message it. A can't change B's settings.

### Your own Bots

On the **What it can access** tab of the Bot that should get access, tick the Bots it should be able to read and message under **Your Bots**. Only the Bot's creator sees this list, and it shows the other Bots they created in this organization.

### Bots that belong to someone else

Share the other Bot with yours the way you would with a person:

* Someone who can share the target Bot adds your Bot on its **Who can use** tab.
* Or your Bot requests access, and the request appears under **Access requests** on the target Bot.

### Who sees more

Access passes through a Bot. If A can reach B, the people who can use A can reach B's work through A, so connecting two Bots can show a Bot's work to people it was never shared with:

| Bot A (gets access) | Bot B (is accessed) | What changes |
| - | - | - |
| Private | Private | Nothing for anyone else. |
| Shared | Private | Everyone who can use A can read B and message it through A. |
| Private | Shared | Everyone who can use B sees what A writes to it. |
| Shared | Shared | Everyone who can use A can read B and message it through A, and everyone who can use B sees what A writes to it. |

When either Bot is shared, a confirmation says who will see or reach more before the change applies. Sharing A later doesn't remove the access A already has to B, so check **What it can access** on A before you add people to it.

### Remove access between Bots

Untick the Bot under **Your Bots**, or revoke the grant under **Resources** on the **What it can access** tab. Anyone who can share the Bot being accessed can also remove it from that Bot's access list.

Archiving a Bot removes the access between it and other Bots, in both directions. Unarchiving doesn't bring that access back.

## Pull requests as you

By default, a Bot opens pull requests as itself, and each one ends with a note saying which Bot opened it and who it works for. To be the author of pull requests for work you asked for, turn on **Open pull requests as me** on the **What it can access** tab.

Each person turns this on for themselves, including on a shared Bot. Nobody can turn it on for someone else, and the page doesn't show who else has it on. Turning it off doesn't change pull requests the Bot already opened.

People who can configure the Bot can turn the note off with **Sign pull requests**.

## Related pages

* [Devin Bots overview](https://docs.devin.ai/work-with-devin/bots)
* [Connections and secrets](https://docs.devin.ai/work-with-devin/bots/connections.md)
* [Use a Devin Bot in Slack](https://docs.devin.ai/work-with-devin/bots/slack.md)
* [Usage limits](https://docs.devin.ai/work-with-devin/bots/usage-limits.md)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.