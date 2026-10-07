import asyncio

from backend.services.llm.groq_service import GroqService


async def main():

    llm = GroqService()

    response = await llm.generate_json(
        """
    Return ONLY JSON.

    {
    "name":"Narendra",
    "role":"Software Engineer"
    }
    """
    )


    print("\n" + "=" * 80)
    print(response)
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())