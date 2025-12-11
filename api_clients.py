import asyncio
import aiohttp
import requests
from dotenv import load_dotenv

load_dotenv()


async def fetch_senscritique_page(session, username, offset, limit, progress_callback=None):
    """Fetch a single page of SensCritique collection results."""
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.senscritique.com',
        'user-agent': 'Mozilla/5.0'
    }

    json_data = {
        "operationName": "UserCollection",
        "variables": {
            "username": username,
            "limit": limit,
            "offset": offset,
            "order": "LAST_ACTION_DESC",
            "isCollection": True
        },
        "query": 'query UserCollection($action: ProductAction, $categoryId: Int, $gameSystemId: Int, $genreId: Int, $isAgenda: Boolean, $keywords: String, $limit: Int, $month: Int, $offset: Int, $order: CollectionSort, $showTvAgenda: Boolean, $universe: String, $username: String!, $versus: Boolean, $year: Int, $yearDateDone: Int, $yearDateRelease: Int, $isCollection: Boolean, $minDateRelease: Int, $maxDateRelease: Int) {\n  user(username: $username) {\n    ...UserMinimal\n    ...ProfileStats\n    notificationSettings {\n      alertAgenda\n      __typename\n    }\n    collection(\n      action: $action\n      categoryId: $categoryId\n      gameSystemId: $gameSystemId\n      genreId: $genreId\n      isAgenda: $isAgenda\n      keywords: $keywords\n      limit: $limit\n      month: $month\n      offset: $offset\n      order: $order\n      showTvAgenda: $showTvAgenda\n      universe: $universe\n      versus: $versus\n      year: $year\n      yearDateDone: $yearDateDone\n      yearDateRelease: $yearDateRelease\n      isCollection: $isCollection\n      minDateRelease: $minDateRelease\n      maxDateRelease: $maxDateRelease\n    ) {\n      total\n      filters {\n        action {\n          count\n          label\n          value\n          __typename\n        }\n        category {\n          count\n          label\n          value\n          __typename\n        }\n        gamesystem {\n          count\n          label\n          value\n          __typename\n        }\n        genre {\n          count\n          label\n          value\n          __typename\n        }\n        monthDateDone {\n          count\n          label\n          value\n          __typename\n        }\n        releaseDate {\n          count\n          label\n          value\n          __typename\n        }\n        universe {\n          count\n          label\n          value\n          __typename\n        }\n        yearDateDone {\n          count\n          label\n          value\n          __typename\n        }\n        __typename\n      }\n      periodDateRelease {\n        max\n        min\n        __typename\n      }\n      products {\n        ...ProductList\n        episodeNumber\n        seasonNumber\n        totalEpisodes\n        preloadedParentTvShow {\n          ...ProductList\n          __typename\n        }\n        scoutsAverage {\n          average\n          count\n          __typename\n        }\n        currentUserInfos {\n          ...ProductUserInfos\n          __typename\n        }\n        otherUserInfos(username: $username) {\n          ...ProductUserInfos\n          lists {\n            id\n            label\n            listSubtype\n            url\n            __typename\n          }\n          review {\n            id\n            title\n            url\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      tvProducts {\n        infos {\n          channel {\n            id\n            label\n            __typename\n          }\n          showTimes {\n            id\n            dateEnd\n            dateStart\n            __typename\n          }\n          __typename\n        }\n        product {\n          ...ProductList\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserMinimal on User {\n  ...UserNano\n  dateCreation\n  settings {\n    about\n    birthDate\n    country\n    dateLastSession\n    displayedName\n    email\n    firstName\n    gender\n    lastName\n    privacyName\n    privacyProfile\n    showAge\n    showGender\n    showProfileType\n    urlWebsite\n    username\n    zipCode\n    __typename\n  }\n  __typename\n}\n\nfragment UserNano on User {\n  following\n  hasBlockedMe\n  id\n  isBlocked\n  isScout\n  name\n  url\n  username\n  medias {\n    avatar\n    backdrop\n    __typename\n  }\n  __typename\n}\n\nfragment ProductList on Product {\n  category\n  channel\n  dateRelease\n  dateReleaseEarlyAccess\n  dateReleaseJP\n  dateReleaseOriginal\n  dateReleaseUS\n  displayedYear\n  duration\n  episodeNumber\n  seasonNumber\n  frenchReleaseDate\n  id\n  numberOfSeasons\n  originalRun\n  originalTitle\n  rating\n  slug\n  subtitle\n  title\n  universe\n  url\n  yearOfProduction\n  canalVOD {\n    url\n    __typename\n  }\n  tvChannel {\n    name\n    url\n    __typename\n  }\n  countries {\n    id\n    name\n    __typename\n  }\n  gameSystems {\n    id\n    label\n    __typename\n  }\n  medias {\n    picture\n    __typename\n  }\n  genresInfos {\n    label\n    __typename\n  }\n  artists {\n    name\n    person_id\n    url\n    __typename\n  }\n  authors {\n    name\n    person_id\n    url\n    __typename\n  }\n  creators {\n    name\n    person_id\n    url\n    __typename\n  }\n  developers {\n    name\n    person_id\n    url\n    __typename\n  }\n  directors {\n    name\n    person_id\n    url\n    __typename\n  }\n  pencillers {\n    name\n    person_id\n    url\n    __typename\n  }\n  stats {\n    ratingCount\n    __typename\n  }\n  __typename\n}\n\nfragment ProductUserInfos on ProductUserInfos {\n  dateDone\n  hasStartedReview\n  isCurrent\n  id\n  isDone\n  isListed\n  isRecommended\n  isReviewed\n  isWished\n  productId\n  rating\n  userId\n  numberEpisodeDone\n  lastEpisodeDone {\n    episodeNumber\n    id\n    season {\n      seasonNumber\n      id\n      episodes {\n        title\n        id\n        episodeNumber\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  gameSystem {\n    id\n    label\n    __typename\n  }\n  review {\n    author {\n      id\n      name\n      __typename\n    }\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileStats on User {\n  likePositiveCountStats {\n    contact\n    feed\n    list\n    paramIndex\n    review\n    total\n    __typename\n  }\n  stats {\n    ...UserStatsData\n    __typename\n  }\n  __typename\n}\n\nfragment UserStatsData on UserStats {\n  collectionCount\n  diaryCount\n  listCount\n  pollCount\n  topCount\n  followerCount\n  ratingCount\n  reviewCount\n  scoutCount\n  __typename\n}\n'
    }

    async with session.post("https://apollo.senscritique.com/", headers=headers, json=json_data) as response:
        if response.status != 200:
            raise RuntimeError(f"SensCritique error: {response.status}")
        
        data = await response.json()
        
    collection_data = data.get("data", {}).get("user", {}).get("collection", {})
    products = collection_data.get("products", [])
    total = collection_data.get("total", 0)

    items = []
    for p in products:
        title = p.get("title")
        rating = p.get("otherUserInfos", {}).get("rating")
        category = p.get("category")

        if title and rating is not None and category:
            items.append({
                "title": title,
                "rating_sc": float(rating),
                "category": category
            })
    
    if progress_callback:
        progress_callback(offset + len(items), total)

    return items, total


async def fetch_senscritique_collection_async(username, progress_callback=None):
    """Fetch complete SensCritique collection using concurrent pagination."""
    limit = 100
    all_items = []
    
    async with aiohttp.ClientSession() as session:
        first_page, total = await fetch_senscritique_page(session, username, 0, limit, progress_callback)
        all_items.extend(first_page)
        
        if total <= limit:
            return all_items
        
        tasks = [
            fetch_senscritique_page(session, username, offset, limit, progress_callback)
            for offset in range(limit, total, limit)
        ]
        
        results = await asyncio.gather(*tasks)
        
        for page_items, _ in results:
            all_items.extend(page_items)
    
    return all_items


def fetch_senscritique_collection(username, progress_callback=None):
    """Synchronous wrapper for async fetch."""
    return asyncio.run(fetch_senscritique_collection_async(username, progress_callback))


def get_sc_global_rating(title):
    """Fetch global SensCritique rating for a title via search."""
    headers = {
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': '89b7f82c57b4e7741d51b43a07d5f1e4',
        'content-type': 'application/json',
        'origin': 'https://www.senscritique.com',
        'priority': 'u=1, i',
        'referer': f'https://www.senscritique.com/search?query={title}',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    }

    json_data = {
        'operationName': 'SearchProductExplorer',
        'variables': {
            'offset': 0,
            'limit': 16,
            'query': title,
            'filters': [],
            'sortBy': 'RELEVANCE',
        },
        'query': 'query SearchProductExplorer($query: String, $offset: Int, $limit: Int, $filters: [SearchFilter], $sortBy: SearchProductExplorerSort) {\n  searchProductExplorer(\n    query: $query\n    filters: $filters\n    sortBy: $sortBy\n    offset: $offset\n    limit: $limit\n  ) {\n    total\n    aggregations {\n      identifier\n      count\n      items {\n        label\n        count\n        __typename\n      }\n      __typename\n    }\n    sortOptions {\n      id\n      __typename\n    }\n    items {\n      ...ProductList\n      currentUserInfos {\n        ...ProductUserInfos\n        __typename\n      }\n      scoutsAverage {\n        average\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductList on Product {\n  category\n  channel\n  dateRelease\n  dateReleaseEarlyAccess\n  dateReleaseJP\n  dateReleaseOriginal\n  dateReleaseUS\n  displayedYear\n  duration\n  episodeNumber\n  seasonNumber\n  frenchReleaseDate\n  id\n  numberOfSeasons\n  originalRun\n  originalTitle\n  rating\n  slug\n  subtitle\n  title\n  universe\n  url\n  yearOfProduction\n  canalVOD {\n    url\n    __typename\n  }\n  tvChannel {\n    name\n    url\n    __typename\n  }\n  countries {\n    id\n    name\n    __typename\n  }\n  gameSystems {\n    id\n    label\n    __typename\n  }\n  medias {\n    picture\n    pictureWithMetadata {\n      url\n      width\n      height\n      __typename\n    }\n    __typename\n  }\n  genresInfos {\n    label\n    __typename\n  }\n  artists {\n    name\n    person_id\n    url\n    __typename\n  }\n  authors {\n    name\n    person_id\n    url\n    __typename\n  }\n  creators {\n    name\n    person_id\n    url\n    __typename\n  }\n  developers {\n    name\n    person_id\n    url\n    __typename\n  }\n  directors {\n    name\n    person_id\n    url\n    __typename\n  }\n  pencillers {\n    name\n    person_id\n    url\n    __typename\n  }\n  stats {\n    ratingCount\n    __typename\n  }\n  __typename\n}\n\nfragment ProductUserInfos on ProductUserInfos {\n  dateDone\n  hasStartedReview\n  isCurrent\n  id\n  isDone\n  isListed\n  isRecommended\n  isReviewed\n  isWished\n  productId\n  rating\n  userId\n  numberEpisodeDone\n  lastEpisodeDone {\n    episodeNumber\n    id\n    season {\n      seasonNumber\n      id\n      episodes {\n        title\n        id\n        episodeNumber\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  gameSystem {\n    id\n    label\n    __typename\n  }\n  review {\n    author {\n      id\n      name\n      __typename\n    }\n    url\n    __typename\n  }\n  __typename\n}\n'
    }

    try:
        resp = requests.post('https://apollo.senscritique.com/', headers=headers, json=json_data)
        if resp.status_code != 200:
            return None
        data = resp.json()
        items = data.get("data", {}).get("searchProductExplorer", {}).get("items", [])
        if not items:
            return None
        rating = items[0].get("rating")
        if rating is None:
            return None
        return float(rating)
    except Exception:
        return None



