# Contributing

Magyarul: [CONTRIBUTING.hu.md](CONTRIBUTING.hu.md)

This catalogue publishes open agricultural tool designs that people can actually build. Contributions go through GitHub only: an issue form or a pull request. There is no e-mail or web-form intake, and every entry is reviewed by the maintainer before it is merged.

## What you can contribute

1. **A new design** you made or maintain: files (or a link to where they live), a description, a photo of the real thing, its stage and its limitations.
2. **A fix to an existing design**: a better translation, a corrected limitation, a stage update with evidence, a new version of the files, a replacement photo.
3. **A build report**: you built a listed design; tell us when, what version, what happened, with a photo.

Platform code (the website) is not in this repository.

## Three ways in

| You | Do this |
|---|---|
| Have the files and a GitHub account, do not want to write JSON | Open a [new design issue](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml). One language is enough; the reviewer adds the other and prepares the pull request. |
| Comfortable with git | Fork, add `projects/<id>/` as described in [SUBMITTING.md](SUBMITTING.md), run `npm ci && npm run validate`, open a pull request. |
| Built a listed design | File a [build report](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=build-report.yml). |

For a fix to an existing design, either open a [fix issue](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=fix-design.yml) or edit the project directory in a pull request.

## What a design needs

- **Rights.** You hold the rights to the files, text and photos, or they are already under a licence that allows this publication.
- **Licence, stated per file group.** For example `source/` under MIT and everything else under CC BY-SA 4.0. The default for simple designs is CC BY-SA 4.0.
- **Both languages** for title, description, limitations and photo alt text. If you only write one, say so in the issue and the reviewer translates; in a pull request both are required.
- **Honest stage.** `concept` (not built), `prototype` (built once, not in use), `built` (works, in use by the author), `field-tested` (in real use, reported). `built` and `field-tested` need a real photo of the real object.
- **Limitations that a builder needs to know**, including safety: what is untested, what it must not be made of, what it cannot do.
- **A real photo** of the object, taken by you or with permission. No stock or generated imagery.
- **Files under 20 MB each.** Larger files go on a mirror (Printables, your repository) linked from `project.json`.

## Review

The maintainer checks every pull request against this list before merging:

- rights and licence are explicit and match the files;
- HU and EN say the same thing;
- limitations are honest and include safety notes;
- the stage claim is supported (photo, lab note, build report);
- the photo is real and has a provenance sidecar;
- `npm run validate` passes in CI.

A merged entry appears on the website after the next platform deployment, usually within a day.

## Licences of your contribution

By submitting, you agree that the catalogue metadata, documentation and photos you add are published under [CC BY-SA 4.0](LICENSE), and that your design files are published under the licences you state in `project.json`. Scripts in this repository are under [MIT](LICENSE-MIT).
