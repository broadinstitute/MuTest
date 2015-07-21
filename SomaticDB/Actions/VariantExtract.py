from SomaticDB.BasicUtilities.DictUtilities import get_entries_from_dict
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import query_processor
import ast
import pandas as pd


def variant_extract(query, output_filename, max_number_of_records):
    query = query_processor(query)

    output = []

    collection = connect_to_mongo()

    for record in collection.find(ast.literal_eval(query)):

        sample_information = get_entries_from_dict(record, keys=['chromosome',
                                                                 'start',
                                                                 'ref',
                                                                 'alt',
                                                                 'project',
                                                                 'dataset',
                                                                 'sample',
                                                                 'evidence_type'],return_type=dict)


        for sample in sample_information:
            sample_information[sample] = str(sample_information[sample])

        output.append(sample_information)


    output = pd.DataFrame(output)

    if len(output) > max_number_of_records: output = output[:max_number_of_records]


    if output_filename == "<stdout>":
        print "project, dataset, sample, evidence_type, chromosome, start, ref, alt"
        for k, row in output.iterrows():
            row = [row['project'],row['dataset'],row['sample'],row['evidence_type'],row['chrosome'],row['start'],row['ref'],row['alt']]
            row =",".join(row)
            print row
    else:
        output.to_csv(output_filename,index=False,fieldnames=["project",
                                                              "dataset",
                                                              "sample",
                                                              "evidence_type",
                                                              "chromosome",
                                                              "start",
                                                              "ref",
                                                              "alt"], sep='\t')



