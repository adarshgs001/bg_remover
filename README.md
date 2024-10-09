# Background Remover with Custom Background Options

This project is a **Flask**-based web application that allows users to remove backgrounds from images using a machine learning model. It provides advanced features such as **batch processing** of multiple images, the ability to **replace the background** with solid colors, gradients, or predefined templates, and the option to **upload custom backgrounds**.

## Features

- **Basic Background Removal**: Automatically removes the background from images using a pre-trained deep learning model.
- **Batch Processing**: Upload and process multiple images at once, downloading the result as a ZIP archive.
- **Custom Background Options**:
  - Replace the background with a **solid color** or **custom image**.
  - High-quality output for each processed image.
- **Single Image Download**: If a single image is uploaded, it can be downloaded directly without archiving.
- **CPU Execution**: The background removal model runs on the CPU, ensuring compatibility across devices without requiring GPU-based frameworks like CoreML.

## Requirements

- **Python 3.8+**
- **Pip**
- **Virtual Environment (optional but recommended)**

### Dependencies

This project relies on the following Python libraries:

- `Flask`: A micro-framework for web development.
- `rembg`: A Python library that uses U-2-Net to remove image backgrounds.
- `PIL (Pillow)`: For image processing tasks.
- `onnxruntime`: For running the deep learning model.
- `zipfile`: To compress multiple processed images into a ZIP archive.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/bg_remover.git
   cd bg_remover
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:

   ```bash
   python app.py
   ```

   The application will be running at `http://127.0.0.1:5001`.

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5001`.
2. Upload one or more images for background removal.
3. Optionally, choose a **background replacement** option:
   - **Solid Color**: Select a color using the color picker.
   - **Custom Background Image**: Upload a custom background image to replace the background.
4. Submit the form:
   - If you upload one image, it will be processed and available for direct download.
   - If you upload multiple images, they will be processed and returned as a ZIP archive.

## Options in the Web Form

- **Choose Model**:
  - `People`: A model optimized for images with people.
  - `Products`: A model optimized for product photos.
  
- **Precision Level**:
  - `Low`: Faster processing but with less precise background removal.
  - `Medium`: Balanced speed and accuracy (default).
  - `High`: Slower but more accurate background removal.

- **Custom Background Options**:
  - **Solid Color**: Use a color picker to select a solid background color.
  - **Custom Background Image**: Upload your own background image to replace the removed background.

## Error Handling

- If an invalid image is uploaded, or there is an issue during background removal, an error message will be displayed on the web page.
- The application will attempt to resolve model compatibility issues by using CPU execution instead of CoreML.

## Contributing

Feel free to fork this repository, submit pull requests, or file issues. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Additional Notes:
1. Make sure to add a `requirements.txt` file to your project using:
   ```bash
   pip freeze > requirements.txt
   ```
2. Optionally, include an example of the app's usage by adding screenshots or GIFs to the README.
