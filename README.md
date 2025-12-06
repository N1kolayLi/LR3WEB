# LR3 Web - Flask Image Processing Application

## Description

Flask web application for image color channel processing. Upload an image and adjust red, green, and blue channel coefficients to modify image colors. The application generates histograms for each color channel.

## Features

- **Image Upload**: Upload JPEG/PNG images
- **Color Channel Adjustment**: Modify R, G, B coefficients independently (0.0 - 2.0)
- **Histogram Generation**: Automatic histograms for each color channel
- **Real-time Processing**: Instant image processing and display

## Requirements

- Python 3.12+
- Flask 3.1.2
- Pillow 12.0.0
- Matplotlib 3.10.7
- NumPy 2.3.5

All dependencies are listed in `requirements.txt`.

## Installation

### 1. Clone or download the project

```bash
git clone https://github.com/yourusername/LR3WEB.git
cd LR3WEB
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

With virtual environment activated:

```bash
python LR3_WEB.py
```

Application will be available at `http://localhost:5000`

## Project Structure

```
LR3WEB/
├── LR3_WEB.py              # Main Flask application
├── test_app.py             # Unit tests
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD pipeline
├── static/
│   └── uploads/            # Processed images and histograms
└── templates/
    ├── var9.html           # Upload page
    └── res.html            # Results page
```

## Usage

1. Navigate to `http://localhost:5000/var9`
2. Upload an image file
3. Adjust color channel coefficients:
   - `r_coef`: Red channel multiplier (default: 1.0)
   - `g_coef`: Green channel multiplier (default: 1.0)
   - `b_coef`: Blue channel multiplier (default: 1.0)
4. Click "Process" to apply transformations
5. View processed image and generated histograms

## Testing

Run unit tests:

```bash
python -m pytest test_app.py -v
```

Or with unittest:

```bash
python -m unittest test_app.py -v
```

Tests cover:
- Flask route accessibility
- Image file handling
- Color coefficient processing
- NumPy array operations
- Image format conversions

## CI/CD Pipeline

GitHub Actions automatically runs on push/PR:
- Tests across Python 3.12, 3.13, 3.14
- Code linting with flake8
- Syntax checking
- Build verification

See `.github/workflows/ci.yml` for details.

## API Routes

### GET `/var9`
Returns the image upload form.

### POST `/process`
Processes image with color coefficients.

**Parameters:**
- `file` (multipart): Image file
- `r_coef` (float): Red channel coefficient
- `g_coef` (float): Green channel coefficient
- `b_coef` (float): Blue channel coefficient

**Response:** Rendered results page with processed image and histograms

## Output Files

Processed files are saved to `static/uploads/`:
- `original.jpg` - Uploaded original image
- `processed.jpg` - Color-adjusted image
- `red_channel.png` - Red channel histogram
- `green_channel.png` - Green channel histogram
- `blue_channel.png` - Blue channel histogram

## Development

### Setting up for development

```bash
pip install -r requirements.txt
pip install pytest pytest-cov flake8
```

### Code style

Follow PEP 8 conventions. Lint with:

```bash
flake8 LR3_WEB.py test_app.py
```

## Troubleshooting

**Virtual environment activation fails (PowerShell):**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Module not found errors:**
Ensure venv is activated and run:
```bash
pip install -r requirements.txt
```

**Port 5000 already in use:**
Modify in `LR3_WEB.py`:
```python
app.run(debug=True, port=5001)
```

## License

MIT License - feel free to use this project for educational purposes.

## Author

Created for web development coursework (LR3 WEB).
