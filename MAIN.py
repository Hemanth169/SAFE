import numpy as np
import cv2
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Toplevel
from PIL import Image, ImageTk
import os
import imutils
import threading

class ImageStitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Stitcher")
        self.images = []
        self.stitched_image = None
        self.folder_path = ""
        self.image_previews = []  # Initialize image_previews list
        self.setup_ui()
    
    def setup_ui(self):
                
        # Selected folder label
        self.folder_label = tk.Label(self.root, text="Selected Folder:", font=("Helvetica", 12))
        self.folder_label.pack(pady=(10, 5))  # Add vertical padding only

        # Selected folder entry
        self.folder_entry = tk.Label(self.root, width=50)
        self.folder_entry.pack(pady=(0, 10))  # Add vertical padding only

        # Select folder button
        select_image = tk.PhotoImage(file="select.png")
        self.select_button = tk.Button(self.root, image=select_image, text="Select Folder", compound=tk.TOP, command=self.select_folder, bd=0, font=("Helvetica", 10))
        self.select_button.image = select_image
        self.select_button.pack(pady=5)

        # Preview input images button
        preview_image = tk.PhotoImage(file="preview.png")
        self.preview_input_button = tk.Button(self.root, image=preview_image, text="Preview Input Images", compound=tk.TOP, command=self.preview_input_images, bd=0, font=("Helvetica", 10))
        self.preview_input_button.image = preview_image
        self.preview_input_button.pack(pady=5)
        self.preview_input_button.config(state='disabled')  # Initially disabled

        # Stitch images button
        stitch_image = tk.PhotoImage(file="stitch.png")
        self.stitch_button = tk.Button(self.root, image=stitch_image, text="Stitch Images", compound=tk.TOP, command=self.stitch_images_thread, bd=0, font=("Helvetica", 10))
        self.stitch_button.image = stitch_image
        self.stitch_button.pack(pady=5)
        self.stitch_button.config(state='disabled')  # Initially disabled


        # Preview stitched image button
        preview_stitched_image = tk.PhotoImage(file="preview_stitched.png")
        self.preview_button = tk.Button(self.root, image=preview_stitched_image, text="Preview Stitched Image", compound=tk.TOP, command=self.preview_stitched_image, bd=0, font=("Helvetica", 10))
        self.preview_button.image = preview_stitched_image
        self.preview_button.pack(pady=5)
        self.preview_button.config(state='disabled')  # Initially disabled

        # Save stitched image button
        save_image = tk.PhotoImage(file="save.png")
        self.save_button = tk.Button(self.root, image=save_image, text="Save Stitched Image", compound=tk.TOP, command=self.save_stitched_image, bd=0, font=("Helvetica", 10))
        self.save_button.image = save_image
        self.save_button.pack(pady=5)
        self.save_button.config(state='disabled')  # Initially disabled


        # Exit button
        exit_image = tk.PhotoImage(file="exit.png")
        self.exit_button = tk.Button(self.root, image=exit_image, text="Exit", compound=tk.TOP, command=self.root.destroy, bd=0, font=("Helvetica", 10))
        self.exit_button.image = exit_image
        self.exit_button.pack(pady=5)

        


    def select_folder(self):
        file_paths = filedialog.askopenfilenames()
        if not file_paths:
            messagebox.showerror("Error", "No images selected. Please select images.")
            return
        common_dir = os.path.commonpath(file_paths)
        self.folder_entry.config(text=common_dir)
        self.images = self.load_images_from_folder(file_paths)
        if self.images:
            self.preview_input_button.config(state='normal')
            self.stitch_button.config(state='normal')
        else:
            messagebox.showerror("Error", "Failed to load selected images.")

    def load_images_from_folder(self, file_paths):
        images = []
        formats = set()  # Set to store encountered image formats
        supported_formats = ['.jpg', '.jpeg', '.png']  # Define supported image formats
        
        # Check if file_paths is a single string (representing a folder path) or a list/tuple of file paths
        if isinstance(file_paths, str):
            file_paths = [file_paths]  # Convert single string to list containing only that string
        
        for file_path in file_paths:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in supported_formats:
                formats.add(file_ext)  # Add the encountered format to the set
                try:
                    img = cv2.imread(file_path)
                    if img is not None:
                        images.append(img)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image {file_path}: {e}")

        if len(formats) > 1:
            confirm = messagebox.askyesno("Confirmation", "Selected images are of different formats. Continue?")
            if not confirm:
                return []
        return images


    def preview_input_images(self):
        top = Toplevel(self.root)
        top.title("Input Image Previews")

        canvas = Canvas(top, bg="white", width=len(self.images) * 120, height=150)
        canvas.pack()
        # Clear previous input image previews
        for img_preview in self.image_previews:
            canvas.delete(img_preview)

        self.image_previews = []  # Initialize image_previews list

        
        for i, img in enumerate(self.images):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (100, 100))  # Resize for preview
            photo = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.image_previews.append(photo)  # Maintain reference to PhotoImage object
            canvas.create_image(50 + i * 120, 75, image=photo, anchor=tk.CENTER)
            canvas.image = photo
        # Add OK button    
        ok_button = tk.Button(top, text="OK", command=top.destroy)
        ok_button.pack()

    def stitch_images_thread(self):
        threading.Thread(target=self.stitch_images).start()

    def stitch_images(self):
        self.stitch_button.config(state='disabled')
        self.preview_button.config(state='disabled')
        self.save_button.config(state='disabled')

        # Show waiting message
        wait_message = messagebox.showinfo("Please Wait", "Stitching images in progress...")


        stitcher = cv2.Stitcher_create()
        result = stitcher.stitch(self.images)
        if result[0] != cv2.Stitcher_OK:
            messagebox.showerror("Error", "Image stitching failed.")
            return

        self.stitched_image = result[1]
        messagebox.showinfo("Success", "Images stitched successfully!")
        self.preview_button.config(state='normal')
        self.save_button.config(state='normal')

    

    def preview_stitched_image(self):
        if self.stitched_image is not None:
            stitched_img = cv2.resize(self.stitched_image, (800, 600))  # Resize for preview
            cv2.imshow("Stitched Image Preview", stitched_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showerror("Error", "No stitched image to preview!")
    def save_stitched_image(self):
        if self.stitched_image is not None:
            # Process the stitched image
            stitched_img = cv2.copyMakeBorder(self.stitched_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))
            gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
            thresh_img = cv2.threshold(gray, 0, 255 , cv2.THRESH_BINARY)[1]

            contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            areaOI = max(contours, key=cv2.contourArea)

            mask = np.zeros(thresh_img.shape, dtype="uint8")
            x, y, w, h = cv2.boundingRect(areaOI)
            cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

            minRectangle = mask.copy()
            sub = mask.copy()

            while cv2.countNonZero(sub) > 0:
                minRectangle = cv2.erode(minRectangle, None)
                sub = cv2.subtract(minRectangle, thresh_img)

            contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            areaOI = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(areaOI)

            stitched_img = stitched_img[y:y + h, x:x + w]

            # Prompt user to select file path
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                # Save the processed stitched image
                cv2.imwrite(file_path, stitched_img)
                messagebox.showinfo("Success", "Processed stitched image saved successfully!")
        else:
            messagebox.showerror("Error", "No stitched image to save!")            

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageStitcherApp(root)
    root.mainloop()
