'''Exceedingly simple interface for programmatically generating reStructuredText
documents.'''

import sys
import textwrap


class ReStUtilException(Exception) : pass


class ReStBase(object) :
    '''Base reStructuredText component containing text, should be subclassed with
    *build_text* method overridden. Components are expected to add their own
    newline character at the end of their text.'''

    def __init__(self,text='') :
        self.text = text

    def get_text(self) :
        self.build_text()
        return self.text

    def build_text(self) :
        pass

    def __add__(self,obj) :
        if isinstance(obj,str) :
            txt_to_add = obj
        else :
            txt_to_add = obj.get_text()
        return ReStBase(self.get_text() + "\n" + txt_to_add)

    def __str__(self) :
        return self.get_text()


class ReStContainer(ReStBase) :
    '''A container for holding multiple ReSt object. Useful for organizing
    document elements.  Individual components are separated with newlines.'''
    
    def __init__(self,components=None) :
        self.components = components or []

    def build_text(self) :
        self.text = "\n"+''.join([x.get_text()+'\n' for x in self.components])

    def __add__(self,obj) :
        self.add(obj)
        self.build_text()
        return self

    def add(self,component,*args) :
        '''Add the component to the end of the document.  Component is either a
        ReStBase subclass instance or a string.  In the latter case, the string
        is wrapped in a ReStText object for maximal convenience'''

        comps_to_add = [component]+list(args)
        for component in comps_to_add :
            # convenience case, adding a string wraps string in ReStText object
            if isinstance(component,str) :
                component = ReStText(component)
            self.components.append(component)


class ReStSection(ReStContainer) :
    '''Section tag with title, level passed in as constructor argument.  Valid
    levels are integers 1-6.  Documents shouldn't have more than 6 section
    levels anyway.'''

    SECTION_LEVELS = '=-~:#+'

    def __init__(self,title,level=None) :
        ReStContainer.__init__(self)
        self.title = title
        self.level = level or 1
        self.components = [None]

    def build_text(self) :
        char = ReStSection.SECTION_LEVELS[self.level-1 if self.level is not None else 0]
        self.components[0] = ReStBase(self.title+'\n'+char*len(self.title)+'\n')
        ReStContainer.build_text(self)

    def add(self,component,*args) :
        '''Overloaded method that increments other ReStSection components so
        adding sections produces nested subsection structure. Other components
        are added as is.
        
        .. note:: In order for section nesting without specifying *levels* to
           work properly all sections must be added from highest to lowest, e.g.::
           
             sec = ReStSection("section")
             subsec = ReStSection("subsection")
             sec.add(subsec)

             subsec.add("subsection text")
             subsubsec = ReStSection("subsubsection")
             subsec.add(subsubsec)
        '''
        if isinstance(component,ReStSection) :
            component.level = self.level+1
        ReStContainer.add(self,component,*args)


class ReStDocument(ReStContainer) :
    '''Basic Document class, used to collect reStructuredText classes to produce a
    single output file.  Add a component by appending to the *components* member,
    alternatively use the .add() method. Constructor accepts either a file-like 
    object or a filename.'''

    def __init__(self,f) :
        ReStContainer.__init__(self)

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

    def write(self) :
        self._f.write(self.get_text())

    def close(self) :
        self._f.close()


class ReStText(ReStBase) :
    '''Basic text block, text wrapped to 80 characters by default'''

    def __init__(self,text,width=80) :
        ReStBase.__init__(self)
        self.text = textwrap.fill(text,width,
                                  break_long_words=True)
        self.text += '\n'


class ReStImage(ReStBase) :
    '''Image directive, image URI is required, options (height, width, etc.) are
    specified as a dictionary to the constructor'''

    def __init__(self,image_fn,options={}) :
        ReStBase.__init__(self)
        self.image_fn = image_fn
        self.options = options

    def build_text(self) :
        self.text = '.. image:: %s\n'%self.image_fn
        for k,v in self.options.items() :
            self.text += '   :%s: %s\n'%(str(k),str(v))
        self.text += '\n'


class ReStFigure(ReStBase) :
    '''Figure directive, image URI is required, caption is optional,
    options (height, width, etc.) are specified as a dictionary to
    the constructor'''

    def __init__(self,image_fn,caption='',options={}) :
        ReStBase.__init__(self)
        self.image_fn = image_fn
        self.caption = caption
        self.options = options

    def build_text(self) :
        self.text = '.. figure:: %s\n'%self.image_fn
        for k,v in self.options.items() :
            self.text += '   :%s: %s\n'%(str(k),str(v))
        self.text += textwrap.fill(self.caption,
                                   80,
                                   initial_indent='   ',
                                   subsequent_indent='   ',
                                   break_long_words=True,
                                   ) + '\n'

class ReStSimpleTable(ReStBase) :
    '''Simple table markup block, accepts header list and data list of lists,
    all top level lists must have same length unless *ignore_missing* is True,
    in which case all data rows are either truncated or extended to match the
    header or the longest data row if there is no header.
    '''

    def __init__(self,header,data,max_col_width=None,ignore_missing=False) :

        # check to make sure the data rows have the same number of entries as the header
        if not ignore_missing and header is not None and any([len(x)!= len(header) for x in data]) :
            raise ReStUtilException('Not all data rows have same length as header:\n%s\n%s'%(header,data))

        ReStBase.__init__(self)
        self.header = header
        self.data = data

        # max_col_width is now deprecated
        if max_col_width is not None :
            sys.stderr.write('Note: max_col_width argument to ReStSimpleTable ' \
                             'constructor is deprecated, user must text wrap ' \
                             'content manually with new lines\n')

    def build_text(self) :

        # prepare data rows to calculate column widths, text wrapping does not
        # always respect column width on long words
        wrapped_data = []
        if self.header is not None :
            col_widths = [0]*len(self.header)
            longest_row = len(self.header)
        else :
            col_widths = [0]*255 # should never have more than 255 column, right?
            longest_row = max(len(r) for r in self.data)

        for row in self.data :

            extra = ['']*(max(0,longest_row-len(row)))
            row = row[:longest_row]+extra

            wrapped_row_data = []
            for data_cell in row :
                if hasattr(data_cell,'get_text') :
                    cell = data_cell.get_text().split('\n')
                else :
                    cell = str(data_cell).split('\n')
                if len(cell[-1]) == 0 : # splitting can sometimes introduce blank last entry
                    cell = cell[:-1]
                wrapped_row_data.append(cell)

            # pad the wrapped row data with empty strings for shorter cells
            max_data_rows = max([len(x) for x in wrapped_row_data])
            for x in wrapped_row_data :
                x.extend(['']*(max_data_rows-len(x)))

            wrapped_data.append(wrapped_row_data)

            # find actual column widths based on text wrapped data
            wrapped_col_widths = [max(len(y) for y in x) for x in wrapped_row_data]
            col_widths = [max(x,w) for x,w in zip(wrapped_col_widths,col_widths)]

        # factor header into column widths
        if self.header is not None :
            col_widths = [max(len(x),y) for x,y in zip(self.header,col_widths)]

        # line separator
        line_sep = '+-'+'-+-'.join(['-'*x for x in col_widths])+'-+'+'\n'
        self.text = line_sep

        # header row
        if self.header is not None :
            self.text += '| '+' | '.join([h.center(w) for h,w in zip(self.header,col_widths)])+' |'+'\n'
            self.text += line_sep

        # data rows
        for row in wrapped_data :
            for row_line in zip(*row) :
                self.text += '| '+' | '.join([x.ljust(w) for x,w in zip(row_line,col_widths)])+' |'+'\n'
            self.text += line_sep


class ReStTable(ReStBase) :
    '''Table directive, accepts header list and data list of lists, all top
    level lists must have same length unless *ignore_missing* is True, in which
    case all data rows are either truncated or extended to match the header.
    '''

    def __init__(self,header,data,title='',max_col_width=None,options={},ignore_missing=False) :
        ReStBase.__init__(self)
        self._simp_table = ReStSimpleTable(header,data,
                                           max_col_width=max_col_width,
                                           ignore_missing=ignore_missing)
        self.title = title

    def build_text(self) :
        self.text = '.. table:: %s\n\n'%self.title
        tab_text = self._simp_table.get_text()

        # indent the table
        self.text += '   '+tab_text.replace('\n','\n   ')


class ReStHyperlink(ReStBase) :
    '''Hyperlink directive, can be internal or external, direct or indirect
    depending on parameters passed in.  An ReStHyperlink with *name* can appear
    in any other directive as *name_*.  Section titles, footnotes, and citations
    automatically generate hyperlink targets, per reSt documentation.'''

    def __init__(self,name,url='',indirect=False) :
        ReStBase.__init__(self)
        self.name = name
        self.url = url
        self.indirect = indirect

    def build_text(self) :
        self.text = '.. _%s: %s\n'%(self.name,self.url)
        if self.indirect :
            self.text += '\n__ %s_\n'%self.name
