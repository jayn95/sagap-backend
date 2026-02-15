"""
Utility functions for PDF report generation.
Uses reportlab to create simple PDF reports from report data.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from typing import List, Dict
from io import BytesIO

def generate_pdf(data: List[Dict], title: str = "Report") -> bytes:
    """
    Generates a PDF file from a list of dictionaries.
    Returns the file as bytes suitable for StreamingResponse.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []

    if not data:
        elements.append(Table([["No data available"]]))
    else:
        headers = list(data[0].keys())
        table_data = [headers] + [[str(row.get(h, "")) for h in headers] for row in data]

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black)
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()
