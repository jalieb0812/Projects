//jo resize

#include <stdio.h>
//#include <stdlib.h>
#include <stdbool.h>



int main(int argc, char *argv[])
{

    // ensure proper usage (ensures 2 arguements pass into main)
    if (argc != 2)
    {
        fprintf(stderr, "Usage:only one command line argument allowed\n");
        return 1;
    }

    char *infile = argv[1];
    // open input file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open file for reading %s.\n", argv[1]);
        return 2;
    }

    FILE *jpg_outptr = NULL; // create file pointer for output

    unsigned char buffer[512]; //create buffer

    char filename[8]; // create array for filenames

    int filename_counter = 0; // create counter for naming files

    bool first_jpeg = false;

    while (fread(buffer, 1, 512, inptr) != 0x00)
        //read file (at 1 byte 512 times into infile
        //until you hit the end of file demarcaged by the 0)
    {
        //if i found a jpg header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if i have  foudn the first jpeg already//
            if (first_jpeg) //
            {
                fclose(jpg_outptr); //close out previous file

            }

            // else if i already found the first jpeg header//close the previous file  //open outfile///print outfile name //increase filename counter //write to outfile
            else

            {
                first_jpeg = true;

            }


            sprintf(filename, "%03i.jpg", filename_counter);//print out new filename
            jpg_outptr = fopen(filename, "w");//open new file for writing
            if (jpg_outptr == NULL)
            {
                return 2;
            }

            filename_counter ++; //increase filename counter


        }
        if (first_jpeg) //

        {

            fwrite(&buffer, 1, 512, jpg_outptr);//write out 512 byte

        }

    }

    fclose(inptr);
    fclose(jpg_outptr);//close all files

    return 0;

}
