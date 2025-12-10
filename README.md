# AI Image Generator

A Stable Diffusion-based image generator with a user-friendly Gradio web interface. Generate high-quality images from text prompts using AI.

## Features

- 🎨 **Text-to-Image Generation**: Create images from descriptive text prompts
- ⚡ **Optimized Performance**: Fast generation (~1-2 minutes per image on CPU)
- 🌐 **Web Interface**: Easy-to-use Gradio GUI accessible via browser
- 📱 **PWA Support**: Install as a Progressive Web App
- 🔒 **Safety Features**: Built-in content filtering
- 💾 **Auto-Save**: Images automatically saved to local directory

## Requirements

- Python 3.8+
- 8GB+ RAM recommended
- Internet connection (for initial model download)
- Hugging Face account and token

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ownai
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install torch diffusers transformers gradio
```

4. **Set up Hugging Face token**
```bash
huggingface-cli login --token YOUR_TOKEN_HERE
```

## Quick Start

1. **Run the application**
```bash
python ai.py
```

2. **Open your browser**
   - Navigate to: `http://127.0.0.1:7863`

3. **Generate images**
   - Enter a text prompt (e.g., "A beautiful sunset over mountains")
   - Click "Generate Image"
   - Wait ~1-2 minutes
   - View and download your generated image

## Usage Examples

### Good Prompts
- "A beautiful landscape with mountains and sunset"
- "A futuristic city with flying cars and neon lights"
- "A portrait of a person in elegant Victorian clothing"
- "An astronaut exploring Mars with red sky"
- "A cute cat sitting on a windowsill"

### Tips for Better Results
- Be specific and descriptive
- Include artistic terms like "detailed", "high quality", "photorealistic"
- Specify lighting, colors, and mood
- Avoid NSFW content (will return black images)

## Configuration

Edit `ai.py` to customize:

```python
class Config:
    model_name = "runwayml/stable-diffusion-v1-5"
    num_inference_steps = 15  # Lower = faster, higher = better quality
    guidance_scale = 7.5      # Higher = more prompt adherence
```

### Speed vs Quality Trade-offs

| Steps | Generation Time | Quality |
|-------|----------------|---------|
| 10    | ~45 seconds    | Good    |
| 15    | ~1-2 minutes   | Better  |
| 25    | ~2-3 minutes   | Best    |
| 50    | ~4-5 minutes   | Excellent |

## Project Structure

```
ownai/
├── ai.py                          # Main application
├── HOW_TO_USE_AI_GENERATOR.md    # Detailed user guide
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── generated_images/              # Output directory
└── .venv/                         # Virtual environment
```

## Troubleshooting

### Black Images
**Problem**: Generated image is completely black  
**Solution**: Your prompt triggered the NSFW filter. Use appropriate prompts.

### Slow Generation
**Problem**: Takes too long to generate  
**Solution**: 
- Reduce `num_inference_steps` to 10
- Close other applications
- Consider using GPU cloud services

### Connection Issues
**Problem**: Can't access the web interface  
**Solution**:
- Check the terminal for the correct URL
- Try a different port if 7863 is busy
- Restart the application

## Performance

- **CPU Generation**: 1-2 minutes per image (optimized)
- **GPU Generation**: 5-10 seconds per image (if available)
- **Model Size**: ~4-5 GB download
- **Memory Usage**: 4-8 GB RAM

## Advanced Features

### Custom Image Size
```python
image = pipeline(
    prompt,
    height=768,
    width=768,
    num_inference_steps=15
).images[0]
```

### Batch Generation
Generate multiple images at once by modifying the code to use `num_images_per_prompt` parameter.

### Different Models
Try other Stable Diffusion models:
- `CompVis/stable-diffusion-v1-4` (smaller, faster)
- `stabilityai/stable-diffusion-2-1` (newer, better quality)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project uses Stable Diffusion models which have their own licenses. Please review the model licenses on Hugging Face.

## Acknowledgments

- [Stable Diffusion](https://github.com/CompVis/stable-diffusion) by CompVis
- [Diffusers](https://github.com/huggingface/diffusers) by Hugging Face
- [Gradio](https://github.com/gradio-app/gradio) for the web interface

## Support

For detailed usage instructions, see [HOW_TO_USE_AI_GENERATOR.md](HOW_TO_USE_AI_GENERATOR.md)

---

**Note**: This is a CPU-optimized version. For faster generation, consider using GPU-enabled cloud services like Google Colab or AWS.
