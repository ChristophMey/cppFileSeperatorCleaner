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


def deleteSeperatorsInFile(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for line in lines:
            if line.strip() not in patterns:
                f.write(line)


def findAllCxxAndHxxFilesInDir(dir):
    logger.info("Finding all .cxx and .hxx files in directory: %s", dir)
    files = []
    for root, dirs, fileNames in os.walk(dir):
        if "3rd_party" in root:
            continue
        for fileName in fileNames:
            if fileName.endswith(".cxx") or fileName.endswith(".hxx") or fileName.endswith(".cpp") or fileName.endswith(".hpp"):
                logger.info("Found file: %s", os.path.join(root, fileName))
                files.append(os.path.join(root, fileName))
    return files


def init_argparse():
    parser = argparse.ArgumentParser(description="Delete seperators in cxx and hxx files")
    parser.add_argument("-d", "--dir", help="Directory to search for cxx and hxx files", required=True)
    return parser.parse_args()


def main():
    args = init_argparse()
    logger.setLevel(logging.INFO)
    files = findAllCxxAndHxxFilesInDir(args.dir)
    for file in files:
        logger.info("Processing file: %s", file)
        deleteSeperatorsInFile(file)
    logger.info("Done")
