from setuptools import setup

with open('README.md') as fp:
    long_description = fp.read()

def parse_req_line(line):
    line = line.strip()
    if not line or line[0] == '#':
        return None
    return line

def load_requirements(file_name):
    with open(file_name) as fp:
        reqs = filter(None, (parse_req_line(line) for line in fp))
        return list(reqs)

install_requires=load_requirements('requirements.txt')
# On appelle la fonction setup
setup(
    name = "competencesplus",
    version = "1.0.0",
    description = "test",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Jeremy Fouquet',
    author_email = 'jeremy.fouquet02@etud.univ-paris8.fr',
    url = 'https://github.com/jeremyfouquet/competencesplus.git',
    license = 'MIT License',
    install_requires = install_requires
)
