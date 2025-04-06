import customtkinter as ctk
from Source_Code import settings
import os
import sys
from PIL import Image, ImageSequence

cat_frames = {}


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', relative_path)


def apply_appearance_mode():
    user_settings = settings.load_settings()
    mode = user_settings.get("appearance_mode", "Dark")
    ctk.set_appearance_mode(mode)


def apply_theme_color(app, session_type):
    theme_colors = {
        "work": "#e05b46",
        "short_break": "#70c1b3",
        "long_break": "#247ba0"
    }
    color = theme_colors.get(session_type, "#171f27")
    app.configure(fg_color=color)


def apply_initial_theme(app):
    app.configure(fg_color="#09abcb")


def load_cat_images():
    global cat_frames
    CAT_SIZE_DEFAULT = (150, 150)
    CAT_SIZE_SLEEP = (180, 100)

    def load_gif(path, size):
        img = Image.open(path)
        return [img.copy().resize(size, Image.Resampling.LANCZOS) for img in ImageSequence.Iterator(img)]

    cat_frames = {
        "work": load_gif(resource_path("assets/images/pixel-cat-walk.gif"), CAT_SIZE_DEFAULT),
        "short_break": load_gif(resource_path("assets/images/pixel-cat.gif"), CAT_SIZE_DEFAULT),
        "long_break": load_gif(resource_path("assets/images/pixel-cat-sleep.gif"), CAT_SIZE_SLEEP),
    }


def get_cat_image(session_type):
    return cat_frames.get(session_type, cat_frames["work"])
