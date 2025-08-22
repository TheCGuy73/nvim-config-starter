import os
import sys
import argparse
import subprocess
import datetime

# Define the parser for command-line arguments
parser = argparse.ArgumentParser(description="Creates a Git commit in a specified repository.")

parser.add_argument("--date", action="store_true", help="Includes the date and time in the commit message.")
parser.add_argument("--message", type=str, help="The commit message (required).")
parser.add_argument("--commit-type", type=str, help="The commit type (e.g., FIX, PATCH, UPDATE).")
parser.add_argument("--repo-path", type=str, help="The absolute path to the repository folder (required).")
parser.add_argument("--changelog-apply", action="store_true", help="This activate a 'changelog.md' generation.")
def __git_interface_load(message: str, repo_path: str):
    """
    Performs Git operations: initializes the repo if it doesn't exist,
    adds files, and creates the commit.
    """
    # Check if the repository folder exists, otherwise create it
    if not os.path.isdir(repo_path):
        print(f"The folder '{repo_path}' does not exist. Creating it.")
        os.makedirs(repo_path)

    git_dir = os.path.join(repo_path, '.git')

    # If it's not a Git repository, initialize it
    if not os.path.isdir(git_dir):
        print(f"No Git repository found in '{repo_path}'. Initializing it.")
        try:
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            print("Git repository initialized successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error during Git initialization. Make sure Git is installed and in your PATH.")
            print(f"Error: {e}")
            return

    # Add all files to the staging area and create the commit
    try:
        print("Adding all files to the staging area...")
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        print(f"Creating commit with message: '{message}'")
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        print("Commit created successfully!")
        print(commit_result.stdout)

    except subprocess.CalledProcessError as e:
        # If the commit fails, it might be because there's nothing to commit
        if "nothing to commit" in e.stdout or "niente da committare" in e.stdout:
            print("No changes to commit.")
        else:
            print(f"Error during commit creation:")
            print(e.stderr)

def main():
    """
    Main function that orchestrates the script.
    """
    args = parser.parse_args()

    # Checks for required arguments
    if not args.repo_path:
        print("Error: The repository path (--repo-path) is required.")
        parser.print_help()
        sys.exit(1)
        
    if not args.message:
        print("Error: The commit message (--message) is required.")
        parser.print_help()
        sys.exit(1)

    # Check if git is installed
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        print("'git' is installed, proceeding!")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'git' was not found. Make sure it is installed and accessible in the system's PATH.")
        sys.exit(1)
        
    # Initialize commit message parts
    date_arg = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") if args.date else ""
    message_arg = args.message
    commit_type_arg = ""
    changelog_arg = args.changelog_apply 
    if args.commit_type:
        commit_type_upper = args.commit_type.upper()
        if commit_type_upper in ["FIX", "PATCH", "UPDATE"]:
            commit_type_arg = commit_type_upper
        else:
            print(f"Invalid commit type: '{args.commit_type}'. Valid types are: FIX, PATCH, UPDATE.")
            sys.exit(1)
    
    # Build the final commit message
    prefix_parts = [part for part in [commit_type_arg, date_arg] if part]
    if prefix_parts:
        prefix = f"[{'-'.join(prefix_parts)}]"
        final_message = f"{prefix} {message_arg}"
    else:
        final_message = message_arg
    
    if changelog_arg:
        changelog_path = os.path.join(args.repo_path, "CHANGELOG.md")

        with open(changelog_path, "a") as changelog_file:
            changelog_file.write(f"COMMIT DATE: [{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}]\n")
            changelog_file.write(f"{final_message}\n")
    print(f"Generated commit message: {final_message}")
    
    # Ask for user confirmation
    while True:
        try:
            confirm = input("Do you want to confirm the commit creation? (Y/N): ").upper()
            if confirm == "Y":
                __git_interface_load(final_message, args.repo_path)
                sys.exit(0)
            elif confirm == "N":
                print("Operation cancelled.")
                sys.exit(0)
            else:
                print("Invalid input. Please enter Y or N.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)

if __name__ == "__main__":
    main()