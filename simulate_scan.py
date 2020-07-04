from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import img2pdf, pdf2image
from subprocess import run
import os, random, io
#print(os.listdir())
import numpy as np
import random
from PIL import Image, ImageFilter
from tempfile import TemporaryDirectory

letter = (img2pdf.in_to_pt(8.5), img2pdf.in_to_pt(11))
layout = img2pdf.get_layout_fun(letter)

def add_salt_and_pepper(image, n, seed=0):
    np.random.seed(seed)
    image = np.copy(np.array(image))
    output = np.ones_like(image)*127
    R,C,*_ = image.shape
    Z = zip(
        np.random.randint(0,R,n),
        np.random.randint(0,C,n),
        1+np.random.randint(0,15,n)//10,
        np.random.randint(0,127,n),
    )
    for r,c,d,z in Z:
        output[r][c] = z
        for i in range(d):
            for j in range(d):
                if 0<=r+i<R and 0<=c+j<C:
                    output[r+i][c+j] = z

    #output = Image.fromarray(output)
    #output = output.filter(ImageFilter.MinFilter(3))
    #output = output.filter(ImageFilter.GaussianBlur(radius=2))
    output = np.array(output).astype(np.float)/127
    output = np.array(image*output).astype(np.uint8)
    return Image.fromarray(output)



def simulate_scan(ipath, opath):
    reader = PdfFileReader(ipath)
    output = PdfFileWriter()
    n = reader.getNumPages()
    with TemporaryDirectory() as tmp:
        tmp_pdf = os.path.join(tmp, '_tmp.pdf')
        tmp_jpg = os.path.join(tmp, '_tmp.jpg')
        for i in range(n):
            page = reader.getPage(i)
            pdf = PdfFileWriter()
            pdf.addPage(page)
            with open(tmp_pdf, 'wb') as f:
                pdf.write(f)
            imgs = pdf2image.convert_from_path(tmp_pdf)
            img = imgs[0]
            angle = 3*(random.random()-.5)
            img = img.rotate(angle=angle,
                resample=Image.BICUBIC, fillcolor='white')

            img = add_salt_and_pepper(img, 300)
            img.save(tmp_jpg)
            with open(tmp_pdf, "wb") as f:
                f.write(img2pdf.convert([tmp_jpg],
                    layout_fun=layout))
            pdf = PdfFileReader(tmp_pdf)
            page = pdf.getPage(0)
            output.addPage(page)
        with open(opath, 'wb') as f:
            output.write(f)
    return

simulate_scan('signed.pdf', 'scanned.pdf')


def tilt_pages(pdf_path):
    pdf_writer = PdfFileWriter()
    reader = PdfFileReader(pdf_path)

    n = reader.getNumPages()
    for i in range(n):
        page = reader.getPage(i)
        page = page.rotateClockwise(random.randint(0,10))
        writer.addPage(page)

    with open('tilted.pdf', 'wb') as f:
        writer.write(f)
    return


def merge(pdfs, output):
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(output)
    merger.close()
    return


def split(path, name_of_split):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
    return


if __name__ == '__main__':
    path = '.pdf'
    #rotate_pages(path)

