# Welcome to Better Code

This is the development home of the STLab Better Code course.

## Working with the Book

We're migrating from using Jekyll to using
[mdBook](https://github.com/rust-lang/mdBook). The mdBook version is located in
the `./better-code` directory and includes automated CI/CD deployment to GitHub Pages.

The published book is available at: https://stlab.github.io/better-code/

## Prerequisites

Install [Rust and Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html):

**Linux and macOS:**
```bash
curl https://sh.rustup.rs -sSf | sh
```

**Windows:**
Download the installer from [here](https://win.rustup.rs/).

## Installing mdBook and Plugins

**Important**: To ensure consistency between local development and CI, all tool
versions are centrally managed in `versions.toml`. Use the provided installation
scripts to automatically install the correct versions:

**Linux/macOS:**
```bash
./scripts/install-tools.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\install-tools.ps1
```

These scripts automatically install mdBook and all required plugins using the
versions specified in `versions.toml`. This is the same file used by CI, ensuring
perfect consistency.

**Manual Installation:**
If you prefer to install manually, check `versions.toml` for the current version
numbers, then run:
```bash
cargo install mdbook --version <version-from-toml>
cargo install mdbook-katex --version <version-from-toml>
```

## Building and Serving the Book

To build and serve the book locally with live reload:

```bash
mdbook serve ./better-code
```

This will start a local server at http://localhost:3000. You can use the
Simple Browser in VSCode/Cursor to view the book while editing.

To build the book without serving:

```bash
mdbook build ./better-code
```

The built book will be in the `./better-code/book/` directory.

## Adding and Editing Content

1. Edit existing chapters in `better-code/src/`
2. Add new chapters by creating new `.md` files in `better-code/src/`
3. Update `better-code/src/SUMMARY.md` to include new chapters in the table of contents
4. The book will automatically rebuild and redeploy when you push changes to the main branch

### Content Conventions

* Avoid unnecessary HTML tags; use Markdown formatting to the degree possible.
* Wrap lines at 80 columns to support diff-friendly change tracking.
* Each chapter begins with a 2nd-level heading, e.g. `## Chapter Name`. All
  other headings in a chapter are 3rd-level and below.
* Maintain stable file names and heading titles for linkability until another
  solution is in place.

## Automated Deployment

The mdBook is automatically built and deployed to GitHub Pages using GitHub Actions.
When you push changes to the main branch:

1. GitHub Actions builds the book using mdBook with versions from `versions.toml`
2. The built book is deployed to GitHub Pages
3. The book becomes available at https://stlab.github.io/better-code/

No manual deployment steps are required!

## Dependency Management

All tool versions (mdBook, plugins, and future tools like Swift) are managed in
`versions.toml` at the repository root. To update a version:

1. Edit the version number in `versions.toml`
2. Run the appropriate install script to update locally
3. Test your changes
4. Commit - CI will automatically use the new version

## Legacy Jekyll Content

The legacy Jekyll files remain in the `archive/` directory for reference during
the transition. You can ignore these unless you're working on the migration.

**Running the Jekyll version (for reference only):**

If you need to run the legacy Jekyll site:

```bash
bundle exec jekyll serve -l
```

This will start a server at http://localhost:4000.

Alternatively, if you have [docker-compose](https://docs.docker.com/compose/):

```bash
docker-compose up
```
