#!/usr/bin/env python3
# Path: annotate_variants.py
import requests
import logging
import sys

logger = logging.getLogger('annotate_variants')
logger.setLevel(logging.WARNING)

ENSEMBL_URL = 'http://rest.ensembl.org/vep/human/hgvs/'

def get_response(variant: str) -> dict:
    """
    It takes a variant as input, and returns the response from the Ensembl API as a JSON object
    
    :param variant: the variant to be annotated
    :return: The response is a json object.
    """
    with requests.Session() as s:
        # handle exceptions for requests
        try:
            url = ENSEMBL_URL + variant
            # get the response from the server
            response = s.get(url, headers={'Content-Type': 'application/json'})
            # check if the response is ok
            if response.ok:
                # return the response as a json object
                return response.json()[0]
            logging.error(f"{variant} could not be annotated with error: {response.json()['error']}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving the annotation for the variant {variant}: {e}")
            return None

def validate_variant(variant: str) -> bool:
    """
    It validates the variant by checking if it has the correct format
    
    :param variant: the variant to be validated
    :return: True if the variant is valid, False otherwise
    """
    # check if the variant has the correct format
    if variant.count(':') != 1:
        return False
    return True


def read_variants(file_name: str) -> list:
    """
    It reads a variants file line by line, removes the newline character from each line, and adds the line to a
    set if it is not already in the set
    
    :param file_name: the name of the file to read
    :return: A set of variants
    """
    # create an empty set to store the variants
    variants = set()
    # open the file
    with open(file_name) as f:
        # read the file line by line
        for line in f:
            # remove the newline character from the line
            line = line.rstrip()
            logger.info(f"Annotating variant {line}")
            # add the variant to the list if it is not already in the list
            if line not in variants and validate_variant(line):
                variants.add(line)
    return variants

def get_unique_genes(transcript_consequences: list) -> str:
    """
    It takes a list of transcript consequences and returns a comma-separated string of unique gene
    symbols
    
    :param transcript_consequences: a list of dictionaries, each dictionary representing a transcript
    consequence
    :return: A string of comma-separated gene symbols.
    """
    genes = set()
    for transcript in transcript_consequences:
        genes.add(transcript['gene_symbol'])

    return ", ".join(genes)

def write_annotations(file_name: str, annotations: list) -> None:
    with open(file_name, 'w') as f:
        f.write('variant\tassembly_name\tseq_region_name\tstart\tend\tmost_severe_consequence\tstrand\tgenes\n')
        for annotation in annotations:
            f.write(f"{annotation['variant']}\t{annotation['assembly_name']}\t{annotation['seq_region_name']}\t{annotation['start']}\t{annotation['end']}\t{annotation['most_severe_consequence']}\t{annotation['strand']}\t{annotation['genes']}\n")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: annotate-variants.py <variants_file> <output_file>")
        sys.exit(1)
    annotations = []
    error_variants = []
    # read the variants from the file passed a command line argument
    variants = read_variants(sys.argv[1])
    logger.info(f"{len(variants)} variants to be annotated")
    # loop through the variants and get the response from the server
    for variant in variants:
        response = get_response(variant)
        if response is None:
            error_variants.append(variant)
            continue
        try:
            annotations.append({
                'variant': variant,
                'assembly_name': response['assembly_name'],
                'seq_region_name': response['seq_region_name'],
                'start': response['start'],
                'end': response['end'],
                'most_severe_consequence': response['most_severe_consequence'],
                'strand': response['strand'],
                'genes': get_unique_genes(response['transcript_consequences'])
            })
        except Exception as e:
            logger.error(f"Error retrieving the annotation for the variant {variant}: {e}")
            error_variants.append(variant)
    # write the annotations to a file
    write_annotations(sys.argv[2], annotations)
    logger.warning(f"{len(annotations)} annotations were retrieved")
    logger.warning(f"{len(error_variants)} variants could not be annotated")
    error_variants = "\n".join(error_variants)
    logger.warning(f"The following variants could not be annotated: {error_variants}")

if __name__ == '__main__':
    main()
