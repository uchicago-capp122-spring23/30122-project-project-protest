##################################################
# Author: Josemaria Macedo Carrillo              #
# Task: Extract JSON files with newspaper data   #
# Last updated: 03-07-23                         #
##################################################

import time
import requests
import json
import os
import calendar
import shutil
from project_protests.query_params import query_lst, from_date, to_date, filters_lst
from project_protests.config import nyt_api_key


begin_date = from_date.replace("-", "")
end_date = to_date.replace("-", "")

def create_dirs(tags = query_lst, filters = filters_lst,
                begin_date = begin_date, end_date = end_date):
    """
    Create directories and all json files from articles that meet query search
        parameters

    Inputs:
        tags (lst): list of tags to look for. The tags to filter for are looked
            in the filter sections defined by the "filters" argument.
        filters (lst): list of filters where to look tags. They can be
            "headline", "lead_paragraph" and/or "body"
        begin_date (str): 8 digits (YYYYMMDD) string that specify the begin date
            or from when to start looking for articles.
        end_date (str): 8 digits (YYYYMMDD) string that specify the end date or
            until when to stop looking for articles.
    """
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_dir, "raw_data")

    # Remove directories and JSON files before creating them again if they
    # already existed
    if os.path.exists(path):
        folders = os.listdir(path)
        folders.remove("nyt_articles.csv")
        for folder in folders:
            shutil.rmtree(os.path.join(path, folder), ignore_errors = True)
    
    begin_year = int(begin_date[:4])
    end_year = int(end_date[:4])
    first_month = 1
    last_month = 12
    
    # We create JSONs for each year and month because the NYT API has a page
    # limit of 200 pages per query search
    for year in range(begin_year, end_year + 1):
        if year == end_year:
            last_month = int(end_date[4:6])

        for month in range(first_month, last_month + 1):
            year_str = str(year)
            month_dir = calendar.month_name[month]
            new_dir = os.path.join(path, year_str, month_dir)
            if os.path.exists(new_dir) == False:
                os.makedirs(new_dir)
            
            month_str = str(month) 
            if len(month_str) == 1:
                month_str = "0" + month_str
            
            _, day = calendar.monthrange(year, month)
            begin_new = year_str + month_str + "01"
            end_new = year_str + month_str + str(day)
            get_json(tags, filters, begin_new, end_new)


def get_json(tags, filters, begin_date, end_date):
    """
    Create json files from articles that meet query search parameters for a
    specific year because of API restrictions with numbers of pages

    Inputs:
        tags (lst): list of tags to look for. The tags to filter for are looked
            in the body, headline and byline of the articles.
        filters (lst): list of filters where to look tags. They can be "headline",
            "lead_paragraph" and/or "body"
        begin_date (str): 8 digits (YYYYMMDD) string that specify the begin date
            or from when to start looking for articles.
        end_date (str): 8 digits (YYYYMMDD) string that specify the end date or
            until when to stop looking for articles.
    """
    year = begin_date[:4]
    month_name = calendar.month_name[int(begin_date[4:6])]
    resp = make_request(tags, filters, begin_date, end_date)
    resp_json = json.loads(resp.text)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_dir, "raw_data", year, month_name,
                            "nyt_0.json")
    
    with open(file_name, "w") as f:
        json.dump(resp_json, f, indent=1)
        f.close()

    # Get number of articles that match our query search parameters
    hits = resp_json["response"]["meta"]["hits"]

    # Get maximum number of pages we can query
    max_pages = int(hits / 10)

    # Query everything and save the jsons
    for page_n in range(1, max_pages + 1):
        page_str = str(page_n)
        resp = make_request(tags, filters, begin_date, end_date, page_str)
        resp_json = json.loads(resp.text)
        name = "nyt_" + page_str + ".json"
        file_name = os.path.join(current_dir, "raw_data", year, month_name,
                                name)
        
        with open(file_name, "w") as f:
            json.dump(resp_json, f, indent=1)
            f.close()


def make_request(tags, filters, begin_date, end_date, page = "0"):
    """
    Make a GET request to the NYT Article Search API with a request delay of 6
        seconds to avoid reaching request limit of 60 requests per minute.

    Inputs:
        tags (lst): list of tags (strings) to look for. The tags to filter for
            are looked in the body, headline and byline of the articles.
        filters (lst): list of filters where to look tags. They can be "headline",
            "lead_paragraph" and/or "body"
        begin_date (str): 8 digits (YYYYMMDD) string that specify the begin date
            or from when to start looking for articles.
        end_date (str): 8 digits (YYYYMMDD) string that specify the end date or
            until when to stop looking for articles.
        page (str): number of page string that states where to look for articles.
    
    Return (Response): API request response with specified query parameters
    """

    url = create_url(tags, filters, begin_date, end_date, page)
    time.sleep(6)
    resp = requests.get(url)

    return resp


def create_url(tags, filters, begin_date, end_date, page):
    """
    Create request url for API based on query search parameters passed to the
        function.
    
    Inputs:
        tags (lst): list of tags (strings) to look for. The tags to filter for
            are looked in the filters defined in the "filters" parameter.
        filters (lst): list of filters where to look tags. They can be "headline",
            "lead_paragraph" and/or "body"
        begin_date (str): 8 digits (YYYYMMDD) string that specify the begin date
            or from when to start looking for articles.
        end_date (str): 8 digits (YYYYMMDD) string that specify the end date or
            until when to stop looking for articles.
        page (str): number of page string that states where to look for articles.

    Return (str): URL string with query to send request to NYT Article Search 
        API
    """

    endpoint = "https://api.nytimes.com/svc/search/v2/articlesearch.json?" 
    tags_copy = tags[:]
    filters_copy = filters[:]

    for i,tag in enumerate(tags_copy):
        tags_copy[i] = "\"" + tag + "\""
    for i, fil in enumerate(filters_copy):
        filters_copy[i] = fil + ":(" + " OR ".join(tags_copy) + ")"
    
    fq = "fq=" + " OR ".join(filters_copy)
    url = endpoint + fq + "&begin_date=" + begin_date + "&end_date=" + end_date +\
            "&page=" + page + "&api-key=" + nyt_api_key

    return url