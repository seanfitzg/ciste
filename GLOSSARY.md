# Ciste Support

Customer support for Ciste, a fictional Irish neobank: customers chat with an agent that can explain fees, act on their cards, refund fees and open disputes, within bank policy.

## Language

### Customers and money

**Customer**:
A person who banks with Ciste and holds exactly one Account.
_Avoid_: User, client, account holder

**Account**:
The single current account a Customer holds, identified by one IBAN.
_Avoid_: Wallet, profile

**Card**:
A payment card issued against an Account; an Account has two or three.

**Masked**:
The only form in which an IBAN or card number may be shown: every character hidden except the last four.
_Avoid_: Redacted, obfuscated, hidden

**Freeze**:
A reversible block on one Card that stops new Transactions until the Card is unfrozen.
_Avoid_: Block, cancel, lock

**Tier**:
The service level of a Customer, either retail or premium; it belongs to the Customer, not the Account.
_Avoid_: Plan, level, segment

**Transaction**:
A movement of money on an Account, either a merchant charge or a Fee.
_Avoid_: Payment, entry

**Fee**:
A charge Ciste itself applies to an Account under a section of the Fees and Terms.
_Avoid_: Charge (when it means a merchant charge)

**Merchant charge**:
A Transaction raised by a third-party merchant, not by Ciste.

### Remedies

**Refund**:
Ciste reversing one of its own Fees back to the Customer's Account; never applies to a Merchant charge.
_Avoid_: Credit, reimbursement, chargeback

**Refund cap**:
The largest amount a single Refund may be for a given Tier: €50 retail, €150 premium; a Fee can be refunded at most once.
_Avoid_: Refund limit, allowance

**Reviewer**:
A Ciste staff member who approves, edits or rejects a proposed Refund before it is issued; only Refunds within the Refund cap ever reach a Reviewer.
_Avoid_: Approver, admin, operator

### Conversations

**Conversation**:
One continuous chat between a Customer and Ciste support, from first message until the Customer leaves or it is Escalated.
_Avoid_: Session, chat, ticket

**Escalation**:
A handoff of a Conversation to a human support person; once Escalated, the Conversation accepts no further messages.
_Avoid_: Ticket, transfer, handover

### Consent

**Approval**:
A Reviewer's decision (approve, edit or reject) on a proposed Refund.
_Avoid_: Confirmation, sign-off

**Confirmation**:
A Customer's explicit yes or no before a Card is frozen or unfrozen.
_Avoid_: Approval, consent

**Dispute**:
A Customer's formal challenge to a Merchant charge, investigated by Ciste and possibly pursued with the merchant.
_Avoid_: Complaint, claim, refund request

**Dispute Report**:
The structured findings of a Dispute investigation: the Merchant charge in question, a reason code, an evidence summary and a recommendation. It is internal to Ciste; the Customer only ever sees the Dispute reference.
_Avoid_: Case file, dispute summary

**Dispute reference**:
The identifier (such as D-0042) a Customer is given when a Dispute is opened.
_Avoid_: Case number, ticket number
