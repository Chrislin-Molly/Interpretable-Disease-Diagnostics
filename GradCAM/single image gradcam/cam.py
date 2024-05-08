import cv2
import numpy as np
import os
import pandas as pd
from configparser import ConfigParser
from generator import AugmentedImageSequence
# from models.keras import ModelFactory
from keras import backend as kb
from keras.layers import Dense
from keras.applications.densenet import DenseNet121  # Import DenseNet model
from keras.models import Model  # Import Model from Keras

def get_output_layer(model, layer_name):
    # get the symbolic outputs of each "key" layer (we gave them unique names).
    layer_dict = dict([(layer.name, layer) for layer in model.layers])
    layer = layer_dict[layer_name]
    return layer


def create_cam(df_g, output_dir, image_source_dir, model, generator, class_names):
    file_name = df_g["file_name"]
    print(f"process image: {file_name}")

    # draw bbox with labels
    img_ori = cv2.imread(filename=os.path.join(image_source_dir, file_name))
    print("img_ori inside cam function:", img_ori)
    print("img_ori.shape inside cam function:", img_ori.shape)
    label = df_g["label"]
    if label == "Infiltrate":
        label = "Infiltration"
    index = class_names.index(label)

    output_path = os.path.join(output_dir, f"{label}.{file_name}")

    img_transformed = generator.load_image(file_name)

    # CAM overlay
    # Get the 512 input weights to the softmax.
    class_weights = model.layers[-1].get_weights()[0]
    final_conv_layer = get_output_layer(model, "bn")
    # print(model.summary())
    get_output = kb.function([model.layers[0].input], [final_conv_layer.output, model.layers[-1].output])
    [conv_outputs, predictions] = get_output([np.array([img_transformed])])
    # print("Prediction is: ",np.argmax(predictions))
    conv_outputs = conv_outputs[0, :, :, :]

    # Create the class activation map.
    cam = np.zeros(dtype=np.float32, shape=(conv_outputs.shape[:2]))
    for i, w in enumerate(class_weights[index]):
        cam += w * conv_outputs[:, :, i]
    # print(f"predictions: {predictions}")
    cam /= np.max(cam)
    cam = cv2.resize(cam, img_ori.shape[:2])
    
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap[np.where(cam < 0.2)] = 0

    # Resize heatmap to match the shape of img_ori
    heatmap_resized = cv2.resize(heatmap, (img_ori.shape[1], img_ori.shape[0]))
    img = heatmap_resized * 0.5 + img_ori

    # add label & rectangle
    # ratio = output dimension / 1024
    ratio = 1
    x1 = int(df_g["x"] * ratio)
    y1 = int(df_g["y"] * ratio)
    x2 = int((df_g["x"] + df_g["w"]) * ratio)
    y2 = int((df_g["y"] + df_g["h"]) * ratio)
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(img, text=label, org=(5, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8, color=(0, 0, 255), thickness=1)
    cv2.imwrite(output_path, img)

# 

import csv
import os

def add_image_to_csv(csv_file, image_path):
    image_name = os.path.basename(image_path)
    finding_label = "Pneumonia"
    bbox = [0, 0, 0, 0]

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Index","Finding Label","x","y","w","h"])
        writer.writerow([image_name, finding_label, 0,0,0,0])

def remove_columns_from_csv(csv_file):
    with open(csv_file, 'w', newline='') as file:
            pass  # Writing nothing will clear the file
# /////////////
def main_exec(image_path):
    # parser config
    config_file = "D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\config.ini"
    cp = ConfigParser()
    cp.read(config_file)

    # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00002980_000.png"
    # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00003028_006.png"
    # default config
    output_dir = cp["DEFAULT"].get("output_dir")
    print(output_dir)
    base_model_name = cp["DEFAULT"].get("base_model_name")
    print(base_model_name) 
    class_names = cp["DEFAULT"].get("class_names").split(",")
    image_source_dir = cp["DEFAULT"].get("image_source_dir")
    image_dimension = cp["TRAIN"].getint("image_dimension")
    print("image source dir:",image_source_dir)
    print("\n")
    # print("img_ori:",image_source_dir)
    print("img_ori image path:",image_path)
    print("\n")

    # parse weights file path
    output_weights_name = cp["TRAIN"].get("output_weights_name")
    weights_path = os.path.join(output_dir, output_weights_name)
    best_weights_path = os.path.join(output_dir, f"best_{output_weights_name}")

    # CAM config
    bbox_list_file = r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\buff.csv"
    use_best_weights = cp["CAM"].getboolean("use_best_weights")
    
    print("** load model **")
    if use_best_weights:
        print("** use best weights **")
        model_weights_path = best_weights_path
    else:
        print("** use last weights **")
        model_weights_path = weights_path
    model_weights_path=r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\experiments\1\best_weights.h5"
    # Load DenseNet model
    base_model = DenseNet121(weights=None, include_top=False, input_shape=(image_dimension, image_dimension, 3))
    x = base_model.output
    x = Dense(len(class_names), activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=x)

    # Load weights into the model
    model.load_weights(model_weights_path)

    print("read bbox list file")
    df_images = pd.read_csv(bbox_list_file, header=None, skiprows=1)
    df_images.columns = ["file_name", "label", "x", "y", "w", "h"]

    print("create a generator for loading transformed images")
    cam_sequence = AugmentedImageSequence(
        dataset_csv_file=r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\experiments\1\test.csv",
        class_names=class_names,
        source_image_dir=image_source_dir,
        batch_size=1,
        target_size=(image_dimension, image_dimension),
        augmenter=None,
        steps=1,
        shuffle_on_epoch_end=False,
    )

    image_output_dir = os.path.join(output_dir, "cam")
    if not os.path.isdir(image_output_dir):
        os.makedirs(image_output_dir)

    print("create CAM-output.")
    df_images.apply(
        lambda g: create_cam(
            df_g=g,
            output_dir=image_output_dir,
            image_source_dir=image_source_dir,
            model=model,
            generator=cam_sequence,
            class_names=class_names,
        ),
        axis=1,
    )

#////////////////////
def main_dev():
    # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00002980_000.png"
    image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00005869_001.png"
    # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00003028_006.png"

    csv_file = r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\buff.csv"
    add_image_to_csv(csv_file, image_path)
    main_exec(image_path)
    # Example: Removing columns at the end
    # columns_to_remove = ["Image Index","Finding Label","x","y","w","h"]
    remove_columns_from_csv(csv_file)

if __name__ == "__main__":
    main_dev()



# # /////////////
# def main_exec():
#     # parser config
#     config_file = "D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\config.ini"
#     cp = ConfigParser()
#     cp.read(config_file)

#     # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00002980_000.png"
#     # image_path =r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\images\00003028_006.png"
#     # default config
#     output_dir = cp["DEFAULT"].get("output_dir")
#     print(output_dir)
#     base_model_name = cp["DEFAULT"].get("base_model_name")
#     print(base_model_name) 
#     class_names = cp["DEFAULT"].get("class_names").split(",")
#     image_source_dir = cp["DEFAULT"].get("image_source_dir")
#     image_dimension = cp["TRAIN"].getint("image_dimension")
#     print("image source dir:",image_source_dir)
#     print("\n")
#     # print("img_ori:",image_source_dir)
#     print("img_ori image path:",image_path)
#     print("\n")

#     # parse weights file path
#     output_weights_name = cp["TRAIN"].get("output_weights_name")
#     weights_path = os.path.join(output_dir, output_weights_name)
#     best_weights_path = os.path.join(output_dir, f"best_{output_weights_name}")

#     # CAM config
#     bbox_list_file = r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\data\buff.csv"
#     use_best_weights = cp["CAM"].getboolean("use_best_weights")
    
#     print("** load model **")
#     if use_best_weights:
#         print("** use best weights **")
#         model_weights_path = best_weights_path
#     else:
#         print("** use last weights **")
#         model_weights_path = weights_path
#     model_weights_path=r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\experiments\1\best_weights.h5"
#     # Load DenseNet model
#     base_model = DenseNet121(weights=None, include_top=False, input_shape=(image_dimension, image_dimension, 3))
#     x = base_model.output
#     x = Dense(len(class_names), activation='softmax')(x)
#     model = Model(inputs=base_model.input, outputs=x)

#     # Load weights into the model
#     model.load_weights(model_weights_path)

#     print("read bbox list file")
#     df_images = pd.read_csv(bbox_list_file, header=None, skiprows=1)
#     df_images.columns = ["file_name", "label", "x", "y", "w", "h"]

#     print("create a generator for loading transformed images")
#     cam_sequence = AugmentedImageSequence(
#         dataset_csv_file=r"D:\Tapasvi\Projects\Main_Project_Fully_Functional\GradCAM\CheXNet-Keras-master\experiments\1\test.csv",
#         class_names=class_names,
#         source_image_dir=image_source_dir,
#         batch_size=1,
#         target_size=(image_dimension, image_dimension),
#         augmenter=None,
#         steps=1,
#         shuffle_on_epoch_end=False,
#     )

#     image_output_dir = os.path.join(output_dir, "cam")
#     if not os.path.isdir(image_output_dir):
#         os.makedirs(image_output_dir)

#     print("create CAM-output.")
#     df_images.apply(
#         lambda g: create_cam(
#             df_g=g,
#             output_dir=image_output_dir,
#             image_source_dir=image_source_dir,
#             model=model,
#             generator=cam_sequence,
#             class_names=class_names,
#         ),
#         axis=1,
#     )

# # if __name__ == "__main__":
# #     main()