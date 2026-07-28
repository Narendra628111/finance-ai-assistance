DOMAIN_PROMPT = """
You are a classifier.

Determine whether the following question is related to:

- Banking
- Finance
- Loans
- Insurance
- Investments
- RBI regulations
- Credit cards
- KYC
- Accounts
- Payments
- Taxes

Reply with ONLY one word.

finance
or

other

Question:
{question}
"""