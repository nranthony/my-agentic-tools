# Document Generation Tools

Tools for generating professional documents in various formats including LaTeX, PDF, and Word.

## Tools Included

- **LaTeX Generation**: Template-based LaTeX document creation
- **PDF Creation**: Direct PDF generation with ReportLab
- **HTML to PDF**: Convert HTML/CSS to PDF with WeasyPrint
- **Markdown Processing**: Enhanced markdown with custom extensions
- **Word Documents**: Create and modify .docx files

## Key Features

- Template-based document generation
- Dynamic content injection
- Multi-format export (PDF, LaTeX, Word, HTML)
- Citation management
- Image and chart embedding
- Custom styling and themes

## Installation

```bash
# From root directory
pip install -e .[document-generation]

# Or install individually
cd document-generation && pip install -e .
```

## System Requirements

For LaTeX functionality, install a LaTeX distribution:
- **Ubuntu/Debian**: `sudo apt-get install texlive-full`
- **macOS**: Install MacTeX
- **Windows**: Install MiKTeX

## Quick Start

```python
from document_generation.latex_generator import LaTeXGenerator
from document_generation.pdf_creator import PDFCreator

# LaTeX example
generator = LaTeXGenerator(template="research_paper")
generator.set_content({
    "title": "My Research Paper",
    "author": "Author Name",
    "sections": [...]
})
generator.compile_to_pdf("output.pdf")

# Direct PDF creation
pdf = PDFCreator()
pdf.add_heading("Document Title")
pdf.add_paragraph("Content here...")
pdf.save("direct_output.pdf")
```

## Templates

Templates are located in `templates/` directory:
- `research_paper.tex`
- `report.tex`
- `presentation.tex`
- `resume.tex`