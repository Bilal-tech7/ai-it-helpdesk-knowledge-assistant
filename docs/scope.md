# Project Scope: AI IT Helpdesk Knowledge Assistant

## Setting
A fictional mid-sized organisation (working name: Northwind Logistics). The knowledge base consists of original demonstration guides written for this project. Real company IT procedures are confidential, so results show the technique works, not that it fits any specific company's policies.

## 1. Problem
Employees and IT support staff often struggle to find reliable guidance for routine IT issues such as password resets, VPN access and Wi-Fi problems. Existing options, including limited help-page menus and fixed-option chatbots, frequently fail to resolve the problem, and when they fail, there is often no clear route to a human or any visibility of what happened to the request. This wastes employees’ time, makes support staff repeatedly answer the same questions, and leaves unresolved requests hard to track.

## 2. Users
- Employees: want a quick, reliable answer to a routine IT question without waiting for IT support or searching long documents.
- IT support staff: want approved guidance found quickly, and unresolved requests passed on as tracked tickets.
- Knowledge-base administrator: wants to review which questions the assistant couldn’t answer, and which issues keep coming back, so they can spot gaps or outdated guides and fix them.

## 3. Five support topics
1. Password reset, lockouts and MFA
2. VPN and remote access
3. Wi-Fi and network connectivity
4. Software installation and access requests
5. Printing and hardware basics

Evidence strength: password/login/MFA is supported by every source reviewed; software installation by the public sources and Torrens guides; VPN, Wi-Fi and printing by the public helpdesk sources only (vendor blogs). Topics will be revisited if the employee interview contradicts them.

## 4. Out of scope (what it will NOT do)
- Fixing outages, downtime or slow systems (infrastructure problems)
- Granting access or changing settings on devices; it gives guidance only
- Answering questions outside the five chosen topics or non-IT questions; these are escalated, not guessed
- Giving answers without an approved source; if no supporting passage exists, it says so and escalates
- Handling personal or sensitive data; the interface shows a notice not to share passwords or personal details, and the assistant never asks for them
- Production-grade security hardening; warnings and source checks reduce risk but do not prevent misuse

## 5. Success measures
**Status (28 Oct 2026):** The value check against a plain FAQ search and the automated sensitive-data test were not completed. See "Not done yet" in the README.
Measured using a test set of 30-50 questions (covered, ambiguous and out-of-scope).
Targets are provisional and will be revised after the first test run.

- **Covered questions:** when the answer is in the guides, the assistant gives a correct answer on at least 80% of questions.
- **Uncovered questions:** when the answer is not in the guides, the assistant says so and escalates to a ticket on at least 90% of questions, without guessing.
- **Sources:** when it cites a source, the cited passage supports the answer in at least 90% of cases.
- **No loops:** it never repeats the same clarifying question or fixed options more than once before offering escalation.
- **Ambiguous questions:** the assistant asks one clarifying question or escalates, without guessing, on at least 80% of ambiguous questions.
- **Ticket workflow:** every escalation creates a ticket with a visible status, in all workflow tests.
- **Sensitive data:** across the test set, the assistant never asks for or repeats passwords or personal details.
- **Value check:** compare it with a plain FAQ search on answer correctness and time to find an answer, and record whether the AI adds value.

## 6. Evidence

**Public helpdesk sources** [desk research: vendor blogs, not independent], checked 22 Oct 2026
- Password resets and lockouts appear as a top request category in every source reviewed.
- VPN, MFA and Wi-Fi/network problems appear in several sources, especially for remote workers.
- Software installation, access requests and printing appear in two or three sources.
- Caveat: most sources are written by companies selling helpdesk or AI tools, so percentages are their claims, not independent data.
- Sources:
  - https://herothemes.com/blog/help-desk-ticket-examples/ (help desk ticket examples)
  - https://www.retellai.com/ar/blog/service-desk-knowledge-base-examples (service desk knowledge base examples)
  - https://www.reworked.co/digital-workplace/a-look-at-whats-been-driving-top-it-support-requests-during-the-pandemic/ (IT support requests during the pandemic)
  - https://www.solarwinds.com/blog/the-10-most-common-service-desk-requests (10 most common service desk requests)
  - https://www.cloudswitched.com/blog/reduce-it-support-tickets (reducing IT support tickets)
  - https://www.eesel.ai/blog/help-desk-ticket (most common help desk ticket issues)
  - https://www.atiba.com/common-it-help-desk-issues/ (common IT help desk issues)
  - https://helpmepcs.com/blog/level-1-helpdesk (Level 1 helpdesk questions)

**University IT help pages review** [verified: university web pages], checked 22 Oct 2026

Torrens University:
- https://www.torrens.edu.au/studying-with-us/student-support (IT support listed as one support category, alongside library and study support)
- https://studenthub.torrens.edu.au/Hub/student-email
- https://studenthub.torrens.edu.au/Hub/student-portal
- https://mfastu.torrens.edu.au/ (MFA overview: 14-day re-verification, Authenticator app, backup phone numbers)
- https://mfastu.torrens.edu.au/torrens-mfa/Torrens_MFA_FAQ.pdf (MFA FAQ: lost phones, registration errors, device changes; fallback is contacting Student Support)

University of Sydney:
- https://www.sydney.edu.au/students/student-contacts-enquiries/student-it.html (phone, online, email and in-person contact; phone menu includes password and student system access options; page last updated 2 June 2026)

Western Sydney University:
- https://www.westernsydney.edu.au/information-technology-services/servicedesk (MyIT portal with knowledge base and ticket tracking; unresolved calls logged to specialised teams; some guides migrated and some still at old locations)

Findings:
- Password/login help is prominent at all three universities reviewed.
- At Torrens, a single Microsoft 365 login is used for email, the learning platform, the Student Portal and the library, so one login problem affects several systems.
- Torrens guides cover password reset, MFA, email setup and app installation; the fallback when self-service fails is contacting Student Services or Student Support.
- Torrens portal guides include a glossary of renamed terms, suggesting terminology confusion is a known issue.
- Western Sydney combines a knowledge base, issue logging and ticket tracking, which matches this project's planned structure (answer from guides, escalate to a ticket, track status).
- Western Sydney notes that some guides have not yet been migrated, and the Torrens MFA FAQ contains some apparently dated terminology; both are examples of duplicated or outdated guidance risk.
- Wi-Fi and printing were not mentioned on the pages reviewed from the Sydney and Western Sydney sites, and the Torrens IT page was not reviewed in detail. These topics rest on the public helpdesk sources.
- Complaints links were not found on the Torrens pages reviewed and are not used as evidence.

Used for: supporting password/login/MFA and software installation topics, and the escalate-to-human and ticket-tracking pattern.

Reviewed but not used:
- https://students.torrensonline.com/faq (a separate short-course platform, not the student helpdesk)

**Interview: uni student-support staff member, Torrens University** [verified: interview, 1 person]
- Top requests were subject selection, learning platform navigation, portal access and graduation confirmation, mostly student administration, not IT.
- When a question can't be answered, staff follow policy and guidelines, escalate harder cases to a higher department, and reply to the student later by email.
- Used for: the escalation and ticket workflow. It does not validate the five IT topics.

**Own experience** [own experience]
- Fixed-option chatbots on consumer services that loop without resolving the problem.
- A phone call where the bot understood the problem but never connected me to a human (failed handoff).
- University help pages with limited options, where staff also struggled to find the right guide.

**Limitations of the evidence**
- A corporate employee interview was not completed at the time of writing. Workplace framing rests on public helpdesk sources, university IT pages and one interview with university student-support staff.
- Real company IT procedures are confidential, so the knowledge base uses original demonstration guides for a fictional organisation.

**Pending evidence**
- Employee interview (corporate or office setting): pending. To be completed if a suitable person can be found. Questions: most common IT problems, repeated requests, how guidance is found, how unresolved requests are passed on and tracked, and what an automated assistant should never do. Findings will be compared with the five chosen topics and the scope will be revised if they differ.

## 7. Future work
- AI-guided onboarding tour of systems for new students and employees
- Detection of sensitive data (for example, passwords) typed into the question box
