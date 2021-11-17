from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.styles.styles import Styles
from docx.shared import RGBColor

class Word:
    def __init__(self, Text, Data, loghandle):
        self.Text = Text
        self.Data = Data
        self.loghandle = loghandle
        self.document = Document()

    def paragraphrun_style(self, paragraphrun, bold=True, size=None, name=None):
        paragraphrun.font.bold = bold
        if size is None:
            paragraphrun.font.size = Pt(14)
        else:
            paragraphrun.font.size = Pt(int(size))

        if name is None:
            paragraphrun.font.name = "Arial"
        else:
            paragraphrun.font.name = name
        paragraphrun.font.color.rgb = RGBColor(0,0,0)

    def generate_first_page(self):
        default_paragrah =  self.document.add_paragraph()
        default_paragrah.style.font.size = Pt(11)
        default_paragrah.style.font.name = "Calibri(Body)"
        self.document.add_paragraph()

        paragraph = self.document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        title = paragraph.add_run(self.Text["Title"]["name"]+"\n")
        self.paragraphrun_style(title, size=20)

        summary = paragraph.add_run(self.Text["Title"]["summary"]+"\n")
        self.paragraphrun_style(summary, size=12)

        hw = paragraph.add_run(self.Text["Title"]["hw"]+"\n")
        self.paragraphrun_style(hw, size=12)

        line = paragraph.add_run(self.Text["Title"]["line"]+"\n")
        self.paragraphrun_style(line, bold=False, size=12)
        version = paragraph.add_run(self.Text["Title"]["version"]+"\n")
        self.paragraphrun_style(version, bold=False, size=16)

        self.document.add_page_break()


    def heading2_1_content(self):
        content1 = "This Test Report documents a summary of the features and related known defects supported by this platform release.\nTo give a simple and quick overview, the most important parts of this document are: \n"
        content2 = "Traffic light"
        content3 = ""
        paragraph = self.document.add_paragraph()
        purpose = paragraph.add_run(content1)
        #self.paragraphrun_style(purpose, bold=False, size=11, name="Calibri(Body)")


    def heading3_1_content(self):
        content1 = "List of supported features and the known defects."
        paragraph = self.document.add_paragraph()
        purpose = paragraph.add_run(content1)
        table = self.document.add_table(rows=2, cols=3)
        cell = table.cell(0,0)
        cell.text = "Feature"
        cell = table.cell(0,1)
        cell.text = "Name"
        cell = table.cell(0,2)
        cell.text = "Known Defects"

    def generate_second_page(self):
        heading1 = self.document.add_heading(level=1)
        SUMMARY = heading1.add_run(self.Text["Heading"]["heading1"]+"\n")
        self.paragraphrun_style(SUMMARY)

        heading2 = self.document.add_heading(level=1)
        INTRODUCTION = heading2.add_run(self.Text["Heading"]["heading2"]+"\n")
        self.paragraphrun_style(INTRODUCTION)

        heading2_1 = self.document.add_heading(level=2)
        PURPOSE = heading2_1.add_run(self.Text["Heading"]["heading2.1"]+"\n")
        self.paragraphrun_style(PURPOSE)

        self.heading2_1_content()

        heading3 = self.document.add_heading(level=1)
        TEST_RESULTS = heading3.add_run(self.Text["Heading"]["heading3"]+"\n")
        self.paragraphrun_style(TEST_RESULTS)

        heading3_1 = self.document.add_heading(level=2)
        SUPPORTED_FEATURES = heading3.add_run(self.Text["Heading"]["heading3.1"]+"\n")
        self.paragraphrun_style(SUPPORTED_FEATURES)
        self.heading3_1_content()

    def generate_word(self):
        self.generate_first_page()
        self.generate_second_page()
        #paragraph = self.document.add_paragraph(self.Text["Title"]["name"])


# section = document.section[0]
# header = section.header
# paragraph = header.paragraphs[0]
#
# paragraph.text = "\t\tTEMPLATE v0.1"
# Title
# paragraph.style.font.size = Pt(20)
#
# document.add_heading('Document Title', 0)
    def save(self):
        self.document.save('demo.docx')
