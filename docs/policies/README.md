# Starter Policy Documents

These are the policy documents for the AI Architect customer support agent.

They describe a fictional e-commerce store called Northstar Outfitters.
The company sells everyday travel, home, and lifestyle products online.
The store is deliberately ordinary so students do not need domain expertise to understand the policies or ask useful questions.

The support agent should answer customer questions using only these approved documents.
When a question cannot be answered from these documents, the message should be labelled `Human Needed`.

## Files

- `refund-policy.md`: returns, exchanges, store credit, refund timing, return shipping, and edge cases.
- `shipping-policy.md`: processing times, delivery regions, shipping speeds, tracking, lost packages, address changes, and split shipments.
- `opening-hours.md`: support hours, response times, weekend coverage, holidays, and time zones.
- `warranty-policy.md`: warranty length, covered defects, exclusions, claim evidence, remedies, and refurbished replacements.
- `account-policy.md`: account creation, password resets, guest checkout, order history, saved addresses, deletion, and support identity checks.
- `privacy-policy.md`: collected data, payment data, service providers, retention, deletion requests, marketing preferences, and security.

## Teaching Notes

These docs are intentionally more detailed than tiny demo snippets, but still small enough to inspect in a lesson.

They are good starter material for:

- document loading tests
- source attribution tests
- unsupported-answer behaviour
- off-topic refusal behaviour
- Gmail label smoke checks after deployment

The docs include overlapping topics on purpose.
For example, a question about a faulty returned item may involve both `refund-policy.md` and `warranty-policy.md`.
A question about account deletion may involve both `account-policy.md` and `privacy-policy.md`.

Students can edit these files later in the course, then run the ingest command to update Postgres.

## Example Questions

- Can I return an opened item?
- How long does standard shipping take to Canada?
- When is customer support open?
- My order tracking has not updated for a week. What should I do?
- What does the warranty cover?
- Can I delete my account and all my data?
- Do you store my full card number?
- Can I get a refund for a final sale item?
- Can support tell me my password?
