# Image Caption Generator

A simple Flask web app that generates captions for images you upload. It uses the pretrained [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) model from Hugging Face to describe what's in a picture in plain English.

## Features

- Upload an image from the browser and get an automatic caption
- Preview of the uploaded image next to its caption
- Powered by `Salesforce/blip-image-captioning-base` (runs on CPU, uses GPU automatically if available)
- Basic upload safety: allowed file types only, size limit, and unique sanitized filenames
- Friendly error messages when something goes wrong

## Tech Stack

- Python 3.9+
- [Flask](https://flask.palletsprojects.com/)
- [PyTorch](https://pytorch.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) (BLIP)
- [Pillow](https://python-pillow.org/)

## Project Structure

```
.
├── app.py              # Flask app and caption generation
├── templates/
│   └── index.html      # Upload form and results page
├── uploads/            # Uploaded images (created automatically)
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

> **Note:** The first run downloads the BLIP model (a few hundred MB), so it may take a minute. After that it loads from the local cache.

## Usage

1. Open the app in your browser.
2. Choose an image (PNG, JPG, JPEG, GIF, BMP or WEBP, up to 16 MB).
3. Click the upload/generate button.
4. The image and its generated caption appear on the page.

## How It Works

1. The uploaded image is saved to the `uploads/` folder under a unique, safe filename.
2. The image is converted to RGB and preprocessed with `BlipProcessor`.
3. `BlipForConditionalGeneration` generates caption tokens (up to 50 new tokens).
4. The tokens are decoded into text and shown on the page.

## Configuration

You can tweak these in `app.py`:

| Setting | Where | What it does |
| --- | --- | --- |
| `MODEL_NAME` | top of file | Swap in `Salesforce/blip-image-captioning-large` for higher-quality (slower) captions |
| `MAX_CONTENT_LENGTH` | `app.config` | Maximum upload size |
| `ALLOWED_EXTENSIONS` | top of file | File types accepted |
| `max_new_tokens` | `model.generate(...)` | Maximum caption length |

## Troubleshooting

- **Slow first request:** the model is downloading or loading; later requests are faster.
- **Out of memory:** use the base model (default) or run on a machine with more RAM/VRAM.
- **Unsupported file type:** make sure the image is one of the allowed formats.

## Future Improvements

- Multiple image uploads at once
- Option to guide the caption with a text prompt
- Copy-to-clipboard button for captions
- Docker support

## Acknowledgements

- [Salesforce BLIP](https://github.com/salesforce/BLIP) for the captioning model
- [Hugging Face](https://huggingface.co/) for the Transformers library

## License

Add a license of your choice (for example, MIT) and update this section.
