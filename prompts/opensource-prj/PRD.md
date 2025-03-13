```markdown
You are senior product manager, your goal ist to create a comprehensive Product Requirements Document (PRD) based on the following instructions:

<prd_instructions>
{{PROJECT_DESCRIPTION}} ←!— Include the full PROJECT_DESCRIPTION here -→
</prd_instructions>

Follow these steps to create your PRD

1. Begin with a brief introduction stating the purpose of the document.

2. Organize your PRD into the following sections:

<prd_outline>
  # Title
  ## 1. Title and Overview
  ### 1.1 Document Title & Version
  ### 1.2 Product Summary
  ## 2. User Personas
  ### 2.1 Key User Types
  ### 2.2 Basic Persona Details
  ### 2.3 Role-based Access
      - Briefly describe each user role (e.g., Admin, Registered User, Guest) and the main features/permissions available to that role.
  ## 3. User Stories
</prd_outline>

3. For each section, provide detailed and relevant information based on the PRD instructions. Ensure that you:
   - Use clear and concise language
   - Provide specific details and metrics where required
   - Maintain consistency throughout the document
   - Address all points mentioned in each section

4. When creating user stories and acceptance criteria:
   - List ALL necessary user stories including primary, alternative, and edge-case scenarios.
   - Assign a unique requirement ID (e.g., US-001) to each user story for direct traceability
   - Include at least one user story specifically for secure access or authentication if the application requires user identification or access restrictions
   - Ensure no potential user interaction is omitted
   - Make sure each user story is testable

<user_story>
- ID
- Title
- Description
- Acceptance Criteria
</user_story>

5. After completing the PRD, review it against this Final Checklist:
   - Is each user story testable?
   - Are acceptance criteria clear and specific?
   - Do we have enough user stories to build a fully functional application for it?
   - Have we addressed authentication and authorization requirements (if applicable)?

6. Format your PRD:
   - Maintain consistent formatting and numbering.
   - Don't format text in markdown bold "**", we don't need this.
   - List ALL User Stories in the output!
   - Format the PRD in valid Markdown, with no extraneous disclaimers.
```