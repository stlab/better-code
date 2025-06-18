# Welcome to Better Code

This is the development home of the STLab Better Code course.

## Working with the Book

We're migrating from using Jekyll to using
[mdBook](https://github.com/rust-lang/mdBook). The mdBook version is located in
the `./better-code` directory and includes automated CI/CD deployment to GitHub Pages.

## Installing and updating mdBook

Install [Rust and
Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html):

Linux and macOS:

```
curl https://sh.rustup.rs -sSf | sh
```

On Windows, you can download the installer from
[here](https://win.rustup.rs/).

Once you have Rust and Cargo installed, you can install or upgrade mdBook by running:

```
cargo install mdbook
```

## Building the book

To build the book, run:

```
mdbook serve ./better-code
```

Open the browser to http://localhost:3000 to see the book. You can use the
Simple Browser in VSCode/Cursor to view the book while editing.

## Automated Deployment

The mdBook is automatically built and deployed to GitHub Pages using GitHub Actions.
When you push changes to the main branch:

1. GitHub Actions will build the book using mdBook
2. The built book will be deployed to GitHub Pages
3. The book will be available at https://stlab.github.io/better-code/

No manual deployment steps are required!

### Conventions and Guidelines

* Avoid unnecessary HTML tags; use Markdown formatting to the degree possible.
* Wrap lines at 80 columns to support diff-friendly change tracking.
* Chapters are represented as individual Markdown files in the chapters/
  subdirectory.
* Each chapter begins with a 2nd-level heading, e.g. `## Chapter Name`.  All
  other headings in a chapter are 3rd-level and below.
* Each file's name starts with a 4-digit number that determines its order in the
  overall document.  Initial numbering is spaced by 100s.
* Maintain stable file names and heading titles for linkability until another
  solution is in place.

### Older draft

Please see the [latest published draft](https://stlab.github.io/better-code/)
for information about the motivation for this project.

### Infrastructure

The book is being migrated from [Jekyll](https://jekyllrb.com) to [mdBook](https://github.com/rust-lang/mdBook).
The new mdBook version is automatically built and deployed to [GitHub Pages](https://pages.github.com) using GitHub Actions.

The legacy Jekyll files remain in the root directory for reference during the transition.

### Running a local server

If you are able to install the necessary parts for jekyll,

```
bundle exec jekyll serve -l
```

will start a server for the site at http://localhost:4000.

Creating a complete installation of jekyll and all the parts needed for github
pages development can be fraught.  If you install
[docker-compose](https://docs.docker.com/compose/), you can start the server
by invoking

```
docker-compose up
```

in the root directory of your working copy.
