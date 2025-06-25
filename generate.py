#!/usr/bin/env python3

import os
import shutil
import jinja2
import sys
from re import sub

def snake(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()

# Prompt the user for project name and group
project = input("Enter the project name (default: MyProject): ").strip() or "MyProject"

if not project:
    print("Error: project cannot be empty.")
    sys.exit(1)

project_name_snake = snake(project)

image_name = input(f"Enter the image name (default: {project_name_snake}): ").strip() or project_name_snake

group = input(f"Enter the group (default: com.example.{project_name_snake}): ").strip() or f"com.example.{project_name_snake}"

# Exit with error if group is empty
if not group:
    print("Error: Group cannot be empty.")
    sys.exit(1)

group_directory = group.replace(".", os.sep)

# Set up Jinja2 environment
template_loader = jinja2.FileSystemLoader(searchpath="./template")
template_env = jinja2.Environment(loader=template_loader)

# Directory containing the templates
template_dir = "template"

# Output directory named after the project name
output_dir = f"./{project}"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to replace placeholders in directory names
def replace_placeholders_in_path(path, replacements):
    parts = path.split(os.sep)
    new_parts = []
    for part in parts:
        for placeholder, replacement in replacements.items():
            part = part.replace(placeholder, replacement)
        new_parts.append(part)
    return os.sep.join(new_parts)

# Replacements dictionary
replacements = {
    "{{project}}": project,
    "{{group}}": group_directory
}

# List of files and directories to copy directly
direct_copy_items = {"gradle", "gradlew", "gradlew.bat"}

# Directories to exclude from copying
excluded_directories = {"build", ".gradle", "target", "out", "bin", ".idea", ".vscode", "__pycache__", "node_modules"}

# Iterate over all files and directories in the template directory
for root, dirs, files in os.walk(template_dir):
    # Skip the output directory and excluded directories
    dirs[:] = [d for d in dirs if os.path.join(root, d) != output_dir and d not in excluded_directories]

    # Process directories to copy directly
    for dir_name in direct_copy_items:
        if dir_name in dirs:
            src_dir = os.path.join(root, dir_name)
            dst_dir = os.path.join(output_dir, os.path.relpath(src_dir, template_dir))
            shutil.copytree(src_dir, dst_dir)
            dirs.remove(dir_name)

    # Process files
    for file_name in files:
        template_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(template_path, template_dir)
        output_file_path = os.path.join(output_dir, relative_path)

        # Copy files directly if they are in the direct copy list
        if file_name in direct_copy_items:
            print(f"Copying file: {template_path}")
            output_file_path = replace_placeholders_in_path(output_file_path, replacements)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            shutil.copy2(template_path, output_file_path)
            continue

        try:
            print(f"Processing {template_path} -> {output_file_path}")
            # Try to load the file as a Jinja2 template
            template = template_env.get_template(relative_path)

            # Render the template with the project name and group
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
            output_file_path = replace_placeholders_in_path(output_file_path, replacements)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            shutil.copy2(template_path, output_file_path)

# Process directories
for root, dirs, files in os.walk(output_dir, topdown=False):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        new_dir_path = replace_placeholders_in_path(dir_path, replacements)
        if dir_path != new_dir_path:
            os.rename(dir_path, new_dir_path)

print("Project files and directories have been generated.")