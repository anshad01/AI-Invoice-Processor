import streamlit as st
from PIL import Image
from backend import process_invoice, convert_pdf_to_images

# Page config
st.set_page_config(page_title="Invoice Processor", layout="wide")
st.title("🧾 AI Invoice Processor")

# Upload file
uploaded_file = st.file_uploader("Upload an invoice (image or PDF)", type=["jpg", "jpeg", "png", "pdf"])

# Check if a file was uploaded
if uploaded_file:
    file_type = uploaded_file.type
    images = []

    try:
        # Handle PDF files
        if "pdf" in file_type:
            images = convert_pdf_to_images(uploaded_file)
            if not images:
                st.error("❌ Failed to convert PDF to images.")
        else:
            # Handle image files
            image = Image.open(uploaded_file).convert("RGB")
            images = [image]

        # Display and process each image
        for idx, image in enumerate(images):
            st.image(image, caption=f"Page {idx + 1}", use_column_width=True)

            with st.spinner(f"🔍 Processing Page {idx + 1}..."):
                try:
                    data = process_invoice(image)
                    st.success(f"✅ Page {idx + 1} processed successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to process Page {idx + 1}: {str(e)}")
                    continue

            # Show extracted fields
            if data:
                st.subheader(f"📄 Extracted Key Fields - Page {idx + 1}")
                for word, label in data:
                    st.markdown(f"**{label}**: {word}")
            else:
                st.warning("⚠️ No data extracted from this page.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
