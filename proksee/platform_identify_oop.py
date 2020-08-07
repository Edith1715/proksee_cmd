import os
import gzip
import sys

# Declaring global variables based on zipped or unzipped files
GZ_FALSE = 0
GZ_TRUE = 1


class PlatformIdentify():

    def __init__(self, output_dir, forward, reverse):
        self.output_dir = output_dir
        self.forward = forward
        self.reverse = reverse

    # Checking files for valid fastq extension, passing to dictionary
    def fastq_extn_check(self):
        if self.reverse is None:
            file_list = [self.forward]
        else:
            file_list = [self.forward, self.reverse]
        f_name_dicn = {}
        fastq_ext = ['fastq', 'fq']
        for f_name in file_list:
            array_f = f_name.split('.')
            try:
                if (array_f[-2] in fastq_ext and array_f[-1] == 'gz'):
                    f_name_dicn[f_name] = GZ_TRUE
                elif (array_f[-1] in fastq_ext):
                    f_name_dicn[f_name] = GZ_FALSE
            except IndexError:
                pass
        return f_name_dicn


    # Identifying sequencing platform based on read
    def plat_iden(self, open_file):
        count_line = 0
        for line in open_file:
            count_line += 1
            if count_line == 1:
                first_line = line.rstrip('\n')
                break
        chars_ill = first_line.split(':')
        chars_pac = first_line.split('/')
        if len(chars_ill) == 3:
            platform = 'Ion Torrent'
        elif len(chars_ill) > 4:
            platform = 'Illumina'
        elif len(chars_pac) > 2:
            platform = 'Pacbio'
        else:
            platform = 'Unidentifiable'
        return platform


    # Opening files within input directory and assigning plat_iden method
    def platform_output(self, f_name_dicn):
        fastq_platform = {}
        for file in f_name_dicn:
            if (f_name_dicn[file] == GZ_TRUE):
                with gzip.open(file, mode='rt') as open_file:
                    fastq_platform[os.path.basename(file)] = self.plat_iden(open_file)
            elif (f_name_dicn[file] == GZ_FALSE):
                with open(file, mode='r') as open_file:
                    fastq_platform[os.path.basename(file)] = self.plat_iden(open_file)
        return fastq_platform