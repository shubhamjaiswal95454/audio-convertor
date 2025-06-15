# Audio file uploader
uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav", "ogg", "flac", "m4a"])

# Select output format
output_format = st.selectbox("Select output format", ["mp3", "wav", "ogg", "flac"])

if uploaded_file is not None:
    # Convert the uploaded file to AudioSegment
    with tempfile.NamedTemporaryFile(delete=False) as temp_in:
        temp_in.write(uploaded_file.read())
        temp_in_name = temp_in.name
    
    # Load the audio with pydub
    try:
        loaded_audio = AudioSegment.from_file(temp_in_name)
        st.success("Audio loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load audio file. Error: {e}")
        return
    
    # Convert to selected format
    st.write(f"Converting to .{output_format}...")

    # Create a temporary file for output
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_out:
        output_path = temp_out.name
    
    # Export the file in the desired format
    try:
        loaded_audio.export(output_path, format=output_format)
        st.success(f"File converted to .{output_format} successfully!")
        
        # Download link for the converted file
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download converted file",
                data=file,
                file_name=f"converted.{output_format}",
                mime=f"audio/{output_format}"
            )
    except Exception as e:
        st.error(f"Failed to convert audio file. Error: {e}")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_in_name):
            os.remove(temp_in_name)
        if os.path.exists(output_path):
            os.remove(output_path)
