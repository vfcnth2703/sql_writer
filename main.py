# coding=utf-8
import sys
from var_dump import var_dump as vd
import const
from pprint import pprint as pp
import os.path


class Parse_engine():
    """
        Main parser
    """
    def __init__(self):
        self.file_info = None
        self.data = None


    def set_data(self,data):
        self.file_info,self.data = data

class Converter:
    '''
        Conver specific files into format Select into ...
    '''

    def __init__(self, file_name, file_reader, file_writer,parse_engine,file_selector):
        self.file_name = file_name
        self.file_reader = file_reader
        self.file_writer = file_writer
        self.parse_engine = parse_engine
        self.data = self.load_file()
        self.file_selector = file_selector
        self.selector_init()
        self.parse_engine.set_data(self.packing_data())



    def selector_init(self):
        self.file_selector.set_data(self.data)
        self.file_selector.first_row = self.file_selector.find_first_row()
        self.file_selector.header = self.file_selector.select_header()
        self.file_selector.file_info = (self.file_selector.first_row,self.file_selector.header)


    def load_file(self):
        return self.file_reader.read(self.file_name)


    def save_file(self):
        self.file_writer.write(self.file_name, self.lines)


    def get_data(self):
        return self.data


    def packing_data (self):
        return (self.file_selector.file_info, self.data)


class FileSelector:
    '''
        Class for selecting engines
    '''

    def __init__(self):
        self.output_type = const.output_type
        self.input_type = const.input_type
        self.data = None

    def select_header(self):
        if self.data[0].strip() == self.output_type:
            return (const.output_header_line)
        elif self.data[0].strip() == self.input_type:
            return (const.input_header_line)
        else:
            sys.exit('File in wrong format')


    def find_first_row(self):
        global i
        for i, item in enumerate(self.data):
            if item.startswith(const.start_data):
                break
            else:
                i = 0
        return i

    def set_data(self,data):
        self.data = data

class FileReader:
    '''
        Reading files
    '''

    def __init__(self, file_checker):
        self.file_checker = file_checker

    def read(self, file_name):
        self.file_checker.check(file_name)
        with open(file_name, 'r') as f:
            return list(f.readlines())


class FileWriter:
    '''
        Write result file
    '''

    def save(self, file_name, lines):
        with open(file_name, 'w') as f:
            f.writelines(self, lines)


class FileChecker:
    '''
        Checking existing target file
    '''
    def check(self, file_name):
        if not os.path.exists(file_name):
            sys.exit('File not found')


def main():
    file = 'import_small.csv'
    # file = 'roma_data.csv'
    file_checker = FileChecker()
    file_writer = FileWriter()
    file_reader = FileReader(file_checker)
    parse_engine = Parse_engine()
    file_selector  = FileSelector()
    converter = Converter(file, file_reader, file_writer,parse_engine,file_selector)
    vd(converter.file_selector.file_info)
    # pprint(converter.load_file())


if __name__ == '__main__':
    main()
