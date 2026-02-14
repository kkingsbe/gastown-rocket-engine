# Communication Outbox - Agent 1 (Requirements Owner)

## Purpose

This directory serves as the **outbox** for Agent 1 (Requirements Owner). This is where Agent 1 sends messages to Agent 2 (Design & Implementation) and Agent 3 (Verification & Validation).

## Types of Messages

The following types of messages should be placed in this directory:

### Approvals or Rejections for RFIs from Agent 2
- **Approvals:** Confirming design decisions, material substitutions, or implementation approaches
- **Rejections:** Declining proposed solutions with reasons and alternatives
- **Conditional Approvals:** Approvals with specific requirements or modifications

### Responses to Findings from Agent 3
- Acknowledgment of verification failures or discrepancies
- Guidance on how to resolve issues
- Instructions for re-verification or corrective actions
- Decisions on acceptability of deviations

### Clarifications or Additional Requirements Information
- Explanations of requirement specifications
- Additional context or interpretation guidance
- Updates to requirements when necessary
- Answers to questions from Agent 2 or Agent 3

## How Agents 2 and 3 Should Process Messages

### For Agent 2 (Design & Implementation)
1. **Monitor outbox regularly** for messages from Agent 1
2. **Review approvals** and proceed with implementation as authorized
3. **Address rejections** by understanding the reasons and proposing alternatives
4. **Incorporate clarifications** into design and implementation work
5. **Respond via inbox** when necessary to confirm receipt or ask follow-up questions

### For Agent 3 (Verification & Validation)
1. **Check outbox** for responses to findings or discrepancies reported
2. **Follow guidance** on resolving verification failures
3. **Re-verify** as instructed after corrective actions
4. **Confirm receipt** of responses via inbox when appropriate
5. **Proceed** with verification work based on Agent 1's decisions

## Message Format

Messages should use the following filename convention: `[AGENT]-[MSG_TYPE]-[YYYYMMDD]-[SEQ].md`

Example: `AGENT1-APPROVAL-20250214-001.md`

Each message should include:
- **From:** Which agent sent it
- **To:** Which agent is the recipient
- **Date:** Message date
- **Type:** RFI | STATUS_UPDATE | FINDING | RESPONSE | APPROVAL | REJECTION
- **Subject:** Brief subject line
- **Related REQ IDs:** (if applicable)
- **Related DES/VER IDs:** (if applicable)
- **Body:** The message content

Example:
---
From: Agent 1 (Requirements Owner)
To: Agent 2 (Design & Implementation)
Date: 2025-02-14
Type: APPROVAL
Subject: Material substitution approved for nozzle
Related REQ IDs: REQ-018
Related DES IDs: DES-001

Body:
[Approval message with any conditions or notes]
---

## Communication Workflow

```
Agent 1 → comms/outbox/ → Agent 2/3 receives and processes → comms/inbox/ → Agent 1
```

This outbox is a critical communication channel for the multi-agent workflow, ensuring that Agent 1 can provide timely guidance, approvals, and responses to keep the design and verification processes moving forward efficiently.
