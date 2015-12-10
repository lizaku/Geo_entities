#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  stat.py

import codecs, json, re
#import rpy2.robjects as robjects
    
def base_parse(base, type_entity):
    decades = {}
    centuries = {}
    authors = {}
    for fl in base:
        if len(base[fl][type_entity]) > 0:
            ent = 1
        else:
            ent = 0
        if base[fl]['century'] in centuries:
            centuries[base[fl]['century']]['all'] += 1
            centuries[base[fl]['century']]['ent'] += ent
        else:
            centuries[base[fl]['century']] = {'all': 1, 'ent': ent}
            
        if len(base[fl][type_entity]) > 0:
            ent = 1
        else:
            ent = 0
        if base[fl]['decade'] in decades:
            decades[base[fl]['decade']]['all'] += 1
            decades[base[fl]['decade']]['ent'] += ent
        else:
            decades[base[fl]['decade']] = {'all': 1, 'ent': ent}
            
        if len(base[fl][type_entity]) > 0:
            ent = 1
        else:
            ent = 0
        if base[fl]['author'] in authors:
            authors[base[fl]['author']]['all'] += 1
            authors[base[fl]['author']]['ent'] += ent
        else:
            authors[base[fl]['author']] = {'all': 1, 'ent': ent}
    return (centuries, decades, authors)

def extractor(type_entity):
    f = codecs.open('../' + type_entity +'.json', 'r', 'utf-8')
    data = json.load(f)
    f.close()
    f = codecs.open('../file_base.json', 'r', 'utf-8')
    base = json.load(f)
    f.close()
    results = base_parse(base, type_entity)
    separated_data(data, results, type_entity)        

def separated_data(data, base, type_entity):
    ents = ['centuries', 'decades', 'authors']
    for key in ents:
        dec_percent = []
        decades_lst = []
        if key == 'centuries':
            r = base[0]
        elif key == 'decades':
            r = base[1]
        elif key == 'authors':
            r = base[2]
        dic = data[key]
        fw = codecs.open('../prepared_data/rel_data/' + key + '_' + type_entity + '.csv', 'w', 'utf-8')
        for cert in sorted(dic):
            if cert == 'XXI':
                continue
            elif cert == '0':
                continue
            elif re.search('[0-9]{4}', cert):
                if int(cert) > 1940:
                    continue
                dec_percent.append(str((float(r[cert]['ent']) / r[cert]['all']) * 100))
                decades_lst.append(cert)
            fw.write(cert + '\t' + str(r[cert]['all']) + '\t' + str(r[cert]['ent']) + '\t' + str((float(r[cert]['ent']) / r[cert]['all']) * 100) + '\n')
        fw.close()
        if len(dec_percent) > 0:
            fr = codecs.open('../prepared_data/rel_data/' + key + '_' + type_entity + '.R', 'w', 'utf-8')
            fr.write(type_entity + ' <- c(' + ','.join(dec_percent) + ')\n')
            fr.write('decades <- c(' + ','.join(decades_lst) + ')\n')
            fr.close()

def main():
    types = ['cities', 'countries']
    for tp in types:
        extractor(tp)
    return 0

if __name__ == '__main__':
	main()

#robjects.r('dec_years_seq <- c("' + dec_years_seq + '")')
#log10(x) + 1

# for word in sorted(rhyme, key=rhyme.get, reverse=True):
#    val = rhyme[word]
