## Welcome to Better Code

This is the development home of the STLab Better Code course.

Please see the [latest published draft](https://stlab.github.io/better-code/)
for information about the motivation for this project.

### Infrastructure

The reference is developed as a [Jekyll](https://jekyllrb.com) website,
currently being served by [GitHub Pages](https://pages.github.com).

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
