import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI Photo Editor", page_icon="🖼️", layout="centered")

# ===================== USER AUTH =====================
USER_FILE = "users.txt"

# Ensure user file exists
if not os.path.exists(USER_FILE):
    open(USER_FILE, "w").close()

def load_users():
    users = {}
    with open(USER_FILE, "r") as f:
        for line in f:
            if "," in line:
                u, p = line.strip().split(",", 1)
                users[u] = p
    return users

def save_user(username, password):
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def auth_ui():
    st.title("🔐 User Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])
    users = load_users()

    # -------- LOGIN --------
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # -------- REGISTER --------
    with tab2:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if not new_user or not new_pass:
                st.warning("Fields cannot be empty")
            elif new_user in users:
                st.warning("User already exists")
            else:
                save_user(new_user, new_pass)
                st.success("Registration successful. Please login.")

if not st.session_state.logged_in:
    auth_ui()
    st.stop()

# ===================== LOAD AI MODEL (FAST) =====================
@st.cache_resource
def load_sr():
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel("models/EDSR_x2.pb")
    sr.setModel("edsr", 2)
    return sr

sr = load_sr()

# ===================== SESSION STATE =====================
if "history" not in st.session_state:
    st.session_state.history = []
if "redo" not in st.session_state:
    st.session_state.redo = []
if "ai_done" not in st.session_state:
    st.session_state.ai_done = False

# ===================== FUNCTIONS =====================
def ai_enhance(img):
    max_size = 800
    h, w = img.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return sr.upsample(img)

def apply_adjustments(img, b, c, s, sh, r, f):
    img = Image.fromarray(img)
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)
    img = ImageEnhance.Sharpness(img).enhance(sh)
    img = img.rotate(r, expand=True)

    if f == "Grayscale":
        img = ImageOps.grayscale(img)
    elif f == "Invert":
        img = ImageOps.invert(img.convert("RGB"))

    return np.array(img)

# ===================== MAIN UI =====================
st.title("🤖 AI-Based Photo Editing Application")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

uploaded = st.file_uploader("📁 Upload Image", type=["jpg", "png", "jpeg"])

if uploaded:
    original = np.array(Image.open(uploaded).convert("RGB"))

    # Run AI enhancement only once
    if not st.session_state.ai_done:
        enhanced = ai_enhance(original)
        st.session_state.history = [enhanced]
        st.session_state.redo = []
        st.session_state.ai_done = True

    st.subheader("📌 Original Image")
    st.image(original, use_column_width=True)

    st.subheader("🎛️ Editing Controls")

    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    saturation = st.slider("Saturation", 0.0, 2.0, 1.0)
    sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0)
    rotate = st.slider("Rotate", -180, 180, 0)
    filter_type = st.selectbox("Filter", ["None", "Grayscale", "Invert"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Apply"):
            edited = apply_adjustments(
                st.session_state.history[-1],
                brightness, contrast, saturation,
                sharpness, rotate, filter_type
            )
            st.session_state.history.append(edited)
            st.session_state.redo.clear()

    with col2:
        if st.button("Undo") and len(st.session_state.history) > 1:
            st.session_state.redo.append(st.session_state.history.pop())

    with col3:
        if st.button("Redo") and st.session_state.redo:
            st.session_state.history.append(st.session_state.redo.pop())

    st.subheader("📌 Edited Image")
    st.image(st.session_state.history[-1], use_column_width=True)

    if st.button("💾 Save Image"):
        os.makedirs("output", exist_ok=True)
        Image.fromarray(st.session_state.history[-1]).save("output/final_image.jpg")
        st.success("Image saved in output/final_image.jpg")
