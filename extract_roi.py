import cv2
import json
import os

# Initialize global variables
drawing = False
start_point = (-1, -1)
end_point = (-1, -1)
roi_data = {}
image_resized = None

# Function to resize the image to fit the screen
def resize_image(image, max_width=2000, max_height=900):
    height, width = image.shape[:2]
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width / max_width > height / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        return image  # No resizing needed if the image is already smaller

    return cv2.resize(image, (new_width, new_height))

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, drawing, roi_data, image_resized
    
    # When the left mouse button is pressed, start drawing the rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    
    # While moving the mouse, update the end point of the rectangle
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
            img_copy = image_resized.copy()
            cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow("Draw ROI", img_copy)
    
    # When the left mouse button is released, finalize the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        cv2.rectangle(image_resized, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Draw ROI", image_resized)
        
        # Calculate width and height of the ROI
        x1, y1 = start_point
        x2, y2 = end_point
        roi_data = {
            "x": min(x1, x2),
            "y": min(y1, y2),
            "width": abs(x2 - x1),
            "height": abs(y2 - y1)
        }
    

        # Crop the image using the ROI coordinates

# Load the image
image_path = r'C:\Users\USER\Desktop\paid_ocr\process_image_0.png'  # Replace with your image path
img = cv2.imread(image_path)

# Resize the image to fit the screen
image_resized = resize_image(img)

        # Save the cropped image as JPG
# Create a window and set the mouse callback function
cv2.namedWindow("Draw ROI")
cv2.setMouseCallback("Draw ROI", draw_rectangle)

# Display the resized image and allow the user to draw the ROI
while True:
    cv2.imshow("Draw ROI", image_resized)
    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# Save the ROI data into a JSON file
json_file_path = 'roi_data_mouse.json'
with open(json_file_path, 'w') as json_file:
    json.dump(roi_data, json_file, indent=4)

print(f"ROI data has been saved to {json_file_path}")
