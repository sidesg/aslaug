import argparse
from importlib.metadata import version

ASLAUG_VERSION = version("aslaug")

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--allocated",
        help="Instruct tsk_recover to export only allocated files (recovers all files by default)",
        action="store_true",
    )
    parser.add_argument(
        "-b",
        "--bulkextractor",
        help="Run Bulk Extractor on source",
        action="store_true",
    )
    parser.add_argument(
        "--ssn_mode",
        help="Specify ssn_mode for Bulk Extractor (0, 1, or 2)",
        action="store",
        type=int,
    )
    parser.add_argument("--regex", help="Specify path to regex file", action="store")
    parser.add_argument(
        "-d",
        "--diskimage",
        help="Use disk image instead of dir as input (Linux and macOS only)",
        action="store_true",
    )
    parser.add_argument(
        "--hfs", help="Use for raw disk images of HFS disks", action="store_true"
    )
    parser.add_argument(
        "--hfs_resforks",
        "--resforks",
        help="HFS option: Extract AppleDouble resource forks from HFS disks",
        action="store_true",
    )
    parser.add_argument(
        "--hfs_partition",
        help="HFS option: Specify partition number as integer for unhfs to extract (e.g. --hfs_partition 1)",
        action="store",
        type=int,
    )
    parser.add_argument(
        "--hfs_fsroot",
        help="HFS option: Specify POSIX path (file or dir) in the HFS file system for unhfs to extract (e.g. --hfs_fsroot /Users/tessa/backup/)",
        action="store",
        type=str,
    )
    parser.add_argument(
        "--tsk_imgtype",
        help="TSK option: Specify format of image type for tsk_recover. See tsk_recover man page for details",
        action="store",
    )
    parser.add_argument(
        "--tsk_fstype",
        help="TSK option: Specify file system type for tsk_recover. See tsk_recover man page for details",
        action="store",
    )
    parser.add_argument(
        "--tsk_sector_offset",
        help="TSK option: Sector offset for particular volume for tsk_recover to recover",
        action="store",
    )
    parser.add_argument(
        "--hash", help="Specify hash algorithm", dest="hash", action="store", type=str
    )
    parser.add_argument(
        "-k",
        "--keepsqlite",
        help="Retain Brunnhilde-generated sqlite db after processing",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--largefiles",
        help="Enable virus scanning of large files",
        action="store_true",
    )
    parser.add_argument(
        "-n", "--noclam", help="Skip ClamAV virus scan", action="store_true"
    )
    parser.add_argument(
        "-r",
        "--removefiles",
        help="Delete 'carved_files' directory when done (disk image input only)",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--throttle",
        help="Pause for 1s between Siegfried scans",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbosesf",
        help="Log verbose Siegfried output to terminal while processing",
        action="store_true",
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Display Brunnhilde version",
        action="version",
        version=ASLAUG_VERSION,
    )
    parser.add_argument(
        "-w",
        "--warnings",
        "--showwarnings",
        help="Add Siegfried warnings to HTML report",
        action="store_true",
    )
    parser.add_argument(
        "-z",
        "--scanarchives",
        help="Decompress and scan zip, tar, gzip, warc, arc with Siegfried",
        action="store_true",
    )
    parser.add_argument(
        "--csv",
        help="Path to Siegfried CSV file to read as input (directories only)",
        action="store",
        type=str,
    )
    parser.add_argument(
        "--stdin",
        help="Read Siegfried CSV from piped stdin (directories only)",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        help="Overwrite reports directory if it already exists",
        action="store_true",
    )
    parser.add_argument(
        "--in-memory-db",
        help="Use in-memory sqlite database rather than writing it to disk",
        action="store_true",
    )
    parser.add_argument("source", help="Path to source directory or disk image")
    parser.add_argument("destination", help="Path to destination for reports")

    return parser

def args_to_dict(parsedargs: argparse.Namespace) -> dict:
    args = dict()
