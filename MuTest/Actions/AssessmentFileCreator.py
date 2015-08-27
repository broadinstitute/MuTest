from collections import defaultdict
import pandas as pd

def create_assessment_file(tsv, results, output_file, evaluation_rules):
    metadata = pd.read_csv(tsv,'\t')

    if evaluation_rules != "NN":
        evaluation_rules  = evaluation_rules.split(',')
        evaluation_rules  = map(lambda x: tuple(x.split(':')),evaluation_rules)
        evaluation_rules = dict(evaluation_rules)
    else:
       evaluation_rules = defaultdict(lambda : "NN")

    results_data = map(lambda x: x.strip(), open(results).readlines())

    metadata_rows = map(lambda x: dict(x[1]), list(metadata.iterrows()))

    out_rows=[]

    print evaluation_rules

    for result,metadata in zip(results_data, metadata_rows):

        metadata['data_filename']   = result

        evaluation_rule = metadata['project']

        if evaluation_rules.has_key(evaluation_rule):
            metadata['evidence_type'] = evaluation_rules[evaluation_rule]
        else:
            metadata['evidence_type'] ='.'

        out_rows.append(metadata)

    out = pd.DataFrame(out_rows)

    out.to_csv(output_file,sep='\t',index=False)