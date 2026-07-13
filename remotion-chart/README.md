# Event-driven architecture diagram

A minimal 1920 by 1080 Remotion composition showing this flow:

`Event → API → Database + Queue → Worker`

## Commands

Install dependencies:

```console
npm install
```

Open Remotion Studio:

```console
npm run dev
```

Render the composition:

```console
npx remotion render EventDrivenSystem out/event-driven-system.mp4
```

Run lint and type checks:

```console
npm run lint
```

The title is editable through the composition's default props in
`src/Composition.tsx`.
