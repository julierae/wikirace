import asyncio
from aiohttp import ClientSession
from urllib.parse import unquote

API_ENDPOINT = "https://en.wikipedia.org/w/api.php"


async def fetch_links(session, page_title, prop="links"):
    all_links = []
    continue_param = {}
    prop_continue = "lhcontinue" if prop == "linkshere" else "plcontinue"
    prop_limit = "lhlimit" if prop == "linkshere" else "pllimit"

    while True:
        params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": prop,
            f"{prop_limit}": "max",
            **continue_param,
        }
        try:
            async with session.get(API_ENDPOINT, params=params) as response:
                data = await response.json()
                if "errors" in data:
                    return None, f"API Error: {data['errors']}"
                if "warnings" in data:
                    return None, f"API Warning: {data['warnings']}"
                page = next(iter(data["query"]["pages"].values()))
                all_links.extend([link["title"] for link in page.get(prop, [])])

                if "continue" not in data:
                    break
                continue_param = {
                    f"{prop_continue}": data["continue"][f"{prop_continue}"]
                }
        except Exception as e:
            return None, f"API Error: {e}"

    return all_links, None


async def bidirectional_search(start_title, end_title, session, max_depth=20):
    forward_queue = asyncio.Queue()
    backward_queue = asyncio.Queue()
    forward_visited = {start_title: [start_title]}
    backward_visited = {end_title: [end_title]}

    await forward_queue.put((start_title, 0))
    await backward_queue.put((end_title, 0))

    while not forward_queue.empty() and not backward_queue.empty():
        try:
            # Process forward direction
            current_title, depth = await forward_queue.get()
            if depth > max_depth:
                continue

            links, error = await fetch_links(session, current_title, "links")
            if error:
                return None, error
            for link in links:
                if link in backward_visited:
                    return (
                        forward_visited[current_title] + backward_visited[link],
                        None,
                    )
                if link not in forward_visited:
                    forward_visited[link] = forward_visited[current_title] + [link]
                    await forward_queue.put((link, depth + 1))

            # Process backward direction
            current_title, depth = await backward_queue.get()
            if depth > max_depth:
                continue

            links_here, error = await fetch_links(session, current_title, "linkshere")
            if error:
                return None, error
            for link in links_here:
                if link in forward_visited:
                    return (
                        forward_visited[link] + backward_visited[current_title],
                        None,
                    )
                if link not in backward_visited:
                    backward_visited[link] = [link] + backward_visited[current_title]
                    await backward_queue.put((link, depth + 1))
        except Exception as e:
            return None, f"API Error: {e}"

    return None, "No path found"


async def calculate_path(start_title, end_title) -> tuple[list[str] | None, str | None]:

    async with ClientSession() as session:
        path, error = await bidirectional_search(start_title, end_title, session)

    if error:
        return None, error

    return path, None
