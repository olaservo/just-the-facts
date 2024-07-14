import requests
from bs4 import BeautifulSoup
import yaml
import os
from urllib.parse import urlparse

def load_config(url, config_name=None):
    """
    Load the configuration for a specific website from a YAML file.
    If config_name is not provided, attempt to derive it from the URL.
    """
    if not config_name:
        domain = urlparse(url).netloc
        config_name = domain.split('.')[-2]  # Get the second-level domain

    config_path = os.path.join('configs', f'{config_name}.yaml')
    
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file for {config_name} not found. Please ensure {config_path} exists.")

def get_print_view_url(url, config):
    """
    Transform the given URL to its print view version based on the config.
    """
    print_url_format = config.get('print_url_format', '{url}')
    return print_url_format.format(url=url)

def scrape_recipe(url, config_name=None):
    # Load the configuration for this website
    config = load_config(url, config_name)
    
    # Get the print view URL
    print_url = get_print_view_url(url, config)
    
    # Fetch the webpage content
    response = requests.get(print_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the recipe title
    title_selector = config['selectors']['title']
    title = soup.select_one(title_selector).text.strip() if soup.select_one(title_selector) else "Unknown Recipe"
    
    # Find the ingredients list
    ingredients = []
    ingredients_selector = config['selectors']['ingredients']
    ingredients_section = soup.select_one(ingredients_selector)
    if ingredients_section:
        ingredients = [item.text.strip() for item in ingredients_section.select('li')]
    
    # Find the instructions
    instructions = []
    instructions_selector = config['selectors']['instructions']
    instructions_section = soup.select_one(instructions_selector)
    if instructions_section:
        instructions = [item.text.strip() for item in instructions_section.select('li')]
    
    return {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions
    }

# Example usage
if __name__ == "__main__":
    recipe_url = input("Enter the URL of the recipe: ")
    config_name = input("Enter the config name (or press Enter to auto-detect): ").strip() or None
    
    try:
        recipe_data = scrape_recipe(recipe_url, config_name)
        
        print(f"\nRecipe: {recipe_data['title']}")
        print("\nIngredients:")
        for ingredient in recipe_data['ingredients']:
            print(f"- {ingredient}")
        print("\nInstructions:")
        for i, instruction in enumerate(recipe_data['instructions'], 1):
            print(f"{i}. {instruction}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the configuration file exists in the 'configs' directory.")
    except Exception as e:
        print(f"An error occurred: {e}")