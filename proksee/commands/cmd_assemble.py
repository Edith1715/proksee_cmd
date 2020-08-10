import click
import os
import sys

# import platform detection
from proksee.platform_identify import PlatformIdentify

# import quality module
from proksee.read_quality import ReadFiltering

# import organism detection
from proksee.organism_detection import OrganismDetection

# import assembler
from proksee.assembler import Assembler

@click.command('assemble',
               short_help='Assemble reads.')
@click.argument('forward', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('reverse', required=False,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output_dir', required=True,
              type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, forward, reverse, output_dir):

    #raise click.UsageError("command not yet implemented")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Step 1: Platform detection
    # Pass forward and reverse datasets to platform detection module and ensure that both files are of the same platform
    platform_identify = PlatformIdentify(forward, reverse)
    platform = platform_identify.identify_platform(forward, reverse)
    print(platform)

    # Step 2: Quality Check
    # Pass forward and reverse datasets to quality check module and calculate quality statistics
    read_filtering = ReadFiltering(forward, reverse, output_dir)
    filtering = read_filtering.filter_read(forward, reverse, output_dir)
    print(filtering)

    forward_filtered = os.path.join(output_dir, 'fwd_filtered.fastq')
    if reverse is None:
        reverse_filtered = None
    else:
        reverse_filtered = os.path.join(output_dir, 'rev_filtered.fastq')

    # Step 3: Organism Detection
    # Pass forward and reverse datasets to organism detection module and return the dominate genus and species
    organism_identify = OrganismDetection(forward_filtered, reverse_filtered, \
        output_dir)
    major_organism = organism_identify.major_organism(forward_filtered, \
        reverse_filtered, output_dir)
    print(major_organism)

    # Step 4: Assembly (Only skesa for now)
    # Pass forward and reverse datasets to assembly module and return a path to the results or paths to specific files
    assembler = Assembler(forward_filtered, reverse_filtered, output_dir)
    assembly = assembler.perform_assembly(forward_filtered, reverse_filtered, output_dir)
    print(assembly)