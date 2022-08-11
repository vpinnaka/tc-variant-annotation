# write units tests for all the functions in the annotate_variants.py file
import pytest
import tempfile

from annotatevariants.annotate_variants import get_response, validate_variant, read_variants, get_unique_genes, write_annotations

def test_get_response():
    """
    It tests the get_response function by checking if the response is a json object
    """
    # create a variant
    variant = 'NC_000002.12:g.39006443C>T'
    # get the response from the server
    response = get_response(variant)
    # check if the response is a json object
    assert isinstance(response, dict)


def test_validate_variant():
    """
    It tests the validate_variant function by checking if the variant is valid
    """
    # create a variant
    variant = 'NC_000002.12:g.39006443C>T'
    # check if the variant is valid
    assert validate_variant(variant) == True


def test_validate_variant_invalid():
    """
    It tests the validate_variant function by checking if the variant is invalid
    """
    # create a variant
    variant = 'NC_000002.12g.39006443C>T'
    # check if the variant is invalid
    assert validate_variant(variant) == False


def test_read_variants():
    """
    It tests the read_variants function by checking if the variant is in the set
    """
    # create a set of variants
    with tempfile.NamedTemporaryFile() as f:
        # write the variants to the temp file
        f.write(b'NC_000002.12:g.39006443C>T\n')
        f.write(b'NC_000002.12:g.39006443C>T\n')
        f.flush()
        # read the variants from the temp file
        variants_from_file = read_variants(f.name)
        # check if the variants are in the set
        assert variants_from_file == set(['NC_000002.12:g.39006443C>T'])


def test_get_unique_genes():
    """
    It tests the get_unique_genes function by checking if the genes are unique
    """
    # create a list of transcript consequences
    transcript_consequences = [
        {'transcript_id': 'ENST00000372059', 'gene_symbol': 'SYNE1'},
        {'transcript_id': 'ENST00000372059', 'gene_symbol': 'SYNE1'},
    ]
    # get the unique genes
    unique_genes = get_unique_genes(transcript_consequences)
    # check if the genes are unique 
    assert unique_genes == 'SYNE1'


def test_write_annotations():
    """
    It tests the write_annotations function by checking if the annotations are written to the file
    """
    # create a list of annotations
    annotations = [
        {
            'variant': 'NC_000002.12:g.39006443C>T',
            'assembly_name': 'GRCh38',
            'seq_region_name': '2',
            'start': 39006443,
            'end': 39006443,
            'most_severe_consequence': 'missense_variant',
            'strand': 1,
            'genes': 'SYNE1, SYNE2'
        }
    ]
    with tempfile.NamedTemporaryFile() as f:
        # write the annotations to the file
        write_annotations(f.name, annotations)
        # read the annotations from the file
        with open(f.name) as f:
            annotations_from_file = f.readlines()
            # check if the annotations are written to the file
            assert annotations_from_file[0] == 'variant\tassembly_name\tseq_region_name\tstart\tend\tmost_severe_consequence\tstrand\tgenes\n'
            assert annotations_from_file[1] == 'NC_000002.12:g.39006443C>T\tGRCh38\t2\t39006443\t39006443\tmissense_variant\t1\tSYNE1, SYNE2\n'


    





