import streamlit as st
from pydub import AudioSegment
import tempfile
import os

def main():
    st.title("Audio File Converter")

    # Upload audio file
    uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav", "ogg", "flac", "m4a"])

    # Select output format
    output_format = st.selectbox("Select the output format", ["mp3", "wav", "ogg", "flac"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_in:
            temp_in.write(uploaded_file.read())
            temp_in_name = temp_in.name

        try:
            # Load the audio file
            audio = AudioSegment.from_file(temp_in_name)
            st.success("Audio loaded successfully!")

            # Convert to the desired format
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_out:
                output_path = temp_out.name
            audio.export(output_path, format=output_format)
            st.success(f"File converted to .{output_format} successfully!")

            # Download the converted file
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download converted file",
                    data=file,
                    file_name=f"converted.{output_format}",
                    mime=f"audio/{output_format}"
                )

        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            # Clean up temporary files
            os.remove(temp_in_name)
            if os.path.exists(output_path):
                os.remove(output_path)

if __name__ == "__main__":
    main()
