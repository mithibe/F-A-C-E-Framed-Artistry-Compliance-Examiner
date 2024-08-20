import cv2
import mediapipe as mp
import numpy as np

def is_plain_background(input_image_path, threshold=15):
    """
    Check if the background is plain by calculating the color variance.
    A lower variance indicates a more uniform (plain) background.
    
    Args:
    - image: The image in which to check the background.
    - threshold: The threshold for determining if the background is plain.
    
    Returns:
    - Boolean: True if the background is plain, False otherwise.
    """
    # Convert to grayscale
    gray_image = cv2.cvtColor(input_image_path, cv2.COLOR_BGR2GRAY)
    
    # Calculate the variance of the pixel values
    variance = np.var(gray_image)
    
    # Compare variance against threshold
    return variance < threshold

def process_image(input_image_path, output_image_path):
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    
    # Initialize MediaPipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
    
    # Load the input image
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"Error: Unable to load image from path {input_image_path}")
        return False
    
    # Check if the background is plain
    if not is_plain_background(input_image_path):
        print("The background is not plain. Skipping background removal.")
        return False
    
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    results = face_detection.process(image_rgb)

    if results.detections:
        # Perform background removal
        segmentation_results = selfie_segmentation.process(image_rgb)
        mask = segmentation_results.segmentation_mask
        
        # Create a white background
        white_bg = np.ones(image.shape, dtype=np.uint8) * 255
        
        # Create a mask where the detected face region is kept and the background is white
        condition = mask > 0.5
        output_image = np.where(condition[..., None], image, white_bg)

        # Save the output image
        cv2.imwrite(output_image_path, output_image)
        return True
    else:
        print("No face detected.")
        return False
