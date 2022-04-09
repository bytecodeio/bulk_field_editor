from array import array
from ast import arg
from operator import mod
import csv
import lookml, argparse

def main(repo_name, github_access_token, branch, modifications_file_path):
    project = lookml.Project(
        repo= repo_name,
        access_token=github_access_token,
        branch=branch
    )
    modifications:array(object) = parse_modifications_from_file(modifications_file_path)
    for mod_item in modifications:
        apply_mod_item_update(project, mod_item)
    
def parse_modifications_from_file(filename):
    with open(filename) as file_handle:
        reader = csv.reader(file_handle, skipinitialspace=True)
        rows = []
        for row in reader:
            rows.append(row)
        headers: array = rows[0]
        i=1
        returndata = []
        properties = ['file_name', 'view_name', 'field_name', 'primary_key', 'description']
        while i<len(rows):
            rowdata = {}
            for property in properties:
                try:
                    rowdata[property]=rows[i][headers.index(property)]
                except ValueError:
                    pass
            returndata.append(rowdata)
            i+=1
        return returndata
    
def apply_mod_item_update(project: lookml.Project, moditem: object):
    view_name = moditem['view_name']
    field_name = moditem['field_name']
    view_file = moditem['file_name']
    view_obj = project[view_file]
    field_to_update =  view_obj['views'][view_name][field_name]
    if isinstance(field_to_update, lookml.lookml.Dimension):
        dimension: lookml.lookml.Dimension = field_to_update
        try:
            try:
                if moditem['primary_key'] != "yes" and moditem['primary_key'] != "no":
                    print(moditem['primary_key'] + " is not a valid value for primary_key") 
                else:
                    dimension.primary_key = moditem['primary_key']
            except:
                pass
            try:
                if moditem['description'] != '':
                    if moditem['description'] == '!remove':
                        dimension.description = ''
                    else: 
                        dimension.description = moditem['description']
            except:
                pass
            #TODO: other properties
        except:
            pass
    elif isinstance(field_to_update,lookml.lookml.Measure):
        measure: lookml.lookml.Measure = field_to_update
    project.put(view_obj)

class InvalidDimensionAttributeValue(Exception):
    pass
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_name', dest='repo_name', type=str)
    parser.add_argument('--github_access_token', dest='github_access_token', type=str)
    parser.add_argument('--branch', dest='branch', type=str)
    parser.add_argument('--modifications_file_path', dest='modifications_file_path', type=str)
    args = parser.parse_args()
    main(repo_name=args.repo_name, github_access_token=args.github_access_token, branch=args.branch, modifications_file_path=args.modifications_file_path)
