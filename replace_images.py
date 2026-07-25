import os
import shutil
import tempfile
import zipfile
import gc


def replace_images(input_doc, output_doc, images_folder="images"):

    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    temp_zip.close()

    try:

        with zipfile.ZipFile(input_doc, "r") as zin:
            with zipfile.ZipFile(
                temp_zip.name,
                "w",
                compression=zipfile.ZIP_DEFLATED,
            ) as zout:

                for item in zin.infolist():

                    if item.filename.startswith("word/media/"):

                        image_name = os.path.basename(item.filename)
                        image_path = os.path.join(images_folder, image_name)

                        if os.path.exists(image_path):

                            with open(image_path, "rb") as img:

                                # Stream image instead of reading everything at once
                                zout.writestr(item, img.read())

                            print(f"Replaced {item.filename}")

                        else:
                            zout.writestr(item, zin.read(item.filename))

                    else:
                        zout.writestr(item, zin.read(item.filename))

                    gc.collect()

        shutil.move(temp_zip.name, output_doc)

        print("\nImages inserted successfully.")

    finally:

        if os.path.exists(temp_zip.name):
            os.remove(temp_zip.name)

        gc.collect()