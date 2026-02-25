import os
import shutil
os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")

#AI generated
def collect_open_pipe_plots(base_dir="weird_shapes",
                            target_dir="all_open_pipe_plots"):

    os.makedirs(target_dir, exist_ok=True)

    for folder in os.listdir(base_dir):

        folder_path = os.path.join(base_dir, folder)

        if os.path.isdir(folder_path):

            source_file = os.path.join(folder_path, "open_pipes_plot.png")

            if os.path.isfile(source_file):

                # Rename to avoid overwriting
                new_name = f"{folder}_open_pipes_plot.png"
                target_path = os.path.join(target_dir, new_name)

                shutil.copy2(source_file, target_path)

                print(f"Copied: {new_name}")

    print("Done collecting plots.")

collect_open_pipe_plots()