import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import cv2
import mediapipe as mp
from threading import Thread
import time
import numpy as np
import pygame
import random
import os
import tkinter as tk
import sounddevice as sd
import threading


class PokemonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catching Pokemon Game!")
        self.game_running = False
        pygame.mixer.init() 
        self.play_background_music()
        self.current_menu_index = 0
        self.hand_state = "open"  # Default hand state
        self.buttons = []
        self.last_button_time = 0  # Cooldown for button press
        self.sound_tracking_active = False  # Flag for sound tracking activity
        self.hand_tracking_active = False  # Flag for hand tracking activity
        self.sound_tracking_thread = None
        self.track_hand_thread = None
        self.menu_screen()

    def play_background_music(self):
        try:
            # Đường dẫn tới nhạc nền
            background_music_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON\\BG_MUSIC.mp3"
            if os.path.exists(background_music_path):
                pygame.mixer.music.load(background_music_path)  # Tải nhạc nền
                pygame.mixer.music.play(-1, 0.0)  # Phát nhạc liên tục (-1 để lặp lại vô hạn)
            else:
                print("Không tìm thấy tệp nhạc nền.")
        except Exception as e:
            print(f"Lỗi khi phát nhạc nền: {e}")

    def menu_screen(self):
        self.clear_screen()

        self.canvas = tk.Canvas(self.root, width=1360, height=760)
        self.canvas.pack()

        self.play_gif_background(self.canvas)

        # Create the buttons for the menu screen
        self.buttons = [
            self.create_button("Tutorial", self.tutorial_screen, 700, 350),
            self.create_button("Play Game", self.start_game, 700, 450),
            self.create_button("Exit Game", self.root.quit, 700, 550),
        ]
        self.current_menu_index = 0
        self.highlight_button(self.buttons[self.current_menu_index])

        # Start hand tracking only if not active
        if not self.hand_tracking_active:
            self.hand_tracking_active = True
            self.track_hand_thread = threading.Thread(target=self.track_hand_menu, daemon=True)
            self.track_hand_thread.start()

        # Start sound detection only if not active
        if not self.sound_tracking_active:
            self.sound_tracking_active = True
            self.sound_tracking_thread = threading.Thread(target=self.track_sound_menu, daemon=True)
            self.sound_tracking_thread.start()

    def play_gif_background(self, canvas):
        gif_path = "C:\\Users\\Admin\\Desktop\\CATCHING POKEMON\\MENU_BG.png"
        self.frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(gif_path))]

        def update(ind):
            frame = self.frames[ind % len(self.frames)]
            canvas.create_image(0, 0, anchor="nw", image=frame)
            self.root.after(100, update, ind + 1)

        update(0)


    def play_catch_sound(self):
        """
        Phát âm thanh khi bắt được Pokémon.
        """
        try:
            # Đường dẫn tới tệp âm thanh
            catch_sound_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON\\CATCHING_SOUND.mp3"
            
            # Kiểm tra xem tệp âm thanh có tồn tại không
            if os.path.exists(catch_sound_path):
                # Sử dụng mixer.Sound để phát âm thanh
                sound = pygame.mixer.Sound(catch_sound_path)
                sound.play()
            else:
                print(f"Không tìm thấy tệp âm thanh: {catch_sound_path}")
        except Exception as e:
            print(f"Lỗi khi phát âm thanh: {e}")


    def create_button(self, text, command, x, y):
        button = tk.Button(
            self.root,
            text=text,
            font=("Black Ops One", 24),
            bg="white",
            fg="black",
            relief="raised",
            highlightbackground="white",
            highlightthickness=2,
            command=command  # Giữ lại command gốc, không cần âm thanh khi chọn nút
        )
        self.canvas.create_window(x, y, window=button, width=200, height=60)
        return button


    def highlight_button(self, button):
        def play_hover_sound():
            try:
                hover_sound_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON\\CHANGE_BUTTON.mp3"
                if os.path.exists(hover_sound_path):
                    sound = pygame.mixer.Sound(hover_sound_path)
                    sound.play()
            except Exception as e:
                print(f"Lỗi khi phát âm thanh chuyển nút: {e}")

        # Đặt mặc định cho tất cả các nút
        for btn in self.buttons:
            btn.config(
                bg="white",
                highlightbackground="white",  # Màu viền khi không chọn
                highlightthickness=2,
                relief="raised",
            )

        # Thay đổi nút được chọn
        button.config(
            bg="lightgreen",
            highlightbackground="#34D399",  # Màu viền
            highlightthickness=4,
            relief="solid",
        )

        # Phát âm thanh khi chuyển nút
        play_hover_sound()


    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tutorial_screen(self):
        self.stop_hand_tracking()
        self.stop_sound_tracking()
        self.clear_screen()

        self.canvas = tk.Canvas(self.root, width=1360, height=760, bg="lightgreen")
        self.canvas.pack()
        self.canvas.create_text(640, 100, text="Tutorial", font=("Black Ops One", 60), fill="black")

        instructions = (
            "1. Move your hand in front of the camera to control the hand cursor.\n"
            "2. Catch the Pokémon by closing your hand when hovering over it.\n"
            "3. Each Pokémon has different points based on rarity.\n"
            "4. You have 60 seconds to catch as many Pokémon as possible.\n\n"
            "Good luck, Trainer!"
        )
        self.canvas.create_text(640, 300, text=instructions, font=("Black Ops One", 18), fill="black", justify="center")

        self.buttons = [
            self.create_button("BACK", self.menu_screen, 640, 550)
        ]
        self.current_menu_index = 0
        self.highlight_button(self.buttons[self.current_menu_index])

        # Start sound detection for the BACK button but only if not already active
        if not self.sound_tracking_active:
            self.sound_tracking_active = True
            self.sound_tracking_thread = threading.Thread(target=self.track_sound_tutorial, daemon=True)
            self.sound_tracking_thread.start()

    def start_game(self):
        self.stop_hand_tracking()
        self.stop_sound_tracking()
        self.game_running = True
        self.clear_screen()
        pygame.mixer.music.stop() 
        self.initialize_game()

    def stop_hand_tracking(self):
        self.hand_tracking_active = False
        if self.track_hand_thread and self.track_hand_thread.is_alive():
            self.track_hand_thread = None

    def stop_sound_tracking(self):
        self.sound_tracking_active = False
        if self.sound_tracking_thread and self.sound_tracking_thread.is_alive():
            self.sound_tracking_thread = None

    def track_hand_menu(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Couldn't open camera.")
            return

        with mp.solutions.hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
            while self.hand_tracking_active:
                success, frame = cap.read()
                if not success:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Get landmarks for each finger except the thumb (index 1-4)
                        index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                        middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                        ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
                        pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
                        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                        thumb_cmc = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_CMC]

                        # Calculate distances between the thumb and other fingers to determine if thumb is extended
                        distance_thumb_index = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
                        distance_thumb_middle = ((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2) ** 0.5
                        distance_thumb_ring = ((thumb_tip.x - ring_tip.x) ** 2 + (thumb_tip.y - ring_tip.y) ** 2) ** 0.5
                        distance_thumb_pinky = ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2) ** 0.5

                        # Determine if the "like" gesture is made:
                        thumb_extended = ((thumb_tip.x - thumb_cmc.x) ** 2 + (thumb_tip.y - thumb_cmc.y) ** 2) ** 0.5 > 0.1
                        other_fingers_curled = (distance_thumb_index < 0.05 and distance_thumb_middle < 0.05 and
                                                distance_thumb_ring < 0.05 and distance_thumb_pinky < 0.05)

                        current_time = time.time()

                        # Check if the "like" gesture is made and trigger button press
                        if thumb_extended and other_fingers_curled:
                            if current_time - self.last_button_time > 0.5:
                                self.last_button_time = current_time
                                # Ensure that the current_menu_index is valid and that the button exists
                                if self.buttons and 0 <= self.current_menu_index < len(self.buttons):
                                    button = self.buttons[self.current_menu_index]
                                    if button.winfo_exists():  # Ensure the button still exists in the UI
                                        button.invoke()

                        # Pinch gesture: navigate to next button (thumb and index finger close)
                        elif distance_thumb_index < 0.05:
                            if current_time - self.last_button_time > 0.5:
                                self.last_button_time = current_time
                                self.current_menu_index = (self.current_menu_index + 1) % len(self.buttons)
                                self.highlight_button(self.buttons[self.current_menu_index])

            cap.release()

    def track_sound_menu(self):
        # Sampling rate and the duration of a sample window
        fs = 44100  # Sample rate (Hz)
        duration = 0.6  # Duration of the sample window (seconds)

        while self.sound_tracking_active:
            # Record sound from the microphone
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
            sd.wait()  # Wait for the recording to finish

            # Convert the audio signal to an absolute value and calculate the peak volume
            peak_volume = np.max(np.abs(recording))

            # If the peak volume is greater than a higher threshold, consider it a "clap"
            if peak_volume > 0.6:  # Increased threshold for detecting a clap (tune as needed)
                current_time = time.time()

                if current_time - self.last_button_time > 1.0:  # Avoid double trigger with longer cooldown
                    self.last_button_time = current_time
                    # Ensure that the current_menu_index is valid and that the button exists
                    if self.buttons and 0 <= self.current_menu_index < len(self.buttons):
                        button = self.buttons[self.current_menu_index]
                        if button.winfo_exists():  # Ensure the button still exists in the UI
                            button.invoke()

            # Small delay to prevent constant firing of the action
            time.sleep(0.1)

    def track_sound_tutorial(self):
        # Sampling rate and the duration of a sample window
        fs = 44100  # Sample rate (Hz)
        duration = 0.6  # Duration of the sample window (seconds)

        while self.sound_tracking_active:
            # Record sound from the microphone
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
            sd.wait()  # Wait for the recording to finish

            # Convert the audio signal to an absolute value and calculate the peak volume
            peak_volume = np.max(np.abs(recording))

            # If the peak volume is greater than a higher threshold, consider it a "clap"
            if peak_volume > 0.6:  # Increased threshold for detecting a clap (tune as needed)
                current_time = time.time()

                if current_time - self.last_button_time > 1.0:  # Avoid double trigger with longer cooldown
                    self.last_button_time = current_time
                    # Ensure that the current_menu_index is valid and that the button exists
                    if self.buttons and 0 <= self.current_menu_index < len(self.buttons):
                        button = self.buttons[self.current_menu_index]
                        if button.winfo_exists():  # Ensure the button still exists in the UI
                            # Only invoke if the user is still on the tutorial screen
                            if button['text'] == "BACK":
                                button.invoke()

            # Small delay to prevent constant firing of the action
            time.sleep(0.1)



    def initialize_game(self):
        self.root.config(cursor="none")

        pygame.mixer.init()
        self.load_music()

        self.canvas = tk.Canvas(self.root, width=1280, height=650)
        self.canvas.pack()

        self.load_images()

        self.score = 0
        self.score_label = tk.Label(self.root, text=f"SCORE: {self.score}", font=("Bytebounce", 40))

        self.time_left = 60
        self.timer_label = tk.Label(self.root, text=f"TIME LEFT: {self.time_left}s", font=("Bytebounce", 40))

        # Create a frame to center the labels horizontally
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=20)  # This frame will fill the entire width of the root window

        # Center the score label and time label inside the frame
        self.score_label.pack(side="left", padx=260)  # Small gap to the right of the score label
        self.timer_label.pack(side="left", padx=120)  # Small gap to the left of the time label

        # Align the entire frame to the center of the root window
        top_frame.place(relx=0.5, rely=0.05, anchor="center")

        self.setup_game_data()

        self.current_pokemon = None
        self.show_pokemon()
        self.update_timer()

        self.hand_tracking_thread = threading.Thread(target=self.track_hand, daemon=True)
        self.hand_tracking_thread.start()

        self.load_map_layers()
        self.animate_layers()

    def load_map_layers(self):
        try:
            self.layers = []

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\GRASS1_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.1})  # Di chuyển chậm hơn

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\GRASS2_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.1})  # Di chuyển chậm hơn

            # Layer 1: Grass - Lớp gần
            grass_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\WATER1_LAYER.png"
            grass_layer = ImageTk.PhotoImage(Image.open(grass_path))
            grass_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=grass_layer)
            self.layers.append({"id": grass_layer_id, "image": grass_layer, "speed": 0.2})  # Di chuyển nhanh hơn

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\WATER2_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.1})  # Di chuyển chậm hơn

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\FLOWER_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.2})  # Di chuyển chậm hơn

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\LEAF_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.2})  # Di chuyển chậm hơn

            # Layer 2: Rocks - Lớp trung
            rocks_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\CLOUD_LAYER.png"
            rocks_layer = ImageTk.PhotoImage(Image.open(rocks_path))
            rocks_layer_id = self.canvas.create_image(0, 0, anchor="nw", image=rocks_layer)
            self.layers.append({"id": rocks_layer_id, "image": rocks_layer, "speed": 0.2})  # Di chuyển chậm hơn

            print("Layers loaded successfully.")
        except Exception as e:
            print(f"Error loading map layers: {e}")

    def animate_layers(self):
        if not hasattr(self, 'layer_directions'):
            # Initialize directions for each layer
            self.layer_directions = [1 for _ in self.layers]

        for i, layer in enumerate(self.layers):
            dx = layer["speed"]  # Adjusted horizontal speed for each layer
            dy = 0  # Vertical movement (can be adjusted if needed)

            # Reverse direction if the layer hits a boundary
            layer_id = layer['id']
            coords = self.canvas.coords(layer_id)
            if coords:
                x, y = coords
                if x <= -3 or x >= 3:  # Adjust range based on your canvas size
                    self.layer_directions[i] *= -1

            # Move the layer
            self.canvas.move(layer_id, dx * self.layer_directions[i], dy)

        # Repeat the animation
        self.root.after(30, self.animate_layers)

    def end_game(self):
        self.game_running = False
        pygame.mixer.music.stop()
        self.canvas.delete("all")

        # Hiển thị nền Game Over
        end_bg_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON\\Gmae_Over.png"
        self.end_bg_image = ImageTk.PhotoImage(Image.open(end_bg_path))
        self.canvas.create_image(0, 0, anchor="nw", image=self.end_bg_image)

        # Hiển thị điểm số cuối cùng với viền
        final_score_text = f"FINAL SCORE: {self.score}"

        # Vẽ viền đỏ
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:  # Các hướng của viền
            self.canvas.create_text(
                640 + dx, 350 + dy,
                text=final_score_text,
                font=("Black Ops One", 30),
                fill="red"
            )

        # Vẽ chữ màu trắng ở giữa
        self.canvas.create_text(
            640, 350,
            text=final_score_text,
            font=("Black Ops One", 30),
            fill="white"
        )

        # Đặt lại con trỏ chuột
        self.root.config(cursor="arrow")

        # Nút Play Again
        play_again_button = self.create_button("PLAY AGAIN", self.start_game, 640, 500)
        # Nút Main Menu
        main_menu_button = self.create_button("MAIN MENU", self.menu_screen, 640, 600)

        self.buttons = [play_again_button, main_menu_button]
        self.current_menu_index = 0
        self.highlight_button(self.buttons[self.current_menu_index])

        # Bắt đầu theo dõi âm thanh và cử chỉ tay cho màn hình Game Over
        if not self.hand_tracking_active:
            self.hand_tracking_active = True
            self.track_hand_thread = threading.Thread(target=self.track_hand_end_game, daemon=True)
            self.track_hand_thread.start()

        if not self.sound_tracking_active:
            self.sound_tracking_active = True
            self.sound_tracking_thread = threading.Thread(target=self.track_sound_end_game, daemon=True)
            self.sound_tracking_thread.start()

    def track_hand_end_game(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Couldn't open camera.")
            return

        with mp.solutions.hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
            while self.hand_tracking_active:
                success, frame = cap.read()
                if not success:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Get landmarks for each finger except the thumb (index 1-4)
                        index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                        middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                        ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
                        pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
                        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                        thumb_cmc = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_CMC]

                        # Calculate distances between the thumb and other fingers to determine if thumb is extended
                        distance_thumb_index = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
                        distance_thumb_middle = ((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2) ** 0.5
                        distance_thumb_ring = ((thumb_tip.x - ring_tip.x) ** 2 + (thumb_tip.y - ring_tip.y) ** 2) ** 0.5
                        distance_thumb_pinky = ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2) ** 0.5

                        # Determine if the "like" gesture is made:
                        thumb_extended = ((thumb_tip.x - thumb_cmc.x) ** 2 + (thumb_tip.y - thumb_cmc.y) ** 2) ** 0.5 > 0.1
                        other_fingers_curled = (distance_thumb_index < 0.05 and distance_thumb_middle < 0.05 and
                                                distance_thumb_ring < 0.05 and distance_thumb_pinky < 0.05)

                        current_time = time.time()

                        # Check if the "like" gesture is made and trigger button press
                        if thumb_extended and other_fingers_curled:
                            if current_time - self.last_button_time > 0.5:
                                self.last_button_time = current_time
                                # Ensure that the current_menu_index is valid and that the button exists
                                if self.buttons and 0 <= self.current_menu_index < len(self.buttons):
                                    button = self.buttons[self.current_menu_index]
                                    if button.winfo_exists():  # Ensure the button still exists in the UI
                                        button.invoke()

                        # Pinch gesture: navigate to next button (thumb and index finger close)
                        elif distance_thumb_index < 0.05:
                            if current_time - self.last_button_time > 0.5:
                                self.last_button_time = current_time
                                self.current_menu_index = (self.current_menu_index + 1) % len(self.buttons)
                                self.highlight_button(self.buttons[self.current_menu_index])

            cap.release()

    def track_sound_end_game(self):
        # Sampling rate and the duration of a sample window
        fs = 44100  # Sample rate (Hz)
        duration = 0.6  # Duration of the sample window (seconds)

        while self.sound_tracking_active:
            # Record sound from the microphone
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
            sd.wait()  # Wait for the recording to finish

            # Convert the audio signal to an absolute value and calculate the peak volume
            peak_volume = np.max(np.abs(recording))

            # If the peak volume is greater than a higher threshold, consider it a "clap"
            if peak_volume > 0.6:  # Increased threshold for detecting a clap (tune as needed)
                current_time = time.time()

                if current_time - self.last_button_time > 1.0:  # Avoid double trigger with longer cooldown
                    self.last_button_time = current_time
                    # Ensure that the current_menu_index is valid and that the button exists
                    if self.buttons and 0 <= self.current_menu_index < len(self.buttons):
                        button = self.buttons[self.current_menu_index]
                        if button.winfo_exists():  # Ensure the button still exists in the UI
                            button.invoke()

            # Small delay to prevent constant firing of the action
            time.sleep(0.1)

    def load_music(self):
        try:
            bg_music = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\BGMUSIC.mp3"
            if os.path.exists(bg_music):
                pygame.mixer.music.load(bg_music)
                pygame.mixer.music.play(-1)
            else:
                print(f"Music file not found: {bg_music}")
        except Exception as e:
            print(f"Error loading music: {e}")

    def load_images(self):
        try:
            bg_image_path = r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON \\MAP copy.png"
            self.background_image = ImageTk.PhotoImage(Image.open(bg_image_path))
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

            self.hand_open_image = ImageTk.PhotoImage(
                Image.open(r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\OPEN-.png").resize((400, 200), Image.LANCZOS))
            self.hand_closed_image = ImageTk.PhotoImage(
                Image.open(r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\CLOSE.png").resize((400, 200), Image.LANCZOS))
            self.hand_image_id = self.canvas.create_image(640, 335, image=self.hand_open_image)
        except Exception as e:
            print(f"Error loading images: {e}")

    def setup_game_data(self):
        self.pokemons = [
            {"name": "FISHY", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\FISHY.png", "rarity": 1, "type": "Water", "points": 20},
            {"name": "VAPOREON-", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\VAPOREON-.png", "rarity": 2, "type": "Water", "points": 20},
            {"name": "PIKACHU", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\PIKACHU.png", "rarity": 4, "type": "Land", "points": 30},
            {"name": "LIGHTNING", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\LIGHTNING.png", "rarity": 3, "type": "Land", "points": 40},
            {"name": "WHITEDRAGON", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\WHITEDRAGON.png", "rarity": 3, "type": "Flying", "points": 30},
            {"name": "GHOST", "image": r"C:\\Users\\Admin\\Desktop\\CATCHING POKEMON GAME\\GHOST.png", "rarity": 1, "type": "Flying", "points": 10},
       ]
        self.spawn_locations = {
            "Flying": [
                (240, 80), (320, 100), (400, 130), (1100, 120), (1180, 150),
                (800, 60), (900, 100)
            ],
            "Water": [
                (580, 380), (600, 400), (640, 420), (680, 380), (700, 400),
                (760, 440)
            ],
            "Land": [
                (300, 580), (350, 600), (400, 620), (900, 600), (1000, 650),
                (850, 500), (900, 520)
            ],
        }

    def show_pokemon(self):
        if not self.game_running:
            return

        if self.current_pokemon and self.current_pokemon.get('image_id'):
            self.canvas.delete(self.current_pokemon['image_id'])

        pokemon = random.choice(self.pokemons)
        self.current_pokemon = pokemon

        try:
            pokemon_image = ImageTk.PhotoImage(Image.open(pokemon["image"]).resize((120, 120), Image.LANCZOS))
        except Exception as e:
            print(f"Error loading Pokémon image: {e}")
            return

        # Select a random spawn location from the available coordinates for the Pokémon's type
        spawn_area = self.spawn_locations.get(pokemon["type"], [(400, 300)])  # Default spawn if no type match
        spawn_location = random.choice(spawn_area)
        pokemon_image_id = self.canvas.create_image(spawn_location[0], spawn_location[1], image=pokemon_image)

        self.current_pokemon.update({"image_id": pokemon_image_id, "image_obj": pokemon_image})

        self.canvas.tag_raise(pokemon_image_id)
        self.canvas.tag_raise(self.hand_image_id)

        self.root.after(1000, self.show_pokemon)

    def update_timer(self):
        if self.time_left <= 0:
            self.end_game()
        else:
            self.time_left -= 1
            self.timer_label.config(text=f"TIME LEFT: {self.time_left}s")
            self.root.after(1000, self.update_timer)


    def track_hand(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Couldn't open camera.")
            return

        with mp.solutions.hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
            while self.game_running:
                success, frame = cap.read()
                if not success:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
                        index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

                        x = int(wrist.x * 1280)
                        y = int(wrist.y * 670)
                        self.canvas.coords(self.hand_image_id, x, y)

                        # Calculate the distance between the index and thumb tips to detect the hand "closed"
                        distance = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5

                        if distance < 0.07:  # If the hand is closed (distance threshold)
                            self.canvas.itemconfig(self.hand_image_id, image=self.hand_closed_image)
                            self.check_pokemon_collision(x, y, distance)
                        else:
                            self.canvas.itemconfig(self.hand_image_id, image=self.hand_open_image)

                        # Raise the hand image above the Pokémon for interaction
                        self.canvas.tag_raise(self.hand_image_id)

    def check_pokemon_collision(self, x, y, distance):
        if not self.current_pokemon:
            return

        bbox = self.canvas.bbox(self.current_pokemon['image_id'])
        if not bbox:
            return  # No bounding box (e.g., image not found on the canvas)

        x1, y1, x2, y2 = bbox

        # Ensure the current Pokémon is set
        if self.canvas.bbox(self.current_pokemon['image_id']):
            x1, y1, x2, y2 = self.canvas.bbox(self.current_pokemon['image_id'])

            # Check if the hand is within the bounding box and the hand is closed enough
            if x1 <= x <= x2 and y1 <= y <= y2 and distance < 0.07:
                self.score += self.current_pokemon['points']
                self.score_label.config(text=f"SCORE: {self.score}")
                self.canvas.delete(self.current_pokemon['image_id'])
                self.play_catch_sound()
                self.current_pokemon = None  # Reset the current Pokémon


if __name__ == "__main__":
    root = tk.Tk()
    game = PokemonGame(root)
    root.mainloop()









