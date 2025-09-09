# Problem to solve

When designing functionalities in a software product, the product manager spends
considerable time refining the problem and splitting it into tasks that are
feasible for developers.

This takes time and corners are sometimes cut to maintain time-to-market.
A agentic workflow refining an idea to a set of requirements and tasks will
enable faster development and ultimately ttm.

# Proposed solution

A series of agents, each with a specific role and set of tools, that emulate the
collaboration that happens in a product team normally.

The agents are:
- **Product Manager**: Acting as the overall product lead, responsible for discovering areas of opportunity for customers and users, and framing them in actionable product areas. Ultimately responsible for the value and viability of the product.
- **Engineering Manager**: Acting as the technical lead, responsible for evaluating and designing solutions that will be feasible and cost-effective.
- **Product Designer**: Acting as the visual lead, responsible for creating an experience that is intuitively usable.
- **Functional Analyst**: Acting as the right-hand of the product and engineering manager, responsible for breaking down solutions into functional increments (tasks).
- **Scrum Master**: Acting as the process guardian, responsible for team velocity and ensuring that each initiative document is broken down into manageable tasks.
- **Market Analyst**: Responsible for market research and deep analysis of available information through desk research. Also knows when data is missing and how to acquire it (e.g., qualitative research, interviews, surveys, etc.).

# Acceptance criteria
Each agent has a set of tools that they use to accomplish their role.
Each agent is clearly defined as per best-practices and has a clear purpose.
There is a feedback loop between agents with clear exit criteria (maximum 5 iterations of the full loop per pid).

