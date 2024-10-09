from flask import Flask, request, send_file, render_template, redirect, url_for, flash
from rembg import remove, new_session
from io import BytesIO
from PIL import Image
import zipfile
import os
import onnxruntime as ort

# Use CPU execution provider
ort.set_default_logger_severity(3)  # Reduce logging verbosity
session_options = ort.SessionOptions()
session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED

# Modify model loading to use CPU execution provider
people_model = new_session(model_name="u2net", session_options=session_options)
product_model = new_session(model_name="u2netp", session_options=session_options)


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Use CPU execution provider to avoid CoreML issues
people_model = new_session(model_name="u2net")
product_model = new_session(model_name="u2netp")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'images' not in request.files:
        flash('No images provided, please upload images.')
        return redirect(url_for('index'))

    files = request.files.getlist('images')
    precision = request.form.get('precision', 'medium')
    model_type = request.form.get('model', 'people')
    custom_bg_color = request.form.get('bg_color', None)  # Custom background color from form
    custom_bg_file = request.files.get('bg_file', None)  # Custom background image file

    if len(files) == 0:
        flash('No selected files, please choose images.')
        return redirect(url_for('index'))

    output_images = []
    try:
        # Select model based on the user's choice
        model = product_model if model_type == 'products' else people_model

        # Process each image
        for file in files:
            input_image = file.read()

            # Remove background
            output_image = remove(input_image, session=model)

            # Load the processed image into PIL
            img = Image.open(BytesIO(output_image))

            # Apply custom background if provided
            if custom_bg_color:
                bg_color = Image.new("RGBA", img.size, custom_bg_color)
                img = Image.alpha_composite(bg_color, img)

            if custom_bg_file:
                custom_bg = Image.open(custom_bg_file)
                custom_bg = custom_bg.resize(img.size)
                img = Image.alpha_composite(custom_bg, img)

            # Save the output image in memory
            img_io = BytesIO()
            img.save(img_io, 'PNG', quality=95)  # Save in high quality
            img_io.seek(0)

            output_images.append((file.filename, img_io))

        # Handle single or multiple image uploads
        if len(output_images) == 1:
            # Return single image directly
            filename, img_io = output_images[0]
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f"processed_{filename}")

        # Multiple files, return as a ZIP archive
        else:
            zip_io = BytesIO()
            with zipfile.ZipFile(zip_io, 'w') as zipf:
                for filename, img_io in output_images:
                    zipf.writestr(f"processed_{filename}", img_io.getvalue())
            zip_io.seek(0)
            return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name='processed_images.zip')

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
