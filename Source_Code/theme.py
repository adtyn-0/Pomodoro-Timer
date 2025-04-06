import customtkinter as ctk
import settings
import os
from PIL import Image, ImageSequence
from customtkinter import CTkImage

cat_frames = {}  # Loaded dynamically below


def apply_appearance_mode():
    user_settings = settings.load_settings()
    mode = user_settings.get("appearance_mode", "Dark")
    ctk.set_appearance_mode(mode)


def apply_theme_color(app, session_type):
    theme_colors = {
        "work": "#e05b46",         # reddish-orange for work
        "short_break": "#70c1b3",  # mint green for short break
        "long_break": "#247ba0"    # ocean blue for long break
    }
    color = theme_colors.get(session_type, "#171f27")  # default fallback
    app.configure(fg_color=color)


def apply_initial_theme(app):
    app.configure(fg_color="#09abcb")  # fallback or idle color


# Load images once and reuse them
def load_cat_images():
    global cat_frames
    base_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "assets", "images")

    CAT_SIZE_DEFAULT = (150, 150)
    CAT_SIZE_SLEEP = (180, 100)

    def load_gif(path, size):
        img = Image.open(path)
        return [img.copy().resize(size, Image.Resampling.LANCZOS) for img in ImageSequence.Iterator(img)]

    cat_frames = {
        "work": load_gif(os.path.join(base_path, "pixel-cat-walk.gif"), CAT_SIZE_DEFAULT),
        "short_break": load_gif(os.path.join(base_path, "pixel-cat.gif"), CAT_SIZE_DEFAULT),
        "long_break": load_gif(os.path.join(base_path, "pixel-cat-sleep.gif"), CAT_SIZE_SLEEP),
    }


def get_cat_image(session_type):
    return cat_frames.get(session_type, cat_frames["work"])
