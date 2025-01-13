import subprocess

try:
    subprocess.run(["dot", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Graphviz is available.")
except FileNotFoundError:
    print("Graphviz is not found. Please check your installation.")
