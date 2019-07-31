// JO resize.c


#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage (ensures 4 arguements pass into main)
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 0 || n >= 101)
    {
        fprintf(stderr, "n_factor must be a positive int between 1- 100 \n");
        return 1;
    }
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];


    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfn;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    bfn = bf; // gives bfn value of bf

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, bin;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    bin = bi; // gives bin value of bi

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }


    bin.biWidth *= n ;
    bin.biHeight *= n;
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_n = (4 - (bin.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;//calculate new padding
    bin.biSizeImage = ((sizeof(RGBTRIPLE) * bin.biWidth) + padding_n) * abs(bin.biHeight); // recalculates bisizeimage
    bfn.bfSize = bin.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);// recalculates BFSize




    // write outfile's BITMAPFILEHEADER
    fwrite(&bfn, sizeof(BITMAPFILEHEADER), 1, outptr);



    // write outfile's BITMAPINFOHEADER
    fwrite(&bin, sizeof(BITMAPINFOHEADER), 1, outptr);





    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {

        for (int counter = 0; counter < n; counter++)
        {

            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)

            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int k = 0; k < n; k++)
                {

                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);// write new RGB triple to outfile

                }


            }

            // skip over old padding, if any
            fseek(inptr, padding, SEEK_CUR);

            for (int m = 0; m < padding_n; m++) // add new padding

            {

                fputc(0x00, outptr);


            }

            if (counter < n - 1)
            {
                fseek(inptr, -(bi.biWidth * 3 + padding), SEEK_CUR);
            }



        }



    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;

}