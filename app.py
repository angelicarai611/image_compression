import streamlit as st
from PIL import Image, ImageEnhance
import io
import os

def compress_image(image_file, quality):
    img = Image.open(image_file)

    # Convert RGBA/PNG to RGB
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer, img

def main():
    st.set_page_config(page_title="Image Compressor", layout="centered")
    st.title("🗜️ Image Compression and Enhancement Tool")

    st.markdown("Upload an image, compress it, and enhance it for web use.")

    uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        original_size = os.path.getsize(uploaded_file.name) / 1024 if hasattr(uploaded_file, 'name') else None

        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Image", use_column_width=True)

        quality = st.slider("🔧 Compression Quality (%)", 10, 100, 70)

        # Optional enhancement
        enhance_option = st.selectbox("✨ Enhance Image?", ("None", "Increase Brightness", "Increase Contrast"))
        enhancement_factor = st.slider("Enhancement Factor", 1.0, 2.0, 1.2) if enhance_option != "None" else 1.0

        if st.button("🚀 Compress & Enhance"):
            buffer, img = compress_image(uploaded_file, quality)

            # Apply enhancement
            if enhance_option == "Increase Brightness":
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(enhancement_factor)
            elif enhance_option == "Increase Contrast":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(enhancement_factor)

            # Save again after enhancement
            final_buffer = io.BytesIO()
            img.save(final_buffer, format="JPEG", quality=quality, optimize=True)
            final_buffer.seek(0)

            with col2:
                st.image(final_buffer, caption="Compressed & Enhanced Image", use_column_width=True)

            compressed_size = len(final_buffer.getvalue()) / 1024
            st.markdown(f"💾 **Original size:** {original_size:.2f} KB" if original_size else "")
            st.markdown(f"📉 **Compressed size:** {compressed_size:.2f} KB")

            st.download_button(
                label="📥 Download Compressed Image",
                data=final_buffer,
                file_name="compressed_image.jpg",
                mime="image/jpeg"
            )

if __name__ == "__main__":
    main()
