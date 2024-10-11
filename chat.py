from gradio_client import Client


def chat_gemma(txt: str):
    client = Client("huggingface-projects/gemma-2-2b-jpn-it")
    result = client.predict(
        message=f"{txt}",
        max_new_tokens=1024,
        temperature=0.6,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.2,
        api_name="/chat"
    )
    return result


if __name__ == '__main__':
    from gradio_client import Client, handle_file

    client = Client("finegrain/finegrain-image-enhancer")
    result = client.predict(
        input_image=handle_file('C:/Users/50010242/Pictures/image.webp'),
        prompt="Hello!!",
        negative_prompt="Hello!!",
        seed=42,
        upscale_factor=2,
        controlnet_scale=0.6,
        controlnet_decay=1,
        condition_scale=6,
        tile_width=112,
        tile_height=144,
        denoise_strength=0.35,
        num_inference_steps=18,
        solver="DDIM",
        api_name="/process"
    )
    print(result)
