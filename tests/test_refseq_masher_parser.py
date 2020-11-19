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
import pytest

from proksee.parser.refseq_masher_parser import parse_species_from_refseq_masher


class TestRefSeqMasherParser:

    def test_valid_masher_file(self):
        """
        Tests the parser with a valid RefSeq Masher output file.
        """

        valid_masher_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "rs_masher_good.tab")

        estimations = parse_species_from_refseq_masher(valid_masher_filename)

        estimation = estimations[0]

        assert estimation.species.name == "Listeria monocytogenes"
        assert estimation.species.confidence == 1
        assert estimation.identity == 1
        assert estimation.shared_hashes == 1
        assert estimation.median_multiplicity == 90
        assert estimation.full_taxonomy == "Bacteria; Terrabacteria group; Firmicutes; Bacilli; Bacillales; " \
            + "Listeriaceae; Listeria; monocytogenes"

        estimation = estimations[1]

        assert estimation.species.name == "Listeria phage LP-101"
        assert estimation.species.confidence == 1
        assert estimation.identity == 0.959082
        assert estimation.shared_hashes == float(205/400)
        assert estimation.median_multiplicity == 83
        assert estimation.full_taxonomy == "Viruses; dsDNA viruses, no RNA stage; Caudovirales; Siphoviridae; " \
            + "unclassified; Listeria phage LP-101"

        estimation = estimations[2]

        assert estimation.species.name == "Listeria phage A006"
        assert estimation.species.confidence == 1
        assert estimation.identity == 0.956699
        assert estimation.shared_hashes == float(197/400)
        assert estimation.median_multiplicity == 104
        assert estimation.full_taxonomy == "Viruses; dsDNA viruses, no RNA stage; Caudovirales; Siphoviridae; " \
            + "unclassified; Listeria phage A006"

        estimation = estimations[3]

        assert estimation.species.name == "Listeria innocua"
        assert estimation.species.confidence == 1-1.0596399999999997e-173
        assert estimation.identity == 0.926047
        assert estimation.shared_hashes == float(117/400)
        assert estimation.median_multiplicity == 88
        assert estimation.full_taxonomy == "Bacteria; Terrabacteria group; Firmicutes; Bacilli; Bacillales; " \
            + "Listeriaceae; Listeria; innocua; FSL J1-023"

        estimation = estimations[4]

        assert estimation.species.name == "[Clostridium] cellulolyticum"
        assert estimation.species.confidence == 1-9.228979999999998e-170
        assert estimation.identity == 0.925049
        assert estimation.shared_hashes == float(115/400)
        assert estimation.median_multiplicity == 823
        assert estimation.full_taxonomy == "Bacteria; Terrabacteria group; Firmicutes; " \
            + "Clostridia; les; Ruminococcaceae; Ruminiclostridium; [Clostridium] cellulolyticum"

    def test_missing_masher_file(self):
        """
        Tests the parser with a missing file. This should raise a FileNotFound exception.
        """

        missing_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "missing.file")

        with pytest.raises(FileNotFoundError):
            parse_species_from_refseq_masher(missing_filename)