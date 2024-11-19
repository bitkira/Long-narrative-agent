
from autogen import AssistantAgent
from autogen import GroupChat
import autogen
boneapi = "sk-CSJZkNSq8XHJoRI0LgzNfhrQmSGAQ8QE9WZlnAyTqoln6yqR"
boneurl = "https://open.api.gu28.top/v1"

gpt4_config = {"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl}



conflict_agent = AssistantAgent(
    name="conflict_agent",
    system_message="""Given <identifiers found in the scratchpad>, describe the central conflict in detail (more
                    than 5 sentences). The description should answer the following questions:
                    ⋆ What’s the protagonist’s main goal in this story?
                    ⋆ Why do they want it?
                    ⋆ What’s stopping them from achieving it?
                    <scratchpad>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

character_agent = AssistantAgent(
    name="character_agent",
    system_message="""Given <identifiers found in the scratchpad>, describe the characters in detailed bullet points
                        (more than 5 sentences for each character). The description should answer the following
                        questions:
                        ⋆ What do the characters sound like? Are they talkative or quiet? What kind of slang
                        do they use? What is their sense of humor like?
                        ⋆ What do they look like? Do they have any defining gestures? What’s the first thing
                        people notice about them?
                        ⋆ What are their motivations and internal characteristics? What are their flaws? What
                        are their values? What are they afraid of? How will they change and grow over the
                        course of this story?
                        <scratchpad>
                    """,
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

setting_agent = AssistantAgent(
    name="setting_agent",
    system_message="""Given <identifiers found in the scratchpad>, describe the setting in detail (more than 5
                        sentences). The description should answer the following questions:
                        ⋆ Where does the story take place? Is it set in a fictional world, or is it simply set in
                        someone’s backyard?
                        ⋆ When does the story take place? What decade is it set in? How much time elapses
                        over the course of the story?
                        <scratchpad>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

plot_agent = AssistantAgent(
    name="plot_agent",
    system_message="""Given <identifiers found in the scratchpad>, describe the key plot points in detailed bullet
                        points. <scratchpad>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

#writing agents
section_agent = AssistantAgent(
    name="section_agent",
    system_message="""Given <identifiers found in the scratchpad>, continue the story by writing the <section>part.
                    <If previous sections have been written, include the following in the prompt:>
                    Begin your portion of the story in a way that naturally flows from the previous ending.
                    Match the writing style, vocabulary, and overall mood of the existing text. Do not
                    re-explain details or events that have already been described.
                    <If this is not the meant to be the last section, include the following in the prompt:>
                    Focus only on the <section> part of the story. Do not write about the following parts of the
                    story. Do not end the story.
                    <scratchpad>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

finalizer_agent = AssistantAgent(
    name="finalizer_agent",
    system_message="""Given <identifiers found in the scratchpad>, write a story using the information below.
                    <scratchpad>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

synthetic_agent = AssistantAgent(
    name="synthetic_agent",
    system_message="""Split the following story into sections:
                        ⋆ [Exposition]: The exposition gives the reader the background info they need to
                        jump right into the story’s world. This is often found towards the beginning of the
                        story.
                        ⋆ [Rising Action]: The rising action is the moments in the story that lead up to the
                        climax — choices the main characters have made and the events happening that
                        are at odds with the characters’ goals. This is where the story builds and the reader
                        begins to invest in the characters.
                        ⋆ [Climax]: The climax is the primary turning point and what the story has been
                        building towards.
                        ⋆ [Falling Action]: The falling action is the period of time in a story that follows the
                        climax and leads to the resolution. It can be used to clarify the events of the
                        climax, ease any built-up tension, or wrap up loose ends.
                        ⋆ [Resolution]: This is the end of the story. It answers the remaining unanswered
                        questions in the plot. The resolution is also the time to show the next step in the
                        characters’ lives.
                        For each section, give the section header (marked as [Exposition], [Rising Action],
                        [Climax], [Falling Action], and [Resolution]) followed by the first sentence of that section,
                        copied exactly from the story.
                        [User-Written Response] <the gold output>""",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": boneapi,"base_url":boneurl }]},
    human_input_mode="NEVER",
)

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

planning_group_chat = GroupChat(
    agents=[conflict_agent, character_agent, setting_agent, plot_agent,user_proxy],
    messages=[],
    max_round=50,
    send_introductions=True,
)

writing_group_chat = GroupChat(
    agents=[section_agent, finalizer_agent,user_proxy],
    messages=[],
    max_round=50,
    send_introductions=True,
)

planning_manager = autogen.GroupChatManager(groupchat=planning_group_chat, llm_config=gpt4_config)

writing_manager = autogen.GroupChatManager(groupchat=writing_group_chat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    planning_manager,
    message="""
Write a short story about a myth or legend being fulfilled in an unusual or unexpected way, or even cleverly bypassed. The story
should be between 1,200 and 1,300 words. It should take place during the Covid-19 pandemic in Europe. The narrative should
involve vampires. The genre should be comedic horror. The story should contain visuals of a medieval castle and of a modern
European town. It should occur at night. The narrative should also contain situations where one character does not understand the
other character’s perspective. The story should end with the vampires surviving to prey on human victims in the near future.
""",
)