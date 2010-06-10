import sys
from reStUtil import ReStDocument, ReStSection, ReStTable

doc = ReStDocument(sys.stdout)

# section 1
doc.add(ReStSection("Section 1",level=1))
doc.add("The text in section 1")

doc.add(ReStSection("Subsection 1.1",level=2))
doc.add("The text in subsection 1.1")

doc.add(ReStSection("Section 2",level=1))
doc.add("The text in section 2")

doc.add(ReStSection("Subsection 2.1",level=2))
doc.add("The text in subsection with user specified heading char")

doc.add(ReStSection("Subsection 2.2",level=2))
doc.add("Text in another subsection with user char")

doc.add(ReStSection("Section 3",level=1))
doc.add("This section has many nested subsections")

doc.add(ReStSection("Subsection 3.1",level=2))
doc.add(ReStSection("Subsubsection 3.1.1",level=3))
doc.add(ReStSection("Subsubsubsection 3.1.1.1",level=4))
doc.add(ReStSection("Subsubsubsubsection 3.1.1.1.1",level=5))
doc.add(ReStSection("Subsubsubsubsubsection 3.1.1.1.1.1",level=6))

doc.write()
