# Hen cap editor — prototype

Browser-testable prototype of the patron-facing cap editor from
`../docs/superpowers/specs/2026-09-14-hen-cap-customisation-design.md` §7.
It is written to be dropped into the chirp repository unchanged, so it renders
with chirp's own `@chirpcoop/real-chicken-ui` components and
`@chirpcoop/design-tokens`, aliased **from the chirp checkout's source** — the
chirp repository is read, never written. It landed in chirp on 2026-09-14
(see the integration map below): the live editor is chirp
`packages/real-chicken-ui/src/cap-editor/`, and this tree keeps the reference
prototype.

```sh
pnpm install
pnpm sync:data     # copies ../cad/catalog.json and ../cad/out/layout.json into src/cap-editor/data/
pnpm dev           # http://localhost:5173 with the in-memory mock client
pnpm test          # vitest + testing-library
pnpm typecheck
pnpm build
```

`CHIRP_DIR` sets the chirp checkout location. Set it to an absolute path
(`CHIRP_DIR=/path/to/chirp pnpm dev`): the default `../../chirp` dates from the
standalone repository and now resolves to `projects/holyiot-25008-enclosure/chirp`,
which does not exist, so `pnpm dev`, `test`, `typecheck` and `build` fail
without it. `tsconfig.json`'s `paths` also point at `../../chirp` and must be
edited to match; tsc cannot read env. Do not install or copy chirp packages
into this tree to work around a missing checkout.

## What it looks like

A three-step game — Palette → Motif → Colours — with the cap on stage and a
summary bar stuck to the bottom. Design decisions, the mobile integration
path and a reviewer checklist: [`DESIGN-NOTES.md`](DESIGN-NOTES.md).

## Rules the code already obeys

- Only `var(--rc-*)` and `@chirpcoop/design-tokens` values in TS/CSS; the
  only colour literals are the filament hexes in `data/catalog.json` (data).
- Deep imports only: `@chirpcoop/real-chicken-ui/components`, `/wallet-pill`,
  `/golden-grain`, `/theme-vars`, `/dialog-focus`, `/armed-confirm`,
  `/types`, `/styles.css`. Never `/client` or `/index`: they pull `@chirpcoop/client-sdk`
  and recharts in. In chirp these become relative imports inside the package.
- React 19, TypeScript strict, vitest + testing-library, English-only source;
  Hungarian only inside `src/copy/hu.ts`.

## Integration map (landed in chirp on 2026-09-14, PR Remeny-Farm/chirp#2409; kept for orientation)

| Prototype file | Landed in chirp as |
|---|---|
| `src/cap-editor/*.tsx`, `*.css`, `*.test.tsx` | `packages/real-chicken-ui/src/cap-editor/` |
| `src/copy/{hu,en}.ts` | `packages/real-chicken-ui/src/i18n/cap-editor-copy.ts`, plus `apps/web/messages/{en,hu}/320-hen-cap.json` |
| `src/cap-editor/types.ts` (`CapDesignClient`) + `mock-client.ts` | interface and mock in `packages/real-chicken-ui/src/cap-editor/`; SDK adapter in `packages/app-data/src/adapters/hen-cap.ts`, wired by `apps/web/lib/hen-cap-client.ts` |
| `src/page.tsx` | `apps/web/app/(patron)/account/cap/page.tsx`; mobile `packages/mobile-app/src/hen-cap/CapEditorScreen.tsx` |
| `src/cap-editor/data/layout.json` | `packages/real-chicken-ui/src/cap-editor/data/layout.json`; the catalog copy is `packages/shared-types/src/i18n/hen-cap-catalog.json` |

## Layout gate (manual, needs Playwright)

`pnpm test` runs in jsdom and cannot see geometry. `pnpm check:layout` drives a
real Chromium against a running dev server and fails on page-level horizontal
overflow on any step at 360 / 390 / 1200 px, on a rail that does not scroll
sideways on its own, on an arrow-focused tile left cut off at the rail edge,
and on any chip / tile / tab / card under 44 px. Playwright is not a
devDependency (browser download), so point `NODE_PATH` at an install that has
it:

```sh
pnpm dev                                          # terminal 1
NODE_PATH=/path/to/node_modules pnpm check:layout  # terminal 2
```

Run it before every UI change lands; the scoring reviewer checks the same
things.
