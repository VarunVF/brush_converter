# brush_converter

A tool for converting digital brush formats between different painting applications.

Many popular brush formats are proprietary and undocumented, making it difficult to reuse brushes outside their original software.

`brush_converter` aims to solve this problem. It translates brushes into a readable JSON format which can then be converted into various application-specific brush formats.

## Intermediate JSON

This project reads brush settings into an intermediate JSON file, and a PNG texture when applicable.

JSON format (example):
```json
[
    {
        "name": "Brush 1",
        "type": "bitmap",
        "width": 32,
        "minimumBrushSize": 0.0,
        "opacity": 1,
        "pressureChangesSize": true,
        "pressureChangesOpacity": false,
        "bitmapfile": "GIMP Brush.png",
        "brushSpacing": 1.6,
        "doRotateAlong": 1,
        "rotateAngle": 50,
        "randomRotateAngle": 0,
        "applyForegroundColor": 1,
        "colorJitter": 0,
        "hueJitter": 0
    },
    {
        "name": "Brush 2",
        // other options ...
    },
    // other brushes ...
]
```

## Formats

Conversion between formats may result in loss of detail. Brush settings may not be readable or may be incompatible with other software.

Applications currently supported:
- GIMP
- Medibang Paint
- Procreate

This project hopes to eventually support converting between these applications:
- Clip Studio Paint
- IbisPaint
- Photoshop

## Building the GUI App

`pyinstaller` is used to build the executable. After closing the repo, install the libraries and run the build command.

Example using Windows:
```sh
git clone https://github.com/VarunVF/brush_converter/
cd .\brush_converter\
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
pyinstaller .\brush_converter.spec
```

Finally, run the GUI app using:
```sh
python -m gui.main
```

### Spec File

The spec file is generated using the options of this command:
```sh
pyinstaller --noconsole --onefile --collect-all customtkinter --paths=. gui/main.py --name brush_converter
```
