#!/usr/bin/env python
import os
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
from tempfile import NamedTemporaryFile
import subprocess as sp
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from loguru import logger
from chris_plugin import chris_plugin, PathMapper
from bicpl.obj import PolygonObj
from bicpl.math import difference_average

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _                                  _   _                                                        
      | |                                | | | |                                                       
 _ __ | |______ ___ _ __ ___   ___   ___ | |_| |__  _ __   ___  ___ ___ ______ ___ _ __ _ __ ___  _ __ 
| '_ \| |______/ __| '_ ` _ \ / _ \ / _ \| __| '_ \| '_ \ / _ \/ __/ __|______/ _ \ '__| '__/ _ \| '__|
| |_) | |      \__ \ | | | | | (_) | (_) | |_| | | | | | |  __/\__ \__ \     |  __/ |  | | | (_) | |   
| .__/|_|      |___/_| |_| |_|\___/ \___/ \__|_| |_|_| |_|\___||___/___/      \___|_|  |_|  \___/|_|   
| |                                                                                                    
|_|                                                                                                    
"""


parser = ArgumentParser(description='Calculate smoothness error (difference in curvature between neighbor vertices)',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-p', '--pattern', default='**/*.obj',
                    help='pattern for surface file names to include')
parser.add_argument('-o', '--output-suffix', default='.smtherr.txt', dest='output_suffix', type=str,
                    help='suffix for output files')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='disable status messages')
parser.add_argument('--no-fail', action='store_true', dest='no_fail',
                    help='do not produce non-zero exit status on failures')
parser.add_argument('-V', '--version', action='version',
                    version=f'$(prog)s {__version__}')


@chris_plugin(
    parser=parser,
    title='Surface Smoothness Error',
    category='Surface Extraction',
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    if options.quiet:
        logger.remove()
        logger.add(sys.stderr, level='WARNING')
    else:
        print(DISPLAY_TITLE, file=sys.stderr, flush=True)

    mapper = PathMapper(inputdir, outputdir, glob=options.pattern, suffix=options.output_suffix)

    nproc = len(os.sched_getaffinity(0))
    logger.debug('Using {} threads.', nproc)

    with ThreadPoolExecutor(max_workers=nproc) as pool:
        results = pool.map(lambda t: smtherr(*t), mapper)

    if options.no_fail:
        return
    for _ in results:
        pass


def smtherr(surface: Path, output: Path):
    data = depth_potential(surface, '-mean_curvature')
    obj = PolygonObj.from_file(surface)
    result = np.fromiter(difference_average(obj.neighbor_graph(), data), dtype=np.float64)
    np.savetxt(output, result)  # type: ignore
    logger.info(output)


def depth_potential(filename: str | os.PathLike, arg: str, command: str = 'depth_potential'):
    if not arg.startswith('-'):
        arg = '-' + arg
    with NamedTemporaryFile() as tmp:
        cmd = (command, arg, filename, tmp.name)
        logger.info(' '.join(map(str, cmd)))
        sp.run(cmd, check=True)
        data = np.loadtxt(tmp.name, dtype=np.float32)
    return data


if __name__ == '__main__':
    main()
