#!/usr/bin/env python3
"""
Project Generator Script

Usage:
  python3 generate.py                                    # Interactive mode
  python3 generate.py -p MyApp                          # With project name
  python3 generate.py -p MyApp -g com.mycompany.myapp   # With project and group
  python3 generate.py --project MyApp --group com.mycompany.myapp --image myapp
"""

import os
import shutil
import jinja2
import sys
import argparse
from re import sub

def snake(s):
    """Convert string to snake_case."""
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        s.replace('-', ' '))).split()).lower()

def setup_argument_parser():
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(description='Generate a new project from template')
    parser.add_argument('--project', '-p', help='Project name')
    parser.add_argument('--group', '-g', help='Group/package name (e.g., com.example.myproject)')
    parser.add_argument('--image', '-i', help='Docker image name')
    return parser

def get_project_details():
    """Get project details from command line arguments or user input."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Get project name
    if args.project:
        project = args.project.strip()
    else:
        project = input("Enter the project name (default: MyProject): ").strip() or "MyProject"
    
    if not project:
        print("Error: project cannot be empty.")
        sys.exit(1)
    
    project_name_snake = snake(project)
    
    # Get image name
    if args.image:
        image_name = args.image.strip()
    else:
        image_name = input(f"Enter the image name (default: {project_name_snake}): ").strip() or project_name_snake
    
    # Get group
    if args.group:
        group = args.group.strip()
    else:
        group = input(f"Enter the group (default: com.example.{project_name_snake}): ").strip() or f"com.example.{project_name_snake}"
    
    # Exit with error if group is empty
    if not group:
        print("Error: Group cannot be empty.")
        sys.exit(1)
    
    return project, image_name, group

def setup_jinja_environment(template_dir):
    """Set up Jinja2 environment for template processing."""
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    return jinja2.Environment(loader=template_loader)

def replace_placeholders_in_path(path, replacements):
    """Replace placeholders in directory names."""
    parts = path.split(os.sep)
    new_parts = []
    for part in parts:
        for placeholder, replacement in replacements.items():
            part = part.replace(placeholder, replacement)
        new_parts.append(part)
    return os.sep.join(new_parts)

def should_copy_directory_directly(dir_name, direct_copy_items):
    """Check if a directory should be copied directly without processing."""
    return dir_name in direct_copy_items

def copy_directory_directly(src_dir, output_dir, template_dir):
    """Copy a directory directly without template processing."""
    dst_dir = os.path.join(output_dir, os.path.relpath(src_dir, template_dir))
    shutil.copytree(src_dir, dst_dir)
    print(f"Copied directory: {src_dir} -> {dst_dir}")

def copy_file_directly(template_path, output_file_path, replacements):
    """Copy a file directly without template processing."""
    print(f"Copying file: {template_path}")
    output_file_path = replace_placeholders_in_path(output_file_path, replacements)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    shutil.copy2(template_path, output_file_path)

def process_template_file(template_env, template_path, output_file_path, project, image_name, group, replacements):
    """Process a file as a Jinja2 template."""
    try:
        print(f"Processing {template_path} -> {output_file_path}")
        relative_path = os.path.relpath(template_path, "template")
        template = template_env.get_template(relative_path)
        
        # Render the template with the project details
        output = template.render(project=project, image_name=image_name, group=group)
        
        # Replace placeholders in the output file path
        output_file_path = replace_placeholders_in_path(output_file_path, replacements)
        
        # Ensure the output subdirectory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Save the rendered content to the output file
        with open(output_file_path, "w") as f:
            f.write(output)
    except (jinja2.exceptions.TemplateSyntaxError, UnicodeDecodeError):
        # If the file is not a Jinja2 template or has encoding issues, copy it directly
        print(f"Copying file (template error): {template_path}")
        copy_file_directly(template_path, output_file_path, replacements)

def process_files_and_directories(template_dir, output_dir, template_env, project, image_name, group, replacements):
    """Process all files and directories in the template."""
    # List of files and directories to copy directly
    direct_copy_items = {"gradle", "gradlew", "gradlew.bat"}
    
    # Directories to exclude from copying
    excluded_directories = {"build", ".gradle", "target", "out", "bin", ".idea", ".vscode", "__pycache__", "node_modules"}
    
    # Iterate over all files and directories in the template directory
    for root, dirs, files in os.walk(template_dir):
        # Skip the output directory and excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) != output_dir and d not in excluded_directories]

        # Process directories to copy directly
        for dir_name in list(dirs):  # Create a copy to avoid modification during iteration
            if should_copy_directory_directly(dir_name, direct_copy_items):
                src_dir = os.path.join(root, dir_name)
                copy_directory_directly(src_dir, output_dir, template_dir)
                dirs.remove(dir_name)

        # Process files
        for file_name in files:
            template_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(template_path, template_dir)
            output_file_path = os.path.join(output_dir, relative_path)

            # Copy files directly if they are in the direct copy list
            if file_name in direct_copy_items:
                copy_file_directly(template_path, output_file_path, replacements)
                continue

            # Process as template
            process_template_file(template_env, template_path, output_file_path, project, image_name, group, replacements)

def rename_directories_with_placeholders(output_dir, replacements):
    """Rename directories that contain placeholders."""
    for root, dirs, files in os.walk(output_dir, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            new_dir_path = replace_placeholders_in_path(dir_path, replacements)
            if dir_path != new_dir_path:
                print(f"Renaming directory: {dir_path} -> {new_dir_path}")
                os.rename(dir_path, new_dir_path)

def main():
    """Main function to orchestrate the project generation."""
    # Get project details from command line or prompts
    project, image_name, group = get_project_details()
    
    group_directory = group.replace(".", os.sep)
    
    # Set up Jinja2 environment
    template_dir = "template"
    template_env = setup_jinja_environment(f"./{template_dir}")
    
    # Output directory named after the project name
    output_dir = f"./{project}"
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Replacements dictionary
    replacements = {
        "{{project}}": project,
        "{{group}}": group_directory
    }
    
    # Process all files and directories
    process_files_and_directories(template_dir, output_dir, template_env, project, image_name, group, replacements)
    
    # Rename directories with placeholders
    rename_directories_with_placeholders(output_dir, replacements)
    
    print("Project files and directories have been generated.")

if __name__ == "__main__":
    main()