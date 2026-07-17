# QR Code Certificate Generator 🎓

Automated certificate generation system with QR codes for verification, powered by GitHub Actions.

## Features ✨

- 🎨 **Professional Certificates**: Generate beautiful, customizable certificates
- 📱 **QR Code Integration**: Each certificate includes a unique QR code for verification
- 🤖 **GitHub Actions Automation**: Fully automated certificate generation in the cloud
- 📊 **Multiple Data Formats**: Support for CSV and JSON input data
- 🔒 **Unique IDs**: Each certificate has a unique identifier
- 📦 **Easy Distribution**: Certificates are automatically packaged as artifacts

## Quick Start 🚀

### 1. Setup Repository

1. Fork or clone this repository
2. Ensure the repository has Actions enabled

### 2. Prepare Your Data

Add participant data in either CSV or JSON format to the `data/` directory:

**CSV Format** (`data/participants.csv`):
```csv
name,id,course,date,achievement,email
John Doe,CERT001,Python Programming,2026-07-15,Excellent,john@example.com
Jane Smith,CERT002,Web Development,2026-07-15,Outstanding,jane@example.com
```

**JSON Format** (`data/participants.json`):
```json
[
  {
    "name": "John Doe",
    "id": "CERT001",
    "course": "Python Programming",
    "date": "2026-07-15",
    "achievement": "Excellent",
    "email": "john@example.com"
  }
]
```

### 3. Generate Certificates

#### Automatic Generation (on Push)
Push your data file to the `main` branch:
```bash
git add data/participants.csv
git commit -m "Add participants for certificate generation"
git push origin main
```

#### Manual Generation (Workflow Dispatch)
1. Go to **Actions** tab in your GitHub repository
2. Select **Generate Certificates** workflow
3. Click **Run workflow**
4. (Optional) Customize parameters:
   - **Data file**: Path to your data file (default: `data/participants.csv`)
   - **Verification URL**: Base URL for QR code links (default: `https://example.com/verify?id=`)
5. Click **Run workflow** button

### 4. Download Certificates

After the workflow completes:
1. Go to the workflow run page
2. Scroll to **Artifacts** section at the bottom
3. Download `certificates-{run-number}.zip`
4. Extract the ZIP file to access your certificates

## Local Development 💻

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Create Certificate Template

```bash
python create_template.py
```

This creates a professional certificate template at `templates/certificate_template.png`.

### Generate Certificates Locally

```bash
# From CSV
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output

# From JSON
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.json \
  --output output

# With custom verification URL
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output \
  --verification-url "https://yoursite.com/verify?cert="
```

### View Generated Certificates

Certificates are saved in the `output/` directory as PNG files:
- `certificate_CERT001.png`
- `certificate_CERT002.png`
- etc.

## Configuration ⚙️

### Data Fields

#### Required Fields
- `name`: Participant's full name
- `id`: Unique certificate identifier

#### Optional Fields
- `course`: Course or program name (default: "Course Completion")
- `date`: Certificate issue date (default: current date, format: YYYY-MM-DD)
- `achievement`: Achievement level or grade
- `email`: Participant's email address

### Customization

#### Custom Template
Replace `templates/certificate_template.png` with your own design. Recommended size: 2480×1754 pixels (A4 landscape at 300 DPI).

#### Verification URL
The QR code contains a JSON payload with certificate details and a verification URL. Customize the base URL:
- In GitHub Actions: Set the `verification_url` input parameter
- Locally: Use the `--verification-url` argument

#### Certificate Styling
Edit `generate_certificates.py` to customize:
- Font sizes and styles
- Text positions
- QR code size and position
- Colors

## GitHub Actions Workflow 🔄

The workflow (`.github/workflows/generate-certificates.yml`) automatically:

1. ✅ Sets up Python environment
2. 📥 Installs dependencies
3. 🎨 Creates template (if not exists)
4. 📊 Processes participant data
5. 🎓 Generates certificates with QR codes
6. 📦 Uploads certificates as artifacts
7. 📝 Creates a summary report

### Workflow Triggers

- **Push to main**: Automatically triggers when data files are updated
- **Manual dispatch**: Run anytime from Actions tab with custom parameters

### Workflow Outputs

- **Artifacts**: Certificate images (PNG format)
- **Summary**: Detailed generation report in workflow summary
- **Releases** (optional): Published releases with certificates attached

## QR Code Contents 📱

Each QR code contains a JSON payload:
```json
{
  "id": "CERT001",
  "name": "John Doe",
  "course": "Python Programming",
  "date": "2026-07-15",
  "verification_url": "https://example.com/verify?id=CERT001"
}
```

Scan the QR code with any smartphone to verify certificate authenticity.

## File Structure 📁

```
qr-certificate-generator/
├── .github/
│   └── workflows/
│       └── generate-certificates.yml  # GitHub Actions workflow
├── data/
│   ├── participants.csv               # Sample CSV data
│   ├── participants.json              # Sample JSON data
│   └── README.md                      # Data format documentation
├── templates/
│   └── certificate_template.png      # Certificate template (generated)
├── output/                           # Generated certificates (gitignored)
│   └── .gitkeep
├── create_template.py                # Template generator script
├── generate_certificates.py          # Main certificate generator
├── requirements.txt                  # Python dependencies
├── .gitignore
└── README.md                         # This file
```

## Requirements 📋

- Python 3.8+
- Pillow (PIL) 10.3.0+
- qrcode 7.4.2+
- python-dateutil 2.9.0+

## Troubleshooting 🔧

### Font Issues

If you encounter font-related errors:
- **Windows**: Ensure `arial.ttf` is available in your Windows fonts
- **Linux**: Install DejaVu fonts: `sudo apt-get install fonts-dejavu`
- **macOS**: System fonts should work by default

### Template Not Found

Run `python create_template.py` to generate the template before generating certificates.

### Empty Output

Ensure your data file:
- Is in the correct format (CSV or JSON)
- Contains at least the required fields (`name`, `id`)
- Is located in the path specified

## Examples 📸

### Sample Certificate

Each certificate includes:
- Professional border and design
- Participant name (centered, large)
- Course/program name
- Issue date
- Unique certificate ID
- QR code for verification (bottom right)
- Signature lines

### Sample QR Code

The QR code links to a verification URL and contains all certificate details for authentication.

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Provide details about your setup and the problem
3. Include relevant logs or screenshots

## Roadmap 🗺️

Future enhancements:
- [ ] PDF output format
- [ ] Email distribution integration
- [ ] Database integration for verification
- [ ] Web-based verification portal
- [ ] Batch processing improvements
- [ ] Custom font support
- [ ] Template editor

---

Made with ❤️ using Python and GitHub Actions
