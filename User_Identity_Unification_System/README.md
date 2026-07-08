# User Identity Unification System

## Overview

This repository contains a simple **User Identity Unification System** designed as part of the AI Automation Engineer assessment.

The goal is to identify whether user information received from different platforms belongs to the same person and unify it under a single internal author profile.

The project is represented as a flowchart to demonstrate the overall logic in an easy-to-understand manner.

---

## Problem Statement

An author may contact the platform using different identities across multiple channels.

**Example:**

- 📧 Email: `sara.johnson@xyz.com`
- 📱 WhatsApp: `+91 9876543210`
- 👤 Dashboard Name: `Sara J.`
- 📷 Instagram: `@sarapoetry23`

Although these details appear different, they may belong to the same author. The objective is to detect this and maintain a single internal profile.

---

## Workflow

### Step 1: Receive User Information

The system receives information from different platforms such as:

- Email
- Phone Number
- Name
- Instagram Handle
- Dashboard Name

---

### Step 2: Search Existing Profiles

The system searches the existing author database for possible matches.

---

### Step 3: Compare User Information

The incoming information is compared using:

- Email
- Phone Number
- Name Similarity
- Social Handle Similarity

---

### Step 4: Calculate Confidence Score

A confidence score is generated based on how closely the information matches an existing profile.

---

### Step 5: Decision

The system follows three possible paths:

#### ✅ High Confidence
- Link the information to the existing author profile.
- Keep the same Internal Author ID.

#### 🟡 Medium Confidence
- Send the record for manual verification.
- A support team confirms whether the profiles belong to the same user.

#### 🔴 Low Confidence
- Create a new author profile.
- Generate a new Internal Author ID.

---

### Step 6: Output

The system returns one of the following results:

- ✅ Existing Profile Updated
- 🟡 Manual Verification Required
- 🔴 New Profile Created

---

## Confidence Levels

| Confidence Level | Action |
|------------------|--------|
| High | Link to existing profile |
| Medium | Manual verification |
| Low | Create a new profile |

---

## Flowchart

The flowchart illustrates the complete identity matching process from receiving user information to making the final decision.

> Add your flowchart image here after uploading it.

```text
flowchart.png
````

Or using Markdown:

```markdown
![Identity Unification Flowchart](flowchart.png)
```

---

## Future Improvements

* Implement fuzzy string matching for names.
* Use LLMs to improve identity matching.
* Learn from manual verification decisions.
* Support additional platforms and identifiers.

---

## Technologies (Future Implementation)

* Python
* Fuzzy Matching
* LLM APIs
* Supabase / PostgreSQL
* REST APIs

---

## Conclusion

This project presents a simple, beginner-friendly approach to user identity unification. It demonstrates how data from multiple platforms can be matched using confidence scores while providing a manual verification step for uncertain cases. The design focuses on clarity, scalability, and ease of understanding rather than implementation complexity.

 
```
