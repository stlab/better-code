# Better Code - mdBook

This directory contains the mdBook version of the Better Code course.

## Local Development

### Prerequisites

Install [Rust and Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html):

**Linux and macOS:**
```bash
curl https://sh.rustup.rs -sSf | sh
```

**Windows:**
Download the installer from [here](https://win.rustup.rs/).

### Install (or update) mdBook

```bash
cargo install mdbook
```

### Building and Serving the Book

To build and serve the book locally:

```bash
mdbook serve
```

This will start a local server at `http://localhost:3000`.

To just build the book without serving:

```bash
mdbook build
```

The built book will be in the `book/` directory.

## Deployment

The book is automatically built and deployed to GitHub Pages using GitHub Actions when changes are pushed to the main branch.

## Adding Content

1. Edit existing chapters in the `src/` directory
2. Add new chapters by creating new `.md` files in `src/`
3. Update `src/SUMMARY.md` to include new chapters in the table of contents
4. The book will automatically rebuild when you push changes to GitHub 
