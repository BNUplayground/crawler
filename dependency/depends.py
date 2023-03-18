import subprocess
import sys
import pandas as pd

def get_dependencies(image, package):
    cmd = f"docker run --rm -it {image} apt-cache showpkg {package}"
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode("utf-8").split("\n")
    dependencies = []
    for line in lines:
        if "Depends:" in line:
            parts = line.split()
            if len(parts) > 2:
                dependency = parts[1]
                version = parts[2].strip("()")
                dependencies.append(f"{dependency} ({version})")
    return dependencies

if __name__ == "__main__":
    image = sys.argv[1]
    package = sys.argv[2]
    dependencies = get_dependencies(image, package)
    print(dependencies)
    # df = pd.DataFrame({"Dependency": dependencies})
    # df.to_excel("dependencies.xlsx", index=False)
    