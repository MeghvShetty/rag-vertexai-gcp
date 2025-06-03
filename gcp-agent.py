from configparser import ConfigParser 
from griptape.drivers.prompt.google import GooglePromptDriver
from griptape.drivers.web_search.google import GoogleWebSearchDriver
from griptape.tools import WebSearchTool
from griptape.structures import Agent
from griptape.utils.chat import Chat


config = ConfigParser()
config.read("./secrets.ini")
GOOGLE_API_KEY = config.get("gcp","api_key")
GOOGLE_SEARCH_KEY = config.get("google","search_id")


driver = GoogleWebSearchDriver(
    api_key=GOOGLE_API_KEY,
    search_id = GOOGLE_SEARCH_KEY
)

agent = Agent(
    #How many time has RCB come to finials in IPL ?tools=[WebSearchTool(web_search_driver=driver)],
    prompt_driver=GooglePromptDriver(
        model="gemini-2.0-flash",
        api_key=GOOGLE_API_KEY
    )
)




Chat(agent).start()

