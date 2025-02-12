import open3d as o3d
import numpy as np
import speech_recognition as sr
import pyttsx3
import random
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Define available shapes
shapes = ["Sphere", "Cube", "Cylinder"]

def create_3d_shape(shape_type):
    """Creates a 3D shape based on the given shape_type."""
    if shape_type == "Sphere":
        return o3d.geometry.TriangleMesh.create_sphere(radius=0.8)
    elif shape_type == "Cube":
        return o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
    elif shape_type == "Cylinder":
        return o3d.geometry.TriangleMesh.create_cylinder(radius=0.5, height=1.5)
    return None

def display_shapes():
    """Displays the 3D shapes using Open3D in a structured alignment."""
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    shape_objs = []
    for i, shape in enumerate(shapes):
        obj = create_3d_shape(shape)
        obj.paint_uniform_color(np.random.rand(3))  # Random color
        obj.translate((i * 2.5, 0, 0))  # Better spacing
        vis.add_geometry(obj)
        shape_objs.append(obj)

    vis.run()
    vis.destroy_window()

def list_microphones():
    """Lists all available microphones."""
    print("\n🔍 Available Microphones:")
    mics = sr.Microphone.list_microphone_names()
    
    if not mics:
        print("❌ No microphones found! Check your device settings.")
        return None
    
    for index, mic_name in enumerate(mics):
        print(f"🎤 Microphone {index}: {mic_name}")

    return mics

def recognize_speech():
    """Captures and recognizes speech with error handling."""
    recognizer = sr.Recognizer()

    # List available microphones
    microphones = list_microphones()
    if not microphones:
        return None

    try:
        # Use the first microphone (change index if needed)
        mic_index = 0
        print(f"\n🎙️ Using Microphone: {microphones[mic_index]}")
        
        with sr.Microphone(device_index=mic_index) as source:
            print("🎧 Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            for attempt in range(3):  # Retry up to 3 times
                try:
                    print(f"🎙️ Listening... (Attempt {attempt + 1})")
                    audio = recognizer.listen(source, timeout=5)
                    print("📝 Recognizing speech...")

                    # First, try Google Speech Recognition (online)
                    spoken_text = recognizer.recognize_google(audio)
                    print(f"✅ You said: {spoken_text}")
                    return spoken_text

                except sr.UnknownValueError:
                    print("⚠️ Could not understand the audio! Try again.")
                except sr.WaitTimeoutError:
                    print("⚠️ No speech detected! Speak louder.")
                except sr.RequestError as e:
                    print(f"❌ Google API request failed: {e}")
                    print("🔄 Trying offline recognition (CMU Sphinx)...")

                    # Backup: Try CMU Sphinx (offline recognition)
                    try:
                        spoken_text = recognizer.recognize_sphinx(audio)
                        print(f"✅ You said (offline): {spoken_text}")
                        return spoken_text
                    except sr.UnknownValueError:
                        print("⚠️ Offline recognition also failed. Try again.")
                    except Exception as ex:
                        print(f"❌ CMU Sphinx error: {ex}")

    except Exception as e:
        print(f"❌ Microphone error: {e}")

    return None

def shape_game():
    """Main game function for shape selection."""
    correct_shape = random.choice(shapes)
    shape_index = shapes.index(correct_shape) + 1  # Convert to 1-based index

    print(f"\n🎮 Say the number corresponding to the shape: {correct_shape}")
    engine.say(f"Say the number corresponding to the shape: {correct_shape}")
    engine.runAndWait()

    display_shapes()
    
    user_input = recognize_speech()
    
    if user_input and user_input.isdigit():
        user_choice = int(user_input)
        if user_choice == shape_index:
            print("✅ Correct! Well done!")
            engine.say("Correct! Well done!")
        else:
            print(f"❌ Incorrect! The correct number was {shape_index}. Try again.")
            engine.say(f"Incorrect! The correct number was {shape_index}. Try again.")
    else:
        print("⚠️ Invalid input. Please say 1, 2, or 3.")
        engine.say("Invalid input. Please say one, two, or three.")

    engine.runAndWait()

# Run the shape game
shape_game()
