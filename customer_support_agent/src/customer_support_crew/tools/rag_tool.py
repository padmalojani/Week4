from crewai_tools import PDFSearchTool

# Point to your local company FAQ or document
rag_tool = PDFSearchTool(pdf='knowledge/example.pdf')
