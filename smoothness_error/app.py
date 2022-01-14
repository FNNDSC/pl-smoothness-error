import os
from pathlib import Path
import glob
from chrisapp.base import ChrisApp
import pybicpl as bicpl
import numpy as np


def smoothness(input: str, output: str):
    """
    Calculate smoothness error of a .obj and save the output to a .txt
    """
    data = bicpl.depth_potential(input, '-mean_curvature')
    obj = bicpl.MniObj(input)
    result = bicpl.difference_average(obj.neighbor_graph(), data)
    np.savetxt(output, list(result))


class SmoothnessError(ChrisApp):
    """
    Calculate vertex-wise smoothness error of a .obj surface mesh
    """
    PACKAGE                 = __package__
    TITLE                   = 'Surface Mesh Smoothness Error'
    description             = 'Calculate vertex-wise smoothness error of a .obj surface mesh'
    CATEGORY                = 'Surface Analysis'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument(
            '-p', '--inputPathFilter',
            dest='inputPathFilter',
            help='Selection for which files to evaluate.',
            default='*.obj',
            type=str,
            optional=True
        )
        self.add_argument(
            '-s', '--outputSuffix',
            dest='outputSuffix',
            help='File name suffix for every output.',
            default='.smth_err.txt',
            type=str,
            optional=True
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        output_dir = Path(options.outputdir).resolve()
        os.chdir(options.inputdir)
        input_files = glob.glob(options.inputPathFilter)
        output_files = [output_dir / (f + options.outputSuffix) for f in input_files]

        for input_file, output_file in zip(input_files, output_files):
            smoothness(input_file, output_file)
            print(output_file)

    def show_man_page(self):
        self.print_help()
