

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
# Start your middleware class
import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class CustomUserAgentMiddleware(UserAgentMiddleware):
    # overwrite process request

    def __init__(self,user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        agentlist = settings.getlist('USER_AGENTS')
        return cls(agentlist)

    def process_request(self, request, spider):
        # Set the location of the proxy
        user_agent = random.choice(self.user_agents)
        if user_agent:
            request.headers.setdefault('User-Agent',user_agent)