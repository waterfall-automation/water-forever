import os
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas
except ImportError:
    import subprocess
    print("Installing reportlab library for PDF generation...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Skip title page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#506173"))
        
        # Header
        self.drawString(54, 750, "WATER FOREVER INITIATIVE BRIEF")
        self.setStrokeColor(colors.HexColor("#EAE6DF"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "CONFIDENTIAL · PUBLIC UTILITY BLUEPRINT")
        self.line(54, 52, 558, 52)
        self.restoreState()

def build_pdf():
    pdf_path = "water-forever-brochure.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles matching website visual system
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor("#08121E"),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0D6B73"),
        spaceAfter=120
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#08121E"),
        spaceBefore=15,
        spaceAfter=15,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0D6B73"),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#1A2835"),
        spaceAfter=12
    )
    
    story = []
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>WATER FOREVER</b>", title_style))
    story.append(Paragraph("Digital Water Infrastructure for Generations", subtitle_style))
    story.append(Spacer(1, 100))
    
    meta_text = """
    <b>INITIATIVE BRIEF & ROADMAP</b><br/>
    Version 2.0 (2026)<br/>
    Lead Coordinator: Jasveer Singh<br/>
    Organization: Waterfall Automation / Water Forever Initiative<br/>
    Contact: jasveer@wfmail.in | www.waterforever.org<br/>
    """
    story.append(Paragraph(meta_text, body_style))
    story.append(PageBreak())
    
    # --- PAGE 2: THE CHALLENGE & THE PARADIGM SHIFT ---
    story.append(Spacer(1, 20))
    story.append(Paragraph("01 · Executive Summary & The Opportunity", h1_style))
    story.append(Paragraph("Every generation builds the infrastructure its time demands. From early manual wells to massive industrial concrete dams, humanity adapts physical systems to ensure survival. Today, rising demand, climate uncertainty, and extreme weather volatility call for a new paradigm—a shared layer of intelligence overlaying our physical assets.", body_style))
    
    story.append(Paragraph("The Scarcity Visibility Gap", h2_style))
    story.append(Paragraph("Traditional water management is blind. Water assets operate in complete isolation. Reservoirs, groundwater aquifers, treatment plants, and irrigation districts communicate through manual logs and historical estimates rather than active digital telemetry. The core challenge of modern water management isn't just physical availability—it is visibility, distribution efficiency, and predictive resource allocation.", body_style))
    
    story.append(Paragraph("Core Strategic Goals", h2_style))
    story.append(Paragraph("• <b>Unify Information:</b> Bridge regional agency data silos into a single secure protocol.<br/>"
                           "• <b>Real-time Telemetry:</b> Observe reservoirs, aquifers, and irrigation in real time.<br/>"
                           "• <b>Predictive Allocation:</b> Leverage machine learning to route water before crises emerge.<br/>"
                           "• <b>Open Access:</b> Create an interoperable ecosystem for public and private partnership.", body_style))
    story.append(PageBreak())
    
    # --- PAGE 3: THE WATERFALL GRID ARCHITECTURE ---
    story.append(Spacer(1, 20))
    story.append(Paragraph("02 · The Waterfall Grid", h1_style))
    story.append(Paragraph("The Waterfall Grid is an open-source digital infrastructure standard mapping and routing water dynamically from precipitation catchments down to agricultural, domestic, and industrial nodes.", body_style))
    
    story.append(Paragraph("Five Layers of Digital Infrastructure", h2_style))
    
    layers_data = [
        ["Layer", "System Description", "Telemetry Inputs"],
        ["1. Atmospheric Grid", "Sensing inflow volume before precipitation reaches ground.", "Satellite rain models, snowpack depth"],
        ["2. Storage Grid", "Real-time volumetric tracking of surface reservoirs and aquifers.", "Ultrasonic level, groundwater logs"],
        ["3. Orchestration Layer", "Waterfall Intelligence engines calculating routing priorities.", "AI inflow forecasting, optimization models"],
        ["4. Demand Nodes", "Tracking municipal, agricultural, and industrial demand.", "Smart meters, farm soil moisture sensors"],
        ["5. Circular Recharge", "Monitoring environmental return, purification, and recharge.", "Runoff volume, filtration sensors"]
    ]
    
    t = Table(layers_data, colWidths=[100, 220, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#08121E")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FAF8F5"), colors.HexColor("#F2EFE9")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EAE6DF")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('TOPPADDING', (0,1), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    story.append(Paragraph("By combining these five layers into an active loop, regional water grids can coordinate allocation dynamically. In times of monsoon surplus, excess flow is routed to high-absorption aquifer recharge basins. In times of drought, precision agricultural allocation matches reservoir release to actual soil requirements.", body_style))
    story.append(PageBreak())
    
    # --- PAGE 4: OPEN PARTICIPATION & COLLABORATION ---
    story.append(Spacer(1, 20))
    story.append(Paragraph("03 · Collaboration & Open Governance", h1_style))
    story.append(Paragraph("Digital water infrastructure must operate as a shared public utility. The Waterfall Grid protocol is designed under open standards to prevent vendor lock-in and encourage global participation.", body_style))
    
    story.append(Paragraph("Who Participates in the Grid?", h2_style))
    story.append(Paragraph("• <b>Governments:</b> Align regional planners and environmental boards.<br/>"
                           "• <b>Utilities:</b> Connect SCADA systems to real-time allocation feeds.<br/>"
                           "• <b>Farming Cooperatives:</b> Leverage soil moisture data to schedule precise irrigation.<br/>"
                           "• <b>Researchers & Startups:</b> Develop custom AI routing models on open telemetry APIs.", body_style))
    
    story.append(Paragraph("Initiative Coordination", h2_style))
    story.append(Paragraph("Water Forever is actively coordinating pilot implementations in municipal and agricultural water districts. If you are a state planner, developer, or utility operator, you can request integration coordinates by contacting Jasveer Singh.", body_style))
    
    story.append(Spacer(1, 20))
    
    contact_data = [
        ["Coordinator", "Jasveer Singh (Founder)"],
        ["Email", "jasveer@wfmail.in"],
        ["Phone", "+91 94210 58160"],
        ["Website", "www.waterforever.org"],
        ["Core Repository", "github.com/waterfall-automation/water-forever"]
    ]
    
    ct = Table(contact_data, colWidths=[120, 380])
    ct.setStyle(TableStyle([
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#0D6B73")),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EAE6DF")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAF8F5")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(ct)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Brochure generated successfully.")

if __name__ == "__main__":
    build_pdf()
