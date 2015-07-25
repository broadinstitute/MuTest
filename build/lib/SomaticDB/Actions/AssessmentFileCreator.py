import pandas as pd

def create_assessment_file(tsv, results, output_file, evaluation_rules):
    metadata = pd.read_csv(tsv,'\t')

    evaluation_rules  = evaluation_rules.split(',')
    evaluation_rules  = map(lambda x: tuple(x.split(':')),evaluation_rules)
    evaluation_rules = dict(evaluation_rules)

    results_data = map(lambda x: x.strip(), open(results).readlines())

    metadata_rows = map(lambda x: dict(x[1]), list(metadata.iterrows()))

    out_rows=[]

    for result,metadata in zip(results_data, metadata_rows):

        metadata['data_filename']   = result
        metadata['evidence_type'] = evaluation_rules[metadata['project'] ]

        out_rows.append(metadata)

    out = pd.DataFrame(out_rows)

    out.to_csv(output_file,sep='\t')