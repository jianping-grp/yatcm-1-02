import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()
import pandas as pd
from compounds.models import SubHerb, Herb, TCMTaxonomy
from compounds.models import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='[%(message)s]',
    filename='/home/jianping/django_test/logs/herb_log.txt',
    filemode='w'
)

def upload_sub_herb(line):
    chinese_name = line['Chinese_source'].strip() if isinstance(line['Chinese_source'], unicode) else None
    # chinese_synonyms = line['Chinese_synonym'] if isinstance(line['Chinese_synonym'], unicode) else None
    pinyin_name = line['pinyin'].strip() if isinstance(line['pinyin'], unicode) else None
    english_name = line['English_source'].strip() if isinstance(line['English_source'], unicode) else None
    latin_name = line['latin_name'].strip() if isinstance(line['latin_name'], unicode) else None
    first_catagory_chinese = line['first_catagory_chinese'].strip() if isinstance(line['first_catagory_chinese'],
                                                                                  unicode) else None
    first_catagory_english = line['first_catagory_english'].strip() if isinstance(line['first_catagory_english'],
                                                                                  unicode) else None
    second_catagory_chinese = line['second_catagory_chinese'].strip() if isinstance(line['second_catagory_chinese'],
                                                                                    unicode) else None
    second_catagory_english = line['second_catagory_english'].strip() if isinstance(line['second_catagory_english'],
                                                                                    unicode) else None
    use_part = line['use_part'].strip() if isinstance(line['use_part'], unicode) else None
    drug_property = line['Properties'].strip() if isinstance(line['Properties'], unicode) else None
    meridians = line['Meridians'].strip() if isinstance(line['Meridians'], unicode) else None
    effect = line['Effect'].strip() if isinstance(line['Effect'], unicode) else None
    indication = line['Indication'].strip() if isinstance(line['Indication'], unicode) else None
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

    herb = Herb.objects.get(sub_herb_link_id=sub_herb_link_id)

    sub_herb, created = SubHerb.objects.get_or_create(
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
        # Chinese_synonyms=chinese_synonyms
    )

    sub_herb.herb = herb
    sub_herb.save()

    if line['taxonomy_id']:
        tax_id = line['taxonomy_id']
    else:
        tax_id = line['tax_first']

    if tax_id and tax_id != '':
        try:
            tax_id = int(float(tax_id))
            # print tax_id
            try:
                taxonomy, created = TCMTaxonomy.objects.get_or_create(taxonomy_id=tax_id)
                # taxonomy.save()
                sub_herb.taxonomy = taxonomy
                sub_herb.save()
            except ObjectDoesNotExist:
                logging.warning("Can not find {} in database".format(tax_id))
            except MultipleObjectsReturned:
                logging.warning("Multiple taxonomy with ID {} find in database".format(tax_id))
        except ValueError:
            logging.debug("{} can not convert to integer".format(tax_id))

if __name__ == '__main__':
    sub_herb_file = '/home/jianping/django_test/yatcm/compounds/data/sub_herb_320.xlsx'
    df = pd.read_excel(sub_herb_file)
    for idx, row in df.iterrows():
        print(idx)
        upload_sub_herb(row)
