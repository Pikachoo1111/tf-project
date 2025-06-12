import subprocess

def espeak(text: str, pitch: int=50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode
text = " test, 1 2 3 4  5 6 7 7 q  fd s  d d d "
espeak(text)

