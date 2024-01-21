#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import pypdf

def get_num_pages(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_object = pypdf.PdfReader(pdf_file)
        num_pages = len(pdf_object.pages)
        pdf_file.close()
        return num_pages
    
def write_template_text(title, num_pages, images_dir, images_pattern):
    template_text = [
        f"# {title}",
        f"\n",
    ]
    template_text = ['\n'.join(template_text)]
    for i in range(num_pages):
        slide_text = [
        f"## Slide {i} {{.slide}}",
        f"![Slide {i}]({images_dir}/{images_pattern}{i}.jpg)",
        f"* " ,
        "",
        ]
        slide_text = '\n\n'.join(slide_text)
        template_text.append(slide_text)
    return template_text

def write_images(pdf_path, images_path, images_pattern):
    if not os.path.isdir(images_path):
        os.mkdir(images_path)
    os.system(f"magick -density 150 -quality 75 {pdf_path} {images_path / images_pattern}%d.jpg")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('input', type = str, help = "PDF file to use for template")

    parser.add_argument('--output', '-o', default = '.', help = "output directory")
    parser.add_argument('--img', '-i', action = 'store_true', help = "Use this flag to create images from the specified pdf")
    parser.add_argument('--md', '-t', action = 'store_true', help = "Use this flag to create a markdown template")
    parser.add_argument('--img_pattern', '-p', type = str, default = "img_", help = "Pattern for image filenames. Default is 'image_'")

    args = parser.parse_args()

    input_pdf = Path(args.input)
    create_images = args.img
    create_template = args.md
    output_dir = Path(args.output)
    images_pattern = args.img_pattern

    images_dir = output_dir / "slides"

    num_pages = get_num_pages(input_pdf)

    if create_images:
        write_images(pdf_path = input_pdf, images_path = images_dir, images_pattern =  images_pattern)

    if create_template:
        title = input_pdf.stem
        md_text = write_template_text(title = title, num_pages = num_pages, images_pattern = images_pattern, images_dir = images_dir)
        with open(output_dir / "template.md", "w") as template:
            template.writelines(md_text)
            template.close

if __name__ == '__main__':
    main()














