import configparser
import os
import re
import subprocess
import sys

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
INKSCAPE_PATH = config['DEFAULT']['InkscapePath']

def replace_text(target_doc, target_str, replace_str, id_str):
    pattern = '''id="''' + id_str + '''".+?>''' + target_str + '''<.+?</text>'''
    result = re.search(pattern, target_doc, re.S)
    id_trim_str = target_doc[result.span()[0]: result.span()[1]]

    pattern2 = ">" + target_str + "<"
    result2 = re.search(pattern2, id_trim_str, re.S)

    index_s, index_e = result.span()[0] + result2.span()[0] + 1, result.span()[0] + result2.span()[1] - 1
    target_doc_new = target_doc[:index_s] + replace_str + target_doc[index_e:]

    return target_doc_new

def replace_color(target_doc, replace_rgb, id_str):
    pattern = '''<rect.*?/>'''
    result = re.findall(pattern, target_doc, re.S)

    result_trim = ""
    for i in result:
        if id_str in i:
            result_trim = i

    result2 = re.search(result_trim, target_doc, re.S)
    tmp_trim_txt = target_doc[result2.span()[0]:result2.span()[1]]

    pattern2 = '''fill:#'''
    result3 = re.search(pattern2, tmp_trim_txt, re.S)

    index_s, index_e = result2.span()[0] + result3.span()[1], result2.span()[0] + result3.span()[1] + 6

    target_doc_new = target_doc[:index_s] + replace_rgb + target_doc[index_e:]

    return target_doc_new


def replace_blank(target_doc, replace_alpha, id_str):
    pattern = '''<rect.*?/>'''
    result = re.findall(pattern, target_doc, re.S)

    result_trim = ""
    for i in result:
        if id_str in i:
            result_trim = i

    result2 = re.search(result_trim, target_doc, re.S)
    tmp_trim_txt = target_doc[result2.span()[0]:result2.span()[1]]

    pattern2 = '''fill-opacity:'''
    result3 = re.search(pattern2, tmp_trim_txt, re.S)

    index_s, index_e = result2.span()[0] + result3.span()[1], result2.span()[0] + result3.span()[1] + 3
    # print(target_doc[index_s:index_e])
    target_doc_new = target_doc[:index_s] + str(replace_alpha) + target_doc[index_e:]
    # print(target_doc_new[index_s:index_s+10])

    return target_doc_new


day_ref_set = set([i for i in range(1,31+1,1)])


'''
年、月、日、曜日、何の日、上書き色、何週目
2019,01,01,MON,New Year's Day,#ffb6c1,1
2019,01,02,TUE,2nd,#add8e6,1
2019,01,03,WED,3rd,,2
'''

WEEK_NUM_COLOR = ["#000000",
                "#8b4513",
                "#cd5c5c",
                "#ff8c00",
                "#ffd700",
                "#006400",
                "#4169e1",
                "#9400d3",
                "#808080"]

# read_list_a_month=[[2020,1,1,"MON","New Year's Day","#ffb6c1",1],
# [2020,1,2,"TUE","2nd","#add8e6",1],
# [2020,1,3,"WED","3rd","",2]]


with open('contents.csv', encoding='utf-8') as f:
    read_tmp = f.read()
read_list = [i.split(',') for i in read_tmp.split('\n') if len(i)>0]
read_list = read_list[1:]

with open("template.svg", encoding='utf-8') as f:
    target_doc = f.read()

with open("template_cutline.svg", encoding='utf-8') as f:
    target_doc_cutline = f.read()

export_dir_str = "./export_svg/"



# MONTH_HEADER,01
# YEAR_HEADER,2020
# DAY_01L-31L,33
# DOW_01L-31L,Sun
# DAY_WNUM_01L-31L,01
# DAY_OF_NAME_01-31,DAY_OF_NAME
# day_rect_01L

# DAY_01R-31L,33
# DOW_01R-31L,Sun
# day_rect_01R

#["p1o", "p2o", "p3o", "p4o", "p5o", "p6o", "p7o", "p1u", "p2u", "p3u", "p4u", "p5u", "p6u", "p7u"]


write_svg_filename_list = []
for iii in zip([1, 2, 3, 4, 5, 6, 7, -1, 0, 12, 11, 10, 9, 8], [0, 12, 11, 10, 9, 8, 7, -1, 1, 2, 3, 4, 5, 6],
               ["2", "4", "6", "8", "10", "12", "14", "1", "3", "5", "7", "9", "11", "13"]):

    # 断ち切り線ページ #
    if iii[0] == -1 and iii[1] == -1:
        target_doc_new = target_doc_cutline
        write_svg_filename = export_dir_str + iii[2] + ".svg"
        write_svg_filename_list.append(write_svg_filename)
        with open(write_svg_filename, mode='w', encoding='utf-8') as f:
            f.write(target_doc_new)
        continue
    else:
        target_doc_new = target_doc

    # 左ページ #
    left_month = iii[0]

    if left_month == 0:
        id_str, replace_alpha = "RECT_BLANK_L", 1
        target_doc_new = replace_blank(target_doc_new, replace_alpha, id_str)

    else:
        id_str, replace_alpha = "RECT_BLANK_L", 0
        target_doc_new = replace_blank(target_doc_new, replace_alpha, id_str)

        left_month = str(left_month)
        read_list_a_month = [rline for rline in read_list if rline[1] == left_month]

        READ_YEAR = read_list_a_month[0][0]
        READ_MONTH = read_list_a_month[0][1]

        # 年月
        year_str = str(READ_YEAR).rjust(4, '0')
        id_str, target_str, replace_str = "YEAR_HEADER", "2020", year_str
        target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)  # target_doc

        month_str = str(READ_MONTH).rjust(2, '0')
        id_str, target_str, replace_str = "MONTH_HEADER", "01", month_str
        target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

        # 日の色（交互） 初期化
        for i in range(1, 31, 1):
            day_str = str(i).rjust(2, '0')
            if i % 2 == 0:  # 偶数
                id_str, replace_rgb = "day_rect_" + day_str + "L", "FFFFFF"
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)
            else:  # 奇数
                id_str, replace_rgb = "day_rect_" + day_str + "L", "FFFFFF"
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

        for yi, mi, di, dowi, dnamei, dcolori, wnumi, tmp1, tmp2, tmp3 in read_list_a_month:
            day_str = str(di).rjust(2, '0')
            id_str, target_str, replace_str = "DAY_" + day_str + "L", "33", day_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_week_str = dowi
            id_str, target_str, replace_str = "DOW_" + day_str + "L", "Sun", day_of_week_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_name_str = dnamei
            id_str, target_str, replace_str = "DAY_OF_NAME_" + day_str, "DAY_OF_NAME", day_of_name_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            week_num_str = wnumi
            id_str, target_str, replace_str = "DAY_WNUM_" + day_str + "L", "01", week_num_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            if len(dcolori) == 6:
                id_str, replace_rgb = "day_rect_" + day_str + "L", dcolori
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

        # その月に存在しない日の処理
        day_list = [int(di) for yi, mi, di, dowi, dnamei, dcolori, wnumi, tmp1, tmp2, tmp3 in read_list_a_month]
        day_list_diff = sorted(list(day_ref_set - set(day_list)))  # その月に存在しない日のリスト
        for ddiff in day_list_diff:
            day_str = str(ddiff).rjust(2, '0')
            id_str, target_str, replace_str = "DAY_" + day_str + "L", "33", ""
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_week_str = ''
            id_str, target_str, replace_str = "DOW_" + day_str + "L", "Sun", day_of_week_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_name_str = ''
            id_str, target_str, replace_str = "DAY_OF_NAME_" + day_str, "DAY_OF_NAME", day_of_name_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            week_num_str = ""
            id_str, target_str, replace_str = "DAY_WNUM_" + day_str + "L", "01", week_num_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            id_str, replace_rgb = "day_rect_" + day_str + "L", "CCCCCC"
            target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

    # 右ページ #
    right_month = iii[1]

    if right_month == 0:
        id_str, replace_alpha = "RECT_BLANK_R", 1
        target_doc_new = replace_blank(target_doc_new, replace_alpha, id_str)

    else:
        id_str, replace_alpha = "RECT_BLANK_R", 0
        target_doc_new = replace_blank(target_doc_new, replace_alpha, id_str)

        right_month = str(right_month)
        read_list_a_month = [rline for rline in read_list if rline[1] == right_month]

        READ_YEAR = read_list_a_month[0][0]
        READ_MONTH = read_list_a_month[0][1]

        # 日の色（交互） 初期化
        for i in range(1, 31, 1):
            day_str = str(i).rjust(2, '0')
            if i % 2 == 0:  # 偶数
                id_str, replace_rgb = "day_rect_" + day_str + "R", "FFFFFF"
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)  # target_doc_new
            else:  # 奇数
                id_str, replace_rgb = "day_rect_" + day_str + "R", "FFFFFF"
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

        for yi, mi, di, dowi, dnamei, dcolori, wnumi, tmp1, tmp2, tmp3 in read_list_a_month:
            day_str = str(di).rjust(2, '0')
            id_str, target_str, replace_str = "DAY_" + day_str + "R", "33", day_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_week_str = dowi
            id_str, target_str, replace_str = "DOW_" + day_str + "R", "Sun", day_of_week_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            if len(dcolori) == 6:
                id_str, replace_rgb = "day_rect_" + day_str + "R", dcolori
                target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

        # その月に存在しない日の処理
        day_list = [int(di) for yi, mi, di, dowi, dnamei, dcolori, wnumi, tmp1, tmp2, tmp3 in read_list_a_month]
        day_list_diff = sorted(list(day_ref_set - set(day_list)))  # その月に存在しない日のリスト
        for ddiff in day_list_diff:
            day_str = str(ddiff).rjust(2, '0')
            id_str, target_str, replace_str = "DAY_" + day_str + "R", "33", ""
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            day_of_week_str = ''
            id_str, target_str, replace_str = "DOW_" + day_str + "R", "Sun", day_of_week_str
            target_doc_new = replace_text(target_doc_new, target_str, replace_str, id_str)

            id_str, replace_rgb = "day_rect_" + day_str + "R", "CCCCCC"
            target_doc_new = replace_color(target_doc_new, replace_rgb, id_str)

    write_svg_filename = export_dir_str + iii[2] + ".svg"
    write_svg_filename_list.append(write_svg_filename)
    with open(write_svg_filename, mode='w', encoding='utf-8') as f:
        f.write(target_doc_new)

for fnamei in sorted(write_svg_filename_list):
    basename_without_ext = os.path.splitext(os.path.basename(fnamei))[0]
    export_pdf_filename = ".\\export_pdf\\{0}.pdf".format(basename_without_ext)
    print(fnamei,'->',export_pdf_filename)
    cmd = '''"{0}" -f {1} -A {2}'''.format(INKSCAPE_PATH,fnamei,export_pdf_filename)
    e = subprocess.call(cmd, shell=True)

sys.exit(0)