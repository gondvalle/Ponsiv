# Ponsiv

A small Kivy/KivyMD demo application.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m ponsiv.main
```

Product information is loaded automatically from the ``assets`` directory. Each
product has a JSON description in ``assets/informacion`` and a corresponding
image in ``assets/prendas``. Brand logos live in ``assets/logos``. Adding a new
product only requires placing its JSON and image files in these folders.

The window is fixed at **360×640** and uses a dark theme.
