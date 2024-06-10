import os

from async_lru import alru_cache
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport



# Загружаем GraphQL-запросы один раз при запуске приложения
with open(os.path.join(os.path.dirname(__file__), 'gql', 'senkuro', 'SearchTitles.gql'), 'r', encoding='utf-8') as f:
    SEARCH_TITLES_QUERY = f.read()
with open(os.path.join(os.path.dirname(__file__), 'gql', 'senkuro', 'InfoTitle.gql'), 'r', encoding='utf-8') as f:
    INFO_TITLE_QUERY = f.read()
with open(os.path.join(os.path.dirname(__file__), 'gql', 'senkuro', 'ChaptersTitle.gql'), 'r', encoding='utf-8') as f:
    CHAPTERS_TITLE_QUERY = f.read()
with open(os.path.join(os.path.dirname(__file__), 'gql', 'senkuro', 'ImagesTitle.gql'), 'r', encoding='utf-8') as f:
    IMAGES_TITLE_QUERY = f.read()

URL = "https://api.senkuro.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

transport = AIOHTTPTransport(url=URL, headers=HEADERS)
client = Client(transport=transport, fetch_schema_from_transport=False)


@alru_cache(maxsize=1000, ttl=43200)
async def get_manga_cache(slug: str) -> dict:
    """Возвращает информацию о манге из кеша или делает запрос, если ее там нет."""
    manga = await info_title(slug)
    return manga['manga']


@alru_cache(maxsize=1000, ttl=43200)
async def search_manga(slug: str) -> dict:
    """Ищет мангу по названию."""
    query = gql(SEARCH_TITLES_QUERY)
    return await client.execute_async(query, variable_values={'query': slug})


@alru_cache(maxsize=1000, ttl=43200)
async def info_title(slug: str) -> dict:
    """Возвращает подробную информацию о манге."""
    query = gql(INFO_TITLE_QUERY)
    return await client.execute_async(query, variable_values={'slug': slug})


async def chapters_title(slug: str) -> dict:
    """Возвращает список глав манги."""
    query = gql(CHAPTERS_TITLE_QUERY)
    
    manga_data = await get_manga_cache(slug)
    branch_id = manga_data['branches'][0]['id']

    chapters_list = []
    last_cursor = None
    has_next_page = True

    while has_next_page:
        variable_values = {"branchId": branch_id, "after": last_cursor, "first": 100}
        response = await client.execute_async(query, variable_values=variable_values)
        if response:
            page_info = response['mangaChapters']['pageInfo']
            last_cursor = page_info['endCursor']
            has_next_page = page_info['hasNextPage']
            chapters_list.extend(
                [{'slug': chapter['node']['slug'], 'id': chapter['node']['id'], 'number': chapter['node']['number'],
                  'volume': chapter['node']['volume'], 'name': chapter['node']['name']}
                 for chapter in response['mangaChapters']['edges']]
            )
    return chapters_list


@alru_cache(maxsize=1000, ttl=43200)
async def images_title(slug: str, chapter_id: str) -> dict:
    """Возвращает список изображений главы манги."""
    query = gql(IMAGES_TITLE_QUERY)
    
    manga_data = await get_manga_cache(slug)
    manga_id = manga_data['id']

    return await client.execute_async(query, variable_values={'mangaId': manga_id, 'chapterId': chapter_id})