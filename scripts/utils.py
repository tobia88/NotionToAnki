import os
import httpx

IMAGES_DIR = 'images'

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