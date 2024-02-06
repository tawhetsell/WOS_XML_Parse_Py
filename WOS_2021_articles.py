from collections import defaultdict
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import os
import xml.etree.ElementTree as ET
import re
import numpy as np
import gzip

def standardize_country_name(name):
    return re.sub('[^a-zA-Z]', '', name).lower()

def process_single_file(xml_file, tag='Article'):
    print(f"Starting XML parsing for {xml_file}...")
    all_countries = set()
    country_pairs = defaultdict(int)
    ns = {'ns': 'http://clarivate.com/schema/wok5.30/public/FullRecord'}

    try:
        with gzip.open(xml_file, 'rt') as file:
            for event, elem in ET.iterparse(file):
                if elem.tag.endswith('REC'):
                    doctype_elem = elem.find('.//ns:doctype', ns)
                    if doctype_elem is not None and doctype_elem.text == tag:
                        addresses_elem = elem.find('.//ns:addresses', ns)
                        if addresses_elem is not None and int(addresses_elem.attrib.get('count', 0)) > 1:
                            countries = set()
                            for address_name in addresses_elem.findall('ns:address_name', ns):
                                country_elem = address_name.find('./ns:address_spec/ns:country', ns)
                                if country_elem is not None:
                                    country_name = standardize_country_name(country_elem.text)
                                    countries.add(country_name)
                            all_countries.update(countries)
                            for country1 in countries:
                                for country2 in countries:
                                    if country1 != country2:
                                        country_pairs[(country1, country2)] += 1
                    elem.clear()
    except Exception as e:
        print(f"An error occurred during XML parsing: {e}")

    print(f"Finished XML parsing for {xml_file}. Found {len(all_countries)} countries and {len(country_pairs)} country pairs.")
    return all_countries, country_pairs

def process_file_wrapper(xml_file):
    return process_single_file(xml_file, tag="Article")

if __name__ == '__main__':
    print(f"Number of CPUs: {os.cpu_count()}")

    all_countries = set()
    country_pairs = defaultdict(int)

    xml_files = [f'C:/Users/twhetsell3/WOS_XML/ALL_WOS_XML/2021/WR_2021_20230117130043_CORE_{str(i).zfill(4)}.xml.gz' for i in range(1, 32)]

    with ProcessPoolExecutor(max_workers=10) as executor:
        for chunk_countries, chunk_pairs in executor.map(process_file_wrapper, xml_files):
            all_countries.update(chunk_countries)
            for key, value in chunk_pairs.items():
                country_pairs[key] += value

    print(f"Total countries found: {len(all_countries)}")
    print(f"Total country pairs found: {len(country_pairs)}")

    n = len(fuzzy_country_mapping_dict.keys())
    matrix = np.zeros((n, n), dtype=int)

    countries_list = sorted(list(fuzzy_country_mapping_dict.keys()))
    index_mapping = {country: i for i, country in enumerate(countries_list)}

    for (country1, country2), count in country_pairs.items():
        idx1 = index_mapping[country1]
        idx2 = index_mapping[country2]
        matrix[idx1, idx2] += count
        matrix[idx2, idx1] += count

    df = pd.DataFrame(matrix, index=countries_list, columns=countries_list)

    df.to_csv("country_matrix_2021_articles.csv")

