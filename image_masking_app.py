import streamlit as st
import image_masking_lib as glib


st.set_page_config(layout="wide", page_title="Image Masking")

st.title("Image Masking")


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Image")
    uploaded_image_file = st.file_uploader("Select an image", type=['png', 'jpg'])
    
    if uploaded_image_file:
        uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_image_file.getvalue())
        st.image(uploaded_image_preview)
    else:
        st.image("images/house-1.jpg")
    
    
with col2:
    st.subheader("Mask")
    
    masking_mode = st.radio("Masking mode:", ["Prompt", "Image"], horizontal=True)
    
    if masking_mode == 'Image':
    
        uploaded_mask_file = st.file_uploader("Select an image mask", type=['png', 'jpg'])
        
        if uploaded_mask_file:
            uploaded_mask_preview = glib.get_bytesio_from_bytes(uploaded_mask_file.getvalue())
            st.image(uploaded_mask_preview)
        else:
            st.image("images/mask1.png")
    else:
        mask_prompt = st.text_input("Item to mask:", "house", help="The item to replace (if inpainting), or keep (if outpainting).")
    promptHelp = """
    - house with swimming pool in front, kids playing in the pool , colorful.
    - house in the heart of the city with parked car in front of the house.
    - house in green hill, green mountain background, blue sky.
    - house inside a mountain range.
    - house in golden sunset, golden ray, mountain background, reflective pond in front of the house.
    """
    prompt_text = st.text_area("Prompt text:", "house in a luxury city area , golden hour time, golden light, a lot of people walking in front of the house", height=100, help=promptHelp)
    
    optCol1, optCol2 = st.columns(2)
    with optCol1:
        painting_mode = st.radio("Painting mode:", ["OUTPAINTING", "INPAINTING"])
    with optCol2:
        numImg = st.selectbox("No of Image?",(1,2,3,4,5,6))

    generate_button = st.button("Generate", type="primary")

with col3:
    st.subheader("Result")
    
    imgList = []
    if generate_button:
        with st.spinner("Drawing..."):
            
            if uploaded_image_file:
                image_bytes = uploaded_image_file.getvalue()
            else:
                image_bytes = glib.get_bytes_from_file("images/house-1.jpg")
            
            if masking_mode == 'Image':
                if uploaded_mask_file:
                    mask_bytes = uploaded_mask_file.getvalue()
                else:
                    mask_bytes = glib.get_bytes_from_file("images/mask1.png")
                for i in range(0,int(numImg)):
                    generated_image = glib.get_image_from_model(
                        prompt_content=prompt_text, 
                        image_bytes=image_bytes,
                        masking_mode=masking_mode,
                        mask_bytes=mask_bytes,
                        painting_mode=painting_mode
                    )
                    imgList.append(generated_image)
            else:
                for i in range(0,int(numImg)):
                    generated_image = glib.get_image_from_model(
                        prompt_content=prompt_text, 
                        image_bytes=image_bytes,
                        masking_mode=masking_mode,
                        mask_prompt=mask_prompt,
                        painting_mode=painting_mode
                    )
                    imgList.append(generated_image)
        for img in imgList:    
            st.image(img)
