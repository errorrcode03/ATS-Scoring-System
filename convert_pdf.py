import os
from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)
input_file = "system_architecture.md" # Ensure this file exists in your project root
output_file = "s:/ML/ATS Scoring System/System_Architecture.pdf"

print("Converting...")
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

pdf.add_section(Section(text, toc=False))
pdf.save(output_file)
print(f"Saved to {output_file}")
