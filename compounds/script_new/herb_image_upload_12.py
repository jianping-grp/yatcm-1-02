import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()
import xlrd
import pandas as pd
from compounds.models import *
from django.core.files import File

base_dir = '/home/jianping/django_test/yatcm'
herb_image_dir = os.path.join(base_dir, 'media_1', 'herb_images')

def upload_herb_image(line):
    # print type(line['use_part'])
    # print type(line['related_id'])
    chinese_name = line['Chinese_source'].strip() if isinstance(line['Chinese_source'], unicode) else None
    chinese_synonyms = line['Chinese_synonym'] if isinstance(line['Chinese_synonym'], unicode) else None
    pinyin_name = line['pinyin'].strip() if isinstance(line['pinyin'], unicode) else None
    english_name = line['English_source'].strip() if isinstance(line['English_source'], unicode) else None
    latin_name = line['latin_name'].strip() if isinstance(line['latin_name'], unicode) else None
    first_catagory_chinese = line['first_catagory_chinese'].strip() if isinstance(line['first_catagory_chinese'], unicode) else None
    first_catagory_english = line['first_catagory_english'].strip() if isinstance(line['first_catagory_english'], unicode) else None
    second_catagory_chinese = line['second_catagory_chinese'].strip() if isinstance(line['second_catagory_chinese'], unicode) else None
    second_catagory_english = line['second_catagory_english'].strip() if isinstance(line['second_catagory_english'], unicode) else None
    use_part = line['use_part'].strip() if isinstance(line['use_part'], unicode) else None
    drug_property = line['Properties'].strip() if isinstance(line['Properties'], unicode) else None
    meridians = line['Meridians'].strip() if isinstance(line['Meridians'], unicode) else None
    effect = line['Effect'].strip() if isinstance(line['Effect'], unicode) else None
    indication = line['Indication'].strip() if isinstance(line['Indication'], unicode) else None
    image_dir = line['Location'].strip() if isinstance(line['Location'],unicode) else None
    # suffix = line['suffix'].strip() if isinstance(line['suffix'], unicode) else None
    herb_image_fix_name = line['pic_map_chinese_name'] if isinstance(line['pic_map_chinese_name'], unicode) else None
    # wiki_english = line['English_wiki'].strip() if isinstance(line['English_wiki'], unicode) else None
    if isinstance(line['English_wiki'], unicode):
        wiki_english = line['English_wiki']
    elif isinstance(line['wiki_first'], unicode):
        wiki_english = line['wiki_first']
    else:
        wiki_english = None

    wiki_chinese = line['Chinese_wiki'].strip() if isinstance(line['Chinese_wiki'], unicode) else None
    # related_id = line['related_id'] if isinstance(int(line['related_id']), int) else None  ### Maybe these herbs belong to the same class, Family)
    try:
        int(line['related_id'])
        related_id = int(line['related_id'])
    except:
        related_id = None

    ### among herbs, there are some different use part,they are different, but belong to same herb
    try:
        sub_herb_link_id = int(line['sub_herb_link_id'])
    except:
        sub_herb_link_id = None


    if image_dir:
        suffix = image_dir.split('.')[1]
        if herb_image_fix_name:
            try:
                image_name = herb_image_fix_name + '-*-' + english_name + '.' + suffix
            except:
                image_name = herb_image_fix_name + '.' + suffix
        else:
            if chinese_name:
                try:
                    image_name = chinese_name + '-*-' + english_name + '.' + suffix
                except:
                    image_name = chinese_name + '.' + suffix
            else:
                image_name = english_name + '.' + suffix

        # print image_name

        herb = Herb.objects.get(
            Chinese_name=chinese_name,
            pinyin_name=pinyin_name,
            English_name=english_name,
            latin_name=latin_name,
            first_catagory_chinese=first_catagory_chinese,
            first_catagory_english=first_catagory_english,
            second_catagory_chinese=second_catagory_chinese,
            second_catagory_english=second_catagory_english,
            use_part=use_part,
            effect=effect,
            indication=indication,
            meridians=meridians,
            drug_property=drug_property,
            related_id=related_id,
            sub_herb_link_id=sub_herb_link_id,
            wiki_chinese=wiki_chinese,
            wiki_english=wiki_english,
            Chinese_synonyms=chinese_synonyms

        )

        img = File(open(image_dir))
        herb.image.save(image_name, img)
        herb.save()

if __name__ == '__main__':
    herb_file = '/home/jianping/django_test/yatcm/compounds/data/herb_6220.xlsx'
    df = pd.read_excel(herb_file)
    for idx, row in df.iterrows():
        print idx
        upload_herb_image(row)


