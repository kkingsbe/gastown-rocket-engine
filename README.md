# Requirements-Based Engineering Multi-Agent System

## Overview

Three AI agents running on periodic ~10-minute invocation cycles, implementing a
full requirements-based engineering (RBE) workflow with computational design and
simulation-based verification.

| Agent | Role | Owns | Prompt File |
|---|---|---|---|
| **Agent 1** | Requirements Owner | What must be true | `AGENT_1_REQUIREMENTS_OWNER.md` |
| **Agent 2** | Design & Implementation | How to achieve it (docs + code) | `AGENT_2_DESIGN_IMPLEMENTATION.md` |
| **Agent 3** | Verification & Validation | Proof it's achieved (independent sims + plots) | `AGENT_3_VERIFICATION_VALIDATION.md` |

## How It Works

```
You write REQUIREMENTS.md + CONTEXT.md
        │
        ▼
   ┌─────────────┐
   │   Agent 1    │  Decomposes into REQ_REGISTER.md
   │  Req Owner   │  Assigns work to Agents 2 & 3
   └──────┬───────┘  Maintains TRACE_MATRIX.md
          │
   ┌──────┴──────┐
   ▼              ▼
┌──────────┐  ┌──────────┐
│  Agent 2  │  │  Agent 3  │  (Agent 3 blocked until Agent 2 produces artifacts)
│  Design   │  │  Verify   │
└─────┬─────┘  └─────┬─────┘
      │               │
      ▼               ▼
  design/          verification/
  ├── scripts/     ├── scripts/      ← Independent Python simulations
  ├── data/        ├── data/         ← JSON/CSV computational results
  └── plots/       └── plots/        ← Matplotlib figures with REQ thresholds
      │               │
      └───────┬───────┘
              ▼
       TRACE_MATRIX.md
       (full traceability: REQ → Design Script → Verification Sim + Plot)
```

## Quick Start

1. **Write your `REQUIREMENTS.md`** — plain language, quantitative where possible.
2. **Write your `CONTEXT.md`** — domain physics, equations, material data, reference
   values. This ensures both design and verification agents use the same physics.
3. **Set up the directory:**
   ```bash
   mkdir -p comms/inbox comms/outbox comms/archive
   mkdir -p design/scripts design/data design/plots
   mkdir -p verification/scripts verification/data verification/plots
   ```
4. **Invoke each agent on a ~10-minute timer** using your preferred method
   (cron, Claude Code tasks, etc.), passing the corresponding prompt file as
   the system prompt.

## What Gets Produced

By the end of a sprint, your repo will contain:

```
project/
├── REQUIREMENTS.md              ← Your input (never modified by agents)
├── CONTEXT.md                   ← Your domain reference (never modified)
├── REQ_REGISTER.md              ← Formal shall-statements (Agent 1)
├── TRACE_MATRIX.md              ← Full traceability (Agent 1)
├── TODO_DESIGN.md               ← Agent 2's work queue (Agent 1)
├── TODO_VERIFY.md               ← Agent 3's work queue (Agent 1)
├── DECISIONS.md                 ← Trade studies and decisions (Agent 2, approved by Agent 1)
├── FINDINGS.md                  ← Pass/fail log with numerical data (Agent 3)
├── BLOCKERS.md                  ← Cross-agent blockers (any agent)
│
├── design/                      ← Agent 2's output
│   ├── architecture.md          ← System-level design description
│   ├── performance.md           ← Performance design document
│   ├── mechanical/              ← Mechanical design docs
│   ├── analysis/                ← Thermal, structural analysis docs
│   ├── scripts/                 ← Executable Python design scripts
│   │   ├── performance.py       ← Nozzle sizing, thrust, Isp calculation
│   │   ├── thermal_analysis.py  ← Chamber wall temperature model
│   │   ├── mass_budget.py       ← Component mass roll-up
│   │   └── prop_budget.py       ← Propellant mass and delta-v
│   ├── data/                    ← JSON outputs from scripts
│   │   ├── performance.json     ← All design parameters + computed results
│   │   ├── thermal.json
│   │   └── mass_budget.json
│   └── plots/                   ← Design visualizations
│       ├── nozzle_contour.png
│       └── thrust_vs_pc.png
│
├── verification/                ← Agent 3's output
│   ├── VER-001_thrust.md        ← Verification report with plots embedded
│   ├── VER-002_isp.md
│   ├── SUMMARY.md               ← Final verification summary
│   ├── scripts/                 ← INDEPENDENT verification simulations
│   │   ├── ver001_thrust.py     ← Independent thrust computation
│   │   ├── ver002_isp.py        ← Independent Isp computation
│   │   └── ver003_thermal.py    ← Independent thermal analysis
│   ├── data/                    ← Verification results
│   │   ├── ver001.json          ← Includes Agent2 vs Agent3 comparison
│   │   └── ver002.json
│   └── plots/                   ← ALWAYS include requirement threshold lines
│       ├── ver001_thrust_vs_pc.png
│       ├── ver002_isp_vs_expansion_ratio.png
│       └── ver003_thermal_boundary_sweep.png
│
├── comms/                       ← Inter-agent communication
│   ├── inbox/
│   ├── outbox/
│   └── archive/
│
└── .agent1_done / .agent2_done / .agent3_done / .sprint_complete
```

## Communication Flow

Agents communicate through files, not direct messages:

- **Agent 1 → Agent 2:** Work assignments via `TODO_DESIGN.md`
- **Agent 1 → Agent 3:** Verification tasks via `TODO_VERIFY.md`
- **Agent 2 → Agent 1:** RFIs and trade studies via `comms/outbox/` (with supporting plots/data)
- **Agent 3 → Agent 1:** Failure reports via `comms/outbox/` (with verification plots as evidence)
- **Agent 1 → All:** Responses via `comms/inbox/`

## File Ownership Matrix

| File | Agent 1 | Agent 2 | Agent 3 |
|---|---|---|---|
| `REQUIREMENTS.md` | Read | Read | Read |
| `CONTEXT.md` | Read | Read | Read |
| `REQ_REGISTER.md` | **Read/Write** | Read | Read |
| `TODO_DESIGN.md` | **Write (assign)** | Write (checkboxes) | Read |
| `TODO_VERIFY.md` | **Write (assign)** | Read | Write (checkboxes) |
| `TRACE_MATRIX.md` | **Read/Write** | Read | Read |
| `DECISIONS.md` | **Approve** | Append | Read |
| `FINDINGS.md` | Read | Read | **Read/Write** |
| `design/*` | Read | **Read/Write** | Read |
| `verification/*` | Read | Read | **Read/Write** |
| `BLOCKERS.md` | **Read/Write** | Read/Write | Read/Write |

## Key Design Principle: Independent Verification

The most important aspect of this system is that **Agent 3 writes its own simulation
code from scratch**. It reads Agent 2's design parameters (dimensions, materials,
operating conditions) but implements the physics independently. This catches:

- Coding errors in Agent 2's scripts
- Incorrect assumptions
- Missing boundary conditions (Agent 2 may design for nominal; Agent 3 checks edges)
- Equation implementation bugs

When Agent 2 and Agent 3 agree (delta < 5%), you have strong confidence the design
meets the requirement. When they disagree, you've found a bug before it became a
hardware problem.

## Completion Signals

```
Agent 1 finishes → .agent1_done
Agent 2 finishes → .agent2_done
Agent 3 finishes → .agent3_done
Last agent to finish → .sprint_complete
```

## Adapting for Other Domains

This example uses a satellite thruster, but the workflow works for any
engineering domain. To adapt:

1. **Rewrite `REQUIREMENTS.md`** for your system
2. **Rewrite `CONTEXT.md`** with your domain's:
   - Governing equations
   - Material properties
   - Reference designs
   - Physical constants
   - Design heuristics
3. The agent prompts themselves are domain-agnostic — they work with any
   quantitative engineering requirements.