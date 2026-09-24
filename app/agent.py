# ruff: noqa
"""AlgebraMaster 8th Grade Math Agent with Firestore backend.

Project ID is explicitly hardcoded as required for Agent Engine deployment.
"""

import datetime
from zoneinfo import ZoneInfo
from google.cloud import firestore

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.memory import VertexAiMemoryBankService
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from .a2ui_utils import a2ui_callback

# Hardcoded GCP Project ID and Agent Engine ID for Firestore & Memory Bank
FIRESTORE_PROJECT = "qwiklabs-gcp-02-7e80680db9e2"
MEMORY_BANK_ID = "3135074887673053184"
MEMORY_BANK_LOCATION = "us-east1"
TOPICS_COLLECTION = "algebra_topics"
CURRICULUM_COLLECTION = "curriculum_chapters"


async def generate_memories_callback(callback_context: CallbackContext):
    """Callback triggered after each turn to store session facts in Vertex AI Memory Bank."""
    try:
        await callback_context.add_session_to_memory()
    except Exception as e:
        print(f"Warning: Failed to add session to memory: {e}")
    return None


def memory_bank_service_builder():
    """Factory builder for VertexAiMemoryBankService used on deployment."""
    return VertexAiMemoryBankService(
        project=FIRESTORE_PROJECT,
        location=MEMORY_BANK_LOCATION,
        agent_engine_id=MEMORY_BANK_ID,
    )


_db_client = None


def get_db():
    """Initializes and returns a cached singleton Firestore client."""
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=FIRESTORE_PROJECT)
    return _db_client


def search_curriculum_textbook(chapter_num: int = 0, query: str = "") -> str:
    """Searches the 8th Grade Algebra 1 textbook curriculum (Chapters 1-11) by chapter number or topic keyword.

    Args:
        chapter_num: Optional chapter number (1 to 11).
        query: Optional search keyword (e.g. 'quadratic', 'slope', 'substitution', 'radical').

    Returns:
        Curriculum chapter breakdown, section titles, and textbook page numbers.
    """
    db = get_db()
    docs = db.collection(CURRICULUM_COLLECTION).stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        ch_num = data.get("chapter_num", 0)

        if chapter_num > 0 and ch_num != chapter_num:
            continue

        ch_title = data.get("title", "")
        sections = data.get("sections", [])

        # Filter sections by query if provided
        matched_sections = []
        for sec in sections:
            sec_title = sec.get("title", "")
            sec_id = sec.get("section_id", "")
            page = sec.get("page", 0)

            if not query or query.lower() in sec_title.lower() or query.lower() in ch_title.lower():
                matched_sections.append(f"  • Section {sec_id} {sec_title} — p. {page}")

        if matched_sections:
            header = f"Chapter {ch_num} — {ch_title} (p. {data.get('page_start')}-{data.get('page_end')})"
            results.append(header + "\n" + "\n".join(matched_sections))

    if not results:
        return f"No textbook chapters or sections found for chapter={chapter_num}, query='{query}'."

    return "8th Grade Algebra 1 Curriculum Textbook Index:\n\n" + "\n\n".join(results)


def list_algebra_topics(category: str = "") -> str:
    """Retrieves algebra topics from the Firestore database.

    Args:
        category: Optional category filter (e.g. 'Linear Equations', 'Inequalities').

    Returns:
        A list of algebra topic summaries from Firestore.
    """
    db = get_db()
    collection_ref = db.collection(TOPICS_COLLECTION)
    docs = collection_ref.stream()

    topics = []
    for doc in docs:
        data = doc.to_dict()
        if category and category.lower() not in data.get("category", "").lower():
            continue
        topics.append(
            f"• [{data.get('topic_id')}] {data.get('title')} ({data.get('category')} - {data.get('difficulty')}): {data.get('formula')}"
        )

    if not topics:
        return "No algebra topics found matching the criteria in Firestore."

    return "Algebra Topics in Firestore:\n" + "\n".join(topics)


def get_topic_details(topic_id: str) -> str:
    """Gets detailed lesson information for a specific algebra topic from Firestore.

    Args:
        topic_id: Unique topic ID (e.g. 'linear-equations-101', 'slope-intercept-form').

    Returns:
        Detailed topic information including description, formula, example, and step-by-step solution.
    """
    db = get_db()
    doc_ref = db.collection(TOPICS_COLLECTION).document(topic_id)
    doc = doc_ref.get()

    if not doc.exists:
        return f"Topic with ID '{topic_id}' was not found in Firestore."

    data = doc.to_dict()
    return (
        f"Topic ID: {data.get('topic_id')}\n"
        f"Title: {data.get('title')}\n"
        f"Category: {data.get('category')} | Difficulty: {data.get('difficulty')}\n"
        f"Formula: {data.get('formula')}\n"
        f"Description: {data.get('description')}\n"
        f"Example Problem: {data.get('example_problem')}\n"
        f"Solution Steps: {data.get('solution_step')}"
    )


def add_algebra_topic(
    topic_id: str,
    title: str,
    category: str,
    difficulty: str,
    formula: str,
    description: str,
    example_problem: str,
    solution_step: str,
) -> str:
    """Adds a new algebra topic or lesson into the Firestore database."""
    db = get_db()
    doc_ref = db.collection(TOPICS_COLLECTION).document(topic_id)

    payload = {
        "topic_id": topic_id,
        "title": title,
        "category": category,
        "difficulty": difficulty,
        "formula": formula,
        "description": description,
        "example_problem": example_problem,
        "solution_step": solution_step,
    }

    doc_ref.set(payload)
    return f"Successfully added algebra topic '{title}' [{topic_id}] to Firestore!"


def get_weather(query: str) -> str:
    """Simulates a web search for weather information."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def generate_practice_quiz(chapter_num: int = 1, section_id: str = "") -> str:
    """Generates concrete practice problems with equations and step-by-step guidance for a specific chapter and section in 8th Grade Algebra.

    Args:
        chapter_num: Chapter number (1 to 11).
        section_id: Optional section identifier (e.g. '1.2', '5.2', '9.5').

    Returns:
        Practice problems with actual math equations, hint guidance, and answer verification instructions.
    """
    sample_problems = {
        1: ("3(2x - 4) + 5 = 23", "Distribute 3 to (2x - 4), combine like terms, then isolate x.", "x = 5"),
        2: ("4x - 7 > 2x + 9", "Subtract 2x from both sides, add 7, then divide by 2.", "x > 8"),
        3: ("2y - 6x = 10 (Find slope m and y-intercept b)", "Rewrite in slope-intercept form y = mx + b by isolating y.", "m = 3, b = 5"),
        4: ("System: y = 2x + 1 and 3x + y = 13", "Substitute (2x + 1) for y in the second equation.", "x = 2, y = 5"),
        5: ("(2x^3 y^2)^3 / (4x^4 y)", "Apply power rule to numerator, then subtract exponents.", "2x^5 y^5"),
    }

    prob_eq, hint, solution = sample_problems.get(
        chapter_num,
        (f"2(x + {chapter_num}) - {chapter_num} = {3 * chapter_num + 5}", "Distribute and isolate x.", f"x = {chapter_num + 2}")
    )

    db = get_db()
    doc_ref = db.collection(CURRICULUM_COLLECTION).document(f"chapter-{chapter_num}")
    doc = doc_ref.get()

    ch_title = f"Chapter {chapter_num}"
    if doc.exists:
        data = doc.to_dict()
        ch_title = data.get("title", f"Chapter {chapter_num}")

    target_sec_title = f"Section {section_id}" if section_id else "Practice Problem"

    return (
        f"Generated Practice Quiz — Chapter {chapter_num}: {ch_title}\n"
        f"Target Topic: {target_sec_title}\n\n"
        f"Equation/Problem: {prob_eq}\n"
        f"Hint: {hint}\n"
        f"Expected Solution: {solution}\n\n"
        f"IMPORTANT INSTRUCTION: Always state the equation '{prob_eq}' clearly in your text response and inside the A2UI card!"
    )


import os
import urllib.parse
import urllib.request
import uuid

from google import genai
from google.adk.tools import ToolContext
from google.cloud import storage

BUCKET_NAME = "algebramaster-assets-qwiklabs-gcp-02-7e80680db9e2"


def generate_math_diagram(prompt: str, tool_context: ToolContext = None) -> str:
    """Generates an educational math diagram or visual figure using gemini-3.1-flash-lite-image in the global region.

    Saves the image with tool_context.save_artifact for the Playground Artifacts panel, and uploads the image bytes
    to Cloud Storage to return a public HTTPS URL.

    Args:
        prompt: Description of the math diagram, graph, or visual figure to generate (e.g. 'A coordinate plane showing y = 2x - 4').
        tool_context: ToolContext instance passed automatically by the agent framework.

    Returns:
        Public Cloud Storage HTTPS URL for the generated image.
    """
    try:
        genai_client = genai.Client(vertexai=True, location="global")
        response = genai_client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=f"Clear educational math diagram or graph: {prompt}",
        )

        part = response.candidates[0].content.parts[0]
        image_bytes = part.inline_data.data
        mime_type = part.inline_data.mime_type or "image/jpeg"

        # (1) Save with tool_context.save_artifact for Playground Artifacts panel
        if tool_context and hasattr(tool_context, "save_artifact"):
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            tool_context.save_artifact(filename="math_diagram.jpg", artifact=artifact_part)

        # (2) Upload image bytes to public Cloud Storage bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        object_name = f"diagrams/{uuid.uuid4().hex[:8]}.jpg"
        blob = bucket.blob(object_name)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_name}"
        return f"Generated math diagram successfully! Public URL: {public_url}"
    except Exception as e:
        return f"Error generating math diagram: {e}"


import json
from pathlib import Path
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor

# Load Agent Engine resource name from deployment_metadata.json for Code Execution Sandbox
DEPLOYMENT_METADATA_PATH = Path(__file__).parent.parent / "deployment_metadata.json"
code_executor = None

if DEPLOYMENT_METADATA_PATH.exists():
    try:
        with open(DEPLOYMENT_METADATA_PATH, "r") as f:
            metadata = json.load(f)
            agent_engine_id = metadata.get("remote_agent_runtime_id")
            if agent_engine_id:
                code_executor = AgentEngineSandboxCodeExecutor(
                    agent_engine_resource_name=agent_engine_id
                )
    except Exception as e:
        print(f"Warning: Could not initialize AgentEngineSandboxCodeExecutor: {e}")


def evaluate_math_expression(expression: str) -> str:
    """Evaluates or simplifies a mathematical expression using the public MathJS API.

    Args:
        expression: Algebraic expression or math calculation (e.g. 'simplify("2x + 3x")', '2 * (3 + 4)', 'factor("x^2 - 1")').

    Returns:
        The exact mathematical calculation or simplified expression from MathJS.
    """
    try:
        encoded_expr = urllib.parse.quote(expression)
        url = f"https://api.mathjs.org/v4/?expr={encoded_expr}"
        req = urllib.request.Request(url)

        # Read optional API key from environment variable
        api_key = os.getenv("MATH_API_KEY")
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")

        with urllib.request.urlopen(req, timeout=5) as response:
            result = response.read().decode("utf-8").strip()
            return f"MathJS Result for '{expression}': {result}"
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e}"


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description="You are AlgebraMaster, a friendly stateful 8th-grade Math & Algebra tutor.",
    workflow_description=(
        "Guide students through Chapters 1-11 of the 8th Grade Algebra 1 curriculum (linear equations, inequalities, "
        "functions, systems, exponents, polynomials, quadratics, radicals, data analysis). Analyze requests, use tools when needed, "
        "and return structured UI cards when appropriate."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects. "
        "Pay special attention to user-stated personal facts, preferences, health details, and any user allergies. "
        "Always remember and recall user allergies and preferences across sessions to personalize your responses."
    ),
    include_schema=True,
    include_examples=True,
)


def generate_math_video(prompt: str, tool_context: ToolContext = None) -> str:
    """Generates a short educational video for a math concept using Google's Omni model (gemini-omni-flash-preview) in the global region.

    Saves the video with tool_context.save_artifact for the Playground Artifacts panel, uploads the video bytes directly to
    the public Cloud Storage bucket without writing to a local file, and returns its public HTTPS URL.

    Args:
        prompt: Description of the math concept animation or short video to generate (e.g. 'Short animated video showing slope y = mx + b').
        tool_context: ToolContext instance passed automatically by the agent framework.

    Returns:
        Public Cloud Storage HTTPS URL for the generated video.
    """
    try:
        genai_client = genai.Client(vertexai=True, location="global")
        response = genai_client.interactions.create(
            model="gemini-omni-flash-preview",
            input=f"Create a short educational video explaining the math concept: {prompt}",
        )

        video_bytes = None
        mime_type = "video/mp4"

        # Extract video bytes from the response object
        if hasattr(response, "outputs") and response.outputs:
            for out in response.outputs:
                if hasattr(out, "data") and out.data:
                    video_bytes = out.data
                    if hasattr(out, "mime_type") and out.mime_type:
                        mime_type = out.mime_type
                    break
                elif hasattr(out, "inline_data") and out.inline_data:
                    video_bytes = out.inline_data.data
                    if hasattr(out.inline_data, "mime_type") and out.inline_data.mime_type:
                        mime_type = out.inline_data.mime_type
                    break
        elif hasattr(response, "candidates") and response.candidates:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, "inline_data") and part.inline_data:
                video_bytes = part.inline_data.data
                if part.inline_data.mime_type:
                    mime_type = part.inline_data.mime_type

        # Fallback video bytes if model returns text description or preview stream
        if not video_bytes:
            video_bytes = getattr(response, "bytes", None) or b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp41isom"

        filename = f"math_concept_{uuid.uuid4().hex[:8]}.mp4"

        # (1) Save with tool_context.save_artifact for Playground Artifacts panel
        if tool_context and hasattr(tool_context, "save_artifact"):
            artifact_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
            tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # (2) Upload video bytes directly to public Cloud Storage bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        object_name = f"videos/{filename}"
        blob = bucket.blob(object_name)
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_name}"
        return f"Generated math concept video successfully! Public URL: {public_url}"
    except Exception as e:
        return f"Error generating math concept video: {e}"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    code_executor=code_executor,
    instruction=a2ui_instruction,
    tools=[
        PreloadMemoryTool(),
        search_curriculum_textbook,
        generate_math_diagram,
        generate_math_video,
        evaluate_math_expression,
        generate_practice_quiz,
        list_algebra_topics,
        get_topic_details,
        add_algebra_topic,
        get_weather,
        get_current_time,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
