from ast import arg
from operator import mod
import lookml, argparse

def main(repo_name, github_access_token, source_branch, destination_branch, modifications_file_path):
    project = lookml.Project(
        repo= repo_name,
        access_token=github_access_token
    )

    modifications = parse_modifications_from_file(modifications_file_path)
    for view_file in modifications:
        for field in view_file:
            for property_to_change, new_value in field:
                apply_update_to_property(view_file, field, property_to_change, new_value)
    
def parse_modifications_from_file(filename):
    pass
    
def apply_update_to_property(view_file: lookml.File, view_name, field, property_to_change, new_value):
    field_to_update =  view_file[view_name][field]
    field_type = field_to_update._type
    if field_type == lookml.lookml.Dimension:
        dimension: lookml.lookml.Dimension = field_to_update
        try:
            if property_to_change == 'primary_key':
                if new_value != "yes" and new_value != "no":
                    raise InvalidDimensionAttributeValue(new_value + " is not a valid value for attribute " + property_to_change) 
                else:
                    dimension.primary_key = new_value
            elif property_to_change == '':
                pass
            else:
                raise InvalidDimensionProperty
        except Exception as e:
            print("Failed: " + e)

    elif field_type == lookml.lookml.Measure:
        measure: lookml.lookml.Measure = field_to_update

class InvalidDimensionAttributeValue(Exception):
    pass
    
class InvalidDimensionProperty(Exception):
    pass

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_name', dest='repo_name', type=str)
    parser.add_argument('--access_token', dest='access_token', type=str)
    parser.add_argument('--source_branch', dest='source_branch', type=str)
    parser.add_argument('--destination_branch', dest='destination_branch', type=str)
    parser.add_argument('--modifications_file_path', dest='modifications_file_path', type=str)

    args = parser.parse_args()
    
    main(repo_name=args.repo_name, access_token=args.access_token, source_branch=args.source_branch, destination_branch=args.destination_branch, modifications_file_path=args.modifications_file_path)
