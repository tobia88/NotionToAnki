import os
import httpx
from config_loader import config_loader

IMAGES_DIR =  config_loader.output_dir + '\\images'

def download_image(url, name):
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    image_path = os.path.join(IMAGES_DIR, f"{name}.jpg")
    if os.path.exists(image_path):
        print(f"Image already exists for: {name}, skipping download.")
        return

    print(f"Downloading image for: {name}")

    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        total = int(response.headers["Content-Length"])
        with open(image_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_bytes():
                f.write(chunk)
                downloaded += len(chunk)
                percentage = (downloaded / total) * 100
                print(f"Downloading {name}: {percentage:.2f}% complete", end='\r')

    print(f"\nImage saved to: {image_path}")


def is_image_downloaded(id: str) -> bool:
    """
    Check if image is already downloaded by if the image name is starting with the id
    """
    is_exists = any(file_name.startswith(f"{id}_") for file_name in os.listdir(IMAGES_DIR))
    return is_exists


def get_absolute_image_url(id: str) -> str:
    """
    Get the absolute image url by the id
    """
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.startswith(f"{id}_"):
            return os.path.join(IMAGES_DIR, file_name)

    return None


def get_all_downloaded_images_paths() -> list[str]:
    """
    Get all downloaded images
    """
    return [file_name for file_name in os.listdir(IMAGES_DIR)]


def get_image_url(id: str) -> str:
    """
    Get the image url by the id
    """
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.startswith(f"{id}_"):
            return file_name

    return None


if __name__ == "__main__":
    paths = get_all_downloaded_images_paths()
    for path in paths:
        print(path)