from time import sleep, localtime
from os import system, name
from sys import argv

if name == 'posix':
    terminal_clr_scr = 'clear'
else:
    terminal_clr_scr = 'cls'

class LoadingBar:
    def __init__(self, 
                 *,
                 loading_time: float,
                 length: int, 
                 complete_symbol: str,
                 incomplete_symbol: str):
        self.loading_time = loading_time
        self.length = length
        self.complete_symbol = complete_symbol
        self.incomplete_symbol = incomplete_symbol
        self.bar = self.incomplete_symbol * self.length

    def __default_file_name(self):
        return ''.join( \
               [f'{date_element}-' for date_element in (localtime()[0:6])]) \
               + 'bar.txt'

    def generate_bars(self, reverse = False):
        bars, buffer = [], None
        for i in range(self.length + 1):
            buffer = (self.complete_symbol * (i)) + self.bar[i:]
            if reverse:
                buffer = ''.join(list(reversed( \
                         buffer)))
            # Let's use dicts!
            bars.append({'bar': buffer, 'percentage': f'{(i/self.length) * 100}%'})
        return bars

    def dump_bars(self, *, file, reverse = False, verbose = True, percent_show = True):
        for bar_and_percentage in self.generate_bars():
            if percent_show:
                print(bar_and_percentage['bar'], bar_and_percentage['percentage'],
                      sep = ' ', file = file)
            else:
                print(bar_and_percentage['bar'], sep = '\n', file = file)

        if verbose:
            print(f'Successfully dumped {file.name}!')

    def show_loading_bar(self, reverse = False, progress_hidden = False, verbose = True, 
                         dump = True, percent_show = True, name = None):
        if dump:
           if not name: 
               name = self.__default_file_name()

           with open(name, 'w') as f:
               self.dump_bars(file = f, reverse = reverse, verbose = False) 

        for bar_and_percentage in self.generate_bars(reverse):
            if progress_hidden:
                system(terminal_clr_scr)
             
            if percent_show:
                print(bar_and_percentage['bar'], bar_and_percentage['percentage'],
                      sep = ' ')
            else:
                print(bar_and_percentage['bar'], sep = '\n')
                
            sleep(self.loading_time)

        if verbose:
            print("\nLoading complete!")
