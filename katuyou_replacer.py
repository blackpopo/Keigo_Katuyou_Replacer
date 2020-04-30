from collections import defaultdict

import os
from pprint import pprint

class Katuyou:
    def __init__(self, base_dir):
        self.base2te = defaultdict(str)
        self.te2base = defaultdict(str)
        self.base2renyou = defaultdict(str)
        self.renyou2base = defaultdict(str)
        self.meirei2base = defaultdict(str)
        self.base2meirei = defaultdict(str)
        self.base2mizen = defaultdict(str)
        self.mizen2base = defaultdict(str)
        
        self.files = os.listdir(base_dir)
        
        base_dict = {'base2te.txt':self.base2te, 'te2base.txt': self.te2base, 'base2renyou.txt': self.base2renyou,
                      'renyou2base.txt': self.renyou2base, 'base2meirei.txt': self.base2meirei, 'meirei2base.txt': self.meirei2base,
                      'mizen2base.txt': self.mizen2base, 'base2mizen.txt': self.base2mizen}
        for file in self.files:
            rev_file = '2'.join(reversed(str(file).rstrip('.txt').split('2'))) + '.txt'
            with open(os.path.join(base_dir, file), 'r') as f:
                lines = f.readlines()
            for line in lines:
                key, value = line.rstrip('\n').split('\t')
                base_dict[file][key] = value
                base_dict[rev_file][value] = key
        
    def convert_base2te(self, tokens):
        try:
            return self.base2te[tokens]
        except:
            return tokens
        
    def convert_te2base(self, tokens):
        try:
            return self.te2base[tokens]
        except:
            return tokens
        
    def convert_base2renyou(self, tokens):
        try:
            return self.base2renyou[tokens]
        except:
            return tokens
        
    def convert_renyou2base(self, tokens):
        try:
            return self.renyou2base[tokens]
        except:
            return tokens

    def convert_meirei2base(self, tokens):
        try:
            return self.base2renyou[tokens]
        except:
            return tokens

    def convert_base2meirei(self, tokens):
        try:
            return self.base2meirei[tokens]
        except:
            return tokens
        
    def convert_mizen2base(self, tokens):
        try:
            return self.mizen2base[tokens]
        except:
            return tokens

    def convert_base2mizen(self, tokens):
        try:
            return self.base2mizen[tokens]
        except:
            return tokens

    def convert_meirei2renyou(self, tokens):
        try:
            return self.base2renyou[self.meirei2base[tokens]]
        except:
            return tokens

    def convert_renyou2meirei(self, tokens):
        try:
            return self.base2meirei[self.renyou2base[tokens]]
        except:
            return tokens
        
    def convert_mizen2renyou(self, tokens):
        try:
            return self.base2renyou[self.mizen2base[tokens]]
        except:
            return tokens
           
    def convert_renyou2mizen(self, tokens):
        try:
            return self.base2mizen[self.renyou2base[tokens]]
        except:
            return tokens
        
    def convert_renyou2te(self, tokens):
        try:
            return self.base2te[self.renyou2base[tokens]]
        except:
            return tokens
        
    def convert_te2renyou(self, tokens):
        try:
            return self.te2base[self.base2renyou[tokens]]
        except:
            return tokens