import requests
import replicate
import base64
import os

REPLICATE_API = os.getenv("Replicate_API")



def Deepbooru(url):
  file = requests.get(str(url))
  format = str(url).split(".")[-1]
  encoded_alpha = base64.b64encode(file.content).decode("utf-8")

  encoded_final = f"data:image/{format};base64,{encoded_alpha}"

  data = {
    'data': [encoded_final, 0.5]
  }
  response = requests.post(
    "https://hysts-deepdanbooru.hf.space/api/predict",
    json = data
    ).json()
  results = response["data"][0]['confidences']

  tags = []
  accuracies = []
  for i in range(len(results)):
    tag = results[i]['label'].replace("_"," ").title()
    accuracy = results[i]['confidence']
    tags.append(tag)
    accuracies.append(accuracy)

  return dict(zip(tags, accuracies))


class StableDiffusion:
  """
  Stable Diffusion using Replicate API
  """
  
  def __init__(self):
    client = replicate.Client(REPLICATE_API)
    base = client.models.get("stability-ai/stable-diffusion")
    self.model = base.versions.get(
      "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
    )

  def input(
            self,
            prompt,
            negative_prompt,
            dimensions="768x768",
            total_img = 1,
            steps = 25,
            scale = 7.5,
            scheduler="DPMSolverMultistep"
  ):
    inputs = {
      'prompt': prompt,
      'negative_prompt': negative_prompt,
      'image_dimensions': dimensions,
      'num_outputs': total_img,
      'num_inference_steps': steps,
      'guidance_scale': scale,
      'scheduler': scheduler
    }
    output = self.model.predict(**inputs)
    return {
      'image_url': output[0],
      'negative_prompt': negative_prompt,
      'dimensions': dimensions,
      'steps': steps,
      'scheduler': scheduler,
      'scale': scale
    }



class PastelMix:


  def __init__(self):
    client = replicate.Client(REPLICATE_API)
    base = client.models.get('elct9620/pastel-mix')
    self.model = base.versions.get('ba8b1f407cd6418fa589ca73e5c623c081600ecff19f7fc3249fa536d762bb29')

  def input(
    self,
    prompt,
    negative_prompt,
    width,
    height,
    steps,
    guidance,
    seed,
    hires
  ):
    inputs = {
      'prompt': prompt,
      'neg_prompt': negative_prompt,
      'width': width,
      'height': height,
      'steps': steps,
      'guidance': guidance,
      'seed': seed,
      'hires': hires
    }
    output = self.model.predict(**inputs)
    return output



