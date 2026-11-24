import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Nand to Tetris Capstone Project | ETCCNT301 — Hitarth Srivastava (Roll: 2501730430)")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, text)
        self.drawString(54, 35, "School of Engineering & Technology, K.R. Mangalam University — Personal K = 30")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        
        self.restoreState()

def build_pdf(filename="capstone/Capstone_Report_Hitarth_2501730430.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E293B'),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=5
    )

    story = []

    # ==================== PAGE 1 ====================
    story.append(Paragraph("Capstone Project: Make the Computer Draw a Box", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Nand to Tetris – I (ETCCNT301) — School of Engineering & Technology, K.R. Mangalam University", subtitle_style))
    story.append(Spacer(1, 6))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Hitarth Srivastava", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("2501730430", body_style)],
        [Paragraph("<b>Personal Number K:</b>", body_style), Paragraph("<b>30</b> (from roll digits '30')", body_style),
         Paragraph("<b>Repository:</b>", body_style), Paragraph("Hitarth-code/Nand-To-Tetris-Capstone", body_style)],
        [Paragraph("<b>K mod 3 Feature:</b>", body_style), Paragraph("30 mod 3 = 0 (Export <code>symbols.txt</code>)", body_style),
         Paragraph("<b>Box Dimensions:</b>", body_style), Paragraph("Row 30, H=20, W=48px (3 words)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[105, 145, 105, 145])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # Section 1: Executive Summary & K Calculations
    story.append(Paragraph("1. Project Overview & Mathematical Specifications", h1_style))
    story.append(Paragraph(
        "The objective of this Capstone project is to demonstrate end-to-end computer engineering: assembling the hardware chips "
        "into a complete Hack computer, authoring a custom Python assembler, and executing an interactive graphics program "
        "(<code>Box.asm</code>) that renders a customized black rectangular box whenever any key is pressed and clears it upon release.",
        body_style
    ))
    
    calc_data = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Formula / Rule</b>", body_style), Paragraph("<b>Calculated Value for K = 30</b>", body_style)],
        [Paragraph("Personal Number K", body_style), Paragraph("Last 2 digits of Roll No (2501730430)", body_style), Paragraph("<b>K = 30</b>", body_style)],
        [Paragraph("Assembler Extra Feature", body_style), Paragraph("K mod 3 (0: symbols.txt, 1: error msg, 2: warning)", body_style), Paragraph("<b>30 mod 3 = 0</b> (Save all symbols to symbols.txt)", body_style)],
        [Paragraph("Box Vertical Start", body_style), Paragraph("Row K", body_style), Paragraph("<b>Row 30</b>", body_style)],
        [Paragraph("Box Height", body_style), Paragraph("Fixed specification: 20 rows", body_style), Paragraph("<b>20 rows</b> (Rows 30 to 49 inclusive)", body_style)],
        [Paragraph("Box Width", body_style), Paragraph("16 * ((K mod 4) + 1) pixels from left edge", body_style), Paragraph("16 * ((30 mod 4) + 1) = 16 * 3 = <b>48 pixels (3 words)</b>", body_style)],
        [Paragraph("Base Screen Address", body_style), Paragraph("SCREEN + 32 * K (where SCREEN = 16384)", body_style), Paragraph("16384 + 32 * 30 = <b>17344 (0x43C0)</b>", body_style)]
    ]
    calc_table = Table(calc_data, colWidths=[125, 200, 175])
    calc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(calc_table)
    story.append(Spacer(1, 6))

    # Section 2: Part A - Hardware Architecture
    story.append(Paragraph("2. Part A – Hardware Architecture (CPU, Memory, Computer)", h1_style))
    story.append(Paragraph(
        "• <b>Memory.hdl:</b> Integrates 16K Data RAM (0x0000–0x3FFF), Screen Memory Map (0x4000–0x5FFF), and Keyboard Register (0x6000). "
        "A <code>DMux4Way</code> routes the load bit based on <code>address[13..14]</code>, and a <code>Mux4Way16</code> selects the active memory component.<br/>"
        "• <b>CPU.hdl:</b> Decodes 16-bit instructions (A-instruction vs C-instruction). Coordinates A-Register, D-Register, Hack ALU, "
        "memory write flags (<code>writeM</code>, <code>addressM</code>), and PC jump conditions using status flags (<code>zr</code>, <code>ng</code>, <code>pos</code>).<br/>"
        "• <b>Computer.hdl:</b> Connects the CPU, Memory, and ROM32K instruction memory into a complete clock-driven computer.",
        body_style
    ))

    # ==================== PAGE 2 ====================
    story.append(PageBreak())
    
    story.append(Paragraph("2.1 Hardware Simulator Verification & Results", h2_style))
    story.append(Paragraph(
        "The chips were verified in the official Nand2Tetris Hardware Simulator using official test scripts. "
        "Below is the exact simulation output for <b>Memory.hdl</b> and <b>CPU.hdl</b>, showing successful comparison verification:",
        body_style
    ))

    # Insert user's exact Memory screenshot
    if os.path.exists('capstone/memory_test_result.png'):
        story.append(Image('capstone/memory_test_result.png', width=500, height=210))
        story.append(Paragraph("<b>Figure 1:</b> Nand2Tetris Hardware Simulator running <code>Memory.tst</code> on <code>Memory.hdl</code> (Simulation successful).", caption_style))
        story.append(Spacer(1, 4))

    # Insert CPU screenshot
    if os.path.exists('capstone/cpu_test_result.png'):
        story.append(Image('capstone/cpu_test_result.png', width=500, height=180))
        story.append(Paragraph("<b>Figure 2:</b> Nand2Tetris Hardware Simulator running <code>CPU.tst</code> on <code>CPU.hdl</code> (Simulation successful).", caption_style))
        story.append(Spacer(1, 4))

    # Section 3: Part B - Python Assembler
    story.append(Paragraph("3. Part B – Custom Hack Assembler (assembler.py)", h1_style))
    story.append(Paragraph(
        "A two-pass assembler was implemented in Python (<code>assembler.py</code>) to translate Hack assembly code (<code>.asm</code>) "
        "into 16-bit binary machine instructions (<code>.hack</code>).<br/>"
        "• <b>Pass 1:</b> Strips whitespace and comments, builds symbol table for labels <code>(LABEL)</code> bound to ROM line addresses.<br/>"
        "• <b>Pass 2:</b> Encodes A-instructions and C-instructions. Dynamically allocates user variables to RAM starting at address 16.<br/>"
        "• <b>Extra Feature (K mod 3 = 0):</b> The assembler exports <b><code>symbols.txt</code></b> containing all defined labels, "
        "user variables, and predefined architectural symbols with their corresponding memory addresses.<br/>"
        "• <b>Validation:</b> Outputs generated for official benchmarks (<code>Add.asm</code>, <code>Max.asm</code>, <code>Rect.asm</code>, <code>Pong.asm</code>) "
        "match the official Nand2Tetris assembler with 100% binary identity.",
        body_style
    ))

    # ==================== PAGE 3 ====================
    story.append(PageBreak())
    
    # Section 4: Part C - Box Program
    story.append(Paragraph("4. Part C – Interactive Box Program (Box.asm & Box.hack)", h1_style))
    story.append(Paragraph(
        "<code>Box.asm</code> was programmed in Hack assembly to implement an interactive graphics routine personalized to <b>K = 30</b>. "
        "The program was converted to machine code using our custom <code>assembler.py</code> into <code>Box.hack</code> (49 instructions).",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Keyboard Polling:</b> Probes the memory-mapped keyboard register at address <code>24576 (KBD)</code>. If <code>RAM[24576] != 0</code>, "
        "color word is set to <code>-1 (0xFFFF)</code>. If <code>RAM[24576] == 0</code>, color word is set to <code>0 (0x0000)</code>.<br/>"
        "• <b>Screen Memory Stride Arithmetic:</b> Each row in the Hack screen spans 32 words (512 pixels). Row 30 starts at address "
        "<code>16384 + 32 * 30 = 17344</code>. The program draws 3 words per row (words 0, 1, 2) covering 48 contiguous horizontal pixels.<br/>"
        "• <b>Nested Loop Logic:</b> A row loop iterates 20 times (decrementing <code>rows_left</code> from 20 down to 0). In each iteration, "
        "words at <code>addr</code>, <code>addr+1</code>, and <code>addr+2</code> are populated with the current color, and <code>addr</code> is "
        "incremented by 32 (<code>addr = addr + 32</code>) to advance cleanly to the next display row.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>CPU Emulator Execution & Screen Verification:</b>", h2_style))
    if os.path.exists('capstone/box_emulator_result.png'):
        story.append(Image('capstone/box_emulator_result.png', width=500, height=230))
        story.append(Paragraph("<b>Figure 3:</b> CPU Emulator executing <code>Box.hack</code>. When key 'A' (KBD=65) is pressed, the solid black box renders at Row 30 (48x20 px).", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Verification Proof:</b> As verified in the emulator, when any key is pressed, all 60 words (rows 30..49, columns 0..2) "
        "transition to 0xFFFF (solid black pixels). When the key is released, RAM[24576] resets to 0, and the exact same drawing loop clears all "
        "60 words back to 0x0000 (white), instantly making the box disappear without display flickering.",
        body_style
    ))

    # ==================== PAGE 4 ====================
    story.append(PageBreak())

    # Section 5: Mistake Fixed
    story.append(Paragraph("5. Engineering Reflection: One Mistake I Fixed", h1_style))
    story.append(Paragraph(
        "<b>The Issue Encountered:</b> During early testing of <code>Box.asm</code>, the screen only rendered the first row of 48 pixels, "
        "while the remaining 19 rows failed to appear. Upon inspecting data memory in the simulator, data registers <code>RAM[0..2]</code> "
        "were being unexpectedly overwritten with <code>-1</code>, while screen addresses below 17344 remained blank.<br/><br/>"
        "<b>Root Cause Analysis:</b> In Hack assembly, commutative addition is mathematically symmetric ($D+M = M+D$), but the Hack CPU "
        "hardware specification strictly defines the ALU computation mnemonics with <code>D</code> as the primary operand (<code>D+A</code> and <code>D+M</code>). "
        "In <code>Box.asm</code>, the address increment was written as <code>@32; D=A; @addr; M=M+D</code>. Because the initial assembler dictionary "
        "only mapped <code>D+M</code>, looking up <code>M+D</code> returned the default computation bits (<code>0000000</code>, representing <code>D&A</code>). "
        "With $a=0$, $A=17$, and $D=32$, computing $32 \\& 17$ evaluated to 0. Consequently, <code>addr</code> was unintentionally reset to <code>0</code> "
        "after the first iteration, causing subsequent rows to write to addresses 0, 1, and 2 instead of screen memory!<br/><br/>"
        "<b>Resolution:</b> The issue was resolved across two fronts: (1) Corrected <code>Box.asm</code> to standard <code>M=D+M</code>, and "
        "(2) Enhanced <code>assembler.py</code> with full bidirectional support for all commutative ALU operations (<code>D+A/A+D</code>, "
        "<code>D+M/M+D</code>, <code>D&M/M&D</code>, <code>D|M/M|D</code>). Re-assembling and running the code produced all 20 rows (60 words) "
        "with zero memory corruption.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 6: Viva Guide
    story.append(Paragraph("6. Viva Defense & Live Code Modification Guide", h1_style))
    story.append(Paragraph(
        "To prepare for the 5-minute viva demonstration and on-the-spot changes, key parameter locations in <code>Box.asm</code> are indexed below:",
        body_style
    ))
    
    viva_data = [
        [Paragraph("<b>Requested Viva Change</b>", body_style), Paragraph("<b>Target Location in Box.asm</b>", body_style), Paragraph("<b>Modification Example</b>", body_style)],
        [Paragraph("Move box vertically (e.g. down 10 rows)", body_style), Paragraph("Line 28: <code>@17344</code>", body_style), Paragraph("Change to <code>@17664</code> (17344 + 32 * 10)", body_style)],
        [Paragraph("Change box height (e.g. 30 rows)", body_style), Paragraph("Line 34: <code>@20</code>", body_style), Paragraph("Change <code>@20</code> to <code>@30</code> (rows_left counter)", body_style)],
        [Paragraph("Change box width (e.g. 4 words / 64px)", body_style), Paragraph("Line 57 (after Word 2 draw)", body_style), Paragraph("Add drawing for <code>addr+3</code> using target pointer", body_style)],
        [Paragraph("Invert behavior (white on press, black default)", body_style), Paragraph("Lines 16 & 24 (color setup)", body_style), Paragraph("Swap <code>M=-1</code> and <code>M=0</code> assignments", body_style)]
    ]
    viva_table = Table(viva_data, colWidths=[150, 140, 200])
    viva_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(viva_table)
    story.append(Spacer(1, 6))

    # Section 7: Submission Deliverables
    story.append(Paragraph("7. Submission Deliverables Summary", h1_style))
    story.append(Paragraph(
        "• <b>GitHub Repository:</b> <code>https://github.com/Hitarth-code/Nand-To-Tetris-Capstone.git</code><br/>"
        "• <b>Folder:</b> <code>capstone/</code> containing: <code>CPU.hdl</code>, <code>Memory.hdl</code>, <code>Computer.hdl</code>, "
        "<code>assembler.py</code>, <code>Box.asm</code>, <code>Box.hack</code>, and <code>symbols.txt</code>.<br/>"
        "• <b>Report File:</b> <code>Capstone_Report_Hitarth_2501730430.pdf</code> submitted on ZOSIMA portal.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()
