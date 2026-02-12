# Based on/incorporating logic from CSPExtract
# Original Source: https://github.com/Loperamide/CSPExtract/
# License: Unlicense

import os
import sqlite3


def get_last_pos(str, source):
    str_find = bytearray(str, 'ascii')
    last_pos = 0
    pos = 0
    while True:
        pos = source.find(str_find, last_pos)
        if pos == -1:
            break
        last_pos = pos + 1
    return (last_pos -1)


def extract_png_from_layer(working_file, output_dir):
    try:
        with open(working_file, "rb") as inputFile:
            content = inputFile.read()
            if content != "":
                s = 'PNG'
                begin_pos = get_last_pos(s, content)
                begin_pos -= 1

                s = 'IEND'                
                end_pos = get_last_pos(s, content)
                end_pos += 4

                output_filename = os.path.join(output_dir, os.path.basename(working_file) + ".png")
                with open(output_filename, 'wb') as outputFile:
                    outputFile.write(content[begin_pos:end_pos])
    except FileNotFoundError:
        print(f"File not found: {working_file}")


def extract_sqlite_layers(working_file, output_dir):
    con = sqlite3.connect(working_file)
    cur = con.cursor()
    cur.execute("select _PW_ID, FileData from MaterialFile")
    row = cur.fetchone()
    while row != None:
        #extract images
        file_name = working_file + "." + str(row[0]) + ".layer"
        with open(file_name, 'wb') as outputFile:
            outputFile.write(row[1])
            extract_png_from_layer(file_name, output_dir)
        os.remove(file_name)
        row = cur.fetchone()
    cur.close()


def read_sut(db_file: str, output_dir: str) -> list[dict]:
    con = sqlite3.connect(db_file)

    info_row = con.execute("select _PW_ID, FileData from MaterialFile").fetchone()
    file_name = os.path.basename(db_file) + "." + str(info_row[0]) + ".layer.png"

    brush_json = [
        {
            "name": con.execute("SELECT NodeName from Node;").fetchone()[0],
            "type": "bitmap",
            "width": con.execute("SELECT BrushSize from Variant;").fetchone()[0],
            "minimumBrushSize": 0.0,
            "opacity": con.execute("SELECT Opacity from Variant;").fetchone()[0],
            "pressureChangesSize": True,
            "pressureChangesOpacity": False,
            "bitmapfile": file_name,
            "brushSpacing": con.execute("SELECT BrushInterval from Variant;").fetchone()[0],
            "doRotateAlong": 1,
            "rotateAngle": con.execute("SELECT BrushRotation from Variant;").fetchone()[0],
            "randomRotateAngle": con.execute("SELECT BrushRotationRandomScale from Variant;").fetchone()[0],
            "applyForegroundColor": 1,
            "colorJitter": 0,
            "hueJitter": 0
        }
    ]

    con.close()
    extract_sqlite_layers(db_file, output_dir)

    return brush_json
