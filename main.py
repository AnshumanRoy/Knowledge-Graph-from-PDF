# importing relevant libraries
import os
import configparser

from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from neo4j import GraphDatabase

from langchain_core.documents import Document

# reading credentials and setting as environment variables
config = configparser.ConfigParser()
config.read("settings.cfg")

for section in config.sections():
    for key, value in config.items(section):
        os.environ[key] = value

URI = os.environ.get("URI")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

# verifying credentials
AUTH = (USERNAME, PASSWORD)
with GraphDatabase.driver(URI, auth=AUTH) as driver: 
    driver.verify_connectivity()

# initialising graph
graph = Neo4jGraph(url=URI, username=USERNAME, password=PASSWORD)

# initializing graph transformer with llm model
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_transformer = LLMGraphTransformer(llm=llm)

# text for consideration
text = """
"Paradise Lost" by John Milton is an epic poem that delves into the biblical story of the Fall of Man, exploring themes of free will, disobedience, and redemption. Set in both Heaven and Hell, the poem begins with Lucifer and his rebel angels being cast out of Heaven due to their defiance against God. In Hell, Lucifer rallies his followers, vowing to seek revenge against God by corrupting his newest creation, mankind.

Meanwhile, in Heaven, God announces his plan to create Earth and its inhabitants, Adam and Eve. He foresees their eventual fall but allows them free will to choose their actions. Lucifer, now known as Satan, sees this as an opportunity to undermine God's authority. He journeys to Earth and disguises himself as a serpent, tempting Eve to eat the forbidden fruit from the Tree of Knowledge.

Eve succumbs to temptation and shares the fruit with Adam, leading to their expulsion from the Garden of Eden. They experience shame and guilt for their disobedience, realizing the consequences of their actions. As they face the harsh realities of the fallen world, they also find hope in the promise of redemption.

Throughout the poem, Milton explores the complexities of human nature, portraying Adam and Eve as flawed yet capable of growth and redemption. Despite their fall from grace, they demonstrate resilience and a willingness to accept responsibility for their actions.

In the latter part of the poem, Milton shifts focus to the Son of God, who offers himself as a sacrifice to atone for humanity's sins. Through his selfless act, he provides a path to salvation for mankind, offering hope for redemption and reconciliation with God.

"Paradise Lost" is not only a theological work but also a profound exploration of human experience and the struggle between good and evil. Milton's rich language and vivid imagery bring to life the epic battle between Heaven and Hell, while his nuanced portrayal of characters invites readers to contemplate the complexities of morality and divine justice.

In conclusion, "Paradise Lost" is a timeless masterpiece that continues to captivate readers with its profound themes and lyrical beauty. It serves as a testament to the enduring power of literature to explore the depths of the human soul and wrestle with the mysteries of existence.
"""

# converting text to graph
documents = [Document(page_content=text)]
graph_documents = llm_transformer.convert_to_graph_documents(documents)

# printing graph nodes and relationships 
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")

# adding graph to neo4j instance for querying and visualization
graph.add_graph_documents(graph_documents)