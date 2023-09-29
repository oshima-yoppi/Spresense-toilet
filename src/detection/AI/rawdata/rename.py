import os


images_paths = os.listdir("images")
masks_paths = os.listdir("masks")

for path in images_paths:
    os.rename("images/" + path, "images/" + path.replace(" 小", ""))
for path in masks_paths:
    os.rename("masks/" + path, "masks/" + path.replace(" 小", ""))