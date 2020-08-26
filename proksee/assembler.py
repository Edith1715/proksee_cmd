'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

Written by: Arnab Saha Mandal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''

import os
import subprocess


# Defining assembler class for creating genome assembly using skesa
class Assembler():

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir

    # Creating skesa command to be executed
    def __skesa_string(self):
        if self.reverse is None:
            skesa_str = 'skesa --fastq ' + self.forward + ' --use_paired_ends'

        else:
            skesa_str = 'skesa --fastq ' + self.forward + ',' + self.reverse

        return skesa_str

    # Method for running skesa command
    def __skesa_func(self, skesa_str):
        '''Creating skesa output and log files'''
        skesa_out = open(os.path.join(self.output_dir, 'skesa.out'), 'w+')
        skesa_log = open(os.path.join(self.output_dir, 'skesa.log'), 'w+')

        '''Running skesa as a subprocess module. Capturing return code.
        Raising error otherwise'''
        try:
            rc = subprocess.check_call(skesa_str, shell=True,
                                       stdout=skesa_out, stderr=skesa_log)
        except subprocess.CalledProcessError as e:
            raise e

        return rc

    # Method for integrating private functions
    def perform_assembly(self):
        skesa_string = self.__skesa_string()
        return_code = self.__skesa_func(skesa_string)

        '''Creating skesa completion output string'''
        output_string = 'SKESA assembled reads and log files written ' + \
            'to output directory. Return code {}'.format(return_code)

        return output_string
