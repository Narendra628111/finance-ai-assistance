import asyncio
from pathlib import Path

from backend.services.document.loader_factory import LoaderFactory


async def main():
    file_path = Path(r"C:\Users\Satish\Downloads\GTT.png")

    print("=" * 80)
    print("FILE:", file_path)
    print("=" * 80)

    # Check factory
    print("Supported:", LoaderFactory.is_supported(file_path))

    # Create loader
    loader = LoaderFactory.get_loader(file_path)

    print("Loader:", loader.__class__.__name__)

    # Extract
    text = await loader.load()

    print("=" * 80)
    print("EXTRACTED TEXT")
    print("=" * 80)
    print(text)
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())