I want you to generate frontend implementation plan .md file - phase by phase using ReactJs, Typescript, Tailwind, Shacdn/ui Could you review and understand Requirements.md and ImplementationPlan.md and consider following concepts for implementation plan

Generate following Pages and separate path route for each page
Home Page
default route /regulus, should contain Product name : RegulusAI, navigation, Hero section , Features, How to Use, Footer
Hero section should highlight Pain faced by Compliance team and captions to explain our solution
Hero section should include simple graphic or animation on right side to show complete workflow from transactions to alerts to AI Analyst to cases to Complaince Manager( Human)
Home page should have route to following pages

Login Page

Transaction Page /regulus/transaction-demo
This should be publically accessible without any login
I should be able to select a customer , simulation scenario and initiate a transaction
I should be able to select a customer and manually enter and initiate transaction

Transaction Monitoring - Regulus AI product main page.
route should be /regulus/monitoring
This should be accessible by Compliance Manager after login and this is our product main page.
We should have following side menu options, option to return back to Home page.

1. Dashboard to show key metrics - number of transactions today, number of alerts today, number of false positive cases, number of high confidence cases and some graphs to show trends for transactions, alerts and cases.
2. Transactions to view List of Transactions and filter Transactions
3. Alerts to view List of Alerts and filter Alerts
4. Cases to view List of Cases and filter Cases. I should be able to view Case Details in new page by clicking on Case Row. Take Decisions by selecting Case Id, Generate Document in Case Details page
