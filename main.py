# coding=utf-8
import sys

from var_dump import var_dump as vd
import const
from pprint import pprint as pp
import os.path


class Converter:
    '''
        Conver specific files into format Select into ...
    '''

    def __init__(self, file_name, file_reader, file_writer):
        self.file_name = file_name
        self.file_reader = file_reader
        self.file_writer = file_writer
        self.data = None

    def load_file(self):
        return self.file_reader.read(self.file_name)

    def save_file(self):
        self.file_writer.write(self.file_name, self.lines)

    def set_data(self):
        self.data = self.load_file()

    def get_data(self):
        return self.data

class FileSelector:
    '''
        Class for selecting engines
    '''

    def __init__(self, data):
        self.output_type = const.output_type
        self.input_type = const.input_type
        self.data = data

    def select_header(self):
        if self.data[0].strip() == self.output_type:
            return const.export_header_line
        if self.data[0].strip() == self.input_type:
            return const.import_header_line

    def first_row(self):
        for i, item in enumerate(self.data):
            if item.startswith(const.start_data):
                break
        return i


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
    file_checker = FileChecker()
    file_writer = FileWriter()
    file_reader = FileReader(file_checker)
    converter = Converter(file, file_reader, file_writer)
    vd(converter.load_file())
    # pprint(converter.load_file())


if __name__ == '__main__':
    main()
