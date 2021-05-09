import pyensembl
import io
import base64

def parse_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('utf-8')
    HGNC_list = decoded.split()
    GRCh37_list = HGNC_list_to_GRCh37(HGNC_list)
    ensembl_list = HGNC_list_to_ensembl(GRCh37_list)
    return ensembl_list

def upload_file_prompt(filename):
    if '.txt' not in filename:
        return 'You can only upload txt files!'
    else:
        return 'File ' + filename + ' uploaded'
    
def upload_add_file_prompt(list_of_filenames):
    if any('.txt' not in filename for filename in list_of_filenames):
        return 'You can only upload txt files!'
    else:
        return 'Files ' + ", ".join(list_of_filenames) + ' uploaded'

def find_repeated(genes_list, list_of_genes_lists):
    repeated_genes = list()
    for glist in list_of_genes_lists:
        repeated_genes = repeated_genes + [g for g in genes_list if g in glist]
    unique_genes = list(set(repeated_genes))
    return unique_genes

ensembl_37 = pyensembl.EnsemblRelease(release=75)
ensembl_38 = pyensembl.EnsemblRelease(release=100)

def GRCh38_to_GRCh37(name):
    try:
        #check if name is in GRCh37 table
        ensembl_37.gene_ids_of_gene_name(name)
    except:
        #if name is not found in GRCh37 table convert it to ensemble and then to GRCh38
        ensemble_id = ensembl_38.gene_ids_of_gene_name(name)
        return ensembl_37.gene_name_of_gene_id(ensemble_id[0])
    return name

def HGNC_list_to_GRCh37(genes_list):
    return [GRCh38_to_GRCh37(gname) for gname in genes_list]

def HGNC_list_to_ensembl(genes_list):
    return [ensembl_37.gene_ids_of_gene_name(gname)[0] for gname in genes_list]