'''Exceedingly simple interface for programmatically generating reStructuredText
documents.'''

import sys
import textwrap


class ReStUtilException(Exception) : pass


class BaseReSt(object) :
    '''Base reStructuredText component, does nothing, should be subclassed with
    *build_text* method overridden. Components are expected to add their own
    newline character at the end of their text'''

    def __init__(self) :
        self.text = ''

    def get_text(self) :
        self.build_text()
        return self.text

    def build_text(self) :
        pass


class ReStDocument(BaseReSt) :
    '''Basic Document class, used to collect reStructuredText classes to produce a
    single output file.  Add a component by appending to the *components* member,
    alternatively use the .add() method. Constructor accepts either a file-like 
    object or a filename.'''

    def __init__(self,f) :
        BaseReSt.__init__(self)

        # check for file-like object
        if hasattr(f,'write') :
            self._f = f
        # check for filename
        elif isinstance(f,str) or isinstance(f,unicode) :
            self._f = open(f,'w')
        else :
            raise ReStUtilException('Unrecognized parameter format to ReStDocument, \
                                     must either have a .write(str) method or be a \
                                     filename')
        self.components = []
        self.add("\n")

    def build_text(self) :
        self.text = ''.join([x.get_text()+'\n' for x in self.components])

    def add(self,component) :
        '''Add the component to the end of the document.  Component is either a
        BaseReSt subclass instance or a string.  In the latter case, the string
        is wrapped in a ReStText object for maximal convenience'''

        # convenience case, adding a string wraps string in ReStText object
        if isinstance(component,str) :
            component = ReStText(component)
        self.components.append(component)

    def write(self) :
        self._f.write(self.get_text())


class ReStText(BaseReSt) :
    '''Basic text block, text wrapped to 80 characters by default'''

    def __init__(self,text,width=80) :
        BaseReSt.__init__(self)
        self.text = textwrap.fill(text,width,
                                  break_long_words=True)

    def build_text(self) :
        self.text += '\n'

class ReStImage(BaseReSt) :
    '''Image directive, image URI is required, options (height, width, etc.) are
    specified as a dictionary to the constructor'''

    def __init__(self,image_fn,options={}) :
        BaseReSt.__init__(self)
        self.image_fn = image_fn
        self.options = options

    def build_text(self) :
        self.text = '.. image:: %s\n'%self.image_fn
        for k,v in self.options :
            self.text += '   :%s: %s\n'%(str(k),str(v))
        self.text += '\n'


class ReStFigure(BaseReSt) :
    '''Figure directive, image URI is required, caption is optional,
    options (height, width, etc.) are specified as a dictionary to
    the constructor'''

    def __init__(self,image_fn,caption='',options={}) :
        BaseReSt.__init__(self)
        self.image_fn = image_fn
        self.caption = caption
        self.options = options

    def build_text(self) :
        self.text = '.. figure:: %s\n'%self.image_fn
        for k,v in self.options :
            self.text += '   :%s: %s\n'%(str(k),str(v))
        self.text += textwrap.fill(self.caption,
                                   80,
                                   initial_indent='   ',
                                   subsequent_indent='   ',
                                   break_long_words=True,
                                   ) + '\n'

class ReStSimpleTable(BaseReSt) :
    '''Simple table markup block, accepts header list and data list of lists,
    all top level lists must have same length.  If *max_col_width* is provided
    then column text will be textwrapped if length exceeds value'''

    def __init__(self,header,data,max_col_width=sys.maxint) :

        # check to make sure the data rows have the same number of entries as the header
        if any([len(x)!= len(header) for x in data]) :
            raise ReStUtilException('Not all data rows have same length as header:\n%s\n%s'%(header,data))

        BaseReSt.__init__(self)
        self.header = header
        self.data = data
        self.max_col_width = max_col_width

    def build_text(self) :

        # prepare data rows to calculate column widths, text wrapping does not
        # always respect column width on long words
        wrapped_data = []
        col_widths = [0]*len(self.header)
        for row in self.data :

            # text wrap row data
            if self.max_col_width :
                wrapped_row_data = [textwrap.wrap(str(x),self.max_col_width,break_long_words=True) for x in row]
            else :
                wrapped_row_data = [[str(x)] for x in row]

            # pad the wrapped row data with empty strings for shorter cells
            max_data_rows = max([len(x) for x in wrapped_row_data])
            for x in wrapped_row_data :
                x.extend(['']*(max_data_rows-len(x)))

            wrapped_data.append(wrapped_row_data)

            # find actual column widths based on text wrapped data
            wrapped_col_widths = [max(len(y) for y in x) for x in wrapped_row_data]
            col_widths = [max(x,w) for x,w in zip(wrapped_col_widths,col_widths)]

        # factor header into column widths
        col_widths = [max(len(x),y) for x,y in zip(self.header,col_widths)]

        # line separator
        line_sep = '+-'+'-+-'.join(['-'*x for x in col_widths])+'-+'+'\n'
        self.text = line_sep

        # header row
        self.text += '| '+' | '.join([h.center(w) for h,w in zip(self.header,col_widths)])+' |'+'\n'
        self.text += line_sep

        # data rows
        for row in wrapped_data :
            for row_line in zip(*row) :
                self.text += '| '+' | '.join([x.ljust(w) for x,w in zip(row_line,col_widths)])+' |'+'\n'
            self.text += line_sep


class ReStTable(BaseReSt) :
    '''Table directive, accepts header list and data list of lists,
    all top level lists must have same length'''

    def __init__(self,header,data,title='',max_col_width=None,options={}) :
        BaseReSt.__init__(self)
        self._simp_table = ReStSimpleTable(header,data,max_col_width)
        self.title = title

    def build_text(self) :
        self.text = '.. table:: %s\n\n'%self.title
        tab_text = self._simp_table.get_text()

        # indent the table
        self.text += '   '+tab_text.replace('\n','\n   ')


class ReStSection(BaseReSt) :
    '''Section tag with title, level passed in as constructor argument.  Valid
    levels are integers 1-6.  Documents shouldn't have more than 6 section
    levels anyway.'''

    SECTION_LEVELS = '=-~:#+'

    def __init__(self,title,level=1) :
        BaseReSt.__init__(self)
        self.title = title
        self.level = level
        self.char = ReStSection.SECTION_LEVELS[level-1]

    def build_text(self) :
        self.text = self.title+'\n'+self.char*len(self.title)+'\n'

class ReStHyperlink(BaseReSt) :
    '''Hyperlink directive, can be internal or external, direct or indirect
    depending on parameters passed in.  An ReStHyperlink with *name* can appear
    in any other directive as *name*_.  Section titles, footnotes, and citations
    automatically generate hyperlink targets, per reSt documentation.'''

    def __init__(self,name,url='',indirect=False) :
        BaseReSt.__init__(self)
        self.name = name
        self.url = url
        self.indirect = indirect

    def build_text(self) :
        self.text = '.. _%s: %s\n'%(self.name,self.url)
        if self.indirect :
            self.text += '\n__ %s_\n'%self.name
