import torch
from diffusers import StableDiffusionPipeline
from transformers import CLIPTokenizer, CLIPTextModel
import os
import gradio as gr  # For the GUI

class Config:
    """Configuration class for easy upgrades."""
    def __init__(self):
        self.model_name = "runwayml/stable-diffusion-v1-5"  # Switched to v1-5 for better stability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "generated_images"
        self.num_inference_steps = 15  # Reduced from 25 to 15 for faster generation (30-40% faster)
        self.guidance_scale = 7.5

class ModelHandler:
    """Handles model loading and upgrades."""
    def __init__(self, config):
        self.config = config
        self.pipeline = None
        self.load_model()

    def load_model(self):
        """Load the AI model."""
        print(f"Loading model: {self.config.model_name}")
        try:
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if self.config.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            ).to(self.config.device)
            print("Pipeline loaded successfully:", self.pipeline is not None)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.pipeline = None

    def upgrade_model(self, new_model_name):
        """Upgrade to a new model version."""
        self.config.model_name = new_model_name
        self.load_model()
        print(f"Model upgraded to: {new_model_name}")

class ImageGenerator:
    """Main class for generating images."""
    def __init__(self, config=None):
        self.config = config or Config()
        self.model_handler = ModelHandler(self.config)
        os.makedirs(self.config.output_dir, exist_ok=True)

    def generate_image(self, prompt, output_filename="generated_image.png"):
        """Generate an image from a text prompt."""
        print(f"Generating image for prompt: '{prompt}'")
        if self.model_handler.pipeline is None:
            print("Pipeline not loaded—cannot generate.")
            return None
        try:
            image = self.model_handler.pipeline(
                prompt,
                num_inference_steps=self.config.num_inference_steps,
                guidance_scale=self.config.guidance_scale
            ).images[0]
            print("Image generated, checking if black...")
            # Simple check for black image (all pixels near 0)
            import numpy as np
            img_array = np.array(image)
            if img_array.mean() < 10:  # Threshold for "black"
                print("Warning: Generated image appears black!")
            output_path = os.path.join(self.config.output_dir, output_filename)
            image.save(output_path)
            print(f"Image saved to: {output_path}")
            return image
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

# GUI Function
def create_gui(generator):
    """Create and launch the Gradio GUI."""
    def generate_and_display(prompt):
        if not prompt.strip():
            return "Please enter a prompt!", None
        image = generator.generate_image(prompt)
        if image is None:
            return "Generation failed—check terminal for errors.", None
        return f"Image generated for: '{prompt}'", image

    with gr.Blocks() as interface:
        gr.Markdown("# AI Image Generator for Research")
        gr.Markdown("Enter a text prompt to generate images. If black, check terminal logs.")
        
        prompt_input = gr.Textbox(label="Prompt", placeholder="e.g., Evolved human male body in 2100")
        generate_btn = gr.Button("Generate Image")
        status_output = gr.Textbox(label="Status", interactive=False)
        image_output = gr.Image(label="Generated Image")
        
        generate_btn.click(generate_and_display, inputs=prompt_input, outputs=[status_output, image_output])
    
    interface.launch(pwa=True)

# Example Usage
if __name__ == "__main__":
    generator = ImageGenerator()
    
    # Optional: Upgrade the model before launching GUI
    # generator.model_handler.upgrade_model("stabilityai/stable-diffusion-2-1")
    
    # Launch the GUI
    create_gui(generator)
