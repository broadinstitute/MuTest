import pandas as pd

def create_assessment_file(tsv, results, outputfile, evaluation_results):
    data = pd.read_csv(tsv)

