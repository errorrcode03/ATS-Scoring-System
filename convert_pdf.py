from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)
input_file = "C:/Users/SAYAN/.gemini/antigravity/brain/36b96c92-692e-44ce-b4ae-26b1d867f2cd/system_architecture.md"
output_file = "s:/ML/ATS Scoring System/System_Architecture.pdf"

print("Converting...")
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

pdf.add_section(Section(text, toc=False))
pdf.save(output_file)
print(f"Saved to {output_file}")
