from setuptools import setup, find_packages

setup(
    name="PDV Rex",
    version="1.0.0",
    author="Luan Alves",
    author_email="luanalves9895@gmail.com",
    description="O PDV Rex foi desenvolvido para agilizar seu dia-a-dia.",
    long_description="Agilidade, organização e flexibilidade. Você encontra no PDV Rex.",
    long_description_content_type="text/plain",  # Se você usar Markdown
    url="https://github.com/LuanAllves/Gerador-de-Recibo",
    packages=find_packages(),
    install_requires=[
        # Lista de dependências
    ],
    entry_points={
        "console_scripts": [
            "PDV Rex = pdv.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #exemplo de licença
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', # versao minima do python
)