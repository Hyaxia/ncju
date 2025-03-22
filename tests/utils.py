def get_size_of_file(path: str) -> int:
    """
    Calculate size of a file in bytes by running ls -l 
    """
    import subprocess

    result = subprocess.run(["ls", "-l", path], stdout=subprocess.PIPE)
    size = int(result.stdout.split()[4])
    return size
    