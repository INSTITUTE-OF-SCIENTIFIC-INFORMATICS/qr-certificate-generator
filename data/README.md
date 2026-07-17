# Certificate Generator Configuration

## Data Format

Participant data can be provided in CSV or JSON format.

### CSV Format
```csv
name,id,course,date,achievement,email
John Doe,CERT001,Python Programming,2026-07-15,Excellent,john@example.com
```

### JSON Format
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

## Required Fields
- `name`: Participant's full name
- `id`: Unique certificate ID

## Optional Fields
- `course`: Course or program name (default: "Course Completion")
- `date`: Certificate issue date (default: current date)
- `achievement`: Achievement level or grade
- `email`: Participant's email address

## Verification URL
Set the `verification_url` parameter to customize where the QR code links to.
Default: `https://example.com/verify?id=`

The full verification URL will be: `{verification_url}{certificate_id}`
