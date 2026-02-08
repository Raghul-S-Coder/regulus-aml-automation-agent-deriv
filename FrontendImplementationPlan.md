# RegulusAI Frontend Implementation Plan (React + TypeScript + Tailwind + shadcn/ui)

## Goals
1. Build a clean, production-like UI for RegulusAI that aligns with the AML requirements.
2. Provide separate, well-defined routes for each page.
3. Enable public demo flows (Transaction Demo) and authenticated flows (Monitoring).
4. Keep the UI modular and ready to integrate with the backend API.

## Route Map
1. `/regulus` (Home)
2. `/regulus/login` (Login)
3. `/regulus/transaction-demo` (Public Transaction Demo)
4. `/regulus/monitoring` (Protected shell with sidebar)
5. `/regulus/monitoring/dashboard`
6. `/regulus/monitoring/transactions`
7. `/regulus/monitoring/alerts`
8. `/regulus/monitoring/cases`
9. `/regulus/monitoring/cases/:caseId`

## UI Stack
1. React + TypeScript (Vite)
2. Tailwind CSS
3. shadcn/ui components (Button, Card, Tabs, Table, Input, Select, Dialog, Badge, Breadcrumb, Sheet)
4. Recharts (for dashboard charts)
5. React Router
6. TanStack Query (data fetching and caching)

## Branding and Theme System (Emerald)
**Primary Direction**
1. Emerald-first palette for all interactive UI elements (buttons, links, focus rings, badges, charts).
2. Light and dark theme supported via `class` strategy on `html`.

**Tailwind Design Tokens (Plan-Level)**
1. Add CSS variables in `globals.css` for both themes: `--brand`, `--brand-foreground`, `--surface`, `--surface-2`, `--border`, `--text`, `--text-muted`.
2. Map Tailwind colors to tokens in `tailwind.config.ts` under `theme.extend.colors`.
3. Set shadcn/ui `primary` to emerald tokens.

**Theme Toggle**
1. Add a `ThemeToggle` component to `PublicLayout` and `MonitoringLayout`.
2. Persist theme in `localStorage` and respect system preference on first load.

## Phase 1: Project Setup and Base Structure
**Scope**
1. Initialize `frontend` with Vite React + TS.
2. Add Tailwind and shadcn/ui.
3. Configure absolute imports and shared UI styles, including emerald branding tokens.
4. Establish route scaffolding.

**Deliverables**
1. `frontend/src/app` folder with `routes`, `pages`, `components`, `layouts`, `hooks`, `api`.
2. Base `App.tsx` with route switch.
3. Tailwind config with emerald-first design tokens (light + dark).

**Acceptance Criteria**
1. App loads with `/regulus` as default route.
2. Tailwind styles applied.
3. shadcn/ui components render correctly.
4. Light and dark theme both render with emerald as primary color.

## Phase 2: Global Layouts and Navigation
**Scope**
1. Public layout for Home, Login, Transaction Demo.
2. Protected layout for Monitoring (sidebar + top bar + content).
3. Navigation links between Home, Login, Transaction Demo, Monitoring.
4. Theme toggle placement in top bar and public header.

**Deliverables**
1. `PublicLayout` with header and footer slots.
2. `MonitoringLayout` with sidebar, breadcrumbs, and home link.
3. Centralized route config and auth guard placeholder.
4. `ThemeToggle` component and theme persistence hook.

**Acceptance Criteria**
1. Sidebar renders only under `/regulus/monitoring/*`.
2. Navigation is consistent across routes.
3. Theme toggle switches between light and dark without layout shifts.

## Phase 3: Home Page `/regulus`
**Scope**
1. Hero with pain points for compliance teams and RegulusAI solution.
2. Graphic or animation on right: workflow from Transactions → Alerts → AI Analyst → Cases → Compliance Manager.
3. Features section, How to Use section, Footer.
4. Apply emerald branding to primary CTAs, highlights, and workflow nodes.

**Deliverables**
1. `HomePage` with sections and CTA buttons.
2. Simple animation using CSS keyframes or SVG transitions.
3. Visual workflow component.

**Acceptance Criteria**
1. Hero communicates the compliance team pain and solution clearly.
2. Workflow visual is visible on the right side of the hero.
3. CTA routes to Login and Transaction Demo.

## Phase 4: Login Page `/regulus/login`
**Scope**
1. Simple login form for Compliance Manager.
2. Client-side validation.
3. Stub auth flow (local state or mock token).
4. Emerald branded primary button and focus states.

**Deliverables**
1. `LoginPage` with username/password inputs and submit button.
2. Mock `authService` returning a token.
3. Redirect to `/regulus/monitoring` after login.

**Acceptance Criteria**
1. Form validates empty fields.
2. Successful login routes to Monitoring shell.

## Phase 5: Transaction Demo `/regulus/transaction-demo`
**Scope**
1. Public access, no auth required.
2. Form to select customer and scenario.
3. Form to manually enter transaction.
4. Emerald-themed tab indicator and primary action buttons.

**Deliverables**
1. `TransactionDemoPage` with tabs for "Scenario" and "Manual".
2. Customer selector, scenario selector, amount/currency/type fields.
3. Submit action calls simulation or transaction endpoint.

**API Mapping**
1. `GET /api/v1/customers`
2. `GET /api/v1/simulate/scenarios`
3. `POST /api/v1/simulate/scenario`
4. `POST /api/v1/transactions`

**Acceptance Criteria**
1. Demo works without login.
2. Forms validate required fields.
3. Submission shows success or error toast.

## Phase 6: Monitoring Shell `/regulus/monitoring`
**Scope**
1. Sidebar links for Dashboard, Transactions, Alerts, Cases.
2. Top bar with user info and logout.
3. Emerald active state for nav items and badges.

**Deliverables**
1. `MonitoringLayout` with sidebar items and route outlet.
2. Protected routes via auth guard.

**Acceptance Criteria**
1. Non-authenticated users are redirected to `/regulus/login`.
2. Sidebar has link back to Home.

## Phase 7: Dashboard `/regulus/monitoring/dashboard`
**Scope**
1. KPI cards: transactions today, alerts today, false positives, high confidence cases.
2. Trend charts for transactions, alerts, cases.
3. Emerald highlight for positive metrics and chart accents.

**Deliverables**
1. `DashboardPage` with KPI cards and charts.
2. Data adapters for dashboard metrics.

**API Mapping**
1. `GET /api/v1/transactions?date=today`
2. `GET /api/v1/alerts?date=today`
3. `GET /api/v1/cases?status=OPEN`

**Acceptance Criteria**
1. KPIs show aggregated values.
2. Charts render trend data.

## Phase 8: Transactions List `/regulus/monitoring/transactions`
**Scope**
1. Filterable list with status, type, amount range, date range.
2. Paginated table.
3. Emerald accents for filters and active states.

**Deliverables**
1. `TransactionsPage` with filters and table.
2. Reusable `DataTable` component.

**API Mapping**
1. `GET /api/v1/transactions`

**Acceptance Criteria**
1. Filters update query and refresh results.

## Phase 9: Alerts List `/regulus/monitoring/alerts`
**Scope**
1. Filter by severity, rule, date range.
2. Paginated table.
3. Emerald accents for filtering controls and selected rows.

**Deliverables**
1. `AlertsPage` with filters and table.

**API Mapping**
1. `GET /api/v1/alerts`

**Acceptance Criteria**
1. Filters update list correctly.

## Phase 10: Cases List and Case Details
**Scope**
1. Cases list with status filter.
2. Case row opens Case Details page.
3. Case Details allow decision and document generation.
4. Emerald emphasis for decision actions and case status chips.

**Deliverables**
1. `CasesPage` table and filters.
2. `CaseDetailsPage` with summary, agent scores, and documents.
3. Decision modal (Accept/Reject) with reason.
4. "Generate Document" action and viewer.

**API Mapping**
1. `GET /api/v1/cases`
2. `GET /api/v1/cases/:caseId`
3. `POST /api/v1/cases/:caseId/decisions`
4. `POST /api/v1/cases/:caseId/generate-sar`
5. `GET /api/v1/cases/:caseId/documents`

**Acceptance Criteria**
1. Clicking a case row navigates to details.
2. Decisions and document generation update UI state.

## Phase 11: Shared UI Components and Visual Polish
**Scope**
1. Create reusable cards, tables, badges, filters, and empty states.
2. Add consistent loading and error states.
3. Enhance hero animation and dashboard micro-interactions.
4. Apply emerald color rules consistently across components.

**Deliverables**
1. `components/ui` wrappers for shadcn/ui.
2. `LoadingState`, `ErrorState`, `EmptyState`.
3. `WorkflowGraphic` component for hero.
4. `theme.ts` or `useTheme` hook for light/dark mode.

**Acceptance Criteria**
1. UI looks consistent and polished.
2. All pages handle loading, error, and empty states.
3. Emerald branding is applied to all primary and interactive elements.
4. Light and dark modes are visually coherent.

## Phase 12: Integration and QA
**Scope**
1. Connect all pages to backend endpoints.
2. Validate auth guard behavior.
3. Confirm routes and data flow.

**Deliverables**
1. `api/client.ts` with base URL and headers.
2. `hooks` for data fetching.
3. QA checklist and bug fixes.

**Acceptance Criteria**
1. All routes render without errors.
2. API calls work with real backend.
3. Public and protected routes behave correctly.

## Data and State Notes
1. Use TanStack Query for caching and pagination.
2. Centralize filters in URL query params for shareable views.
3. Use local storage for auth token (mock or real).

## Non-Functional Requirements
1. Responsive design for desktop and tablet.
2. Accessibility basics: labels, focus states, contrast.
3. Consistent typography and spacing scale.
