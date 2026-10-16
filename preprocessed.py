
from tempfile import template
import json
import time
import sys
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm
sys.stdout.reconfigure(encoding='utf-8')




def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts =[]
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
            time.sleep(2)


   


    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        currrent_tags = post['tags']
        new_tags = { unified_tags[tag] for tag in currrent_tags}
        post['tags'] = list(new_tags)
    
    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
    unique_tags_list = ','.join(unique_tags)

    

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "AI", "ArtificialIntelligence", "DeepMind" can be all merged into a single tag "Artificial Intelligence". 
       Example 2: "LLM", "KV cache", "Prompt Caching" can be mapped to "Large Language Models"
       Example 3: "WorldModels", "WorldLabs", "ComputerVision" can be mapped to "Computer Vision"
       Example 4: "NVIDIA", "HUAWEI", "Blackwell" etc. can be mapped to "Hardware & Tech"
       Example 5: "Python", "Android", "Software" can be mapped to "Software Development"
    2. Each tag should follow title case convention. example: "Artificial Intelligence", "Large Language Models"
    3. Output should be a JSON object, No preamble
    4. Output should have mapping of original tag and the unified tag. 
       For example: {{"ArtificialIntelligence": "Artificial Intelligence", "AI": "Artificial Intelligence", "LLM": "Large Language Models"}}
    
    Here is the list of tags: 
    {tags}
'''





def extract_metadata(post):
    template = '''

    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Banglish (banglish means bangla + english)


    here is the actual post on which you need to perform this task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain =pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")    
    return res




if __name__=="__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")


