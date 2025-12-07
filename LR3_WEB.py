from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
@app.route('/var9')
def var9():
    return render_template('var9.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    if not file:
        return redirect(url_for('var9'))

    original_path = os.path.join(UPLOAD_FOLDER, 'original.jpg')
    file.save(original_path)

    img = Image.open(original_path).convert("RGB")
    arr = np.array(img)

    r_coef = float(request.form.get('r_coef', 1.0))
    g_coef = float(request.form.get('g_coef', 1.0))
    b_coef = float(request.form.get('b_coef', 1.0))

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    r = np.clip(r * r_coef, 0, 255)
    g = np.clip(g * g_coef, 0, 255)
    b = np.clip(b * b_coef, 0, 255)
    new_arr = np.stack([r, g, b], axis=2).astype(np.uint8)

    new_img = Image.fromarray(new_arr)
    processed_path = os.path.join(UPLOAD_FOLDER, 'processed.jpg')
    new_img.save(processed_path)

    def plot_histogram(channel, color, name):
        plt.figure()
        plt.hist(channel.flatten(), bins=256, color=color, alpha=0.7)
        plt.title(f'Распределение {name}')
        plt.xlabel('Интенсивность')
        plt.ylabel('Количество пикселей')
        plt.savefig(os.path.join(UPLOAD_FOLDER, f'{name}.png'))
        plt.close()

    plot_histogram(r, 'red', 'red_channel')
    plot_histogram(g, 'green', 'green_channel')
    plot_histogram(b, 'blue', 'blue_channel')

    return render_template('res.html')

if __name__ == '__main__':
    app.run(debug=True)