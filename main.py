# coding=utf-8
from var_dump import var_dump as vd
import const
from pprint import pprint as pp
import reader  # CSV Files
import os.path


class Converter:
    '''
        Conver specific files into format Select into ...
    '''

    def __init__(self, file_name, file_reader, file_writer):
        self.file_name = file_name
        self.file_reader = file_reader
        self.file_writer = file_writer

    def load_file(self):
        return self.file_reader.read(self.file_name)

    def save_file(self):
        self.file_writer.write(self.file_name, self.lines)


class Selector:
    '''
        Class for selecting engines
    '''

    def __int__(self, file_reader, file_name):
        self.file_reader = file_reader
        self.file_name = file_name
        self.output_type = const.output_type
        self.input_type = const.input_type

    def select(self):
        if self.file_reader(self.file_name)[0] == self.output_type:
            return const.export_header_line
        if self.file_reader(self.file_name)[0] == self.input_type:
            return const.import_header_line


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
            raise IOError("File not found.")


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
