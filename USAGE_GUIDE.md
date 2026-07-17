# How to Generate Certificates with Your Own Data

This guide explains how to upload your own CSV file (marksheet) and custom certificate template to generate certificates with QR codes.

## Step 1: Prepare Your Marksheet (CSV File)

### Supported CSV Formats

#### Format 1: Marksheet with Component Scores
```csv
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Anu Gamage,20/25,20/25,20/25,20/25,80/100
John Doe,23/25,24/25,22/25,24/25,93/100
```

The system will:
- Parse scores from "scored/total" format
- Calculate percentage automatically
- Assign letter grades (A+, A, B+, etc.)
- Generate unique certificate IDs
- Create QR codes with all verification data

#### Format 2: Simple Format with Direct Values
```csv
name,course,score,grade,date
John Doe,Python Programming,95,A+,2026-07-15
Jane Smith,Web Development,88,B+,2026-07-15
```

### CSV Field Mapping

The generator recognizes these field names (case-insensitive):

| Field | Alternative Names | Description | Required |
|-------|------------------|-------------|----------|
| Name | name | Participant full name | ✅ Yes |
| Course | course | Course/program name | Optional |
| Total Marks | Total_Marks, total_marks | Final score in "X/Y" format | Optional |
| score | percentage | Direct percentage value | Optional |
| grade | Grade | Letter grade | Optional |
| date | Date | Issue date (YYYY-MM-DD) | Optional |
| Course Assignments | - | Component score | Optional |
| Practical Modules | - | Component score | Optional |
| Final Assignment | - | Component score | Optional |
| Final Presentation | - | Component score | Optional |

## Step 2: Upload Your CSV File

### Option A: Via GitHub Web Interface
1. Navigate to your repository on GitHub
2. Click on the `data/` folder
3. Click "Add file" → "Upload files"
4. Drag and drop your CSV file (e.g., `marksheet.csv`)
5. Commit the changes

### Option B: Via Git Command Line
```bash
# Copy your CSV file to the data folder
cp /path/to/your/marksheet.csv data/participants.csv

# Add and commit
git add data/participants.csv
git commit -m "Add marksheet for certificate generation"
git push origin main
```

## Step 3: Upload Your Certificate Template (Optional)

### Template Requirements
- **Format**: PNG (recommended) or JPEG
- **Size**: 2480×1754 pixels (A4 landscape at 300 DPI) or similar
- **Color**: RGB mode
- **Design Tips**:
  - Leave center area clear for participant name (~y: 600-900px)
  - Reserve space below name for score/grade (~y: 1000-1200px)
  - Keep bottom-right corner clear for QR code (300×300px)
  - Keep bottom-left clear for certificate ID

### Upload Your Template

1. Navigate to `templates/` folder in your repository
2. Upload your template file as `certificate_template.png`
3. Or use a different name and specify it in the workflow

```bash
# Via command line
cp /path/to/your/template.png templates/certificate_template.png
git add templates/certificate_template.png
git commit -m "Add custom certificate template"
git push origin main
```

## Step 4: Configure Text Positioning (Optional)

If you want precise control over where text appears on your template, edit `config.json`:

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
    }
  },
  "qr_code": {
    "x": 2100,
    "y": 1400,
    "size": 280
  }
}
```

Adjust the `x` and `y` coordinates to match your template design.

## Step 5: Run the Certificate Generator

### Automatic Generation (Push to Main)
When you push your CSV file to the `main` branch, GitHub Actions automatically:
1. Detects the new data file
2. Generates certificates with QR codes
3. Packages them as downloadable artifacts

```bash
git push origin main
# Wait for the workflow to complete
# Download certificates from Actions → Workflow Run → Artifacts
```

### Manual Generation (Workflow Dispatch)
1. Go to **Actions** tab in your GitHub repository
2. Select **Generate Certificates with QR Codes** workflow
3. Click **Run workflow**
4. Configure options:
   - **Data file**: Path to your CSV (e.g., `data/marksheet.csv`)
   - **Verification URL**: Base URL for QR verification
   - **Course name**: Default course name (if not in CSV)
   - **Use config**: Whether to use `config.json` positioning
5. Click **Run workflow** button

## Step 6: Download Your Certificates

### From Artifacts
1. Go to the completed workflow run
2. Scroll to **Artifacts** section
3. Download `certificates-{run-number}.zip`
4. Extract to get your certificate PNG files

### From Releases (Manual Trigger Only)
1. Go to **Releases** section in your repository
2. Find the release `certificates-v{run-number}`
3. Download individual certificates or the full bundle

## What's in the QR Code? 📱

Each QR code contains JSON data:
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

Anyone can scan the QR code with a smartphone to:
- View certificate details
- Verify authenticity
- Check scores and grades

## Grade Scale

The system automatically assigns letter grades based on percentage:

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

## Troubleshooting

### Problem: Certificates not generated
- Check that your CSV file is properly formatted
- Verify the "Name" column exists
- Check workflow logs in Actions tab

### Problem: Text not positioned correctly
- Create/edit `config.json` to adjust text positions
- Use pixel coordinates based on your template size
- Set `use_config: true` in workflow inputs

### Problem: QR code overlaps with template design
- Adjust QR code position in `config.json`
- Default position: bottom-right (x:2100, y:1400)
- Ensure your template has clear space there

### Problem: Missing template
- Upload your template to `templates/certificate_template.png`
- Or let the system auto-generate a default template

## Example Workflow

1. **Prepare CSV**: Export marks from your system as CSV
2. **Upload**: Place in `data/participants.csv`
3. **Push**: `git push origin main`
4. **Wait**: GitHub Actions generates certificates (~1-2 minutes)
5. **Download**: Get ZIP file from Artifacts
6. **Distribute**: Send certificates to participants

## Local Testing

Test certificate generation on your computer:

```bash
# Install dependencies
pip install -r requirements.txt

# Generate certificates
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output \
  --config config.json

# Check output
ls output/
```

## Next Steps

- Customize the verification URL to point to your verification system
- Integrate with email distribution system
- Set up a verification portal using the QR code data
- Customize the certificate template with your branding

## Support

For issues or questions:
1. Check the workflow logs in the Actions tab
2. Review this guide for common problems
3. Open an issue in the repository with details
