# coding=utf-8
import my_const
import sys
import os.path


class ParseEngine():
    """
        Main parser
    """

    def __init__(self):
        self.file_info = None
        self.data = None

    def set_data(self, data):
        self.file_info, self.data = data

    def add_space(self, val):
        """
            Делает заданный отступ
        """
        return ' ' * val

    def go_parse(self):
        first_row, header = self.file_info
        data = self.data[first_row:]
        lines = []
        lines.append(f'WITH R ({header})\n AS (\n')
        for item in data:
            line = '\', \''.join(item.replace(my_const.start_data, '').split(';')).strip()
            line = f'{self.add_space(4)}select \'{line}\'\n'
            lines.append(line)
            if item != data[-1]:
                line = f'{self.add_space(6)}union all\n'
                lines.append(line)
        line = ')\n\n'
        lines.append(line)
        line = f'{self.add_space(2)}Select * from R\n\n'
        lines.append(line)
        return lines


class FileCollector:
    def __init__(self):
        self.files = []

    def collect_files(self, *args):
        """
            Делает список файлов с заданными расширениями в
            текущей директории.
        """
        args = tuple(['.' + str(item).lower() for item in args])
        home_dir = os.getcwd()
        for file in sorted(os.listdir(home_dir)):
            if file.lower().endswith(args):
                self.files.append(home_dir + '\\' + file)
        return self.files


class Converter:
    '''
        Convert specific files into format Select into ...
    '''

    def __init__(self, file_name, file_reader, file_writer, parse_engine, file_selector):
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
        self.file_selector.file_info = (self.file_selector.first_row, self.file_selector.header)

    def load_file(self):
        return self.file_reader.read(self.file_name)

    def save_file(self):
        self.file_writer.write(self.file_name, self.lines)

    def get_data(self):
        return self.data

    def packing_data(self):
        return (self.file_selector.file_info, self.data)


class FileSelector:
    '''
        Class for selecting engines
    '''

    def __init__(self):
        self.output_type = my_const.output_type
        self.input_type = my_const.input_type
        self.data = None

    def select_header(self):
        if self.data[0].strip() == self.output_type:
            return (my_const.output_header_line)
        elif self.data[0].strip() == self.input_type:
            return (my_const.input_header_line)
        else:
            sys.exit('File in wrong format')

    def find_first_row(self):
        global i
        for i, item in enumerate(self.data):
            if item.startswith(my_const.start_data):
                break
            else:
                i = 1
        return i

    def set_data(self, data):
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
            f.writelines(lines)

    def set_ext_to_file(self, file, ext='sql'):
        """
            Меняем расширение файла
        """
        return f'{os.path.splitext(file)[0]}.{ext}'


class FileChecker:
    '''
        Checking existing target file
    '''

    def check(self, file_name):
        if not os.path.exists(file_name):
            sys.exit('File not found')


def main():
    file_collector = FileCollector()
    file_checker = FileChecker()
    file_writer = FileWriter()
    file_reader = FileReader(file_checker)
    parse_engine = ParseEngine()
    file_selector = FileSelector()
    for file in file_collector.collect_files('csv'):
        con = Converter(file, file_reader, file_writer, parse_engine, file_selector)
        writer = con.file_writer.set_ext_to_file
        con.file_writer.save(writer(con.file_name), con.parse_engine.go_parse())


if __name__ == '__main__':
    main()
