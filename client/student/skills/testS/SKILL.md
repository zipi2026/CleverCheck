---
name: testS
description: Coordinates the agents involved in building a student test component that loads questions from the server and supports closed and open answers.
---

# testS Skill

Use this skill when you need to build or extend a student test experience that pulls questions from the server and renders both closed and open questions.

## Goal
Create a student-facing test component flow that:
- loads test data from the server
- presents closed questions and open questions appropriately
- supports student answer input
- works as part of the broader CleverCheck student app

## Role of the coordinator
You are currently responsible for creating the student test component and for activating the agents under you to complete the work. You must manage the overall implementation until the component is fully built and integrated.

If you encounter any uncertainty, ambiguity, or missing information, ask the user for clarification instead of making unsupported assumptions.

## Workflow
1. Understand the test requirements.
   - Identify whether the component is for a single test, a test list, or a full exam flow.
   - Clarify the question types that must be supported.

2. Inspect the relevant backend contract.
   - Check the server-side controllers and data sources that provide test and question data.
   - Determine how questions are fetched and what fields are available.

3. Choose the right agents for the work.
   - Use the model-building agent for client-side data structures.
   - Use the UI/design agent for the component layout and student experience.
   - Use the routing agent if a new screen or navigation path is needed.
   - Use the API agent if server-to-server or backend integration logic is required.

4. Build the student test component.
   - Create or update the component for displaying the test.
   - Render closed questions using appropriate selectors or choices.
   - Render open questions using text input or free-response fields.
   - Connect the component to the data source from the server.

5. Ensure the flow is coherent.
   - Make sure the component handles loading, empty states, and submission behavior.
   - Keep the experience simple and student-friendly.
   - Preserve consistent naming and structure.

6. Validate the result.
   - Confirm the component uses the expected data from the server.
   - Check that question types are displayed correctly.
   - Ensure the flow is ready for integration with the wider app.

## Quality criteria
- The student can see the test questions from the server.
- Closed and open questions are rendered correctly.
- The component is easy to use and understandable.
- The implementation is consistent with the existing app architecture.

## When to use this skill
Use this skill for:
- building a student test screen
- connecting exam question data from the server to the client
- creating a test-taking experience with mixed question types
- coordinating multiple agents for a larger frontend feature
