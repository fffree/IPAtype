#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Program Information
#
__author__ = "Florian Breit"
__contact__ = "Florian Breit <florian.breit.12@ucl.ac.uk>"
__copyright__ = "(c) 2012-2015 Florian Breit"
__license__ = "GNU General Public License, Version 3"
__date__ = "16 Dec 2015"
__version__ = "2.0.0"
__title__ = "IPAtype"

#
# IPA character maps
#
# Symbols used by Latex TIPA package:
#   "0123456789:;@|
#   ABCDEFGHIJKLMNOPQRSTUVWXYZ
#   abcdefghijklmnopqrstuvwxyz
# Symbols used for brackets:
#   []/
# Symbols used specifically by IPAtype:
#   !$%^&*()_+-=
#   {}'~#\<>,.?/
# Symbols used with ALT shortcut:
#   0123456789-=
#   []';#\<>,.?/
#   ABCDGIJKLMNOPQRSTUWXYZ
# Symbols used with CTRL shortcut:
#   0
#   FEVH
IPAchars = {
    #PULMONIC CONSONANTS
    'p' : {'name':'Voiceless bilabial plosive',         'shortcut':'p'},
    'b' : {'name':'Voiced bilabial plosive',            'shortcut':'b'},
    't' : {'name':'Voiceless alveolar plosive',         'shortcut':'t'},
    'd' : {'name':'Voiced alveolar plosive',            'shortcut':'d'},
    'ʈ' : {'name':'Voiceless retroflex plosive',        'shortcut':'Alt+T'},
    'ɖ' : {'name':'Voiced retroflex plosive',           'shortcut':'Alt+D'},
    'c' : {'name':'Voiceless palatal plosive',          'shortcut':'c'},
    'ɟ' : {'name':'Voiced palatal plosive',             'shortcut':'&'},
    'k' : {'name':'Voiceless velar plosive',            'shortcut':'k'},
    'g' : {'name':'Voiced velar plosive',               'shortcut':'g'},
    'q' : {'name':'Voicless uvular plosive',            'shortcut':'q'},
    'ɢ' : {'name':'Voiced uvular plosive',              'shortcut':'Alt+G'},
    'ʔ' : {'name':'Voiceless glottal stop',             'shortcut':'P'},
    'm' : {'name':'Voiced bilabial nasal',              'shortcut':'m'},
    'ɱ' : {'name':'Voiced labiodental nasal',           'shortcut':'M'},
    'n' : {'name':'Voiced alveolar nasal',              'shortcut':'n'},
    'ɳ' : {'name':'Voiced retroflex nasal',             'shortcut':'Alt+M'},
    'ɲ' : {'name':'Voiced palatal nasal',               'shortcut':'Alt+J'},
    'ŋ' : {'name':'Voiced velar nasal',                 'shortcut':'N'},
    'ɴ' : {'name':'Voiced uvular nasal',                'shortcut':'Alt+N'},
    'ʙ' : {'name':'Voiced bilabial trill',              'shortcut':'Alt+B'},
    'r' : {'name':'Voiced alveolar trill',              'shortcut':'r'},
    'ʀ' : {'name':'Voiced uvular trill',                'shortcut':'Alt+R'},
    'ѵ' : {'name':'Voiced labiodental flap',            'shortcut':'Ctrl+W'},
    'ɾ' : {'name':'Voiced alveolar tap',                'shortcut':'R'},
    'ɽ' : {'name':'Voiced retroflex tap',               'shortcut':'Alt+Q'},
    'ɸ' : {'name':'Voiceless bilabial fricative',       'shortcut':'F'},
    'β' : {'name':'Voiced bilabial fricative',          'shortcut':'B'},
    'f' : {'name':'Voiceless labiodental fricative',    'shortcut':'f'},
    'v' : {'name':'Voiced labiodental fricative',       'shortcut':'v'},
    'θ' : {'name':'Voiceless dental fricative',         'shortcut':'T'},
    'ð' : {'name':'Voiced dental fricative',            'shortcut':'D'},
    's' : {'name':'Voiceless alveolar fricative',       'shortcut':'s'},
    'z' : {'name':'Voiced alveolar fricative',          'shortcut':'z'},
    'ʃ' : {'name':'Voiceless postalveolar fricative',   'shortcut':'S'},
    'ʒ' : {'name':'Voiced postalveolar fricative',      'shortcut':'Z'},
    'ʂ' : {'name':'Voiceless retroflex fricative',      'shortcut':'$'},
    'ʐ' : {'name':'Voiced retroflex fricative',         'shortcut':'%'},
    'ç' : {'name':'Voiceless palatal fricative',        'shortcut':'C'},
    'ʝ' : {'name':'Voiced palatal fricative',           'shortcut':'J'},
    'x' : {'name':'Voiceless velar fricative',          'shortcut':'x'},
    'ɣ' : {'name':'Voiced velar fricative',             'shortcut':'G'},
    'χ' : {'name':'Voiceless uvular fricative',         'shortcut':'X'},
    'ʁ' : {'name':'Voiced uvular fricative',            'shortcut':'K'},
    'ħ' : {'name':'Voiceless pharyngeal fricative',     'shortcut':'Ctrl+H'},
    'ʕ' : {'name':'Voiced pharyngeal fricative',        'shortcut':'Q'},
    'h' : {'name':'Voiceless glottal fricative',        'shortcut':'h'},
    'ɦ' : {'name':'Voiced glottal fricative',           'shortcut':'H'},
    'ɬ' : {'name':'Voiceless alveolar lateral fricative', 'shortcut':'Alt+L'},
    'ɮ' : {'name':'Voiced alveolar lateral fricative',  'shortcut':'Alt+Z'},
    'ʋ' : {'name':'Voiced labiodental approximant',     'shortcut':'V'},
    'ɹ' : {'name':'Voiced alveolar approximant',        'shortcut':'Alt+A'},
    'ɻ' : {'name':'Voiced retroflex approximant',       'shortcut':'Alt+\\'},
    'j' : {'name':'Voiced palatal approximant',         'shortcut':'j'},
    'ɰ' : {'name':'Voiced velar approximant',           'shortcut':'Alt+W'},
    'l' : {'name':'Voiced alveolar lateral approximant', 'shortcut':'l'},
    'ɭ' : {'name':'Voiced retroflex lateral approximant', 'shortcut':'Alt+/'},
    'ʎ' : {'name':'Voiced palatal lateral approximant', 'shortcut':'L'},
    'ʟ' : {'name':'Voiced velar lateral approximant',   'shortcut':'Alt+7'},
    #NON-PULMONIC CONSONANTS
    'ʘ' : {'name':'Bilabial click',                     'shortcut':'Alt+0'},
    'ǀ' : {'name':'Dental click',                       'shortcut':'Alt+['},
    'ǃ' : {'name':'(Post)alveolar click',               'shortcut':'!'},
    'ǂ' : {'name':'Palatoalveolar click',               'shortcut':'Alt+3'},
    'ǁ' : {'name':'Alveolar lateral click',             'shortcut':'Alt+]'},
    'ɓ' : {'name':'Voiced bilabial implosive',          'shortcut':'Alt+6'},
    'ɗ' : {'name':'Voiced alveolar implosive',          'shortcut':'Alt+5'},
    'ʄ' : {'name':'Voiced palatal implosive',           'shortcut':'Alt+1'},
    'ɠ' : {'name':'Voiced velar implosive',             'shortcut':'Alt+9'},
    'ʛ' : {'name':'Voiced uvular implosive',            'shortcut':'Alt+4'},
    'ʼ' : {'name':'Ejective diacritic',                 'shortcut':'\''},
    #OTHER SYMBOLS
    'ʍ' : {'name':'Voiceless labial-velar fricative',   'shortcut':'Alt+#'},
    'w' : {'name':'Voiced labial-velar fricative',      'shortcut':'w'},
    'ɥ' : {'name':'Voiced labial-palatal approximant',  'shortcut':'4'},
    'ʜ' : {'name':'Voiceless epiglottal fricative',     'shortcut':'Ctrl+F'},
    'ʢ' : {'name':'Voiced epiglottal fricative',        'shortcut':'Alt+C'},
    'ʡ' : {'name':'Epiglottal plosive',                 'shortcut':'Alt+K'},
    'ɕ' : {'name':'Voiceless alveolo-palatal fricative', 'shortcut':'Alt+S'},
    'ʑ' : {'name':'Voiced alveolo-palatal fricative',   'shortcut':'Alt+X'},
    'ɺ' : {'name':'Voiced alveolar lateral flap',       'shortcut':'Alt+Y'},
    'ɧ' : {'name':'Voiceless palatal-velar fricative',  'shortcut':'Alt+P'},
    #VOWELS
    'i' : {'name':'Close front unrounded vowel',        'shortcut':'i'},
    'y' : {'name':'Close front rounded vowel',          'shortcut':'y'},
    'ɪ' : {'name':'Near-close near-front unrounded vowel', 'shortcut':'I'},
    'ʏ' : {'name':'Near-close near-front rounded vowel', 'shortcut':'Y'},
    'e' : {'name':'Close-mid front unrounded vowel',    'shortcut':'e'},
    'ø' : {'name':'Close-mid front rounded vowel',      'shortcut':'Alt+8'},
    'ɛ' : {'name':'Open-mid front unrounded vowel',     'shortcut':'E'},
    'œ' : {'name':'Open-mid front rounded vowel',       'shortcut':'Alt+I'},
    'æ' : {'name':'Near-open front unrounded vowel',    'shortcut':'Ctrl+E'},
    'a' : {'name':'Open front unrounded vowel',         'shortcut':'a'},
    'ɶ' : {'name':'Open front rounded vowel',           'shortcut':'Alt+O'},
    'ɨ' : {'name':'Close central unrounded vowel',      'shortcut':'1'},
    'ʉ' : {'name':'Close central rounded vowel',        'shortcut':'0'},
    'ɘ' : {'name':'Close-mid central unrounded vowel',  'shortcut':'9'},
    'ɵ' : {'name':'Close-mid central rounded vowel',    'shortcut':'8'},
    'ə' : {'name':'Mid central unrounded vowel',        'shortcut':'@'},
    'ɜ' : {'name':'Open-mid central unrounded vowel',   'shortcut':'3'},
    'ɞ' : {'name':'Open-mid central rounded vowel',     'shortcut':'Alt+U'},
    'ɐ' : {'name':'Near-open central unrounded vowel',  'shortcut':'5'},
    'ɯ' : {'name':'Close back unrounded vowel',         'shortcut':'W'},
    'u' : {'name':'Close back rounded vowel',           'shortcut':'u'},
    'ʊ' : {'name':'Near-close near-back unrounded vowel', 'shortcut':'U'},
    'ɤ' : {'name':'Close-mid back unrounded vowel',     'shortcut':'7'},
    'o' : {'name':'Close-mid back rounded vowel',       'shortcut':'o'},
    'ʌ' : {'name':'Open-mid back unrounded vowel',      'shortcut':'2'},
    'ɔ' : {'name':'Open-mid back rounded vowel',        'shortcut':'O'},
    'ɑ' : {'name':'Open back unrounded vowel',          'shortcut':'A'},
    'ɒ' : {'name':'Open back rounded vowel',            'shortcut':'6'},
    #AFFRICATES
    '◌͡◌': {'name':'Combining inverted double breve above diacritic', 'shortcut':'='},
    '◌͜◌' : {'name':'Combining double breve below diacritic', 'shortcut':'Alt+='},
    'k͡p' : {'name':'Voiceless labial-velar plosive',   'shortcut':''},
    't͜s' : {'name':'Voiceless alveolar affricate',     'shortcut':''},
    #SUPRASEGMENTALS
    'ˈ' : {'name':'Primary stress suprasegmental mark', 'shortcut':'"'},
    'ˌ' : {'name':'Secondary stress suprasegmental mark', 'shortcut':','},
    'ː' : {'name':'Long suprasegmental mark',           'shortcut':':'},
    'ˑ' : {'name':'Half-long suprasegmental mark',      'shortcut':';'},
    '◌̆' : {'name':'Extra-short suprasegmental diacritic', 'shortcut':'Alt+\''},
    '|' : {'name':'Minor (foot) group suprasegmental mark', 'shortcut':'|'},
    '‖' : {'name':'Major (intonation) group suprasegmental mark', 'shortcut':'\\'},
    '.' : {'name':'Syllable break suprasegmental mark', 'shortcut':'.'},
    '‿' : {'name':'Linking (absence of a break) suprasegmental mark', 'shortcut':''},
    #DIACRITICS
    '◌̥' : {'name':'Voiceless diacritic',               'shortcut':'Alt+-'},
    '◌̬' : {'name':'Voiced diacritic',                  'shortcut':''},
    '◌ʰ' : {'name':'Aspirated diacritic',               'shortcut':'^'},
    '◌̹' : {'name':'More rounded diacritic',            'shortcut':')'},
    '◌̜' : {'name':'Less rounded diacritic',            'shortcut':'('},
    '◌̟' : {'name':'Advanced diacritic',                'shortcut':'+'},
    '◌̠' : {'name':'Retracted diacritic',               'shortcut':'_'},
    '◌̈' : {'name':'Centralised diacritic',             'shortcut':''},
    '◌̽' : {'name':'Mid-centralised diacritic',         'shortcut':''},
    '◌̩' : {'name':'Syllabic diacritic',                'shortcut':'Alt+,'},
    '◌̯' : {'name':'Non-syllabic diacritic',            'shortcut':'Alt+.'},
    '◌̤' : {'name':'Breathy voiced diacritic',          'shortcut':'Alt+;'},
    '◌̰' : {'name':'Creaky voiced diacritic',           'shortcut':'Alt+?'},
    '◌̼' : {'name':'Linguolabial diacritic',            'shortcut':''},
    '◌ʷ' : {'name':'Labialized diacritic',              'shortcut':'*'},
    '◌ʲ' : {'name':'Palatalized diacritic',             'shortcut':'#'},
    '◌ˠ' : {'name':'Velarized diacritic',               'shortcut':''},
    '◌ˁ' : {'name':'Pharyngealized diacritic',          'shortcut':'?'},
    '◌̴' : {'name':'Velarized or pharyngealized diacritic', 'shortcut':'-'},
    '◌̝' : {'name':'Raised diacritic',                  'shortcut':''},
    '◌̞' : {'name':'Lowered diacritic',                 'shortcut':''},
    '◌˞' : {'name':'Rhoticity diacritic',               'shortcut':'Alt+2'},
    '◌̪' : {'name':'Dental diacritic',                  'shortcut':'Alt+<'},
    '◌̺' : {'name':'Apical diacritic',                  'shortcut':'Alt+>'},
    '◌̻' : {'name':'Laminal diacritic',                 'shortcut':''},
    '◌̃' : {'name':'Nasalized diacritic',               'shortcut':'~'},
    '◌ⁿ' : {'name':'Nasal release diacritic',           'shortcut':''},
    '◌ˡ' : {'name':'Lateral release diacritic',         'shortcut':''},
    '◌̚' : {'name':'No audible release diacritic',      'shortcut':''},
    '◌̘' : {'name':'Advanced tongue root diacritic',    'shortcut':'}'},
    '◌̙' : {'name':'Retracted tongue root diacritic',   'shortcut':'{'},
    #TONES AND WORD ACCENT
    '◌̋' : {'name':'Extra high level tone diacritic',        'shortcut':''},
    '◌́' : {'name':'High level tone diacritic',         'shortcut':''},
    '◌̄ ' : {'name':'Mid level tone diacritic',         'shortcut':''},
    '◌̀' : {'name':'Low level tone diacritic',          'shortcut':''},
    '◌̏' : {'name':'Extra low level tone diacritic',    'shortcut':''},
    '◌̌' : {'name':'Rising contour tone diacritic',     'shortcut':''},
    '◌̂' : {'name':'Falling contour tone diacritic',    'shortcut':''},
    '◌᷄' : {'name':'High rising contour tone diacritic', 'shortcut':''},
    '◌᷅' : {'name':'Low rising contour tone diacritic', 'shortcut':''},
    '◌᷈' : {'name':'Rising falling contour tone diacritic', 'shortcut':''},
    '˥' : {'name':'Extra high level tone mark',         'shortcut':''},
    '˦' : {'name':'High level tone mark',               'shortcut':''},
    '˧' : {'name':'Mid level tone mark',                'shortcut':''},
    '˨' : {'name':'Low level tone mark',                'shortcut':''},
    '˩' : {'name':'Extra low level tone mark',          'shortcut':''},
    '˩˥' : {'name':'Rising contour tone mark',          'shortcut':''},
    '˥˩' : {'name':'Falling contour tone mark',         'shortcut':''},
    '˦˥' : {'name':'High rising contour tone mark',     'shortcut':''},
    '˩˨' : {'name':'Low rising contour tone mark',      'shortcut':''},
    '˧˦˧' : {'name':'Rising falling contour tone mark', 'shortcut':''},
    '↓' : {'name':'Downstep mark',                      'shortcut':''},
    '↑' : {'name':'Upstep mark',                        'shortcut':''},
    '↗' : {'name':'Global rise mark',                   'shortcut':''},
    '↘' : {'name':'Global fall mark',                   'shortcut':''},
    #EXTRA (Not part of the IPA, but needed)
    '◌' : {'name':'Dotted circle combining placeholder mark', 'shortcut':'Ctrl+0'},
    '/' : {'name':'Forward slash bracket',              'shortcut':'/'},
    '[' : {'name':'Left square bracket',                'shortcut':'['},
    ']' : {'name':'Right square bracket',               'shortcut':']'},
    '〈' : {'name':'Left angle bracket',                 'shortcut':'<'},
    '〉' : {'name':'Right angle bracket',                'shortcut':'>'},
}
# Now let's programatically add a field of the actual character (i.e. remove ◌'s)
for key in IPAchars.keys():
    if key is "◌":
        IPAchars[key]['char'] = "◌"
    else:
        IPAchars[key]['char'] = key.replace("◌", "")
del(key)

#
# Map of IPA shortcut symbols
#
IPAshortcuts = {}
for label, props in IPAchars.items():
    if props['shortcut']:
        if props['shortcut'] in IPAshortcuts:
            print(
                "OH NO! The Shortcut %s is used twice! For %s and for %s"
                % (props['shortcut'], IPAshortcuts[props['shortcut']]['name'], props['name'])
            )
        IPAshortcuts[props['shortcut']] = {
            'label':    label,
            'char':     props['char'],
            'name':     props['name'],
            'shortcut': props['shortcut']
        }
del(label, props)