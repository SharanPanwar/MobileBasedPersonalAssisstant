import os
import pygame


MUSIC_FOLDER = "/path/to/your/music/folder"

Initialize Pygame
pygame.init()


music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

Print the list of music files
print("Music files in the folder:")
for i, file in enumerate(music_files):
print(f"{i+1}. {file}")


selected_file_index = int(input("Enter the file number to play: ")) - 1
selected_file = music_files[selected_file_index]
selected_file_path = os.path.join(MUSIC_FOLDER, selected_file)


pygame.mixer.init()
pygame.mixer.music.load(selected_file_path)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
pygame.time.Clock().tick(10)


pygame.quit()
