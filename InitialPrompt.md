I am preparing solution for AI Hackathon.
Hackathon challenge and Requirements are detailed in Requirements.md
I want you to understand the Requirements in details - The Problem, Why This Matters Now, The Opportunity, Constraints , Questions Worth Considering, What Would Blow My Mind
I want you to generate Backend Solution implementation plan phase by phase.
I want to review Implementation plan and modify before starting implementation, do not start coding now.

Could you refer the following concept and expand the implementation plan.

Implementation Plan should consider the following functional, technical, design , coding standards
I want to use Python, FastAPI, SQLite, LangGraph for Agent Orchestration for backend implementation
User proper Project Structure for production ready ( backend, frontend folder separately, we will implement frontend later)
I want you to follow clean code architecture, modularity, secure code, linting standard, logging (loguru), exception handling
log should contain unique request id (UUID), timestamp, source file (line) , message
I want you to generate and return unique error code for each and every exception ( ex : AML0001, AML0002)
Use .env and settings for configuring business variation values like deposit threshold, negligible profit/loss trade
Every API should contain standard header parameters : UUID, X_Forward_For ( Customer IP), X_Device_Id
Create separate Controller for each module ( Customers, Accounts, Transactions, Alerts, Cases) and group related apis

Create following Agents
AML Analyst as Master Agent
Sub Agents:
Behavioral Analyst
Network Analyst
Contextual Scorer
Evidence Collector
False Positve Optimizer
Document Content Generator

Create following tables
Organizations,Users,Customers, Accounts, Transactions, High Risk Account, Alerts, Cases, Case Document Content, Case Decisions and refer DatabaseModel.md for table schema reference, strictly follow the schema and use exact name for all columns

Create following user types
Compliance Manager, Admin in Users table

Functional Requirement
Customer Transactions can be simulated from UI for different scenarios ( ex: high amount deposit, negligible profit/loss trade) - we can focus on AML Transaction monitoring system rathen than focussing on Transactions module, Lets create api for simulating customer transactions, we will generate UI later.
Customer should also be able to initiate transactions manually using the same api for demo purpose.
Transaction should be analyzed and account might be flagged as High Risk Account ( high amount deposit, negligible profit trade )
Every Transaction should be analyzed by pre defined AML Rules and alerts should be generated - this should be scynchronous and transactions should be hold if alert is created, proceed if no alerts.
Alert should also be created if Account is part of High Risk Account table

Every Alert should be analyzed by AML Analyst as Master Agent along with sub agents and create Case for each alerts ( False Positive, Positive-Low Confidence, Positive-Medium Confidence, Postieve-High Confidence)
Each sub agent output should be stored in Cases table for specific Case Id and Document Content Generator should save the content in Case Document Content table and this content can be used for generating SAR document for Positive Cases)

Compliance Manager login, review cases and take action ( Accept, Reject , Generate SAR Document)
Compliance Manager decisions should be captured in Case Decisions table for each Case Id.

