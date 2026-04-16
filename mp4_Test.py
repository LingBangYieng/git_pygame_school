import pygame
import cv2
import sys

# Initialize Pygame
pygame.init()

# Load video with OpenCV
video_path = "assets/StraGOATDreamComesTrue.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    sys.exit()

# Get video size
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create Pygame window
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
        continue

    # Convert BGR (OpenCV) to RGB (Pygame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Flip axes for Pygame (rows -> x, columns -> y)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    # Blit video frame as background
    screen.blit(frame, (0, 0))

    # Here you can draw sprites or other game objects
    # e.g., pygame.draw.rect(screen, (255,0,0), (50,50,100,100))

    pygame.display.update()
    clock.tick(fps)  # Match video FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()