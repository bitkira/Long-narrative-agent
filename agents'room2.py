import requests
import json
import re

boneapi = "sk-"
boneurl = "https:/v1"
model_keyword = "gpt-4o"

gpt4_config = {"model": model_keyword, "api_key": boneapi, "base_url": boneurl}

shared_scratchpad_template = """[SCRATCHPAD] Format
[Creative Writing Task] <the original writing prompt>
[Central Conflict] <the output of the conflict agent>
[Character Descriptions] <the output of the character agent>
[Setting] <the output of the setting agent>
[Key Plot Points] <the output of the plot agent>
[Exposition] <the output of the exposition agent>
[Rising Action] <the output of the rising action agent>
[Climax] <the output of the climax agent>
[Falling Action] <the output of the falling action agent>
[Resolution] <the output of the resolution agent>
"""

def update_shared_scratchpad(shared_scratchpad, section, content):
    pattern = f"(\[{section}\]) <.*?>"
    replacement = f"\1 {content}"
    updated_scratchpad = re.sub(pattern, replacement, shared_scratchpad, flags=re.DOTALL)
    return updated_scratchpad

def call_llm_api(prompt):
    headers = {
        "Authorization": f"Bearer {boneapi}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_keyword,
        "prompt": prompt,
        "max_tokens": 500
    }
    response = requests.post(boneurl, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""

def run_story_workflow(input_prompt):
    shared_scratchpad = shared_scratchpad_template.replace("<the original writing prompt>", input_prompt)
    sections = [
        ("Central Conflict", "Given [Creative Writing Task], describe the central conflict in detail (more than 5 sentences). The description should answer the following questions:\n⋆ What’s the protagonist’s main goal in this story?\n⋆ Why do they want it?\n⋆ What’s stopping them from achieving it?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Character Descriptions", "Given [Creative Writing Task],[Central Conflict], describe the characters in detailed bullet points (more than 5 sentences for each character). The description should answer the following questions:\n⋆ What do the characters sound like? Are they talkative or quiet? What kind of slang do they use? What is their sense of humor like?\n⋆ What do they look like? Do they have any defining gestures? What’s the first thing people notice about them?\n⋆ What are their motivations and internal characteristics? What are their flaws? What are their values? What are they afraid of? How will they change and grow over the course of this story?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Setting", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions], describe the setting in detail (more than 5 sentences). The description should answer the following questions:\n⋆ Where does the story take place? Is it set in a fictional world, or is it simply set in someone’s backyard?\n⋆ When does the story take place? What decade is it set in? How much time elapses over the course of the story?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Key Plot Points", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting], describe the key plot points in detailed bullet points.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Exposition", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points], continue the story by writing the exposition part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Rising Action", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition], continue the story by writing the rising action part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Climax", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action], continue the story by writing the Climax part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Falling Action", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action],[Climax], continue the story by writing the falling action part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}"),
        ("Resolution", "Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action],[Climax],[Falling Action], continue the story by writing the resolution part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n{{shared_scratchpad}}")
    ]
    
    for section, agent_prompt in sections:
        prompt = shared_scratchpad + f"\n{agent_prompt}"
        # Print debugging information before calling API
        print(f"\n--- Debug: Agent for {section} ---\nPrompt:\n{prompt}\n--- End of Prompt ---\n")
        response = call_llm_api(prompt)
        # Print response for debugging
        print(f"\n--- Debug: Response for {section} ---\nResponse:\n{response}\n--- End of Response ---\n")
        shared_scratchpad = update_shared_scratchpad(shared_scratchpad, section, response)
    return shared_scratchpad

# Read inputs from a JSONL file and run the workflow for specified indices
output_stories = {}
with open('tell-me-a-story-train.jsonl', 'r') as file:
    for line_num, line in enumerate(file, start=1):
        if line_num in [1]:
            input_data = json.loads(line)
            input_prompt = input_data.get("inputs", "")
            if input_prompt:
                output_story = run_story_workflow(input_prompt)
                output_stories[f"Story_{line_num}"] = output_story

# Write the output stories to a JSON file
with open('output_stories.json', 'w') as file:
    json.dump(output_stories, file, indent=4)
