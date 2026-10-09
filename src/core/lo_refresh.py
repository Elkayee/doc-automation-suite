"""Invoked by LibreOffice's Python/UNO interpreter, not the app interpreter."""

import sys
import time
from pathlib import Path

import uno


def property_value(name, value):
    prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
    prop.Name, prop.Value = name, value
    return prop


def main():
    port, source, output = sys.argv[1:]
    context = uno.getComponentContext()
    resolver = context.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', context)
    remote = None
    last_error = None
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        try:
            remote = resolver.resolve(f'uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext')
            break
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.2)
    if remote is None:
        raise RuntimeError(f'Không kết nối được LibreOffice/UNO: {last_error}')
    desktop = remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', remote)
    document = None
    try:
        document = desktop.loadComponentFromURL(Path(source).resolve().as_uri(), '_blank', 0, (
            property_value('Hidden', True), property_value('UpdateDocMode', 3),
            property_value('MacroExecutionMode', 0), property_value('ReadOnly', False),
        ))
        if document is None:
            raise RuntimeError('LibreOffice không mở được DOCX')
        for _ in range(2):
            document.TextFields.refresh()
            indexes = document.getDocumentIndexes()
            for index in range(indexes.getCount()):
                indexes.getByIndex(index).update()
            document.refresh()
        for family_name in ('ParagraphStyles', 'CharacterStyles'):
            family = document.StyleFamilies.getByName(family_name)
            for name in family.getElementNames():
                family.getByName(name).CharColor = 0
        output = Path(output)
        document.storeAsURL((output / 'refreshed.docx').as_uri(), (
            property_value('FilterName', 'Office Open XML Text'), property_value('Overwrite', True),
        ))
        document.storeToURL((output / 'rendered.pdf').as_uri(), (
            property_value('FilterName', 'writer_pdf_Export'), property_value('Overwrite', True),
        ))
    finally:
        if document is not None:
            document.close(True)
        desktop.terminate()


if __name__ == '__main__':
    main()
