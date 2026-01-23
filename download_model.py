import os
import urllib.request

def download_hand_model():
    # The official Google URL for the hand landmarker model
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    filename = "hand_landmarker.task"
    
    print(f"📡 Connecting to Google MediaPipe servers...")
    
    try:
        # This downloads the file directly into your current folder
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Success! '{filename}' has been downloaded to: {os.getcwd()}")
    except Exception as e:
        print(f"❌ Error: Could not download the file. {e}")

if __name__ == "__main__":
    download_hand_model()