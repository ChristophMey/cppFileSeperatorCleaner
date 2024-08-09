"""
This module contains the cleaner functions
"""

import os
import logging

import argparse
patterns = [
    "// --- include local component headers ---",
    "// --- include other project specific headers ---",
    "// --- include 3rd party headers ---",
    "// --- include std headers ---",
    "// --- include domain headers ---",
    "//                      Helper C l a s s   D e f i n i t i o n",
    "// =============================================================================",
    "//                              I n c l u d e s",
    "//                        O p e n   N a m e s p a c e",
    "//                      C l a s s   D e f i n i t i o n",
    "//                      C l a s s   I m p l e m e n t a t i o n",
    "//                        C l o s e   N a m e s p a c e",
]

logger = logging.getLogger(__name__)


def delete_seperator_lines(file: str):
    """
    Delete the separators in a file
    :param file: the file to process
    :return: None
    """
    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    with open(file, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip() not in patterns:
                f.write(line)


def find_all_cxx_and_hxx_files_in_dir(searched_directory: str):
    """
    Find all .cxx and .hxx files in a directory

    :param searched_directory:
    :return:
    """
    logger.info("Finding all .cxx and .hxx files in directory: %s", searched_directory)
    files = []
    for root, _, file_names in os.walk(searched_directory):
        if "3rd_party" in root:
            continue

        for file_name in file_names:
            if (file_name.endswith(".cxx")
                    or file_name.endswith(".hxx")
                    or file_name.endswith(".cpp")
                    or file_name.endswith(".hpp")):
                logger.info("Found file: %s", os.path.join(root, file_name))
                files.append(os.path.join(root, file_name))
    return files


def init_argparse():
    """
    Initialize the argument parser
    :return: the parsed arguments
    """
    parser = argparse.ArgumentParser(description="Delete separators in cxx and hxx files")
    parser.add_argument("-d",
                        "--dir",
                        help="Directory to search for cxx and hxx files",
                        required=True)
    return parser.parse_args()


def main():
    """
    Main function
    :return: None
    """
    args = init_argparse()
    logger.setLevel(logging.INFO)
    files = find_all_cxx_and_hxx_files_in_dir(args.dir)
    for file in files:
        logger.info("Processing file: %s", file)
        delete_seperator_lines(file)
    logger.info("Done")
