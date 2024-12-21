from google_images_search import GoogleImagesSearch
import os

# Set up your Google Custom Search API credentials
api_key = 'AIzaSyC6br5zLu_Pc-AWjYSci9-BkCslLpQJGdM'  # Replace with your API key
cx = 'f4fdeeeadc50849b6'     # Replace with your Search Engine ID

# Create a GoogleImagesSearch object
gis = GoogleImagesSearch(api_key, cx)

# Get user inputs
search_term = input("Enter the search term: ")
num_images = int(input("Enter the number of images to download: "))
output_folder = "google_images"

# Ensure the output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define search parameters
search_params = {
    'q': search_term,
    'num': num_images,  # Number of images to download
    'safe': 'high',     # Safe search filter
    'fileType': 'jpg|png',
    'imgType': 'photo',
    'imgSize': 'MEDIUM'
}

# Perform the search and download images
def download_images():
    gis.search(search_params=search_params, path_to_dir=output_folder, custom_image_name=search_term)
    print(f"Downloaded images to folder: {output_folder}")

# Run the function to download images
download_images()
