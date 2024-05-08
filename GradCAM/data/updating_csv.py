# import os
# import pandas as pd

# # Define paths
# csv_file = "D:\Tapasvi\Projects\Main_Project\DATASET_NIH\pneumonia_only.csv"
# output_folder = "D:\Tapasvi\Projects\Main_Project\DATASET_NIH\Pneumonia_Images\Pnuemonia"

# # Read the CSV file
# data = pd.read_csv(csv_file)

# # Get a list of all image names in the output folder
# output_images = []
# for root, dirs, files in os.walk(output_folder):
#     for file in files:
#         output_images.append(file)

# # Filter rows in the CSV file based on whether the image is in the output folder
# data = data[data['Image Index'].isin(output_images)]

# # Save the updated CSV file
# updated_csv_file = "D:\Tapasvi\Projects\Main_Project\DATASET_NIH\Final_BBox.csv"
# data.to_csv(updated_csv_file, index=False)

# print("Updated CSV file saved.")


import os
import pandas as pd

# Path to the folder containing the images
image_folder = "D:\Tapasvi\Projects\Main_Project\CheXNet-Keras-master\CheXNet-Keras-master\data\images"

# Path to the CSV file
csv_file = r"D:\Tapasvi\Projects\Main_Project\CheXNet-Keras-master\CheXNet-Keras-master\data\filtered_data_2.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Function to check if an image file exists in the folder
def image_exists(image_name):
    print(image_name)
    return os.path.exists(os.path.join(image_folder, image_name))

# Filter out rows where image file does not exist
df_filtered = df[df['Image Index'].apply(image_exists)]

# Path to save the new CSV file
new_csv_file = "filtered_data.csv"

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(new_csv_file, index=False)

print("Filtered CSV file saved successfully.")
