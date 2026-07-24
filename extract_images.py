import os
import shutil
import zipfile


def extract_images(docx_path, output_folder="images"):


    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)


    os.makedirs(output_folder)

    with zipfile.ZipFile(docx_path, "r") as docx:

        for file in docx.namelist():

            if file.startswith("word/media/"):

                filename = os.path.basename(file)

                destination = os.path.join(output_folder, filename)

                with docx.open(file) as source:
                    with open(destination, "wb") as target:
                        shutil.copyfileobj(source, target)

    print("Images extracted successfully.")