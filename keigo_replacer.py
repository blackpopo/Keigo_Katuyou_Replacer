from collections import defaultdict
from Katuyou_and_Keigo.katuyou_replacer import Katuyou
from itertools import cycle
import MeCab


class Keigo(Katuyou):
    def __init__(self, katuyou_dir):
        super(Keigo, self).__init__(katuyou_dir)
        self.mecab = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
        self.mecab.parse('')
        self.normal2kenzyou, self.normal2sonkei, self.kenzyou2normal, self.sonkei2normal = defaultdict(str), defaultdict(str), defaultdict(str), defaultdict(str)
        self.sonkei_list, self.kenzyou_list = list(), list()
        
        self.mas = ['ませ', 'まし', 'まし', 'ます', 'ませ', 'ませ','ましょ']
        self.itasu = ['いたさ', 'いたし', 'いたし', 'いたす', 'いたすれ', 'いたせ', 'いたそ']
        self.suru = ['せ', 'し', 'し' ,'する', 'すれ', 'せよ', 'しよ']
        self.ori = ['おら', 'おり', 'おっ', 'おる', 'おれ', 'おれ', 'おろ']
        self.itadaku = ['いただか', 'いただき', 'いただい', 'いただく', 'いただけ', 'いただけ', 'いただこ',
                    '頂か', '頂き', '頂い', '頂く', '頂け', '頂け', '頂こ']
        self.nasaru = ['なさ', 'なし', 'なさっ', 'なす', 'なせ', 'なせ', 'なそ']
        self.naru = ['になら', 'になり', 'になっ', 'になる', 'になれ', 'になれ', 'になろ']
        self.morau = ['もらわ', 'もらい', 'もらっ', 'もらう',  'もらえ', 'もらえ', 'もらお']
        self.kudasaru = ['くださら', 'くださり', 'くださっ','くださる', 'くだされ', 'くだせ', 'くだそ']
        self.narareru = ['になられ', 'になられ', 'になられ', 'になられる', 'になられれ', 'になられ', 'になられよ']
        
        assert len(self.mas) == len(self.itasu) == len(self.suru) == len(self.ori) ==  len(self.nasaru)\
                == len(self.morau) == len(self.kudasaru) == len(self.nasaru) == 7, 'Not The Same Length at init!'
        assert len(self.itadaku) == 14
        
        self.itasu_mas = ['いたし' + mas for mas in self.mas]
        self.sasete_itadaku = ['させて' + itadaku for itadaku in self.itadaku]
        self.sasete_itadaku_mas = ['させて' + 'いただき' + mas for mas in self.mas] + ['させて' + '頂き' + mas for mas in self.mas]
        self.sasete_morau = ['させて' + morau for morau in self.morau]
        self.sasete_morau_mas = ['させて' + 'もらい' + mas for mas in self.mas]
        self.suru_mas = ['し' + mas for mas in self.mas]
        self.itadaku_mas = ['いただき' + mas for mas in  self.mas] + ['頂き' + mas for mas in self.mas]
        
        self.nari_mas = ['になり' + mas for mas in self.mas]
        self.nasaru_mas = ['なさり' + mas for mas in self.mas]
        self.narare_mas = ['になられ' + mas for mas in self.mas]
        self.kudasaru_mas = ['ください' + mas for mas in self.mas] + ['下さい' + mas for mas in self.mas]
        
        self.sonkei_me = self.nari_mas + self.naru + self.nasaru_mas + self.nasaru + \
            self.nasaru_mas + self.narareru + self.suru
        
        self.sonkei_you = self.kudasaru_mas + self.kudasaru 
        
        self.kenzyou_me = self.itasu_mas + self.itasu +  self.itadaku_mas + self.itadaku + self.mas
        
        self.kenzyou_you = self.sasete_itadaku_mas + self.sasete_itadaku + self.sasete_morau_mas + \
            self.sasete_morau
        
        self.freq_dict = {'考':['考え', '考え', '考え', '考え', '考え', '考えろ', '考えよ'],
                          'く': ['くれ', 'くれ', 'くれ', 'くれる', 'くれれ', 'くれ', 'くれよ'],
                          'わか': ['わから', 'わかり', 'わかっ', 'わかる', 'わかれ', 'わかれ', 'わかろ'],
                          '分か': ['分から', '分かり', '分かっ', '分かる', '分かれ', '分かれ', '分かろ'],
                          '読': ['読ま', '読み', '読ん', '読む', '読め', '読め', '読も'],
                          '聞': ['聞か', '聞き', '聞い', '聞く', '聞け', '聞け', '聞こ'],
                          'もら': ['もらわ', 'もらい', 'もらっ', 'もらう', 'もらえ', 'もらえ', 'もらお'],
                          '行': ['行か', '行き', '行っ', '行く', '行け', '行け', '行こ'],
                          '言': ['言わ', '言い', '言っ', '言う', '言え', '言え', '言お'],
                          '伝': ['伝え', '伝え', '伝え', '伝える', '伝えれ', '伝えろ', '伝えよ'],
                          '知': ['知ら', '知り', '知っ', '知る', '知れれ', '知れ', '知ろ'],
                          'い': ['い', 'い', 'い', 'いる', 'いれ', 'いろ', 'いよ'],
                          '見': ['見', '見', '見', '見る', '見れ', '見れ', '見ろ'],
                          '来': ['来', '来', '来', '来る', '来れ', '来い', '来よ'],
                          '面倒を掛け': ['面倒をかけ', '面倒をかけ', '面倒をかけ', '面倒をかける', '面倒をかけれ', '面倒をかけろ', '面倒をかけよ'],
                          '食': ['食べ', '食べ', '食べ', '食べる', '食べれ', '食べろ', '食べよ'],
                          '書': ['書か', '書き', '書い', '書く', '書け', '書け', '書こ'],
                          '座': ['座ら', '座り', '座っ', '座る', '座れれ', '座れ', '座ろ'],
                          '掛': ['掛け', '掛け', '掛け', '掛ける', '掛け', '掛けろ', '掛けよ'],
                          'か': ['かけ', 'かけ', 'かけ', 'かける', 'かけ', 'かけろ', 'かけよ'],
                          '待': ['待た', '待ち', '待っ', '待つ', '待て', '待て', '待と']
                          }
        
        for value in self.freq_dict.values():
            assert len(value) == 7, 'Not The Same Length af Frequent dictionary..'
            
    def convert_keigo2normal(self, line):
        i = 0
        keigo_blocks = list()
        line = self._keigo_exceptions(line)
        res_line = ''
        tokens, positions = self._splitter(line)
        while i < len(tokens):
            token, position = tokens[i], positions[i]
            if (token.startswith('お') or token.startswith('ご') or token.startswith('御')) and token != 'ござい' and token != '御座い':
                if len(token) == 1:
                    i+=1
                    token, position = tokens[i], positions[i]
                    res_line += token
                    if position[0] == '名詞' or position[0] == '動詞':
                        keigo_blocks.append(token)
                    else:
                        pass
                    i+=1
                else:
                    res_line += token
                    keigo_blocks.append(token)
                    i+=1
            elif (position[0] == '名詞' and token != 'ござい' and token != '御座い') and position[4] == 'サ変接続':
                if i+1 <len(tokens) and positions[i+1][4] == '特殊・デス':
                    if tokens[i+1] == 'でし' and i+2<len(tokens) and tokens[i+2] == 'て':
                        res_line += token + 'で'
                        i+=3
                    elif tokens[i+1] == 'でしょ':
                        res_line += token + 'だろ'
                        i+=2
                    elif tokens[i+1] == 'です':
                        res_line += token + 'だ'
                        i+=2
                    else:
                        raise ValueError('Not Desu!{}'.format(token))
                else:
                    keigo_blocks.append(token)
                    res_line += token
                    i+=1
            else:
                if position[0] == '名詞' and  i+1 <len(tokens) and positions[i+1][4] == '特殊・デス':
                    if (tokens[i+1] == 'でし' or tokens[i+1] == 'っし' or tokens[i+1] == 'どし') :
                        if i+2<len(tokens) and tokens[i+2] == 'て':
                            res_line += token + 'で'
                            i+=3
                        elif i+2<len(tokens) and tokens[i+2] == 'た':
                            res_line += token + 'だった'
                            i+=3
                        else:
                            res_line += token
                            i+=1
                    elif tokens[i+1] == 'でしょ'or tokens[i+1] == 'っしょ' or tokens[i+1] == 'どしょ':
                        res_line += token + 'だろ'
                        i+=2
                    elif tokens[i+1] == 'です'or tokens[i+1] == 'っす' or tokens[i+1] == 'どす':
                        res_line += token + 'だ'
                        i+=2
                    else:
                        raise ValueError('Not Desu!{}'.format(token))
                else:
                    res_line += token
                    i+=1
        for block in keigo_blocks:
            res_line = self._build_block(block, res_line)
        res_line = self._last_exceptions(res_line)
        return res_line
    
    def _last_exceptions(self, line):
        exceptions = ['なさ', 'いた', 'お', 'ござい', '御座い', 'くだ', '下']
        for exp in exceptions:
            if exp in line:
                line = self._last_replacer(line, exp)
        tokens, positions = self._splitter(line)
        res_line = ''
        i=0
        while i < len(tokens):
            token, position = tokens[i], positions[i]
            if position[0] == '動詞' and position[5] == '連用形' and i+1 < len(tokens):
                if i+1 < len(tokens) and tokens[i+1] == 'て' or tokens[i+1] == 'で':
                    converted = self.convert_renyou2te(token)
                    if converted.endswith('ん'):
                        res_line += converted + 'で'
                    else:
                        res_line += converted + 'て'
                    i+=2
                elif i+1 < len(tokens) and tokens[i+1] == 'だ' or tokens[i+1] == 'た':
                    converted = self.convert_renyou2te(token)
                    if converted.endswith('ん'):
                        res_line += converted + 'だ'
                    else:
                        res_line += converted + 'た'
                    i+=2
                else:
                    res_line += token
                    i+=1
            else:
                res_line += token
                i+=1
        return res_line
    
    def _last_replacer(self, line, exp):
        if exp == 'なさ':
            nasarare_mas = ['なさられ' + mas for mas in self.mas]
            nasai_mas = ['なさい' + mas for mas in self.mas]
            nasare_mas = ['なされ' + mas for mas in self.mas]
            for src, tgt in zip(nasai_mas + nasarare_mas + nasare_mas + self.nasaru, cycle(self.suru)):
                line = line.replace(src, tgt)
        elif exp == 'いた':
            ita_sare_masu = ['いたされ' + mas for mas in self.mas]
            for src, tgt in zip(ita_sare_masu + self.itasu_mas + self.itasu, cycle(self.suru)):
                line = line.replace(src, tgt)
        elif exp == 'お':
            oru = ['おら', 'おり', 'おっ', 'おる', 'おれ', 'おろ']
            orare_mas = ['おられ' + mas for mas in self.mas]
            ori_mas = ['おり' + mas for mas in self.mas]
            for src, tgt in zip(orare_mas + ori_mas + oru, cycle(self.freq_dict['い'])):
                line = line.replace(src, tgt)
        elif exp == 'ござい' or exp == '御座い':
            if 'でございます' in line or 'で御座います' in line:
                line = line.replace('でございます', 'だ')
                line = line.replace('で御座います', 'だ')
            gozaimas = ['ござい' + mas for mas in self.mas] + ['御座い' + mas for mas in self.mas]
            for src, tgt in zip(gozaimas, cycle(self.suru)):
                line = line.replace(src, tgt)
        elif exp == 'くだ' or exp == '下':
            kudasari_mas = ['くださり' + mas for mas in self.mas] + ['下さり' + mas for mas in self.mas]
            kudasai_mas = ['ください' + mas for mas in self.mas] + ['下さい' + mas for mas in self.mas]
            for src, tgt in zip(kudasari_mas + kudasai_mas, cycle(self.freq_dict['く'])):
                line = line.replace(src, tgt)
        else:
            raise Exception('Not Found at Last Replacer!!!')
        return line
    
    def _keigo_exceptions(self, line):
        exceptions1 = ['いらっしゃい', 'おいで', 'おいとま', '帰られ']
        exceptions2 = ['承知', '頂戴', '拝聴', '拝読', '拝察', '拝見']
        exceptions3 = ['うかが', '伺','申し上げ', '申し伝え', '存じ','おっしゃ', '申', 'いただ', '頂', '賜', '参', '見え', 'お目にかか', 'お手をわずらわ', 'お口になさ']
        for exp in exceptions1:
            if exp in line:
                line = self._exceptions_replacer1(exp, line)
        for exp in exceptions2:
            if exp in line:
                line = self._exceptions_replacer2(exp, line)
        for exp in exceptions3:
            if exp in line:
                line = self._exceptions_replacer3(exp, line)
        return line
                
    def _exceptions_replacer2(self, exception, line):
        base_dict = {'承知': 'わか', '頂戴': 'もら',  '拝聴': '聞', '拝読': '読', '拝察': '考', '拝見': '見'}
        bases = self.freq_dict[base_dict[exception]]
        for addition, base_to in zip(self.kenzyou_me, cycle(bases)):
            line = line.replace(exception + addition, base_to)
        src = bases[2] + 'させて'
        for addition, base_to in zip(self.kenzyou_you, cycle(self.morau)):
            line = line.replace(exception + addition, src + base_to)
        return line
    
    def _exceptions_replacer1(self, exception, line):
        self.exception1_dict = {'いらっしゃ':
                       [('いらっしゃいます','来る'),
                        ('いらっしゃてます', 'います'),
                        ('いらっしゃって', '来て'),
                        ('いらっしゃる', '来る'),
                        ('いらっしゃってる', 'いる')],
                   'おいで':
                        [('おいでになる', '来る'),
                         ('おいでになられる', '来る'),
                         ('おいでになります', '来る'),
                         ('おいでなすった', '来た'),
                         ('おいでなすって', '来てください')],
                   'おいとま':
                        [('おいとまする', '帰る'),
                         ('おいとまさせて', '帰らせて'),
                         ('おいとまして', '帰って')],
                   '帰られ':
                        [('帰られます', '帰る'),
                         ('帰られて', '帰って'),
                         ('帰られる', '帰る')]
                   }
        lists = self.exception1_dict[exception]
        for src, tgt in lists:
            line = line.replace(src, tgt)
    
    def _exceptions_replacer3(self, exception, line):
        self.keigo2normal_dict = {'うかが': '行', '伺': '行', '申し上げ': '言', '申し伝え': '伝え', '存じ上げ': '知', '申': '言', 'おっしゃ': '言',
                                   'いただ': 'もら', '頂': 'もら', '賜': 'もら', '参': '行', '見え': '来', 'お目にかか': '見', 'お手を煩わ': '面倒を掛'
                                  ,'お手をわずらわ': '面倒を掛','お口になさ': '食'}
        self.exception3_dict = {'うかが': ['うかがわ', 'うかがい', 'うかがっ', 'うかがう', 'うかがえ', 'うかがえ','うかがお'],
                                '伺': ['伺わ', '伺い', '伺っ', '伺う', '伺え','うかがえ', '伺お'],
                                '申し上げ': ['申し上げ', '申し上げ', '申し上げ', '申し上げる', '申し上げれ', '申し上げろ','申し上げよ'],
                                '申し伝え': ['申し伝え', '申し伝え', '申し伝え', '申し伝える', '申し伝えれ', '申し伝えろ', '申し伝えよ'],
                                '存じ上げ': ['存じ上げ', '存じ上げ', '存じ上げ', '存じ上げる', '存じ上げれ', '存じ上げろ', '存じ上げよ'],
                                '申': ['申さ', '申し', '申し', '申す', '申せ', '申せ','申そ'],
                                'おっしゃ': ['おっしゃら', 'おっしゃり', 'おっしゃっ', 'おっしゃる', 'おっしゃ', 'おっしゃれ', 'おっしゃろう'],
                                'いただ': ['いただか', 'いただき', 'いただい', 'いただく', 'いただけれ', 'いただこう','いただこう'],
                                '頂': ['頂か', '頂き', '頂い', '頂く', '頂けれ', '頂け', '頂こう'],
                                '賜': ['賜ら', '賜り', '賜っ', '賜る', '賜われ', '賜われ', '賜ろう'],
                                '参': ['参ら', '参り', '参っ', '参る', '参れ', '参れ', '参ろ'],
                                '見え': ['見えられ', '見えられ', '見えられ', '見えられる', '見えられ', '見えられろ', '見えろ'],
                                'お目にかか': ['お目にかから', 'お目にかかり', 'お目にかかっ', 'お目にかかる', 'お目にかかれ', 'お目にかかれ', 'お目にかかろ'],
                                'お手をわずらわ': ['お手をわずらわさ', 'お手をわずらわし', 'お手をわずらわし', 'お手をわずらわす', 'お手をわずらわすれ', 'お手をわずらわせろ', 'お手をわずらわよ'],
                                'お手を煩わ': ['お手をわずらわさ', 'お手をわずらし', 'お手をわずらわし', 'お手をわずらわす', 'お手をわずらわすれ', 'お手をわずらわせろ', 'お手をわずらわせよ'],
                                'お口になさ': ['お口になさら', 'お口になさり', 'お口になさっ', 'お口になさる', 'お口になされ', 'お口になさろ','お口になさろ'],
                                }
        assert  len(self.keigo2normal_dict) == len(self.exception3_dict), 'Not the same len at _exceptions_replacer3'
        for value in self.exception3_dict.values():
            assert len(value) == 7, 'Not the same len at exception3_dict'
        from_list1 = self.exception3_dict[exception]
        from_list2 = [from_list1[2] + mas for mas in self.mas]
        to_list = self.freq_dict[self.keigo2normal_dict[exception]]
        for src, tgt in zip(from_list1 + from_list2, cycle(to_list)):
            line = line.replace(src, tgt)
        return line
    
    def _build_block(self, block, line):
        if block.startswith('お') or block.startswith('御') or block.startswith('ご'):
            strip_block = block[1:]
        else:
            strip_block = block
        try:
            bases = self.freq_dict[strip_block[:-1]]
        except:
            bases = [strip_block + suru for suru in self.suru]
        for addition, base_to in zip(self.sonkei_me, cycle([strip_block])):
            line = line.replace(block+addition, base_to)
        src = strip_block + 'して'
        for addition, base_to in zip(self.sonkei_you, cycle(self.morau)):
            line = line.replace(block + addition, src + base_to)
        for addition, base_to in zip(self.kenzyou_me, cycle(bases)):
            line = line.replace(block + addition, base_to)
        src = bases[2] + 'させて'
        for addition, base_to in zip(self.kenzyou_you, cycle(self.morau)):
            line = line.replace(block + addition, src + base_to)
        line = line.replace(block, strip_block)
        return line
        
    def convert_normal2teinei(self, line):
        line = self.convert_keigo2normal(line)
        return line
        
    def convert_normal2kenzyou(self, line):
        line = self.convert_keigo2normal(line)
        return line
    
    def convert_normal2sonkei(self, line):
        line = self.convert_keigo2normal(line)
        return line
    
    def _splitter(self, line):
        res_tokens, res_positions = list(), list()
        tokens_positions = self.mecab.parse(line).splitlines()
        for t_p in tokens_positions[:-1]:
            tokens, positions_str = t_p.split('\t')
            positions = positions_str.split(',')
            res_tokens.append(tokens)
            res_positions.append(positions)
        return res_tokens, res_positions
        