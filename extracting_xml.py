import os
import re
import pandas as pd
from TextSplitting import sent_seg
from time import perf_counter

s = perf_counter()
n = 0
sentences_header = list(str.split(
    """sentence	
    sent.id	
    genre	
    converted.from.file"""))

commands = [
    '&quot;',
    '&quot',
    '<hi rend="it">',
    '</hi>',
    '<hi rend="it">'
]


def flatten(path: str):
    """
    Changing tree structure of directory into flat list
    with one level dirs only
    :param path:
    """

    for item in os.listdir(path):
        item_path = f'{path}/{item}'
        if not os.path.isdir(item_path):
            if 'header.xml' == item:
                yield path

        else:
            yield from flatten(f'{item_path}')


def extract_sent(text: str, filename: str, genre: str) -> list[dict]:
    """
    it has to remove all the commands from text and extract sentence id info
    :param text: has flags from xml file <p xml:id="p-..."> (here is wanted text) </p>
    :param filename
    :param genre
    :return:
    """
    global n
    sent_dic = {i: None for i in sentences_header}
    sent_dic['converted.from.file'] = filename
    sent_dic['genre'] = genre
    res = []
    for command in commands:
        if command in text:
            text = text.replace(command, "")
    sent_id = re.findall('id=".*"', text)[0]
    sent_id = re.findall("\d+", sent_id)[0]
    sent_dic['sent.id'] = sent_id
    text = text.split('>')[1].split('<')[0]

    for sentence in sent_seg(text):
        n += 1
        print(f"{n} sent found")
        cur_sent_dic = sent_dic.copy()
        cur_sent_dic['sentence'] = sentence
        res.append(cur_sent_dic)
    return res


def read_xml(dir_path: str) -> list[dict]:
    """

    :param dir_path:
    :return: dict
    """
    sent_list = []
    files = os.listdir(dir_path)
    if {'header.xml', 'text_structure.xml'}.issubset(files):
        with open(dir_path + '/' + 'header.xml', 'r') as h:
            genre = None
            for line in h.readlines():
                if a := re.findall('channel" target=.*/>', line):
                    b = re.findall('=".*"',a[0])
                    genre = b[0][3:-1]
                    break

        text_pattern = re.compile('^(<p xml).*(</p>)$')
        with open(dir_path + '/' + 'text_structure.xml', 'r') as f:
            file_name = None
            for line in f.readlines():
                if re.match(text_pattern, line):
                    file_name = dir_path.split("/")[-1]

                    sent_list += [extract_sent(text=line,
                                               filename=file_name,
                                               genre=genre)]



    return sent_list


def xml_to_csv(src_path, dest_path):
    """
    :param src_path: path to directory with xml files
    :param dest_path: path, wheere csv will be created
    :return:
    """
    df = pd.DataFrame(columns=sentences_header)
    print(df.columns)
    with open(dest_path, "w") as csv:
        for path in list(flatten(src_path)):
            for row in read_xml(path):
                print(row)
                if row:
                    df = df._append(row[0], ignore_index=True)
                    df.reset_index()
        df.to_csv(csv)


xml_to_csv("/Users/michalek/Downloads/NKJP_300M_sample",
           "/Users/michalek/PycharmProjects/Coordinations/input/300M_NKJP")
print(sent_seg("Brak mi już sił na ul. Sonaty, dr. hab. nie wyleczył mnie."))

e = perf_counter()

print(e-s)