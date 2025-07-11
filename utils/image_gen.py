# utils/image_gen.py

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler
from diffusers.schedulers.scheduling_ddim import DDIMScheduler

_scheduler_map = {
    "DPMSolver": DPMSolverMultistepScheduler,
    "EulerA": EulerAncestralDiscreteScheduler,
    "DDIM": DDIMScheduler,
}

def load_pipeline(scheduler_name):
    scheduler_cls = _scheduler_map[scheduler_name]
    scheduler = scheduler_cls.from_pretrained("runwayml/stable-diffusion-v1-5", subfolder="scheduler")

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        scheduler=scheduler,
        safety_checker=None,
        torch_dtype=torch.float32
    ).to("cpu")
    return pipe

def generate_sd_image(pipe, prompt, negative_prompt, steps, height, width):
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        height=height,
        width=width
    ).images[0]
    image.save("outputs/generated_image.png")
    return image
