#!/usr/bin/env python3
"""
QR Code Certificate Generator
Generates personalized certificates with QR codes for verification
"""

import os
import csv
import json
import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import argparse


class CertificateGenerator:
    """Generate certificates with QR codes"""
    
    def __init__(self, template_path, output_dir="output", verification_url=None):
        """
        Initialize the certificate generator
        
        Args:
            template_path: Path to the certificate template image
            output_dir: Directory to save generated certificates
            verification_url: Base URL for certificate verification
        """
        self.template_path = template_path
        self.output_dir = output_dir
        self.verification_url = verification_url or "https://example.com/verify?id="
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_qr_code(self, data, size=(200, 200)):
        """
        Generate a QR code from data
        
        Args:
            data: Data to encode in the QR code
            size: Size of the QR code (width, height)
            
        Returns:
            PIL Image object of the QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize(size, Image.Resampling.LANCZOS)
        
        return qr_img
    
    def get_font(self, size):
        """
        Get a font for text rendering
        
        Args:
            size: Font size
            
        Returns:
            PIL ImageFont object
        """
        try:
            # Try to use a nice font if available
            return ImageFont.truetype("arial.ttf", size)
        except:
            try:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
            except:
                # Fall back to default font
                return ImageFont.load_default()
    
    def generate_certificate(self, participant_data):
        """
        Generate a certificate for a participant
        
        Args:
            participant_data: Dictionary containing participant information
                Required keys: name, id
                Optional keys: course, date, achievement, email
        """
        # Load template
        certificate = Image.open(self.template_path).convert("RGBA")
        draw = ImageDraw.Draw(certificate)
        
        # Get certificate dimensions
        width, height = certificate.size
        
        # Extract participant data
        name = participant_data.get('name', 'Participant')
        cert_id = participant_data.get('id', 'CERT001')
        course = participant_data.get('course', 'Course Completion')
        date = participant_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        achievement = participant_data.get('achievement', '')
        email = participant_data.get('email', '')
        
        # Generate QR code with verification URL
        qr_data = json.dumps({
            'id': cert_id,
            'name': name,
            'course': course,
            'date': date,
            'verification_url': f"{self.verification_url}{cert_id}"
        })
        qr_code = self.generate_qr_code(qr_data, size=(250, 250))
        
        # Position QR code (bottom right)
        qr_position = (width - 300, height - 300)
        certificate.paste(qr_code, qr_position)
        
        # Add text to certificate
        # Participant name (centered, large)
        name_font = self.get_font(80)
        name_bbox = draw.textbbox((0, 0), name, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_position = ((width - name_width) // 2, height // 2 - 50)
        draw.text(name_position, name, fill='#1a1a1a', font=name_font)
        
        # Course name (centered)
        course_font = self.get_font(40)
        course_text = f"for completing {course}"
        course_bbox = draw.textbbox((0, 0), course_text, font=course_font)
        course_width = course_bbox[2] - course_bbox[0]
        course_position = ((width - course_width) // 2, height // 2 + 80)
        draw.text(course_position, course_text, fill='#4a4a4a', font=course_font)
        
        # Date (centered)
        date_font = self.get_font(30)
        date_text = f"Date: {date}"
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_position = ((width - date_width) // 2, height // 2 + 160)
        draw.text(date_position, date_text, fill='#6a6a6a', font=date_font)
        
        # Certificate ID (bottom left)
        id_font = self.get_font(20)
        id_text = f"Certificate ID: {cert_id}"
        draw.text((50, height - 80), id_text, fill='#8a8a8a', font=id_font)
        
        # Save certificate
        output_path = os.path.join(self.output_dir, f"certificate_{cert_id}.png")
        certificate.convert("RGB").save(output_path, "PNG")
        
        print(f"✓ Generated certificate for {name} (ID: {cert_id})")
        return output_path
    
    def generate_from_csv(self, csv_path):
        """
        Generate certificates from a CSV file
        
        Args:
            csv_path: Path to CSV file with participant data
            
        CSV format:
            name,id,course,date,achievement,email
        """
        certificates = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cert_path = self.generate_certificate(row)
                    certificates.append(cert_path)
                except Exception as e:
                    print(f"✗ Error generating certificate for {row.get('name', 'Unknown')}: {e}")
        
        return certificates
    
    def generate_from_json(self, json_path):
        """
        Generate certificates from a JSON file
        
        Args:
            json_path: Path to JSON file with participant data
            
        JSON format:
            [
                {"name": "John Doe", "id": "CERT001", "course": "Python", ...},
                ...
            ]
        """
        certificates = []
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for participant in data:
            try:
                cert_path = self.generate_certificate(participant)
                certificates.append(cert_path)
            except Exception as e:
                print(f"✗ Error generating certificate for {participant.get('name', 'Unknown')}: {e}")
        
        return certificates


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate certificates with QR codes')
    parser.add_argument('--template', required=True, help='Path to certificate template image')
    parser.add_argument('--data', required=True, help='Path to participant data (CSV or JSON)')
    parser.add_argument('--output', default='output', help='Output directory for certificates')
    parser.add_argument('--verification-url', default='https://example.com/verify?id=',
                        help='Base URL for certificate verification')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = CertificateGenerator(
        template_path=args.template,
        output_dir=args.output,
        verification_url=args.verification_url
    )
    
    # Generate certificates based on file type
    if args.data.endswith('.csv'):
        print(f"Generating certificates from CSV: {args.data}")
        certificates = generator.generate_from_csv(args.data)
    elif args.data.endswith('.json'):
        print(f"Generating certificates from JSON: {args.data}")
        certificates = generator.generate_from_json(args.data)
    else:
        print("Error: Data file must be CSV or JSON")
        return
    
    print(f"\n✓ Successfully generated {len(certificates)} certificate(s)")
    print(f"✓ Certificates saved to: {args.output}")


if __name__ == '__main__':
    main()
