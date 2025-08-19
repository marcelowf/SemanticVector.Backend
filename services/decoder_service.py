class DecoderService:
    @staticmethod
    async def decode_embedding(embedding: list[float]):
        return "".join([chr(int(x * 100)) for x in embedding])
