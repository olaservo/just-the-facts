import requests
from bs4 import BeautifulSoup
import re

def get_print_view_url(url):
    """
    Transform the given URL to its print view version.
    This function may need to be adjusted based on the specific website structure.
    """
    # This is a generic transformation and may not work for all websites
    return url + "?print"

def scrape_recipe(url):
    # Get the print view URL
    print_url = get_print_view_url(url)
    
    # Fetch the webpage content
    response = requests.get(print_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the recipe title
    title = soup.find('h1').text.strip() if soup.find('h1') else "Unknown Recipe"
    
    # Find the ingredients list
    ingredients = []
    ingredients_section = soup.find('ul', class_=re.compile('ingredients'))
    if ingredients_section:
        ingredients = [item.text.strip() for item in ingredients_section.find_all('li')]
    
    # Find the instructions
    instructions = []
    instructions_section = soup.find('ol', class_=re.compile('instructions'))
    if instructions_section:
        instructions = [item.text.strip() for item in instructions_section.find_all('li')]
    
    return {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions
    }

# Example usage
if __name__ == "__main__":
    recipe_url = input("Enter the URL of the recipe: ")
    recipe_data = scrape_recipe(recipe_url)
    
    print(f"\nRecipe: {recipe_data['title']}")
    print("\nIngredients:")
    for ingredient in recipe_data['ingredients']:
        print(f"- {ingredient}")
    print("\nInstructions:")
    for i, instruction in enumerate(recipe_data['instructions'], 1):
        print(f"{i}. {instruction}")
