# RegulusAI Frontend QA Checklist

## Routing
1. `/regulus` loads Home page.
2. `/regulus/login` loads Login page.
3. `/regulus/transaction-demo` loads Transaction Demo.
4. `/regulus/monitoring/*` redirects to login when unauthenticated.
5. `/regulus/monitoring` loads Dashboard after login.

## Theme
1. Theme toggle switches light/dark.
2. Emerald color applied to primary buttons, active states, badges.

## Home
1. Hero copy matches compliance pain points.
2. Workflow graphic renders and animates.

## Transaction Demo
1. Scenario tab validates customer + scenario.
2. Manual tab validates amount, currency, type.

## Monitoring
1. Sidebar navigation works.
2. Back to Home link works.

## Lists
1. Filters change visible rows for Transactions, Alerts, Cases.
2. Empty state appears with no results.

## Case Details
1. Decision requires reason input.
2. Generate Document action shows status message.
