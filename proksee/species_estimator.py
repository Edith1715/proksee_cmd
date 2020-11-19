"""
Copyright Government of Canada 2020

Written by: Eric Marinier, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os
import subprocess

from proksee.parser.refseq_masher_parser import parse_species_from_refseq_masher
from proksee.species import Species


def estimate_major_species(estimations, ignore_viruses=True):
    """
    Estimates which major species are present in a list of Estimations. Not all estimations will have enough
    evidence to report them as major species. The species will be sorted in descending order of confidence. If
    there are multiple major species reported, then it is possible there is significant contamination.

    PARAMETERS
        estimations (List(Estimation)): a list of species estimations from which to determine major species
            present in the data
        ignore_viruses (bool=True): whether or not to ignore virus estimations

    RETURNS
        species (List(Species)): a list of major species determined from the estimations
    """

    MIN_SHARED_FRACTION = 0.90  # the minimum fraction of shared hashes
    MIN_IDENTITY = 0.90  # the minimum identity; estimation of fraction of bases shared between reads and genome
    MIN_MULTIPLICITY = 5  # the median multiplicity; relates to coverage and redundancy of observations

    species = []

    for estimation in estimations:

        full_taxonomy = str(estimation.full_taxonomy)

        if ignore_viruses and full_taxonomy.startswith("Viruses"):
            continue

        shared_hashes = estimation.shared_hashes
        identity = estimation.identity
        median_multiplicity = estimation.median_multiplicity

        if shared_hashes >= MIN_SHARED_FRACTION and identity >= MIN_IDENTITY and median_multiplicity \
                >= MIN_MULTIPLICITY:

            species.append(estimation.species)

    return species


class SpeciesEstimator:
    """
    This class represents a species estimation tool.

    ATTRIBUTES
        forward (str): the filename of the forward reads
        reverse (str): the filename of the reverse reads
        output_directory (str): the directory to use for program output
    """

    def __init__(self, forward, reverse, output_directory):
        """
        Initializes the species estimator.

        PARAMETERS
            forward (str): the filename of the forward reads
            reverse (str): the filename of the reverse reads
            output_directory (str): the directory to use for program output
        """

        self.forward = forward
        self.reverse = reverse
        self.output_directory = output_directory

    def estimate_species(self):
        """
        Estimates the species present in the reads.

        RETURNS
            species (List(Species)): a list of the estimated major species, sorted in descending order of most complete
                and highest covered; will contain an unknown species if no major species was found
        """

        refseq_masher_filename = self.run_refseq_masher()
        estimations = parse_species_from_refseq_masher(refseq_masher_filename)

        species = estimate_major_species(estimations)

        if len(species) == 0:
            species.append(Species("Unknown", 0.0))

        return species

    def run_refseq_masher(self):
        """
        Runs RefSeq Masher on the reads.

        POST
            If successful, RefSeq Masher will have executed on the reads and the output will be written to the output
            directory. If unsuccessful, an error message will be raised.

            If unsuccessful, the output file we be empty. It is necessary to check to see if the output file contains
            any output.
        """

        output_filename = os.path.join(self.output_directory, "refseq_masher.o")
        error_filename = os.path.join(self.output_directory, "refseq_masher.e")

        output_file = open(output_filename, "w")
        error_file = open(error_filename, "w")

        # create the refseq_masher command
        if self.reverse:
            command = "refseq_masher contains " + str(self.forward) + " " + str(self.reverse)
        else:
            command = "refseq_masher contains " + str(self.forward)

        # run refseq_masher
        try:
            subprocess.check_call(command, shell=True, stdout=output_file, stderr=error_file)

        except subprocess.CalledProcessError:
            pass  # it will be the responsibility of the calling function to insure there was output

        finally:
            output_file.close()
            error_file.close()

        return output_filename