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

### Development Mode (Flask development server)

With virtual environment activated:

```bash
python LR3_WEB.py
```

Application will be available at `http://localhost:5000`

### Production Mode (Gunicorn WSGI server)

Gunicorn is recommended for production deployments.

#### Windows:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
.\run.bat
```

Or manually:

```powershell
gunicorn --bind 0.0.0.0:8000 --workers 4 --config gunicorn_config.py LR3_WEB:app
```

#### macOS/Linux/WSL:

```bash
source venv/bin/activate
chmod +x run.sh
./run.sh
```

Or manually:

```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --config gunicorn_config.py LR3_WEB:app
```

**Custom configuration:**

Create `.env` file from `.env.example` and customize:

```bash
cp .env.example .env
# Edit .env with your settings
```

Available environment variables:
- `GUNICORN_BIND` - Server address and port (default: `0.0.0.0:8000`)
- `GUNICORN_WORKERS` - Number of worker processes (default: CPU count × 2 + 1)
- `GUNICORN_WORKER_CLASS` - Worker type: `sync`, `async`, `gevent` (default: `sync`)
- `GUNICORN_TIMEOUT` - Worker timeout in seconds (default: `30`)
- `GUNICORN_LOG_LEVEL` - Log level: `debug`, `info`, `warning`, `error`, `critical` (default: `info`)

Production application will be available at `http://localhost:8000` (or configured port)

## Project Structure

```
LR3WEB/
├── LR3_WEB.py              # Main Flask application
├── test_app.py             # Unit tests
├── gunicorn_config.py      # Gunicorn configuration
├── run.sh                  # Startup script for Linux/macOS/WSL
├── run.bat                 # Startup script for Windows
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
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

## Deployment

### Render.com (Recommended for cloud hosting)

1. **Prerequisites:**
   - GitHub account with this repository
   - Render.com account (free tier available)

2. **Connect to Render:**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `LR3WEB` repository

3. **Configure deployment:**
   - **Name:** `lr3web` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** Leave empty (Render will use `Procfile`)
   - **Instance Type:** Free (or Starter+)

4. **Environment Variables (optional):**
   - `GUNICORN_WORKERS`: Number of workers (default auto-calculated)
   - `GUNICORN_LOG_LEVEL`: `info` or `debug`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy on every push to `main`
   - Your app will be available at `https://<your-service-name>.onrender.com`

**Note:** Files generated in `static/uploads/` are temporary on Render's free tier (ephemeral storage). For persistent storage, use Render's PostgreSQL or external storage solutions.

### Heroku (Alternative)

If using Heroku instead of Render, the `Procfile` and `runtime.txt` are compatible:

```bash
heroku create <app-name>
git push heroku main
```

### Traditional Server / VPS

For self-hosted deployment:

```bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Clone repository
git clone https://github.com/N1kolayLi/LR3WEB.git
cd LR3WEB

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 --config gunicorn_config.py LR3_WEB:app

# Or use systemd service for auto-restart
# Create /etc/systemd/system/lr3web.service
```

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
