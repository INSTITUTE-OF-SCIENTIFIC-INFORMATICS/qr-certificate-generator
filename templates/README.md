# Certificate Templates

This directory contains certificate templates used by the generator.

## Creating the Template

Run the template creation script:
```bash
python create_template.py
```

This will generate `certificate_template.png` in this directory.

## Custom Templates

You can replace `certificate_template.png` with your own custom template:

### Requirements
- **Format**: PNG (recommended) or JPEG
- **Size**: 2480×1754 pixels (A4 landscape at 300 DPI)
- **Color mode**: RGB

### Design Considerations
- Leave space in the center for participant name (approximately y: 600-800px)
- Leave space below the name for course information (y: 900-1100px)
- Reserve bottom-right corner for QR code (300×300px area)
- Reserve bottom-left for certificate ID text

### Template Layers
The generator adds the following elements to your template:
1. Participant name (centered, large font)
2. Course/program name (centered below name)
3. Issue date (centered below course)
4. Certificate ID (bottom-left)
5. QR code (bottom-right, 250×250px)

## Template Customization

To customize the generated template, edit `create_template.py`:
- Change colors by modifying hex color codes
- Adjust border styles and decorations
- Modify text elements and positioning
- Add logos or additional graphics
