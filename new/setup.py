import subprocess

def run_as_admin(command):
    try:
        subprocess.run(["cmd.exe", "/c", command], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == "__main__":
    # Install and start the service
    run_as_admin("test.exe install")
    run_as_admin("test.exe start")