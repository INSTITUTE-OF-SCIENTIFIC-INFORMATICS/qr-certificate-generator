# QR Code Certificate Generator 🎓

Automated certificate generation system with QR codes for verification, powered by GitHub Actions. Generate professional certificates from marksheet data (scores, grades) or simple participant lists.

## Features ✨

- 🎨 **Professional Certificates**: Generate beautiful, customizable certificates
- 📱 **QR Code Integration**: Each certificate includes a unique QR code for verification
- 📊 **Marksheet Support**: Parse scores from "X/Y" format and auto-calculate grades
- 🤖 **GitHub Actions Automation**: Fully automated certificate generation in the cloud
- 📋 **Multiple Data Formats**: Support for CSV with scores or simple participant data
- 🔒 **Unique IDs**: Auto-generated unique certificate identifiers
- 📦 **Easy Distribution**: Certificates automatically packaged as downloadable artifacts
- ⚙️ **Configurable Layout**: Customize text positions and QR code placement

## Quick Start 🚀

### 1. Prepare Your Data

Create a CSV file with participant information:

**Marksheet Format** (with scores):
```csv
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Anu Gamage,20/25,20/25,20/25,20/25,80/100
John Doe,23/25,24/25,22/25,24/25,93/100
```

**Simple Format**:
```csv
name,course,score,grade,date
John Doe,Python Programming,95,A+,2026-07-15
Jane Smith,Web Development,88,B+,2026-07-15
```

### 2. Upload Your Data

Place your CSV file in the `data/` directory and push to GitHub:
```bash
cp your_marksheet.csv data/participants.csv
git add data/participants.csv
git commit -m "Add participants for certificate generation"
git push origin main
```

### 3. Get Your Certificates

GitHub Actions automatically generates certificates with QR codes!
1. Go to **Actions** tab in your GitHub repository
2. Select **Generate Certificates** workflow
3. Click **Run workflow**
4. (Optional) Customize parameters:
   - **Data file**: Path to your data file (default: `data/participants.csv`)
   - **Verification URL**: Base URL for QR code links (default: `https://example.com/verify?id=`)
5. Click **Run workflow** button

### 4. Download Certificates

After the workflow completes:
1. Go to the workflow run page in **Actions** tab
2. Scroll to **Artifacts** section at the bottom
3. Download `certificates-{run-number}.zip`
4. Extract the ZIP file to access your certificates

## Advanced Usage 🔧

### Custom Certificate Template

Replace `templates/certificate_template.png` with your own design:
- **Size**: 2480×1754 pixels (A4 landscape at 300 DPI)
- **Format**: PNG or JPEG
- Leave space in center for names, scores, and QR code

### Configure Text Positioning

Edit `config.json` to control where elements appear:
```json
{
  "text_elements": {
    "name": {"x": 1240, "y": 750, "font_size": 80, "align": "center"},
    "score": {"x": 1240, "y": 1100, "font_size": 50, "align": "center"}
  },
  "qr_code": {"x": 2100, "y": 1400, "size": 280}
}
```

### Manual Workflow Trigger

1. Go to **Actions** tab → **Generate Certificates with QR Codes**
2. Click **Run workflow**
3. Configure:
   - **Data file**: `data/your_marksheet.csv`
   - **Verification URL**: Your verification endpoint
   - **Course name**: Default course name
   - **Use config**: Enable `config.json` positioning
4. Click **Run workflow**

## How It Works ⚙️

1. **Upload Data**: Push CSV with participant names and scores
2. **Auto-Process**: System parses scores, calculates percentages, assigns grades
3. **Generate IDs**: Unique certificate IDs are auto-generated
4. **Create QR Codes**: Each QR code contains full certificate data
5. **Apply to Template**: Names, scores, grades placed on your template
6. **Package**: Certificates bundled as downloadable artifacts

## Marksheet Processing 📊

The system automatically:
- Parses "20/25" format scores
- Calculates total percentage
- Assigns letter grades (A+, A, B+, B, C+, C, F)
- Generates unique certificate IDs
- Creates verification QR codes

### Grade Scale

| Percentage | Grade |
|------------|-------|
| 90-100% | A+ |
| 85-89% | A |
| 80-84% | A- |
| 75-79% | B+ |
| 70-74% | B |
| 65-69% | B- |
| 60-64% | C+ |
| 55-59% | C |
| 50-54% | C- |
| <50% | F |

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
# From marksheet CSV
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output

# With configuration file
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output \
  --config config.json

# With custom verification URL
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output \
  --verification-url "https://yoursite.com/verify?cert=" \
  --course "Advanced Python Programming"
```

### View Generated Certificates

Certificates are saved in the `output/` directory as PNG files:
- `certificate_Anu_Gamage_CERT-A3F8B92E.png`
- `certificate_John_Doe_CERT-B4C9D3F1.png`
- etc.

## Configuration ⚙️

### Supported CSV Formats

#### Format 1: Marksheet with Scores
```csv
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Anu Gamage,20/25,20/25,20/25,20/25,80/100
```
- System parses "X/Y" format
- Auto-calculates percentages
- Auto-assigns letter grades
- Auto-generates certificate IDs

#### Format 2: Direct Values
```csv
name,course,score,grade,date,id
John Doe,Python,95,A+,2026-07-15,CERT001
```

### Data Fields

#### Recognized Field Names (case-insensitive)
- **Name** / name: Participant's full name (required)
- **Course** / course: Course or program name
- **Total Marks** / Total_Marks: Score in "X/Y" format
- **score** / percentage: Direct percentage value
- **grade** / Grade: Letter grade
- **date** / Date: Issue date (YYYY-MM-DD)
- **id**: Certificate ID (auto-generated if not provided)

#### Optional Component Fields
- Course Assignments
- Practical Modules
- Final Assignment  
- Final Presentation

### Customization

#### Custom Template
Replace `templates/certificate_template.png` with your own design:
- **Recommended size**: 2480×1754 pixels (A4 landscape at 300 DPI)
- **Format**: PNG (recommended) or JPEG
- **Color mode**: RGB
- **Design considerations**:
  - Leave center clear for participant name
  - Reserve space for scores and grades
  - Keep bottom-right corner clear for QR code (300×300px)
  - Keep bottom-left clear for certificate ID

#### Text Positioning (`config.json`)
Control exact placement of all text elements:
```json
{
  "text_elements": {
    "name": {
      "x": 1240,
      "y": 750,
      "font_size": 80,
      "font_color": "#1a1a1a",
      "align": "center"
    },
    "score": {
      "x": 1240,
      "y": 1100,
      "font_size": 50,
      "font_color": "#2c3e50",
      "align": "center",
      "prefix": "Score: ",
      "suffix": "%"
    },
    "grade": {
      "x": 1240,
      "y": 1180,
      "font_size": 40,
      "font_color": "#27ae60",
      "align": "center",
      "prefix": "Grade: "
    }
  },
  "qr_code": {
    "x": 2100,
    "y": 1400,
    "size": 280
  }
}
```

#### Verification URL
Set the `verification_url` parameter to customize where the QR code links to:
- **Default**: `https://example.com/verify?id=`
- **In GitHub Actions**: Set via workflow input parameter
- **Locally**: Use the `--verification-url` argument

The full verification URL will be: `{verification_url}{certificate_id}`

#### Certificate Styling
Edit `generate_certificates.py` to customize:
- Font sizes and styles
- Text positions (if not using config.json)
- QR code size and position
- Colors and formatting

## GitHub Actions Workflow 🔄

The workflow (`.github/workflows/generate-certificates.yml`) automatically:

1. ✅ Sets up Python environment
2. 📥 Installs dependencies
3. 🎨 Creates template (if not exists)
4. 📊 Processes participant data and parses scores
5. 🎓 Calculates grades and generates certificate IDs
6. 🔢 Creates QR codes with complete verification data
7. 📄 Generates certificates from your template
8. 📦 Uploads certificates as artifacts
9. 📝 Creates a detailed summary report

### Workflow Triggers

- **Push to main**: Automatically triggers when data files in `data/` are updated
- **Manual dispatch**: Run anytime from Actions tab with custom parameters

### Workflow Inputs (Manual Trigger)

- **data_file**: Path to your CSV file (default: `data/participants.csv`)
- **verification_url**: Base URL for QR verification
- **course_name**: Default course name if not in data
- **use_config**: Whether to use `config.json` for positioning

### Workflow Outputs

- **Artifacts**: Certificate images (PNG format, 300 DPI)
- **Summary**: Detailed generation report with file list
- **Releases** (manual trigger only): Published releases with certificates attached

## How to Upload Your Own Data 📤

### Method 1: GitHub Web Interface

1. **Upload CSV File**:
   - Navigate to `data/` folder in your repository
   - Click "Add file" → "Upload files"
   - Drag and drop your marksheet CSV
   - Commit changes

2. **Upload Template** (optional):
   - Navigate to `templates/` folder
   - Upload your `certificate_template.png`
   - Commit changes

3. **Automatic Generation**: Certificates are generated automatically on push

### Method 2: Git Command Line

```bash
# Clone your repository
git clone https://github.com/your-username/qr-certificate-generator.git
cd qr-certificate-generator

# Add your files
cp /path/to/marksheet.csv data/participants.csv
cp /path/to/template.png templates/certificate_template.png

# Commit and push
git add data/participants.csv templates/certificate_template.png
git commit -m "Add marksheet and custom template"
git push origin main

# Workflow runs automatically
# Check Actions tab for progress
```

### Method 3: Direct Edit on GitHub

1. Click on `data/participants.csv` in your repository
2. Click the pencil icon (Edit this file)
3. Paste your CSV data
4. Commit changes
5. Certificates generated automatically

## Complete Example Workflow 📋

```bash
# 1. Prepare your marksheet
cat > my_marks.csv << EOF
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Alice Johnson,22/25,23/25,24/25,25/25,94/100
Bob Smith,18/25,19/25,20/25,21/25,78/100
Carol White,25/25,24/25,25/25,24/25,98/100
EOF

# 2. Upload to repository
git clone https://github.com/your-username/qr-certificate-generator.git
cd qr-certificate-generator
cp my_marks.csv data/participants.csv

# 3. Push and let GitHub Actions work
git add data/participants.csv
git commit -m "Add batch 2026-07 participants"
git push origin main

# 4. Monitor progress
# Go to Actions tab → Latest workflow run

# 5. Download certificates
# Once complete, download from Artifacts section
```

## QR Code Contents 📱

Each QR code contains comprehensive certificate data in JSON format:
```json
{
  "id": "CERT-A3F8B92E",
  "name": "Anu Gamage",
  "course": "Course Completion",
  "date": "2026-07-15",
  "score": "80/100",
  "grade": "A-",
  "percentage": 80.0,
  "verification_url": "https://example.com/verify?id=CERT-A3F8B92E"
}
```

Scan the QR code with any smartphone to:
- ✅ Verify certificate authenticity
- 📊 View scores and grades
- 📅 Check issue date
- 🔗 Access verification portal

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

### Completed Features ✅
- [x] Marksheet score parsing ("X/Y" format)
- [x] Automatic grade calculation
- [x] Auto-generated unique certificate IDs
- [x] Comprehensive QR code data (scores, grades, verification)
- [x] Configurable text positioning
- [x] Custom template support
- [x] GitHub Actions automation
- [x] Artifact packaging and distribution

### Planned Enhancements 🚀
- [ ] PDF output format
- [ ] Email distribution integration
- [ ] Database integration for verification
- [ ] Web-based verification portal
- [ ] Bulk email sending with certificates
- [ ] Custom font support
- [ ] Template editor UI
- [ ] Certificate revocation system
- [ ] Multi-language support
- [ ] Digital signatures
- [ ] Batch watermarking

---

**Made with ❤️ using Python and GitHub Actions**

## Documentation

- **[README.md](README.md)** - This file, main documentation
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed guide for uploading data and templates
- **[data/README.md](data/README.md)** - Data format specifications
- **[templates/README.md](templates/README.md)** - Template requirements and customization
