# Neon Genie Quickstart

**Advice only.** Helps turn ideas into roadmaps and approaches without inventing buyers, capital, or proof.

**Site:** https://scrimshawlife-ctrl.github.io/NeonGenie/  
**Full README:** [README.md](./README.md) · **Privacy:** [PRIVACY.md](./PRIVACY.md) · **Version:** [VERSION](./VERSION)

---

## Install

```bash
hermes skills install scrimshawlife-ctrl/NeonGenie/skills/neon-genie
```

Reload Hermes. Or clone and run `./install.sh`, then:

```bash
python scripts/neon_genie.py do doctor
```

---

## Use in Hermes

1. Say **Use Neon Genie**.  
2. Describe who is stuck, what “done” looks like, and your constraints.  
3. Tell it what **not** to invent (buyers, money, skills).  
4. Treat the answer as a **draft**.

### Dashboard wizard

If your Hermes dashboard includes the Neon Genie integration, launch it and
open **Neon Genie** in the sidebar:

```bash
hermes dashboard
# then open /neon-genie
```

Choose a mission, enter the outcome and current state, set research guardrails,
review the generated evidence-bound prompt, and select **Copy and open Chat**.
Clipboard failure keeps you on the review step so you can copy manually. The
wizard prepares the request; the installed Neon Genie skill still runs inside
the real Hermes Chat session and remains advisory only.

### Prompts that work

```text
Use Neon Genie. I'm between jobs with limited money and an app idea.
I need a realistic roadmap and first approaches I can actually run.
Do not invent buyers, capital, or skills I did not declare.
Research public facts if you can; ask me for private facts instead of inventing.
Label every important claim. Do not modify any repo.
```

```text
Use Neon Genie. First cash in 7 days from skills I declare only.
No fictional resources. If you cannot answer, say so.
```

```text
Use Neon Genie. Stay offline: research.enabled=false
Only use what I paste and what is already in this workspace.
```

---

## Optional terminal checks

Most people stop after Hermes chat. From a clone:

```bash
# Healthy install?
python scripts/neon_genie.py do doctor

# One sample package on disk (open run-envelope.json after)
python scripts/neon_genie.py do run --recipe product-audit --out out/neon-genie/demo
```

More samples:

```bash
python scripts/neon_genie.py do run --brief examples/zero-option.brief.yaml --out out/neon-genie/zero
python scripts/neon_genie.py do run --brief examples/capital-sprint.brief.yaml --out out/neon-genie/sprint
```

Maintainer / CI commands: see [CHANGELOG.md](./CHANGELOG.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Privacy (one paragraph)

Sample packaging runs default to **local-only**. The skill does not train models on your content or run silent telemetry. Hermes and model providers have separate policies — see [PRIVACY.md](./PRIVACY.md).
