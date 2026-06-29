# AI Agent Guidance for CleverCheck Client

This repository is a React + TypeScript + Vite frontend app. There is currently no backend code in this workspace, so server-call responsibilities should be implemented in the client layer.

## Primary agent role
- You are responsible for managing server calls.
- Keep network logic isolated from UI components.
- Create or update a dedicated API/service layer under `src/` (for example, `src/api/`, `src/services/`, or `src/lib/`).
- Prefer typed request and response interfaces for all API calls.
- Avoid hardcoding endpoints in components.
- Use `import.meta.env` for environment-specific server URLs.

## Code style and architecture
- The app currently uses React with TypeScript and Vite.
- Keep component files focused on rendering and state; move fetch logic into custom hooks or service modules.
- If you add a new API module, export functions like `getX`, `postY`, or `apiClient` for reuse.
- Use `fetch` or a small abstraction rather than adding a heavy HTTP library unless necessary.

## Scripts and validation
- Install dependencies: `npm install`
- Run dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`

## Notes for agents
- Inspect `src/App.tsx` and the rest of `src/` before changing anything; the current app is still a Vite starter template.
- When asked to work on server calls, create an API abstraction first, then wire it into components.
- If no server call patterns exist, scaffold a minimal API client and use it consistently across the app.
