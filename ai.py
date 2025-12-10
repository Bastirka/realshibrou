import os
import torch
import numpy as np
from diffusers import StableDiffusionPipeline
import gradio as gr


class Config:
    """Configuration class for easy upgrades and tuning."""
    def __init__(self):
        # Bāzes modelis – stabils, populārs
        self.model_name = "runwayml/stable-diffusion-v1-5"

        # Device izvēle – automātiski izmanto GPU, ja ir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Kur saglabāt bildes
        self.output_dir = "generated_images"

        # MAX kvalitātes defaulti (var mainīt GUI)
        self.num_inference_steps = 40      # 40 = augsta kvalitāte, bet vēl nav crazy lēni
        self.guidance_scale = 7.5

        # Izšķirtspēja – labs balanss starp kvalitāti un ātrumu
        self.height = 768
        self.width = 512

        # Negatīvais prompts – lai nebūtu kroplas rokas u.c.
        self.default_negative_prompt = (
            "deformed, extra fingers, mutated hands, poorly drawn hands, extra limbs, "
            "bad anatomy, low quality, blurry, grainy, distorted face"
        )


class ModelHandler:
    """Handles model loading and upgrades."""
    def __init__(self, config: Config):
        self.config = config
        self.pipeline: StableDiffusionPipeline | None = None
        self.load_model()

    def load_model(self):
        """Load or reload the AI model."""
        print(f"Loading model: {self.config.model_name}")
        try:
            dtype = torch.float16 if self.config.device == "cuda" else torch.float32

            pipe = StableDiffusionPipeline.from_pretrained(
                self.config.model_name,
                torch_dtype=dtype,
                safety_checker=None,
                requires_safety_checker=False,
            )

            pipe = pipe.to(self.config.device)

            # Performance optimizations
            if self.config.device == "cuda":
                try:
                    pipe.enable_xformers_memory_efficient_attention()
                    print("xFormers attention enabled for speed.")
                except Exception:
                    print("xFormers not available, using default attention.")
            else:
                # Uz CPU taupām atmiņu
                pipe.enable_attention_slicing("auto")
                print("Attention slicing enabled for CPU.")

            self.pipeline = pipe
            print("Pipeline loaded successfully:", self.pipeline is not None)

        except Exception as e:
            print(f"Error loading model: {e}")
            self.pipeline = None

    def upgrade_model(self, new_model_name: str):
        """Upgrade to a new model version."""
        self.config.model_name = new_model_name
        self.load_model()
        print(f"Model upgraded to: {new_model_name}")


class ImageGenerator:
    """Main class for generating images."""
    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.model_handler = ModelHandler(self.config)
        os.makedirs(self.config.output_dir, exist_ok=True)

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        steps: int | None = None,
        guidance_scale: float | None = None,
        seed: int | None = None,
        output_filename: str = "generated_image.png",
    ):
        """Generate an image from a text prompt."""
        print(f"Generating image for prompt: '{prompt}'")

        if self.model_handler.pipeline is None:
            print("Pipeline not loaded—cannot generate.")
            return None

        # Default parametri
        if steps is None:
            steps = self.config.num_inference_steps
        if guidance_scale is None:
            guidance_scale = self.config.guidance_scale
        if not negative_prompt or not negative_prompt.strip():
            negative_prompt = self.config.default_negative_prompt

        # Seed kontrole (atkārtojamība)
        generator = None
        if seed is not None:
            try:
                seed = int(seed)
                generator = torch.Generator(self.config.device).manual_seed(seed)
                print(f"Using seed: {seed}")
            except ValueError:
                print("Invalid seed, ignoring.")
                generator = None

        try:
            result = self.model_handler.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=int(steps),
                guidance_scale=float(guidance_scale),
                height=self.config.height,
                width=self.config.width,
                generator=generator,
            )
            image = result.images[0]

            # Check for almost-black image
            img_array = np.array(image)
            if img_array.mean() < 10:
                print("Warning: Generated image appears very dark/black.")

            output_path = os.path.join(self.config.output_dir, output_filename)
            image.save(output_path)
            print(f"Image saved to: {output_path}")

            return image

        except Exception as e:
            print(f"Error generating image: {e}")
            return None


def create_gui(generator: ImageGenerator):
    """Create and launch the Gradio GUI."""
    def generate_and_display(prompt, negative, steps, cfg, seed):
        if not prompt or not prompt.strip():
            return "Please enter a prompt!", None

        image = generator.generate_image(
            prompt=prompt,
            negative_prompt=negative,
            steps=steps,
            guidance_scale=cfg,
            seed=seed if seed not in ("", None) else None,
        )

        if image is None:
            return "Generation failed—check terminal for errors.", None

        return f"Image generated for: '{prompt}'", image

    with gr.Blocks() as interface:
        gr.Markdown("# 🧠 AI Image Generator (MAX quality mode)")
        gr.Markdown(
            "Higher steps = better quality but slower. GPU is used automatically if available."
        )

        prompt_input = gr.Textbox(
            label="Prompt",
            placeholder="e.g., ultra detailed portrait, cinematic lighting, 8k",
        )

        negative_input = gr.Textbox(
            label="Negative prompt",
            value=generator.config.default_negative_prompt,
        )

        steps_input = gr.Slider(
            minimum=20,
            maximum=80,  # līdz 80 – ļoti lēns, bet max kvalitāte
            value=generator.config.num_inference_steps,
            step=1,
            label="Steps (num_inference_steps)",
        )

        cfg_input = gr.Slider(
            minimum=1.0,
            maximum=15.0,
            value=generator.config.guidance_scale,
            step=0.5,
            label="Guidance scale (CFG)",
        )

        seed_input = gr.Number(
            label="Seed (optional, same seed = similar image)",
            value=0,
        )

        generate_btn = gr.Button("Generate Image")
        status_output = gr.Textbox(label="Status", interactive=False)
        image_output = gr.Image(label="Generated Image")

        generate_btn.click(
            generate_and_display,
            inputs=[prompt_input, negative_input, steps_input, cfg_input, seed_input],
            outputs=[status_output, image_output],
        )

    interface.launch(pwa=True)


if __name__ == "__main__":
    generator = ImageGenerator()

    # Ja gribi, vari pārslēgties uz citu modeli, piem. SD 2.1:
    # generator.model_handler.upgrade_model("stabilityai/stable-diffusion-2-1")

    create_gui(generator)
