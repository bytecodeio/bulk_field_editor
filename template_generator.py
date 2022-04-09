import lookml, argparse
def main(repo_name, github_access_token, branch, modifications_file_path):
    project = lookml.Project(
        repo= repo_name,
        access_token=github_access_token,
        branch=branch
    )
    project._build_index()
    print(project.dir_list())
    print(project.files())
    output_builder = []
    for v in project.view_files():
        view_file : lookml.ProjectGithub = v
        row_object = {}
        row_object['file_name'] = view_file['name']
        



if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_name', dest='repo_name', type=str)
    parser.add_argument('--github_access_token', dest='github_access_token', type=str)
    parser.add_argument('--branch', dest='branch', type=str, default='master')
    parser.add_argument('--modifications_file_path', dest='modifications_file_path', type=str, default='template.csv')
    args = parser.parse_args()
    main(repo_name=args.repo_name, github_access_token=args.github_access_token, branch=args.branch, modifications_file_path=args.modifications_file_path)
