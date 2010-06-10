import sys
from reStUtil import ReStDocument, ReStSimpleTable, ReStTable

doc = ReStDocument(sys.stdout)

# very simple
header = ["Column A","Column B","Column C"]
data = [['012','345','678']]

doc.add('Simple simple_table, no text wrap')
doc.add(ReStSimpleTable(header,data))

# word wrapped text
header = ["Food", "Deliciousness", "Notes"]
data = [["hot dogs","moderate-high","Depending on the meat used, hot dogs can provide a delicious snack or a mysterious culinary experiment"],
        ["cabbage","low-moderate","Best results often enjoyed when cooked with corned beef or braughwurst"],
        ["pickles and ice cream","low/very high","For pregnant women only"],
       ]

doc.add('Text wrapped simple_table')
doc.add(ReStSimpleTable(header,data,40))

doc.add('Table directive with title and word wrapped data')
doc.add(ReStTable(header,data,title="Food Analysis",max_col_width=40))

doc.write()
