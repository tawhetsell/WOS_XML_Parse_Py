# WOS_XML_Parse_Py
Python script for parsing WOS XML files

The WOS_2021_articles.py script parses the WOS XML files for the year 2021 and generates a matrix where the rows and columns are countries and the cell values are the frequency of country co-occurence in the author affiliations of a WOS record, specifically articles. Such a matrix represents the international collaboration network for the year 2021. The process can be iterated across years in order to produce longitudinal network data from WOS XML data.  

The WOS_2021_articles_disambiguation.py script disambiguates the names of the locations and standardizes the names as three letter ISO codes. 

The scripts were produced iteratively using GPT-4.
