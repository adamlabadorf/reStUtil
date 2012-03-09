import sys
from reStUtil import ReStDocument, ReStSection, ReStTable

doc = ReStDocument(sys.stdout)

# section 1
sec1 = ReStSection("Section 1",level=1)
sec1.add("The text in section 1")

sec1_1 = ReStSection("Subsection 1.1",level=2)
sec1_1.add("The text in subsection 1.1")
sec1 += sec1_1

sec2 = ReStSection("Section 2",level=1)
sec2.add("The text in section 2")

sec2_1 = ReStSection("Subsection 2.1",level=2)
sec2_1.add("The text in subsection 2.1")

sec2_2 = ReStSection("Subsection 2.2",level=2)
sec2_2.add("Text in subsection 2.2")
sec2.add(sec2_1,sec2_2)

sec3 = ReStSection("Section 3",level=1)
sec3.add("This section has many nested subsections")

sec3.add(ReStSection("Subsection 3.1",level=2))
sec3.add(ReStSection("Subsubsection 3.1.1",level=3))
sec3.add(ReStSection("Subsubsubsection 3.1.1.1",level=4))
sec3.add(ReStSection("Subsubsubsubsection 3.1.1.1.1",level=5))
sec3.add(ReStSection("Subsubsubsubsubsection 3.1.1.1.1.1",level=6))

doc.add(sec1,sec2,sec3)

doc.write()
