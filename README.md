# brush_converter

A tool for converting digital brush formats between different painting applications.

Many popular brush formats are proprietary and undocumented, making it difficult to reuse brushes outside their original software.

`brush_converter` aims to solve this problem. It translates brushes into a readable JSON format which can then be converted into various application-specific brush formats.

## Using the GUI App

You can generally convert from any brush to any other brush, as long as the load/save is supported.

For example, to convert brushes from Procreate to Medibang:
1. Go to Procreate > Load:
    - Select the files / folders for each (blue) input button.
    - Click "Load As JSON". This will create a .json file and .png files in your chosen output folder.
2. Go to Medibang > Save:
    - Select the files / folders for each (blue) input button (Medibang config folder will be selected for you).
    - Click "Convert & Save". This will generate / convert the final converted brush.

You can then import generated brush files into your drawing app.
In the case of Medibang, the files are read/written directly from the config folder.

## Formats

Conversion between formats may result in loss of detail. Brush settings may not be readable or may be incompatible with other software.

### Current status of application support:

| Application       | Loading | Saving |
|-------------------|---------|--------|
| GIMP              | ✅ | ✅ |
| Medibang Paint    | ✅ | ✅ |
| Procreate         | ✅ | ✅ |
| Clip Studio Paint | ✅ | ❌ |
| Photoshop         | ✅ | ❌ |
| IbisPaint         | ❌ | ❌ |

### About features marked with '❌'
This project hopes to expand support for these features. However, due to the proprietary and closed nature of these file formats, full implementation is not guaranteed and may ultimately prove technically unfeasible.

Current progress and roadblocks:
- **Clip Studio Paint (Saving)**: Requires rebuilding the internal sqlite database structure while maintaining compatibility with the CSP engine.
- **Photoshop (Saving)**: Requires further research into the undocumented segments of the `.abr` format.
- **IbisPaint**: Exploring methods to decode and interpret the QR code data.

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

## Installation

### Prebuilt executable

The simplest way is to download and run the prebuilt executable from [releases](https://github.com/VarunVF/brush_converter/releases/latest).

Alternatively, to build from source, follow the installation instructions below.

### Building

After cloning the repo, install the dependencies.

Example using Windows:
```sh
git clone https://github.com/VarunVF/brush_converter/
cd .\brush_converter\
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Running

After installing the dependencies, you can run in any of the following ways.

### Running the GUI App (executable)

`pyinstaller` is used to build the GUI app executable. Build and run:
```sh
pyinstaller .\brush_converter.spec
.\dist\brush_converter.exe
```

#### Spec File

The spec file is generated using the options of this command:
```sh
pyinstaller --noconsole --onefile --collect-all customtkinter --paths=. gui/main.py --name brush_converter
```

### Running the GUI App (Python)

Run the Python code directly:
```sh
python -m gui.main
```

### Running the CLI

You can also run the command-line interface for each module directly if you prefer. For example, to use the Photoshop loading module, make sure the dependencies are installed, then run:

```sh
python -m photoshop.load_photoshop <ABR_FILE> <OUTPUT_DIR>
```

Remember to replace `<ABR_FILE>` and `<OUTPUT_DIR>` with your actual file and desired output folder.
Wildcards (`*`) are supported for loading multiple input brush files.
