import openai
import json
import os
# 设置 OpenAI API 密钥
client = openai.OpenAI(api_key="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",
                       base_url="https://openrouter.ai/api/v1")

# 读取 jsonl 文件中的数据
def load_jsonl(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f]
    else:
        raise ValueError(f"Provided path '{file_path}' is not a file. Please provide a valid jsonl file.")

# 保存生成的故事到单独的文件
def save_story(story, story_id, output_dir,model):
    model = model.replace("anthropic/", "")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, f"story_{story_id}_{model}.txt"), 'w', encoding='utf-8') as f:
        f.write(story)

# 使用 OpenAI API 获取故事生成回复
def get_response_from_agent(prompt,model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=5000,
    )
    return response.choices[0].message.content

# 处理每个输入并生成故事
def generate_stories_from_jsonl(jsonl_path, output_dir,model):
    data = load_jsonl(jsonl_path)
    selected_indices = [1, 25, 50, 75, 100]
    
    for index in selected_indices:
        if index < len(data):
            item = data[index]
            input_text = item["inputs"]
            story_id = item["example_id"]

            # 初始化 shared_scratchpad
            shared_scratchpad = f"""[SCRATCHPAD] Format
[Creative Writing Task] {input_text}
[Central Conflict] <the output of the Central Conflict>
[Character Descriptions] <the output of the Character Descriptions>
[Setting] <the output of the Setting>
[Key Plot Points] <the output of the Key Plot Points>
[Exposition] <the output of the Exposition>
[Rising Action] <the output of the Rising Action>
[Climax] <the output of the Climax>
[Falling Action] <the output of the Falling Action>
[Resolution] <the output of the Resolution>
"""

            # 定义智能体的身份信息和对应提示词
            agents = [
                ("Central Conflict", f"Given [Creative Writing Task], describe the central conflict in detail (more than 5 sentences). The description should answer the following questions:\n⋆ What’s the protagonist’s main goal in this story?\n⋆ Why do they want it?\n⋆ What’s stopping them from achieving it?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Character Descriptions", f"Given [Creative Writing Task],[Central Conflict], describe the characters in detailed bullet points (more than 5 sentences for each character). The description should answer the following questions:\n⋆ What do the characters sound like? Are they talkative or quiet? What kind of slang do they use? What is their sense of humor like?\n⋆ What do they look like? Do they have any defining gestures? What’s the first thing people notice about them?\n⋆ What are their motivations and internal characteristics? What are their flaws? What are their values? What are they afraid of? How will they change and grow over the course of this story?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Setting", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions], describe the setting in detail (more than 5 sentences). The description should answer the following questions:\n⋆ Where does the story take place? Is it set in a fictional world, or is it simply set in someone’s backyard?\n⋆ When does the story take place? What decade is it set in? How much time elapses over the course of the story?\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Key Plot Points", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting], describe the key plot points in detailed bullet points.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Exposition", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points], continue the story by writing the exposition part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Rising Action", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition], continue the story by writing the rising action part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Climax", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action], continue the story by writing the Climax part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Falling Action", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action],[Climax], continue the story by writing the falling action part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("Resolution", f"Given [Creative Writing Task],[Central Conflict],[Character Descriptions],[Setting],[Key Plot Points],[Exposition],[Rising Action],[Climax],[Falling Action], continue the story by writing the resolution part.\nBegin your portion of the story in a way that naturally flows from the previous ending.\nMatch the writing style, vocabulary, and overall mood of the existing text. Do not re-explain details or events that have already been described.\nBased on the provided shared_scratchpad, only return the part you are responsible for, and do not answer any other content. For example: As an XX agent, based on the task prompt words and the existing shared shared_scratchpad information, return the XX content you need to be responsible for in the shared shared_scratchpad.\n"),
                ("finalizer", f"Given <identifiers found in the scratchpad>, write a story using the information below."),
            
            
            ]

            # 依次调用每个智能体生成故事部分
            for role, agent_prompt in agents:
                prompt = agent_prompt + "\n" + shared_scratchpad
                agent_response = get_response_from_agent(prompt,model)
                if role == "finalizer":
                    
                    shared_scratchpad = shared_scratchpad + agent_response
                else:
                    
                    shared_scratchpad = shared_scratchpad.replace(f"<the output of the {role}>", agent_response)
            print(shared_scratchpad)
            # 保存故事到文件
            save_story(shared_scratchpad, story_id, output_dir,model)

# 主函数
if __name__ == "__main__":
    jsonl_path =  "/home/zhaoxu/Desktop/ucbagent/test/tellmeastory/tell-me-a-story-train.jsonl"
    output_dir = "/home/zhaoxu/Desktop/ucbagent/test"
    model = ["anthropic/claude-3.5-sonnet"]
    for each in model:
        generate_stories_from_jsonl(jsonl_path, output_dir,each)
