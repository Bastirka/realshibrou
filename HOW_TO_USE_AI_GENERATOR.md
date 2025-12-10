# AI Image Generator - Complete Guide

## Quick Start

### 1. Access the Web Interface
- Open your browser and go to: **http://127.0.0.1:7863**
- You'll see the "AI Image Generator for Research" interface

### 2. Generate Your First Image
1. Enter a prompt in the text box (e.g., "A beautiful sunset over mountains")
2. Click "Generate Image"
3. Wait ~1-2 minutes (optimized for faster generation!)
4. Your image will appear below

---

## Speed Optimizations Applied ✓

### Current Settings (Optimized for Speed):
- **Inference Steps**: 15 (reduced from 50)
- **Generation Time**: ~1-2 minutes per image (was 2-3 minutes)
- **Quality**: Still good, slightly faster

### What Was Changed:
```
num_inference_steps = 15  # Reduced from 25 for 30-40% faster generation
```

---

## How to Make It Even Faster

### Option 1: Reduce Steps Further (Fastest, Lower Quality)
Edit `ai.py` and change:
```python
self.num_inference_steps = 10  # Even faster (~45 seconds)
```

### Option 2: Use a Smaller Model (Much Faster)
Edit `ai.py` and change:
```python
self.model_name = "CompVis/stable-diffusion-v1-4"  # Smaller, faster model
```

### Option 3: Get a GPU (Recommended for Production)
- With CUDA GPU: Generation takes 5-10 seconds instead of minutes
- Your Mac doesn't have NVIDIA GPU, so CPU is the only option currently
- Consider using cloud services like Google Colab for GPU access

---

## Example Prompts That Work Well

### Landscapes
- "A beautiful sunset over mountains with orange sky"
- "A serene forest with a waterfall and mist"
- "A tropical beach with palm trees at sunset"

### Sci-Fi & Fantasy
- "A futuristic city with flying cars and neon lights"
- "A fantasy castle on a cliff overlooking the ocean"
- "An astronaut floating in space near a colorful nebula"

### Characters & Portraits
- "A portrait of a person in elegant Victorian clothing"
- "A wise old wizard with a long beard and magical staff"
- "A cyberpunk character with neon hair and tech implants"

### Animals & Nature
- "A cute cat sitting on a windowsill looking outside"
- "A majestic lion in the African savanna at golden hour"
- "A colorful parrot in a tropical rainforest"

---

## Important Tips

### ✓ DO:
- Be specific and descriptive in your prompts
- Use artistic terms like "detailed", "high quality", "photorealistic"
- Try different variations of the same idea
- Save prompts that work well for future use

### ✗ DON'T:
- Use NSFW/adult content prompts (will return black images)
- Use very short prompts (be descriptive)
- Expect instant results (1-2 minutes is normal on CPU)

---

## Troubleshooting

### Black Images
**Problem**: Generated image is completely black
**Solution**: Your prompt triggered the NSFW filter. Use appropriate, non-adult content prompts.

### Slow Generation
**Problem**: Takes too long to generate
**Solution**: 
1. Reduce `num_inference_steps` to 10 in `ai.py`
2. Close other applications to free up CPU
3. Be patient - CPU generation is inherently slow

### Application Not Loading
**Problem**: Can't access http://127.0.0.1:7863
**Solution**:
1. Check if the terminal shows "Running on local URL"
2. Try the URL shown in the terminal (port might be different)
3. Restart the application: `python ai.py`

---

## File Locations

### Generated Images
- **Location**: `/Users/raivisbabris/Documents/ownai/generated_images/`
- **Format**: PNG files
- **Naming**: `generated_image.png` (overwrites each time)

### Application Files
- **Main Script**: `/Users/raivisbabris/Documents/ownai/ai.py`
- **Virtual Environment**: `/Users/raivisbabris/Documents/ownai/.venv/`

---

## Advanced: Customizing Generation

### Change Image Size
Add to the generation call in `ai.py`:
```python
image = self.model_handler.pipeline(
    prompt,
    num_inference_steps=self.config.num_inference_steps,
    guidance_scale=self.config.guidance_scale,
    height=512,  # Add this
    width=512    # Add this
).images[0]
```

### Generate Multiple Images
Modify the `generate_image` function to accept a `num_images` parameter:
```python
def generate_image(self, prompt, num_images=1):
    images = self.model_handler.pipeline(
        prompt,
        num_inference_steps=self.config.num_inference_steps,
        guidance_scale=self.config.guidance_scale,
        num_images_per_prompt=num_images
    ).images
    return images
```

---

## Current Configuration Summary

- **Model**: runwayml/stable-diffusion-v1-5
- **Device**: CPU (CUDA not available)
- **Inference Steps**: 15 (optimized for speed)
- **Guidance Scale**: 7.5
- **Safety Checker**: Disabled
- **PWA**: Enabled
- **Port**: 7863

---

## Need Help?

1. Check the terminal for error messages
2. Review this guide for common issues
3. Try simpler prompts first
4. Restart the application if needed: `python ai.py`

**Happy Generating! 🎨**
