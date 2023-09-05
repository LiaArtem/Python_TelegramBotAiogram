docker network rm telegram-bot-network
docker network create telegram-bot-network
docker network connect telegram-bot-network RedisContainer
docker network connect telegram-bot-network TelegramBotContainer
# docker network inspect telegram-bot-network