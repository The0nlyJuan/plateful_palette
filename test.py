import requests

def fetch_wikibook_content(title):
    url = "https://en.wikibooks.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'revisions',
        'titles': title,
        'rvprop': 'content',
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        page_id, page_info = next(iter(pages.items()))
        page_content = page_info.get('revisions', [{}])[0].get('*', '')
        
        # Handle redirects
        if '#REDIRECT' in page_content:
            redirect_target = page_content.split('[[', 1)[1].split(']]', 1)[0].strip()
            if not redirect_target.startswith('Cookbook:'):
                redirect_target = 'Cookbook:' + redirect_target
            return fetch_wikibook_content(redirect_target.replace(' ', '_'))
        
        return page_content
    else:
        return None

def extract_information(content):
    ingredients, procedures, notes = [], [], []
    
    # Normalize the content to ensure uniformity
    normalized_content = content.replace("==Ingredients==", "== Ingredients ==") \
                                .replace("==Procedure==", "== Procedure ==") \
                                .replace("==Notes, tips, and variations==", "== Notes, tips, and variations ==")
    
    # Extract the ingredients
    if "== Ingredients ==" in normalized_content:
        ingredients_section = normalized_content.split("== Ingredients ==")[1].split("== Procedure ==")[0]
        ingredients = parse_section(ingredients_section)
    
    # Extract the procedures
    if "== Procedure ==" in normalized_content:
        procedure_section = normalized_content.split("== Procedure ==")[1].split("== Notes")[0]
        procedures = parse_section(procedure_section)
    
    # Extract the notes
    if "== Notes, tips, and variations ==" in normalized_content:
        notes_section = normalized_content.split("== Notes, tips, and variations ==")[1]
        notes = []
        for line in notes_section.split('\n'):
            line = line.strip()
            if line.startswith('[[Category:') or line.startswith("=="):
                break  # Stop if a category starts
            if line:
                notes.append(line)
    
    return ingredients, procedures, notes

def parse_section(section):
    parsed_list = []
    current_sublist = []
    current_header = None

    in_table = False
    table_content = []
    headers = []

    for line in section.split('\n'):
        line = line.strip()
        if line.startswith('==='):
            if current_sublist:
                parsed_list.append(current_sublist)
                current_sublist = []
            current_header = line.replace('=', '').strip()
            current_sublist.append(f"= {current_header}")
        elif line.startswith('[[Category') or line.startswith('=='):
            break
        elif line.startswith('{| class="wikitable"'):
            in_table = True
        elif line.startswith('|}') and in_table:
            in_table = False
            if headers:
                table_content.insert(0, headers)
            current_sublist.append(format_table(table_content))
            table_content = []
            headers = []
        elif in_table:
            if line.startswith('!'):
                headers.append(line.replace('!', '').strip())
            elif line.startswith('|-'):
                table_content.append([])  # Initialize a new row
            elif line.startswith('|'):
                if not table_content:
                    table_content.append([])  # Ensure there's a row to append to
                table_content[-1].append(line.replace('|', '').strip())
        elif line:
            current_sublist.append(line)
    
    if current_sublist:
        parsed_list.append(current_sublist)
    
    return parsed_list

def format_table(table):
    formatted_table = []
    headers = table.pop(0)
    formatted_table.append(" | ".join(headers))
    for row in table:
        formatted_table.append(" | ".join(row))
    return "\n".join(formatted_table)

# Example usage
title = "Cookbook:Drawn_butter"
content = fetch_wikibook_content(title)

print(content)
if content:
    ingredients, procedures, notes = extract_information(content)
    
    print("Ingredients:")
    for sublist in ingredients:
        if isinstance(sublist, list):
            for item in sublist:
                if isinstance(item, list):  # Table content
                    print(" | ".join(item))
                else:
                    print(f"- {item}")
        else:
            print(f"- {sublist}")
        print("\n")
    
    print("Procedures:")
    for sublist in procedures:
        if isinstance(sublist, list):
            for step in sublist:
                print(f"- {step}")
        else:
            print(f"- {sublist}")
        print("\n")
    
    print("Notes:")
    for note in notes:
        print(f"- {note}")
else:
    print("Failed to retrieve data from Wikibooks.")
