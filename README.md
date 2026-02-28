<h1 align="center">
  ft_badges
</h1>

<h4 align="center">
  <img alt="42 Projects Count" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fairone01%2Fft_badges%2Frefs%2Fheads%2Fmain%2Fconfig.json&query=%24.project_count&style=flat-square&labelColor=020617&color=5a45fe&logo=42&label=Supported Projects">
  <img alt="The Unlicense license" src="https://img.shields.io/badge/License-Unlicense-ef00c7?style=flat-square&logo=unlicense&logoColor=fff&labelColor=020617">
  <img alt="Made with Python" src="https://img.shields.io/badge/Made_with-Python-ff2b89?style=flat-square&logo=python&logoColor=fff&labelColor=020617">
  <img alt="Repo size" src="https://img.shields.io/github/repo-size/airone01/ft_badges?style=flat-square&logo=svg&logoColor=fff&label=Repo%20Size&labelColor=020617&color=ff8059">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors-anon/airone01/ft_badges?style=flat-square&logo=github&labelColor=020617&color=ffc248&label=Contributors">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/airone01/ft_badges?style=flat-square&logo=github&labelColor=020617&color=f9f871&label=Last%20commit">
</h4>

<p align="center">
  <b>A dynamic, fully customizable SVG badge generator designed specifically for 42 School projects.</b><br>
  Show off your perfect 125% scores and add some beautiful, optimized vector flair to your GitHub profile READMEs!
</p>

## Documentation & Badge Catalog

**The easiest way to use ft_badges is to visit the documentation website!**

**[ft_badges Documentation](https://airone01.github.io/ft_badges/)**

There, you can browse a visual catalog of all pre-generated badges for standard
42 projects (like `libft`, `ft_printf`, and `minishell`) and instantly copy the
exact Markdown snippets needed for your README.

---

## Quick Usage

> [!WARNING]
> This project is in Alpha. Expect unannounced breaking changes and large
> commits because of the hundreds of SVGs.

If you just want to embed a pre-generated badge for a standard project, you
don't need to download or install anything. Just construct the URL based on your
project and score:

```markdown
![Libft Badge](https://raw.githubusercontent.com/airone01/ft_badges/refs/heads/main/badges/libft--125--logo--dark--noisy.svg)
```

**URL Format Convention**:

```
https://raw.githubusercontent.com/airone01/ft_badges/refs/heads/main/badges/{project_name}--{score}--{logo_style}--{theme}--{variant}.svg
```

For a full breakdown of the parameters, check out the
[**Usage Guide**](https://airone01.github.io/ft_badges/usage/).

---

## Local Generation using the CLI

Want to generate a custom badge with a unique name, specific score, or forced
hex color? You can use the `ft_badges` Python CLI locally. The CLI automatically
handles text wrapping and uses `scour` to optimize the SVG output.

### Installation

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/airone01/ft_badges.git
cd ft_badges
# optionally  set up a venv here as needed
pip install -r requirements.txt
```

### Generate Custom Badges

To generate a single badge with arbitrary values, use the `gen badge` command:

```bash
./main.py gen badge --project "My Custom C++" --score 112 --logo text --theme dark --variant noisy
```

### Batch Generation

If you are modifying the template or configuration and want to regenerate the
entire matrix of standard badges and their corresponding MkDocs Markdown files,
use the `--batch` flag:

```bash
# generate just the svg badges
./main.py gen badge --batch

# generate svg badges and update the MkDocs catalog
./main.py gen md --batch
```

> [!NOTE]
> You can also pass `--config=my_config.json` to process a completely custom
> batch matrix

## License

This project is released under the [Unlicense](LICENSE). It is free and
unencumbered software released into the public domain.

The '42' logo and branding are the intellectual property of 42 (association loi
1901 "42"). This project is an independent student initiative and is not
officially affiliated with, endorsed by, or sponsored by 42 School. Please don't
sue me, I'm just a student.
