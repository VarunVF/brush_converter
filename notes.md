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

Adobe brushes use a proprietary .abr format. This format is complex.

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
