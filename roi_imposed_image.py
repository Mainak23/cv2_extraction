import cv2
import json
import os
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Load the ROI from the JSON file
def load_roi_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def remove_noise_and_deepen_edges(img):
    # Load the image in grayscale
    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(img, (5, 5), 0)
    # Apply median filtering to further reduce noise
    filtered_image = cv2.medianBlur(blurred_image, 5)
    # Apply Sobel operator to detect edges in x and y direction
    sobel_x = cv2.Sobel(filtered_image, cv2.CV_64F, 1, 0, ksize=5)  # X direction
    sobel_y = cv2.Sobel(filtered_image, cv2.CV_64F, 0, 1, ksize=5)  # Y direction
    # Calculate the gradient magnitude
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_magnitude = np.uint8(gradient_magnitude)
    # Threshold the gradient magnitude to create a binary mask
    _, binary_mask = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)
    # Invert the mask to get black edges
    inverted_mask = cv2.bitwise_not(binary_mask)
    # Create a new image to deepen the edges
    result_image = img.copy()
    # Darken the edges based on the inverted mask
    result_image[inverted_mask == 0] = 0  # Set edge areas to black
    # Save the result image
    cv2.imwrite('deepen_edges_cleaned.jpg', result_image)
    print("Image with deepened edges and noise removed saved as 'deepen_edges_cleaned.jpg'")
    return result_image


def extract_segment(image_path, json_path):
    # Read the image in grayscale (no resizing)
    img = cv2.imread(image_path,0)  # Grayscale
    shape_image=img.shape
    # Resize for consistency (adjustable, remove if not needed)
    img_resized = cv2.resize(img, (2000, 900))  # Example resizing, remove if original size needed
    #filtered_image_ = cv2.medianBlur(img_resized, 5)
    # Load ROI coordinates from the JSON file
    roi_data = load_roi_from_json(json_path)
    x = roi_data['x']
    y = roi_data['y']
    width = roi_data['width']
    height = roi_data['height']
    # Create a copy of the image to modify the ROI
    img_with_white_roi = img_resized  .copy()
    print(f"Copied image size: {img_with_white_roi.shape}")
    # Make the region of interest (ROI) white (255)
    img_with_white_roi[y:y + height, x:x + 900] = 255
    img_resized_new = cv2.resize( img_with_white_roi, shape_image)
    #filtered_image_= cv2.medianBlur(img_resized_new , 5)
    # Optional: Apply a blackhat transformation to the ROI (if needed)
    #deepen_edges(img_with_white_roi)
    # Save the modified image with the white ROI
    cv2.imwrite('image_with_white_roi.jpg', img_with_white_roi)

    print("Image with white ROI saved as 'image_with_white_roi.jpg'")

    return img_with_white_roi

image_path = r'C:\Users\USER\Desktop\paid_ocr\process_image_0.png'  # Replace with your image path

json_path = r'C:\Users\USER\Desktop\paid_ocr\roi_data_mouse.json'     # Replace with your JSON path'

new_data=extract_segment(image_path, json_path)


