from PIL import Image

def dominant_color(image_path):
  """
  Algorithm to get a dominant color
  from an image 
  """
  
  image = Image.open(image_path)
  image = image.convert('RGBA')
  pixels = image.getdata()

  red_pixels = 0
  green_pixels = 0
  blue_pixels = 0
  total_pixels = 0

  for pixel in pixels:
    red_pixels += pixel[0]
    green_pixels += pixel[1]
    blue_pixels += pixel[2]
    total_pixels += 1

  avg_red = red_pixels / total_pixels
  avg_green = green_pixels / total_pixels
  avg_blue = blue_pixels / total_pixels

  colors = (int(avg_red), int(avg_green), int(avg_blue))
  return colors
  
