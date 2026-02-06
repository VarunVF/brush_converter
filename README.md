# brush_converter

A tool for converting digital brush formats between different painting applications.

It translates brushes into a readable JSON format which can then be converted into various application-specific brush formats.

Many popular brush formats are proprietary and undocumented, making it difficult to reuse brushes outside their original software.

## Intermediate JSON

This project reads brush settings into an intermediate JSON file, and a PNG texture when applicable.

JSON format:
```json
[
    {
        "name": "brush_1",
        "type": "bitmap",
        "width": 30,
        "bitmapfile": "brush_1.png",
        // other options ...
    },
    {
        "name": "brush_2",
        "type": "bitmap",
        "width": 40,
        "bitmapfile": "brush_2.png",
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

This project hopes to eventually support converting between these applications:
- Clip Studio Paint
- GIMP
- IbisPaint
- Medibang Paint
- Photoshop
- Procreate
