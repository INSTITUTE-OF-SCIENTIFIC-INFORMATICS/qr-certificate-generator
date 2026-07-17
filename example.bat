@echo off
REM Example: Generate certificates locally on Windows

echo Creating certificate template...
python create_template.py

echo.
echo Generating certificates from CSV...
python generate_certificates.py --template templates/certificate_template.png --data data/participants.csv --output output --verification-url "https://example.com/verify?id="

echo.
echo Generated certificates:
dir output\*.png

echo.
echo Done! Check the output directory for your certificates.
pause
