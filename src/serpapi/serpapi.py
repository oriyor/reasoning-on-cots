import hashlib
import os
import json
from typing import Dict


from IPython.utils import io
from serpapi import GoogleSearch

from src.common.config import Config
from src.serpapi.wikipedia import get_wikipedia_text


READ_CACHE = True


def google(question):
    print(f"Asking google: {question}")

    params = {
        "api_key": os.getenv("SERP_API_KEY"),
        "engine": "google",
        "q": question,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }

    with io.capture_output() as captured:  # disables prints from GoogleSearch
        print("hi man what's up?")
        search = GoogleSearch(params)
        res = search.get_dict()

    answer = None
    snippet = None
    title = None

    if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
        answer = res["answer_box"]["answer"]
    if "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
        snippet = res["answer_box"]["snippet"]
        title = res["answer_box"]["title"]
    # elif 'answer_box' in res.keys() and 'snippet_highlighted_words' in res['answer_box'].keys():
    #     toret = res['answer_box']["snippet_highlighted_words"][0]
    elif (
        "answer_box" in res.keys()
        and "contents" in res["answer_box"].keys()
        and "table" in res["answer_box"]["contents"].keys()
    ):
        snippet = res["answer_box"]["contents"]["table"]
        title = res["answer_box"]["title"]
    elif "answer_box" in res.keys() and "list" in res["answer_box"].keys():
        snippet = res["answer_box"]["list"]
        title = res["answer_box"]["title"]
    elif "organic_results" in res and "snippet" in res["organic_results"][0].keys():
        snippet = res["organic_results"][0]["snippet"]
        title = res["organic_results"][0]["title"]
    elif (
        "organic_results" in res
        and "rich_snippet_table" in res["organic_results"][0].keys()
    ):
        snippet = res["organic_results"][0]["rich_snippet_table"]
        title = res["organic_results"][0]["title"]
    else:
        snippet = None
    if snippet is not None:
        title = title.replace("- Wikipedia", "").strip()
        toret = f"{title}: {snippet}"
        toret = f"{toret} So the answer is {answer}." if answer is not None else toret
    else:
        toret = ""
    return [toret, res]


def get_sentences(text, max_num_sentences, reverse=None):
    if text == "":
        return text
    sentences = text.split(". ")
    ret_sentences = ""
    actual_num_sentences = min(max_num_sentences, len(sentences))
    if reverse:
        for i in reversed(range(actual_num_sentences)):
            ret_sentences += f"{sentences[i]}. "
    else:
        for i in range(actual_num_sentences):
            ret_sentences += f"{sentences[i]}. "
    return ret_sentences.strip()


def get_first_sentences(text, max_num_sentences):
    return get_sentences(text, max_num_sentences)


def get_last_sentences(text, max_num_sentences):
    return get_sentences(text, max_num_sentences, reverse=True)


def get_snippet_wiki_paragraph(wikipage_title, snippet):
    full_wikipage_text = get_wikipedia_text(wikipage_title)
    print(f"Wikipedia title: {wikipage_title}")
    print(f"Google snippet: {snippet}")
    try:
        assert snippet in full_wikipage_text
        text_before_snippet, text_after_snippet = full_wikipage_text.split(snippet)
        prev_sentences = get_last_sentences(text_before_snippet, 5).strip()
        next_sentences = get_first_sentences(text_after_snippet, 5).strip()
        return f"{prev_sentences} {snippet} {next_sentences}"
    except AssertionError:
        print("* Unable to find snippet in Wikipedia text, return original snippet.")
    return snippet


def get_question_wiki_snippet(question, cache=None):
    # google_wikipedia_query = f"site:en.wikipedia.org '{question}'"
    try:
        cached_query_results = read_google_res_from_cache(query=question)
        snippet = cached_query_results["snippet"]
        print(f"Read from cache for query: {question}, cached snippet: {snippet}")
    except IOError:
        google_wikipedia_query = (
            f"en.wikipedia.org {question}"  # same as Ori's query format
        )
        snippet, full_results = google(google_wikipedia_query)
        # print(f"full_results: {full_results}")
        # print(f"snippet: {snippet}")
        if cache:
            print(f"Caching snippet: {snippet}")
            cache_google_res(
                question, {"snippet": snippet, "full_results": full_results}
            )
    clean_snippet = snippet.replace("...", "").strip()
    return clean_snippet


def get_question_google_snippet(question, cache=None):
    # google_wikipedia_query = f"site:en.wikipedia.org '{question}'"
    try:
        cached_query_results = read_google_res_from_cache(query=question)
        snippet = cached_query_results["snippet"]
        print(f"Read from cache for query: {question}, cached snippet: {snippet}")
    except IOError:
        google_wikipedia_query = f"{question}"  # same as Ori's query format
        snippet, full_results = google(google_wikipedia_query)
        # print(f"full_results: {full_results}")
        # print(f"snippet: {snippet}")
        if cache:
            print(f"Caching snippet: {snippet}")
            cache_google_res(
                question, {"snippet": snippet, "full_results": full_results}
            )
    clean_snippet = snippet.replace("...", "").strip()
    return clean_snippet


def get_string_hash(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()


def cache_google_res(query: str, res: Dict) -> None:
    """"""
    filename = get_string_hash(query)
    retriever_cache_dir = Config().get("decomposition.retriever_cache_dir")
    with open(f"{retriever_cache_dir}/{filename}.json", "w") as json_file:
        json.dump(res, json_file)
    # with open(f"strategy_qa/google_results_2/{filename}.json", "w") as json_file:
    #     json.dump(res, json_file)


def read_google_res_from_cache(query: str) -> Dict:
    filename = get_string_hash(query)
    retriever_cache_dir = Config().get("decomposition.retriever_cache_dir")
    with open(f"{retriever_cache_dir}/{filename}.json", "r") as f:
        data = json.load(f)
    # with open(f"strategy_qa/google_results_2/{filename}.json", "r") as f:
    #     data = json.load(f)
    return data
