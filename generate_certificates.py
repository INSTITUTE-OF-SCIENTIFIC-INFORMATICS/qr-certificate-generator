#!/usr/bin/env python3
"""
QR Code Certificate Generator
Generates personalized certificates with QR codes for verification
Supports marksheet format with scores and automatic grade calculation
"""

import os
import csv
import json
import qrcode
import hashlib
import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import argparse


class CertificateGenerator:
    """Generate certificates with QR codes"""
    
    def __init__(self, template_path, output_dir="output", verification_url=None, config_path=None):
        """
        Initialize the certificate generator
        
        Args:
            template_path: Path to the certificate template image
            output_dir: Directory to save generated certificates
            verification_url: Base URL for certificate verification
            config_path: Path to configuration JSON file
        """
        self.template_path = template_path
        self.output_dir = output_dir
        self.verification_url = verification_url or "https://example.com/verify?id="
        
        # Load configuration if provided
        self.config = self.load_config(config_path) if config_path and os.path.exists(config_path) else None
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return None
    
    def parse_score(self, score_str):
        """
        Parse score from string format like '20/25' or '80/100'
        Returns tuple (scored, total)
        """
        if not score_str or isinstance(score_str, (int, float)):
            return None, None
        
        match = re.match(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', str(score_str).strip())
        if match:
            return float(match.group(1)), float(match.group(2))
        return None, None
    
    def calculate_grade(self, percentage):
        """Calculate letter grade from percentage"""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'A-'
        elif percentage >= 75:
            return 'B+'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 65:
            return 'B-'
        elif percentage >= 60:
            return 'C+'
        elif percentage >= 55:
            return 'C'
        elif percentage >= 50:
            return 'C-'
        else:
            return 'F'
    
    def generate_certificate_id(self, name, course=""):
        """Generate unique certificate ID based on name and course"""
        data = f"{name}-{course}-{datetime.now().year}".encode('utf-8')
        hash_obj = hashlib.sha256(data)
        return f"CERT-{hash_obj.hexdigest()[:8].upper()}"
        
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
                Can include: name, scores, course assignments, etc.
        """
        # Load template
        certificate = Image.open(self.template_path).convert("RGBA")
        draw = ImageDraw.Draw(certificate)
        
        # Get certificate dimensions
        width, height = certificate.size
        
        # Extract and process participant data
        name = participant_data.get('Name', participant_data.get('name', 'Participant'))
        
        # Parse marksheet data if present
        course_assignments = participant_data.get('Course Assignments', '')
        practical_modules = participant_data.get('Practical Modules', '')
        final_assignment = participant_data.get('Final Assignment', '')
        final_presentation = participant_data.get('Final Presentation', '')
        total_marks = participant_data.get('Total Marks', '')
        
        # Parse total marks
        scored, total = self.parse_score(total_marks)
        if scored is not None and total is not None:
            percentage = (scored / total) * 100
            grade = self.calculate_grade(percentage)
        else:
            # Fallback to provided values
            percentage = participant_data.get('score', participant_data.get('percentage', 0))
            grade = participant_data.get('grade', 'N/A')
        
        # Generate certificate ID
        course = participant_data.get('course', participant_data.get('Course', 'Course Completion'))
        cert_id = participant_data.get('id', self.generate_certificate_id(name, course))
        
        date = participant_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Generate QR code with all verification data
        qr_data = json.dumps({
            'id': cert_id,
            'name': name,
            'course': course,
            'date': date,
            'score': f"{scored}/{total}" if scored else str(percentage),
            'grade': grade,
            'percentage': round(percentage, 2) if isinstance(percentage, (int, float)) else percentage,
            'verification_url': f"{self.verification_url}{cert_id}"
        }, indent=2)
        
        # Get QR code size and position from config or use defaults
        if self.config and 'qr_code' in self.config:
            qr_size = self.config['qr_code'].get('size', 250)
            qr_x = self.config['qr_code'].get('x', width - 300)
            qr_y = self.config['qr_code'].get('y', height - 300)
        else:
            qr_size = 250
            qr_x = width - 300
            qr_y = height - 300
        
        qr_code = self.generate_qr_code(qr_data, size=(qr_size, qr_size))
        certificate.paste(qr_code, (qr_x, qr_y))
        
        # Add text to certificate using config or defaults
        if self.config and 'text_elements' in self.config:
            self.add_text_from_config(draw, {
                'name': name,
                'course': course,
                'date': date,
                'score': round(percentage, 2) if isinstance(percentage, (int, float)) else percentage,
                'grade': grade,
                'certificate_id': cert_id
            })
        else:
            # Use default positioning
            self.add_default_text(draw, name, course, date, percentage, grade, cert_id, width, height)
        
        # Save certificate
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name)
        output_filename = f"certificate_{safe_name}_{cert_id}.png"
        output_path = os.path.join(self.output_dir, output_filename)
        certificate.convert("RGB").save(output_path, "PNG", dpi=(300, 300))
        
        print(f"✓ Generated certificate for {name} (ID: {cert_id}, Score: {percentage:.1f}%, Grade: {grade})")
        return output_path
    
    def add_text_from_config(self, draw, data):
        """Add text elements based on configuration"""
        for element_name, element_config in self.config['text_elements'].items():
            if element_name not in data:
                continue
            
            value = data[element_name]
            prefix = element_config.get('prefix', '')
            suffix = element_config.get('suffix', '')
            text = f"{prefix}{value}{suffix}"
            
            font_size = element_config.get('font_size', 30)
            font = self.get_font(font_size)
            color = element_config.get('font_color', '#000000')
            
            x = element_config.get('x', 0)
            y = element_config.get('y', 0)
            align = element_config.get('align', 'left')
            
            if align == 'center':
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = x - text_width // 2
            
            draw.text((x, y), text, fill=color, font=font)
    
    def add_default_text(self, draw, name, course, date, percentage, grade, cert_id, width, height):
        """Add text elements using default positioning"""
        # Participant name (centered, large)
        name_font = self.get_font(80)
        name_bbox = draw.textbbox((0, 0), name, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_position = ((width - name_width) // 2, height // 2 - 150)
        draw.text(name_position, name, fill='#1a1a1a', font=name_font)
        
        # Course name (centered)
        course_font = self.get_font(40)
        course_text = f"for completing {course}"
        course_bbox = draw.textbbox((0, 0), course_text, font=course_font)
        course_width = course_bbox[2] - course_bbox[0]
        course_position = ((width - course_width) // 2, height // 2 - 30)
        draw.text(course_position, course_text, fill='#4a4a4a', font=course_font)
        
        # Score and Grade (centered)
        score_font = self.get_font(50)
        if isinstance(percentage, (int, float)):
            score_text = f"Score: {percentage:.1f}%  |  Grade: {grade}"
        else:
            score_text = f"Grade: {grade}"
        score_bbox = draw.textbbox((0, 0), score_text, font=score_font)
        score_width = score_bbox[2] - score_bbox[0]
        score_position = ((width - score_width) // 2, height // 2 + 70)
        draw.text(score_position, score_text, fill='#2c3e50', font=score_font)
        
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
    parser = argparse.ArgumentParser(description='Generate certificates with QR codes from marksheet data')
    parser.add_argument('--template', required=True, help='Path to certificate template image')
    parser.add_argument('--data', required=True, help='Path to participant data (CSV or JSON)')
    parser.add_argument('--output', default='output', help='Output directory for certificates')
    parser.add_argument('--verification-url', default='https://example.com/verify?id=',
                        help='Base URL for certificate verification')
    parser.add_argument('--config', help='Path to configuration JSON file (optional)')
    parser.add_argument('--course', default='Course Completion', help='Course name (optional, used if not in data)')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = CertificateGenerator(
        template_path=args.template,
        output_dir=args.output,
        verification_url=args.verification_url,
        config_path=args.config
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
