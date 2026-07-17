# Certificate Generator Data Formats

This directory contains participant data files for certificate generation.

## Supported Formats

### CSV Format (Recommended)

#### Option 1: Marksheet Format with Scores

Perfect for academic certificates with component scores:

```csv
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Anu Gamage,20/25,20/25,20/25,20/25,80/100
John Doe,23/25,24/25,22/25,24/25,93/100
Jane Smith,25/25,24/25,25/25,23/25,97/100
```

**What happens:**
- System parses scores from "X/Y" format
- Calculates total percentage automatically
- Assigns letter grades (A+, A, B+, etc.)
- Generates unique certificate IDs (e.g., CERT-A3F8B92E)
- Creates QR codes with all details

#### Option 2: Simple Format

For basic certificates without detailed scores:

```csv
name,course,score,grade,date
John Doe,Python Programming,95,A+,2026-07-15
Jane Smith,Web Development,88,B+,2026-07-15
Bob Wilson,Data Science,92,A,2026-07-15
```

### JSON Format

Alternative format for programmatic generation:

```json
[
  {
    "name": "John Doe",
    "course": "Python Programming",
    "score": 95,
    "grade": "A+",
    "date": "2026-07-15"
  },
  {
    "name": "Jane Smith",
    "course": "Web Development",
    "score": 88,
    "grade": "B+",
    "date": "2026-07-15"
  }
]
```

## Field Reference

### Recognized Field Names (case-insensitive)

| Field | Alternative Names | Type | Required | Description |
|-------|------------------|------|----------|-------------|
| Name | name | String | ✅ Yes | Participant's full name |
| Course | course | String | No | Course or program name |
| Total Marks | Total_Marks, total_marks | String | No | Final score in "X/Y" format (e.g., "80/100") |
| score | percentage | Number | No | Direct percentage value (0-100) |
| grade | Grade | String | No | Letter grade (A+, A, B+, etc.) |
| date | Date | String | No | Issue date (YYYY-MM-DD format) |
| id | ID | String | No | Certificate ID (auto-generated if not provided) |
| Course Assignments | - | String | No | Component score "X/Y" |
| Practical Modules | - | String | No | Component score "X/Y" |
| Final Assignment | - | String | No | Component score "X/Y" |
| Final Presentation | - | String | No | Component score "X/Y" |

### Field Details

#### Name (Required)
- **Format**: Any string
- **Example**: "Anu Gamage", "John Doe"
- **Used for**: Certificate display name, filename, QR code

#### Course (Optional)
- **Format**: Any string
- **Default**: "Course Completion"
- **Example**: "Advanced Python Programming"
- **Used for**: Certificate text, QR code

#### Total Marks (Optional)
- **Format**: "scored/total" (e.g., "80/100", "45/50")
- **Parsing**: Automatically extracts numbers
- **Triggers**: Automatic percentage and grade calculation
- **Example**: "94/100" → 94% → Grade A

#### score/percentage (Optional)
- **Format**: Number (0-100)
- **Used when**: No "Total Marks" provided
- **Example**: 95, 88.5
- **Triggers**: Automatic grade assignment

#### grade (Optional)
- **Format**: String (A+, A, A-, B+, B, B-, C+, C, C-, F)
- **Auto-assigned when**: score or Total Marks provided
- **Manual value**: Used if provided and no automatic calculation

#### date (Optional)
- **Format**: YYYY-MM-DD
- **Default**: Current date
- **Example**: "2026-07-15"
- **Used for**: Certificate display, QR code

#### id (Optional)
- **Format**: Any string
- **Default**: Auto-generated (CERT-{hash})
- **Example**: "CERT-A3F8B92E"
- **Used for**: Unique identification, QR code, verification

## Automatic Processing

### Score Parsing
The system recognizes these patterns:
- `80/100` → 80%
- `45/50` → 90%
- `20/25` → 80%
- `38.5/40` → 96.25%

### Grade Assignment
Based on percentage:

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
| < 50% | F |

### Certificate ID Generation
When no ID provided:
- Format: `CERT-{8-character-hash}`
- Based on: Name + Course + Year
- Example: `CERT-A3F8B92E`
- Unique: Same inputs always generate same ID

## Example Files

### Example 1: Academic Course Marksheet
```csv
Name,Course Assignments,Practical Modules,Final Assignment,Final Presentation,Total Marks
Alice Johnson,22/25,23/25,24/25,25/25,94/100
Bob Smith,18/25,19/25,20/25,21/25,78/100
Carol White,25/25,24/25,25/25,24/25,98/100
David Brown,20/25,21/25,19/25,20/25,80/100
```

### Example 2: Workshop Completion
```csv
name,course,date
Alice Johnson,Python Basics Workshop,2026-07-15
Bob Smith,Python Basics Workshop,2026-07-15
Carol White,Python Basics Workshop,2026-07-16
```

### Example 3: With Scores and Grades
```csv
name,course,score,grade,date,id
Alice Johnson,Advanced Python,94,A,2026-07-15,CERT-2026-001
Bob Smith,Advanced Python,78,C+,2026-07-15,CERT-2026-002
Carol White,Advanced Python,98,A+,2026-07-15,CERT-2026-003
```

## Best Practices

### CSV Guidelines
1. **First row must be headers** - Field names in first row
2. **Use UTF-8 encoding** - For international characters
3. **Quote fields with commas** - Use "Last, First" for names with commas
4. **Consistent date format** - Always use YYYY-MM-DD
5. **No empty lines** - Remove blank rows at end

### Data Quality
- **Check spelling** - Names appear on certificates exactly as written
- **Verify scores** - Ensure format is "X/Y" not "X out of Y"
- **Test with sample** - Try 1-2 rows first before full batch
- **Backup originals** - Keep source data before uploading

### Naming Convention
- `participants.csv` - Default, auto-detected
- `batch_YYYY-MM-DD.csv` - Dated batches
- `course_name_marks.csv` - Course-specific

## Troubleshooting

### Issue: Certificates not generated
**Check:**
- CSV has "Name" column (required)
- No syntax errors in CSV
- File is in `data/` directory
- Workflow logs in Actions tab

### Issue: Incorrect scores displayed
**Check:**
- Score format is "X/Y" not "X of Y" or "X:Y"
- Numbers are valid (not text like "eighty")
- Decimal separator is "." not ","

### Issue: Wrong grades assigned
**Check:**
- Scores are correct (auto-calculation)
- If providing manual grades, use standard format (A+, B, etc.)

### Issue: Duplicate certificate IDs
**Check:**
- If auto-generating: Same name+course creates same ID (by design)
- If providing IDs: Ensure uniqueness in your data

## Uploading Your Data

### Via GitHub Web Interface
1. Click on `data/` folder
2. Click "Add file" → "Upload files"
3. Drag your CSV file
4. Commit changes
5. Workflow runs automatically

### Via Git Command Line
```bash
cp your_marksheet.csv data/participants.csv
git add data/participants.csv
git commit -m "Add participants for certificate generation"
git push origin main
```

## Verification URL

The default verification URL is `https://example.com/verify?id=`

To customize:
- **GitHub Actions**: Set in workflow input parameter
- **Locally**: Use `--verification-url` argument
- **Config**: Edit in `config.json` (future feature)

Full URL format: `{base_url}{certificate_id}`
