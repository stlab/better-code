# Better Code

Development repository for the STLab Better Code course.

**Read the book:** https://stlab.github.io/better-code/

## Quick Start

### 1. Install Prerequisites

Install [Rust and Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html).


### 2. Install mdBook and Plugins

**Linux/macOS:**
```bash
./scripts/install-tools.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\install-tools.ps1
```

These scripts install mdBook and all required plugins using versions from `versions.txt`.

### 3. Build and Serve

```bash
mdbook serve ./better-code
```

Open http://localhost:3000 in your browser.

## Contributing

### Editing Content

1. Edit markdown files in `better-code/src/`
2. Add new chapters by creating `.md` files and updating `better-code/src/SUMMARY.md`
3. Changes automatically rebuild when you push to the main branch

### Content Conventions

* Use Markdown formatting; avoid unnecessary HTML
* Wrap lines at 80 columns for diff-friendly change tracking
* Start each chapter with a level-2 heading (`## Chapter Name`)
* Use level-3+ headings within chapters
* Keep file names and heading titles stable for linkability

## Deployment

### CI/CD Pipeline

**Pull Requests:**
- Validates build on Ubuntu and Windows
- No deployment; PR check shows build status

**Main Branch:**
- Builds HTML only (no swift-test) using mdBook with versions from `versions.txt`
- Deploys to GitHub Pages
- Available at https://stlab.github.io/better-code/

### Managing Dependencies

All tool versions are centrally managed in `versions.txt`. To update:

1. Edit version number in `versions.txt`
2. Run the appropriate install script locally
3. Test with `mdbook serve ./better-code`
4. Commit - CI automatically uses the new version

## Project Structure

```
better-code/          # mdBook source and configuration
├── src/             # Markdown chapter files
├── book.toml        # mdBook configuration
└── book/            # Generated output (gitignored)
    └── html/        # HTML when swift-test backend is enabled (PR/CI)

scripts/             # Installation scripts
├── install-tools.sh    # Linux/macOS
└── install-tools.ps1   # Windows

versions.txt         # Single source of truth for tool versions
archive/             # Legacy Jekyll site (for reference only)
```

## Advanced Usage


### Building Without Serving

```bash
mdbook build ./better-code
```

With all backends enabled (default), HTML is in `./better-code/book/html/`.
An HTML-only build (as on deploy) writes to `./better-code/book/`.


## Legacy Content

The `archive/` directory contains the legacy Jekyll site for reference during migration.
You can safely ignore it unless working on migration tasks.

To run the Jekyll version (not recommended for regular development):

```bash
bundle exec jekyll serve -l  # Starts server at http://localhost:4000
```

Or with Docker:

```bash
docker-compose up
```
