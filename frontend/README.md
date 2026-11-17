# PDF RAG Assistant - Frontend

Next.js interface for the RAG backend.

## Development environment

```powershell
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

The frontend expects the FastAPI backend to run at `http://localhost:8000`.

## Commands

```powershell
npm run dev
npm run build
npm run start
npm run lint
```

## Components

- `src/app/page.tsx` - page state and backend request
- `src/components/sidebar.tsx` - sidebar
- `src/components/chat-messages.tsx` - message list
- `src/components/chat-input.tsx` - question input
- `src/components/chat-types.ts` - message types
- `src/styles/chat.module.css` - page CSS module

Project installation and startup instructions are available in the [project README](../README.md).
