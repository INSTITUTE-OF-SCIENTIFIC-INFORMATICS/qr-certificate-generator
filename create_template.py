#!/usr/bin/env python3
"""
Create a certificate template
This script generates a blank certificate template that can be used
by the certificate generator.
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_certificate_template(width=2480, height=1754, output_path="templates/certificate_template.png"):
    """
    Create a certificate template
    
    Args:
        width: Width of the certificate in pixels (default: A4 landscape at 300 DPI)
        height: Height of the certificate in pixels
        output_path: Path to save the template
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw decorative border
    border_color = '#2c3e50'
    border_width = 30
    
    # Outer border
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=border_color,
        width=8
    )
    
    # Inner border
    inner_offset = border_width + 20
    draw.rectangle(
        [(inner_offset, inner_offset), (width - inner_offset, height - inner_offset)],
        outline=border_color,
        width=4
    )
    
    # Draw corner decorations
    corner_size = 100
    corner_color = '#3498db'
    
    # Top-left corner
    draw.arc([(border_width + 40, border_width + 40), 
              (border_width + 40 + corner_size, border_width + 40 + corner_size)],
             start=180, end=270, fill=corner_color, width=6)
    
    # Top-right corner
    draw.arc([(width - border_width - 40 - corner_size, border_width + 40), 
              (width - border_width - 40, border_width + 40 + corner_size)],
             start=270, end=360, fill=corner_color, width=6)
    
    # Bottom-left corner
    draw.arc([(border_width + 40, height - border_width - 40 - corner_size), 
              (border_width + 40 + corner_size, height - border_width - 40)],
             start=90, end=180, fill=corner_color, width=6)
    
    # Bottom-right corner
    draw.arc([(width - border_width - 40 - corner_size, height - border_width - 40 - corner_size), 
              (width - border_width - 40, height - border_width - 40)],
             start=0, end=90, fill=corner_color, width=6)
    
    # Get font
    try:
        title_font = ImageFont.truetype("arial.ttf", 120)
        subtitle_font = ImageFont.truetype("arial.ttf", 60)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # Draw title
    title = "CERTIFICATE OF ACHIEVEMENT"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_position = ((width - title_width) // 2, 200)
    draw.text(title_position, title, fill='#2c3e50', font=title_font)
    
    # Draw subtitle
    subtitle = "This certificate is proudly presented to"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_position = ((width - subtitle_width) // 2, 400)
    draw.text(subtitle_position, subtitle, fill='#7f8c8d', font=subtitle_font)
    
    # Draw decorative line under name area
    line_y = height // 2 + 100
    line_start = width // 4
    line_end = 3 * width // 4
    draw.line([(line_start, line_y), (line_end, line_y)], fill='#bdc3c7', width=3)
    
    # Draw signature line placeholders
    sig_y = height - 300
    sig_width = 400
    left_sig_x = width // 3 - sig_width // 2
    right_sig_x = 2 * width // 3 - sig_width // 2
    
    # Left signature line
    draw.line([(left_sig_x, sig_y), (left_sig_x + sig_width, sig_y)], 
              fill='#7f8c8d', width=2)
    
    # Right signature line
    draw.line([(right_sig_x, sig_y), (right_sig_x + sig_width, sig_y)], 
              fill='#7f8c8d', width=2)
    
    try:
        sig_font = ImageFont.truetype("arial.ttf", 30)
    except:
        try:
            sig_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            sig_font = ImageFont.load_default()
    
    # Signature labels
    left_label = "Instructor"
    right_label = "Director"
    
    left_bbox = draw.textbbox((0, 0), left_label, font=sig_font)
    left_label_width = left_bbox[2] - left_bbox[0]
    draw.text((left_sig_x + (sig_width - left_label_width) // 2, sig_y + 20), 
              left_label, fill='#7f8c8d', font=sig_font)
    
    right_bbox = draw.textbbox((0, 0), right_label, font=sig_font)
    right_label_width = right_bbox[2] - right_bbox[0]
    draw.text((right_sig_x + (sig_width - right_label_width) // 2, sig_y + 20), 
              right_label, fill='#7f8c8d', font=sig_font)
    
    # Save the template
    img.save(output_path, 'PNG', dpi=(300, 300))
    print(f"✓ Certificate template created: {output_path}")
    print(f"  Dimensions: {width}x{height} pixels")
    

if __name__ == '__main__':
    create_certificate_template()
