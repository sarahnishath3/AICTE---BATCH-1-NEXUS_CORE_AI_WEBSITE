import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return

    # Replacements
    new_content = content.replace("Skill Seekers", "Nexus Core")
    new_content = new_content.replace("skill-seekers", "nexus-core")
    new_content = new_content.replace("skill_seekers", "nexus_core")
    new_content = new_content.replace("Skill_Seekers", "Nexus_Core")
    new_content = new_content.replace("skillseekersweb", "nexuscoreweb")
    new_content = new_content.replace("logo.svg", "logo.png") # Update logo reference for website

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")

def process_dir(directory):
    for root, dirs, files in os.walk(directory):
        # exclude some dirs
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.venv', 'dist', 'build', '__pycache__']]
        for file in files:
            # only process text files
            if file.endswith(('.md', '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.json', '.yml', '.yaml', '.txt', '.toml', '.mjs', '.astro')):
                replace_in_file(os.path.join(root, file))

process_dir(r"D:\skills_project_09\Skill_Seekers")
process_dir(r"D:\skills_project_09\skillseekersweb")
print("Done replacing text.")
