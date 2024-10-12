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

def parseURL(url: str) -> str:
    return f"{domain[:-1] if url[0] == "/" else ""}{url}"

def makeRequest(path: str) -> Any:
    try:
        with urllib.request.urlopen(f"{base_url}{path}") as response:
            return json.load(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

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

# Get all guides (up to 200 for now)
guides = makeRequest("guides")

for guide in guides:
    full_guide = makeRequest(f"guides/{guide["guideid"]}")

    guideRef = URIRef(full_guide["url"])
    g.add((guideRef, DC.title, Literal(full_guide["title"])))

    # Add author
    addAuthor(full_guide["author"], guideRef)

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

        # Add images
        media = step.get("media", {})
        for imageData in media.get("data", []) if media.get("type") == "image" else []:
            imageRef = URIRef(imageData["standard"])
            g.add((imageRef, RDF.type, IFIXIT.image))
            g.add((imageRef, IFIXIT.mediaOf, stepRef))

with open("data.rdf", "wb") as file:
    file.write(g.serialize(format="xml").encode())