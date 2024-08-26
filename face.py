import cv2
import mediapipe as mp
import numpy as np

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
        return False, 'Image load error'
    
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
        return True, 'Face detected and background removed'
    else:
        return False, 'No face detected'

