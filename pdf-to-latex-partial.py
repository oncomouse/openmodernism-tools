# Script to convert PDFs w/ scanned page images into LaTeX partials.

from subprocess import call
import glob
import string
import os
import argparse

def process_file( target_file ):
    
    # Make the directory:
    if not os.path.exists(target_file.replace('.pdf','')):
        os.makedirs(target_file.replace('.pdf',''))
    if not os.path.exists(target_file.replace('.pdf','') + "/page-images"):
        os.makedirs(target_file.replace('.pdf','') + "/page-images")

    # This requires poppler to work:
    return_status = call(["pdftocairo", "-png", target_file, target_file.replace('.pdf','') + "/page-images/page"])
    # This version can take forever to run, but it works on a wide range of test files and produces quality results.
    
    # This version uses ghostscript and imagemagick but doesn't produce as high-quality results:
    #return_status = call(["convert", '-trim', target_file,  os.getcwd() + "/page-images/page.png"])

    # Get a list of all the page numbers:
    page_images = glob.glob(os.getcwd() + "/" + target_file.replace('.pdf','') + "/page-images/*.png")

    # Base from which we include each image file:
    base_image_template = "\\begin{{figure}}[hbt]\n\t\\centering\n\t\\includegraphics[height=11in,width=8.5in,keepaspectratio]{{{}}}\n\\end{{figure}}\n\\clearpage\n\n"

    # Open a LaTeX file
    f = open(target_file.replace(".pdf", ".tex"), "w")

    # Write the geometry and page fraction reset code:
    f.write("\\newgeometry{{margin=0in}}\n\\providecommand{\\oldpagefraction}{\\floatpagefraction}\n\\renewcommand{\\floatpagefraction}{0.1}\n\n")

    for page_image in page_images:
        page_image = page_image.replace(os.getcwd() + "/","")
        if not ' ' in page_image:
            page_image = page_image.replace(".png", "")

        f.write(base_image_template.format(page_image))

    # Write the geometry and page fraction restore code:
    f.write("\\restoregeometry\n\\renewcommand{\\floatpagefraction}{\\oldpagefraction}")
    f.close()

# Read file names off of the command line and process them:
argparser = argparse.ArgumentParser()
argparser.add_argument('files', metavar='FILE', type=str, nargs='*')
files = argparser.parse_args().files

for file in files:
    process_file(file)
