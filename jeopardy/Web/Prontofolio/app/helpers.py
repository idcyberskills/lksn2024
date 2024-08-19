from bs4 import BeautifulSoup
import random
import string

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

def get_page_title(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        title_tag = soup.title
        return title_tag.string if title_tag else "No title found"
    except Exception as e:
        return f"An error occurred: {e}"
    
def extract_image_url(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        img_tag = soup.find('img')
        
        if img_tag and img_tag.has_attr('src'):
            return img_tag['src']
        else:
            return 'https://via.placeholder.com/300'
    except Exception as e:
        return f"An error occurred: {e}"