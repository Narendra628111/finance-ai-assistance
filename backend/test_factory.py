from backend.services.llm.llm_factory import LLMFactory

llm = LLMFactory.create()

print(type(llm).__name__)