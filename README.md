# Open Modernism Tools

This repository collects tools I'm working on for the Open Modernism project. At the moment, the major project is converting image PDFs into LaTeX files, which I discuss below.

## Converting PDFs of scanned images into LaTeX files

In converting scanned PDF files (whether w/ OCR or w/o OCR) into Markdown for Open Modernism, we have expressed concerns over how to work in an ecology in which some document have been corrected and converted to Markdown and some have not. This tool (`pdf-to-latex-partial.py`) attempts to bridge that gap by converting a PDF of scanned images into a LaTeX partial that can be incorporated into a larger LaTeX document (w/ TOC, etc).

### Requirements

* Python 2.7+
* [Poppler](http://poppler.freedesktop.org/)
* XeTeX (optional; for compiling)
	* graphicx
	* geometry
	* grffile

### How it works

The python script harvests a scanned image PDF file (`Mina Loy - History of Religion of Eros.pdf` and `MrBennettAndMrsBrown.pdf` are provided as examples; one file has an OCR layer, the other doesn't (this matters, sadly)) and creates a directory of `.png` files. It then generates a LaTeX partial that resets the page geometry to have no margins, includes each image, and then restores the original geometry.

The images are generated using Poppler's `pdftocairo` program which uses a complicated PDF rendering algorithm to extract the page images (Cairo is important because w/ OCR there isn't a stable image file that can just be pulled out of the file). For PDFs with OCR layers, this process can take several minutes.

While this may seem like a useless feature (it's essentially doing a ton of work to reproduce something that already exists), the LaTeX partial can then be included into a larger TeX anthology and appear in a TOC and keep proper page numbering.

#### Dependencies for TeX

I've only tried compiling this in `XeTeX`, so YMMV, but as documented in `base.pdf`, the minimum packages needed for this to work are:

* graphicx
* geometry
* grffile

### Use

``` shell
python pdf-to-latex-partial.py [<FILE>]+
```

## Hosting Platform Ideas

* [Ikiwiki](http://ikiwiki.info/) --- Git backend, Markdown support, various account handlers
	* Custom plugin for firing Pandoc + plugins