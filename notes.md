# Notes

Brush info and notes collected over time.

## Clip Studio Paint

Uses the .sut ("subtool) file format, or .sutg for multiple brushes in a single package. This is a SQLite database.

CSP also supports loading .abr brush files.

## GIMP

[GIMP Paintbrush File Format (.gbr)](https://developer.gimp.org/core/standards/gbr/)

## IbisPaint

IbisPaint uses their own QR code reading and loading logic.

The raw data from the QR code starts with "IPBZ". The rest of the data is binary and we need to find a way to decode it.

## Medibang Paint

Primarily uses the Brush2.ini config file to store brush settings. Bitmap brushes reference a bitmap file. Default brushes reference a .bs "script" file which is actually a Lua script.

Brush bitmaps need to be inverted (byte = 255 - byte) for use in Medibang.

### Brush Scripts

This brush script draws red dots with a diameter of 10px.
Code is from the article [MediBang News Vol.11. The road to a Brush Creator.](https://medibangpaint.com/en/use/2022/07/medibangnews_0011/).

```lua
function main( x, y, p )
  bs_ellipse(x, y, 10, 10, 0 , 255, 0, 0, 255 )
  return 1
end
```

`x` and `y` are the x and y coordinates on the canvas where the brush is applied. Coordinates are positive and measured from the topleft corner (0, 0).
`p` likely stands for "pressure" here.

The return value, 0 or 1, may signify whether the brush was able to successfully draw.

## Photoshop

Adobe Photoshop's `.abr` brushes use a proprietary format. Photoshop `.abr` files (specifically version 10/CS6+) function as a binary container for brush "samples". Unlike other some formats, it is a continuous binary stream that requires precise pointer management to navigate.

### Structure and Navigation

The file is organized into `8BIM` resource blocks. To find the pixel data, you must scan for the `8BIMsamp` marker, which acts as the container for all sampled brushes in the set.

Each brush entry within the `samp` block contains a metadata header. Depending on the minor version, this header has a fixed length (e.g., 47 bytes or 301 bytes). If the minor version is unknown, the metadata has variable size, and the data must be found by scanning for a valid "dimension block" (x/y min and max values).

Photoshop requires 4-byte alignment between brush entries. After reading a brush, the file pointer must be moved to the next multiple of 4 to stay in sync with the file structure.

### Pixel Decompression

Photoshop uses a row-based **PackBits RLE (Run-Length Encoding)**. If the data is simply decoded as one giant block, the images will have a "wraparound" or "shifted" glitch.

Immediately following the compression byte, there is a table of `uint16_t` values (one for every row of the brush height). Each row must be decoded individually based on the byte length provided in the table.

### Image Requirements

Like Medibang, 8-bit grayscale brushes need to be inverted for standard bitmap use. 8-bit brushes are standard grayscale, while 32-bit brushes contain interleaved RGB+Alpha data. When extracting 32-bit brushes, the Alpha channel must be de-interleaved (every 4th byte) to create a transparent PNG.

## Procreate

Brushes are stored as .brush or .brushset files. Both of these are simply .zip files. When unzipped, each brush folder contains the image file and a .archive file (which is actually an Apple binary property list file).

The property list file can be loaded like this:
```python
>>> import plistlib
>>> with open("Brush.archive", "rb") as f:
...     data = plistlib.load(f)
>>> data.keys()
dict_keys(['$version', '$objects', '$archiver', '$top'])
```

This is an example structure of the plist data. UIDs are indices in the $objects array.
```
// $version
100000

// $objects
[
  // UID 0
  '$null',
  
  // UID 1
  {
    'shapeOrientation': 1,
    // ...
    'bundledShapePath': UID(0),  // refers to the first object (null)
    // ...
    'bundledGrainPath': UID(2),  // refers to third object (string filename)
    // ...
    'name': UID(4),  // brush name
    '$class': UID(5),  // perhaps code symbols?
    'color': UID(3),  // likely RGBA format brush color
    // ...
  },

  // UID 2
  'grain.jpg',
  
  // UID 3
  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
  
  // UID 4
  'Bubbles',
  
  // UID 5
  {
      '$classname': 'SilicaBrush',
      '$classes': ['SilicaBrush', 'NSObject']
  }
]

// $archiver
NSKeyedArchiver

// $root
{
  'root': UID(1)
}
```
