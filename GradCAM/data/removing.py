import os
import shutil

def remove_extra_images(folder1, folder2):
    # Get the list of files in folder1
    files_folder1 = set(os.listdir(folder1))
    
    # Get the list of files in folder2
    files_folder2 = os.listdir(folder2)
    
    # Iterate over files in folder2
    for file_name in files_folder2:
        # Check if the file exists in folder1
        if file_name not in files_folder1:
            # If the file does not exist in folder1, remove it from folder2
            file_path = os.path.join(folder2, file_name)
            os.remove(file_path)
            print(f"Removed {file_name} from folder2.")

# Path to folder 1
folder1_path = "D:\Tapasvi\Projects\Main_Project\CheXNet-Keras-master\CheXNet-Keras-master\data\cam(op)"

# Path to folder 2
folder2_path = "D:\Tapasvi\Projects\Main_Project\CheXNet-Keras-master\CheXNet-Keras-master\data\images"

# Call the function to remove extra images from folder2
remove_extra_images(folder1_path, folder2_path)
