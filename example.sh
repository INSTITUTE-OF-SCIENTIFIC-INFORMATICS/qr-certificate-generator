# Example: Generate certificates locally

# Step 1: Create the certificate template
echo "Creating certificate template..."
python create_template.py

# Step 2: Generate certificates from CSV data
echo "Generating certificates from CSV..."
python generate_certificates.py \
  --template templates/certificate_template.png \
  --data data/participants.csv \
  --output output \
  --verification-url "https://example.com/verify?id="

# Step 3: View the results
echo "Generated certificates:"
ls -lh output/

echo ""
echo "Done! Check the output/ directory for your certificates."
