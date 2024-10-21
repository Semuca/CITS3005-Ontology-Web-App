import json
import sys
from typing import Any
import urllib.request

from rdflib import RDF, Graph, Literal, Namespace, URIRef, DC

# RDF setup
domain = "https://www.ifixit.com/"
IFIXIT = Namespace(domain)

g = Graph()
g.bind("ifixit", IFIXIT)

# API setup
base_url = f"{domain}api/2.0/"

# Helper functions
def parseURL(url: str) -> str:
    return f"{domain[:-1] if url[0] == "/" else ""}{url}"

def makeRequest(path: str) -> Any:
    try:
        with urllib.request.urlopen(f"{base_url}{path}") as response:
            return json.load(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Get all categories
categories = makeRequest("categories")

# Recursively turn categories into a list of words
def parseCategories(categories: dict[str, Any]) -> list[str]:
    words = []
    for category, value in categories.items():
        if value is None:
            words.append(category)
        else:
            words.extend(parseCategories(value))

    return words

categoryFilters = parseCategories(categories["Game Console"])

# Load cached category mappings if available
try:
    with open("category-mappings.json") as file:
        categoryMappings = json.load(file)
except Exception:
    categoryMappings = {}

# Filter cached category mappings- these guides we know are in the categories we want
initialGuideIds = [guideId for guideId, category in categoryMappings.items() if category in categoryFilters]
nextGuideToCheck = int(max(categoryMappings.keys(), default=0))

# RDF helper functions
def addAuthor(data: Any, authorOf: URIRef) -> None:
    authorRef = URIRef(parseURL(data["url"]))
    g.add((authorRef, RDF.type, IFIXIT.user))
    g.add((authorRef, IFIXIT.username, Literal(data["username"])))
    g.add((authorRef, IFIXIT.authorOf, authorOf))

def addComment(data: Any, commentOf: URIRef) -> None:
    commentRef = URIRef(f"{domain}comments/{data['commentid']}")
    g.add((commentRef, RDF.type, IFIXIT.comment))
    g.add((commentRef, IFIXIT.commentOf, commentOf))
    g.add((commentRef, IFIXIT.rawText, Literal(data["text_raw"])))
    addAuthor(data["author"], commentRef)

    for reply in data.get("replies", []):
        addComment(reply, commentRef)

guidesFetched = 0
def addGuide(guide_id: Any) -> None:
    global guidesFetched
    full_guide = makeRequest(f"guides/{guide_id}")
    guidesFetched += 1

    guideRef = URIRef(full_guide["url"])
    g.add((guideRef, DC.title, Literal(full_guide["title"])))
    g.add((guideRef, RDF.type, IFIXIT.guide))

    # Add author
    addAuthor(full_guide["author"], guideRef)

    # Add category
    categoryRef = URIRef(f"{domain}category/{full_guide["category"].lower().replace(' ', '-')}")
    g.add((categoryRef, RDF.type, IFIXIT.category))
    g.add((categoryRef, IFIXIT.name, Literal(full_guide["category"])))
    g.add((guideRef, IFIXIT.guideOf, categoryRef))

    # Add parts
    for part in full_guide["parts"]:
        partRef = URIRef(parseURL(part["url"]))
        g.add((partRef, RDF.type, IFIXIT.part))
        g.add((partRef, IFIXIT.name, Literal(part["text"])))

    # Add tools
    for tool in full_guide["tools"]:
        toolRef = URIRef(parseURL(tool["url"]))
        g.add((toolRef, IFIXIT.toolOf, guideRef))
        g.add((toolRef, RDF.type, IFIXIT.tool))
        g.add((toolRef, IFIXIT.name, Literal(tool["text"])))

    # Add guide comments
    for comment in full_guide["comments"]:
        addComment(comment, guideRef)

    # Add steps
    for step in full_guide["steps"]:
        stepRef = URIRef(f"{domain}guide/{full_guide['guideid']}/{step['stepid']}")
        g.add((stepRef, RDF.type, IFIXIT.step))
        g.add((stepRef, DC.title, Literal(step["title"])))
        g.add((stepRef, IFIXIT.stepOf, guideRef))

        # Add step comments
        for comment in step["comments"]:
            addComment(comment, stepRef)

        # Add step lines
        for i, line in enumerate(step["lines"]):
            lineRef = URIRef(f"{domain}guide/{full_guide['guideid']}/{step['stepid']}/{i}")
            g.add((lineRef, RDF.type, IFIXIT.line))
            g.add((lineRef, IFIXIT.rawText, Literal(line["text_raw"])))
            g.add((lineRef, IFIXIT.lineOf, stepRef))

        # Add images
        media = step.get("media", {})
        for imageData in media.get("data", []) if media.get("type") == "image" else []:
            imageRef = URIRef(imageData["standard"])
            g.add((imageRef, RDF.type, IFIXIT.image))
            g.add((imageRef, IFIXIT.mediaOf, stepRef))

guidesFetched = 0
guidesToFetch = 100000

# Fetch initial guides
for guideId in initialGuideIds[:guidesToFetch]:
    addGuide(guideId)

# Fetch guides
offset = nextGuideToCheck

while guidesFetched < guidesToFetch:
    guides = makeRequest(f"guides?limit=200&offset={offset}")

    # Update category mappings
    for guide in guides:
        categoryMappings[guide["guideid"]] = guide["category"]

    # Filter guides
    filteredGuides = [guide for guide in guides if guide["category"] in categoryFilters]

    for guide in filteredGuides:
        addGuide(guide["guideid"])
    
    offset += 200
    if (len(guides) == 0):
        break

# Save category mappings
with open("category-mappings.json", "w") as file:
    json.dump(categoryMappings, file)

with open("data.rdf", "wb") as file:
    file.write(g.serialize(format="ttl").encode())