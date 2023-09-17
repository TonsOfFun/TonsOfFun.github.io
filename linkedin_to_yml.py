import argparse
import re
import os

def extract_skills(text):
    m = re.search(r'Skills: (.+)$', text)
    if m:
        return [skill.strip() for skill in m.group(1).split('·')]
    return []

def convert_to_yaml(input_file):
    with open(input_file, 'r') as file:
        data = file.read()

    # Splits at capitalized words, which usually denote new section titles
    sections = re.split(r'(?=\n[A-Z][a-z]+\s[A-Z][a-z]+)', data.strip())

    yaml_output = "professional_experience:\n"

    for section in sections:
        lines = section.split('\n')
        
        # Extract relevant information
        position_company = lines[0].split('·')
        position = position_company[0].strip()
        company = position_company[1].strip() if len(position_company) > 1 else ""
        duration_line = lines[2]
        start_date = re.search(r'\w+ \d+', duration_line).group(0)
        end_date = "Present" if "Present" in duration_line else re.search(r'- (.+?) ·', duration_line).group(1)
        location = lines[4]
        
        # Creating YAML formatted text
        yaml_output += f"  - position: {position}\n"
        yaml_output += f"    company: {company}\n"
        yaml_output += f"    duration:\n"
        yaml_output += f"      start: {start_date}\n"
        yaml_output += f"      end: {end_date}\n"
        yaml_output += f"    location: {location}\n"
        
        # Check for a skills line and extract
        skills = extract_skills(section)
        if skills:
            yaml_output += "    skills:\n"
            for skill in skills:
                yaml_output += f"      - {skill}\n"

    # Derive the output filename by changing the file extension of the input file to .yaml
    output_file = os.path.splitext(input_file)[0] + '.yml'

    with open(output_file, 'w') as outfile:
        outfile.write(yaml_output)

    print(f"YAML output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert LinkedIn Copy Paste TXT to YAML format.')
    parser.add_argument('input_file', type=str, help='Path to the input text file containing resume data.')
    args = parser.parse_args()

    convert_to_yaml(args.input_file)
