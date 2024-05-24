"""Utility functions used in the project"""

from PIL import Image, UnidentifiedImageError
import os
import sys
import pygame

def browse_graphic():
    # Initialize Pygame
    pygame.init()

    # Set up display
    screen_width, screen_height = 400, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Image Viewer')

    # Load images from a folder
    def load_images(path):
        images = [[None for _ in range(55)] for _ in range(21)]
        for x in range(21):
            for y in range(55):
                filename = f"tile_{x}_{y}.png"
                img = pygame.image.load(os.path.join(path, filename))
                img = pygame.transform.scale(img, (screen_width, screen_height))  # Scale images to fit screen
                images[x][y] = img
        return images


    running = True
    image_folder = "tiles"  # Set the path to your images folder
    images = load_images(image_folder)
    current_image = [0, 0]

    if not images:
        print("No images found in the folder.")
        sys.exit()

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 50)

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_image[0] = (current_image[0] + 1) % (len(images[0]) - 1)  # Next image
                elif event.key == pygame.K_LEFT:
                    current_image[0] = (current_image[0] - 1) % (len(images[0]) - 1)  # Previous image
                if event.key == pygame.K_UP:
                    current_image[1] = (current_image[1] - 1) % (len(images[1]) - 1)  # Next imaage
                elif event.key == pygame.K_DOWN:
                    current_image[1] = (current_image[1] + 1) % (len(images[1]) - 1)  # Previous image

        # Display current image
        screen.fill((0, 0, 0))  # Clear screen with black
        screen.blit(images[current_image[1]][current_image[0]], (0, 0))
        text_surface = my_font.render(f'{current_image[1]}_{current_image[0]}', False, (255, 255, 255))
        screen.blit(text_surface, (0,0))
        pygame.display.flip()  # Update display

    pygame.quit()

def slice_image():

    image_path = "tiles\\tiles.png"
    tile_width = 32  # Set your tile width
    tile_height = 32  # Set your tile height
    output_dir = "tiles"

    # Open the image file
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    # Calculate the number of tiles in each dimension
    tiles_x = img_width // tile_width
    tiles_y = img_height // tile_height

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Slice the image into tiles
    for y in range(1, tiles_y):
        for x in range(tiles_x):
            left = x * tile_width
            upper = y * tile_height
            right = left + tile_width
            lower = upper + tile_height
            
            # Crop the tile and resize
            tile = img.crop((left, upper, right, lower))
            tile = tile.resize((60, 60))
            
            # Save the tile
            tile_filename = f"tile_{y-1}_{x}.png"
            tile.save(os.path.join(output_dir, tile_filename))

    print(f"Sliced image into {tiles_x * tiles_y} tiles.")

def overlay_images(input_paths : list[str], output_path : str, display : bool = False) -> Image.Image:

    if len(input_paths) < 2:
        raise ValueError("Cannot overlay less then 2 images")
    
    try:
        # Open the background image
        background = Image.open(input_paths[0]).convert("RGBA")

        # Open the overlay images
        overlays = []
        for path in input_paths[1:]:
            overlays.append(Image.open(path).convert("RGBA"))

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {input_paths} was not found.")
    
    except UnidentifiedImageError:
        raise UnidentifiedImageError(f"The file at {input_paths} could not be identified as an image.")
    
    except OSError:
        raise OSError(f"An error occurred while trying to open the file at {input_paths}.")

    for overlay in overlays:
        # Paste the overlay image on the background image
        background = Image.alpha_composite(background, overlay)

    # Save the combined image
    background.save(output_path)

    # Display the combined image (optional)
    if display: 
        background.show()

def prepare_graphics():
    """
    # get tiles
    slice_image()

    # grass
    os.system("copy tiles\\tile_1_1.png tiles\\grass.png")
    # paths straight
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_7_7.png"], "tiles\\path_hor.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_9_5.png"], "tiles\\path_ver.png")
    # paths corners
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_6_4.png"], "tiles\\path_cor_b_r.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_6_6.png"], "tiles\\path_cor_b_l.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_8_4.png"], "tiles\\path_cor_t_r.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_8_6.png"], "tiles\\path_cor_t_l.png")
    # paths crossing
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_7_5.png"], "tiles\\path_cros.png")
    # paths ends
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_9_4.png"], "tiles\\path_end_l.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_9_6.png"], "tiles\\path_end_r.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_6_7.png"], "tiles\\path_end_t.png")
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_8_7.png"], "tiles\\path_end_b.png")
    # cave
    overlay_images(["tiles\\tile_1_1.png", "tiles\\tile_19_26.png"], "tiles\\slope_l.png") 
    os.system("copy tiles\\tile_14_1.png tiles\\cave.png")
    overlay_images(["tiles\\tile_1_1.png", "tiles\\tile_19_25.png"], "tiles\\slope_r.png")
    # chest
    overlay_images(["tiles\\tile_1_5.png", "tiles\\tile_17_52.png"], "tiles\\chest.png")
    overlay_images(["tiles\\path_end_l.png", "tiles\\tile_17_52.png"], "tiles\\chest_l.png")
    overlay_images(["tiles\\path_end_r.png", "tiles\\tile_17_52.png"], "tiles\\chest_r.png")
    overlay_images(["tiles\\path_end_t.png", "tiles\\tile_17_52.png"], "tiles\\chest_t.png")
    # plants
    overlay_images(["tiles\\grass.png", "tiles\\tile_9_8.png"], "tiles\\plant0.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_9_9.png"], "tiles\\plant1.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_9_10.png"], "tiles\\plant2.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_9_11.png"], "tiles\\plant3.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_10_13.png"], "tiles\\plant4.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_10_14.png"], "tiles\\plant5.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_10_15.png"], "tiles\\plant6.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_11_13.png"], "tiles\\plant7.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_11_14.png"], "tiles\\plant8.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_11_15.png"], "tiles\\plant9.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_8.png"], "tiles\\plant10.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_9.png"], "tiles\\plant11.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_10.png"], "tiles\\plant12.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_11.png"], "tiles\\plant13.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_12.png"], "tiles\\plant14.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_13.png"], "tiles\\plant15.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_14.png"], "tiles\\plant16.png")
    overlay_images(["tiles\\grass.png", "tiles\\tile_17_15.png"], "tiles\\plant17.png")
    #"""

browse_graphic()
prepare_graphics()