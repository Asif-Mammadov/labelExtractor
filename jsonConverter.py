import base64
import json
import os
from glob import glob

from PIL import Image
from argparse import ArgumentParser


def main():
  parser = ArgumentParser(description='Extracts labels from json file')
  parser.add_argument('--in', dest='input_path', action='store', required=True,
                      help='Input folder')
  parser.add_argument('--out', dest='output_path', action='store', required=True,
                      help='Output folder')

  args = parser.parse_args()
  args_dict = vars(args)
  input_path = args_dict['input_path']
  output_path = args_dict['output_path']

  json_files = glob(input_path + "/*.json")
  files_len = len(json_files)
  for i, json_file in enumerate(json_files):
    print("{:.2f} % Extarcting labels for {}".format((i * 100 / files_len), json_file))
    extract(json_file, output_path)
  print("Done!")

def extract(file_name, output_folder):
  f = open(file_name, encoding='utf-8')
  data = json.load(f)

  with open("tmp.jpg", "wb") as fh:
    fh.write(base64.b64decode(data["imageData"]))

  img = Image.open("tmp.jpg")
  count = 0
  for shape in data["shapes"]:
    if shape["shape_type"] == "rectangle":
      points = shape["points"]
      if (points[0][1] > points[1][1]):
        points[0][1], points[1][1] = points[1][1], points[0][1]
      if (points[0][0] > points[1][0]):
        points[0][0], points[1][0] = points[1][0], points[0][0]
      img_res = img.crop((points[0][0], points[0][1], points[1][0], points[1][1]))

      file_name = os.path.join(output_folder, data["imagePath"].split(".")[0] + "_crop_" + str(count))
      img_res.save(file_name + ".jpg")
      text_file = open(file_name + ".txt", "w", encoding='utf-8')
      text_file.write(shape["label"])
      count += 1

if __name__ == "__main__":
  main()