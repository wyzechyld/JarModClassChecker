import os
import zipfile
import shutil

def list_class_files_in_jar(jar_file):
    class_files = []
    with zipfile.ZipFile(jar_file, 'r') as zipf:
        for file_info in zipf.infolist():
            if file_info.filename.endswith('.class'):
                class_files.append(file_info.filename)
    return class_files

def check_mods_compatibility(mod_folder):
    mod_files = [os.path.join(mod_folder, file) for file in os.listdir(mod_folder) if file.endswith('.jar')]
    incompatible_files = []
    
    for i in range(len(mod_files)):
        for j in range(i + 1, len(mod_files)):
            mod1 = mod_files[i]
            mod2 = mod_files[j]
            mod1_classes = set(list_class_files_in_jar(mod1))
            mod2_classes = set(list_class_files_in_jar(mod2))
            
            overlapping_classes = mod1_classes.intersection(mod2_classes)
            
            if overlapping_classes:
                print(f"Mods '{os.path.basename(mod1)}' and '{os.path.basename(mod2)}' may be incompatible due to overlapping class files:")
                for file in overlapping_classes:
                    print(file)
                incompatible_files.extend([mod1, mod2])
            else:
                print(f"Mods '{os.path.basename(mod1)}' and '{os.path.basename(mod2)}' should be compatible.")
    
    if incompatible_files:
        print("\nList of incompatible class files:")
        for file in incompatible_files:
            print(file)
        
        # Create a folder for incompatible mods in the same directory as the script
        script_directory = os.path.dirname(__file__)
        output_folder = os.path.join(script_directory, "Incompatible_Mods")
        os.makedirs(output_folder, exist_ok=True)
        
        # Move incompatible mods to the output folder
        for mod_file in incompatible_files:
            shutil.move(mod_file, os.path.join(output_folder, os.path.basename(mod_file)))
    else:
        print("\nNo incompatible class files found. All mods should be compatible.")

if __name__ == "__main__":
    mod_folder = input("Please enter the path to the folder containing the .jar mod files: ")
    check_mods_compatibility(mod_folder)
