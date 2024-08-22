import tkinter as tk
from PIL import Image, ImageTk

def on_canvas_click(event):
    # Get click coordinates
    x, y = event.x, event.y
    
    # Delete previous image if it exists
    #if hasattr(on_canvas_click, 'previous_image_id'):
        #canvas.delete(on_canvas_click.previous_image_id)
    
    # Create the new image at the clicked coordinates
    on_canvas_click.previous_image_id = canvas.create_image(x, y, image=tk_img_foreground, anchor=tk.CENTER)

# Create main window
root = tk.Tk()
root.title("Test Image Placement")

# Create canvas
canvas = tk.Canvas(root, width=800, height=600)

# Load the transparent image using PIL
foreground_img = Image.open("./assets/Final picture to hang.png").convert("RGBA")
tk_img_foreground = ImageTk.PhotoImage(foreground_img)

background_img = Image.open("./assets/wall.jpg")
tk_img_background = ImageTk.PhotoImage(background_img)

canvas.create_image(0, 0,image=tk_img_background, anchor=tk.CENTER)
canvas.pack(fill="both", expand=True)
# Bind the click event to the on_canvas_click function
canvas.bind("<Button-1>", on_canvas_click)

# Run the application
root.mainloop()
