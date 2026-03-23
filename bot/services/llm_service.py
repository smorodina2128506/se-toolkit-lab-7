"""LLM Service for natural language processing with tool calling."""

import json
import sys
from typing import Any

import httpx

from config import BotSettings


# Define all 9 backend endpoints as LLM tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks available in the system. Use this when user asks about available labs, what labs exist, or lab structure.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of ALL enrolled students and their groups. Use this when user asks about how many students, total enrollment, number of learners, or student count.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab. Use when user asks about score distribution or grade buckets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average pass rates and attempt counts for a lab. Use when user asks about pass rates, scores, completion, or task performance for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'. MUST be provided.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day timeline for a specific lab. Use when user asks about submission timeline, activity over time, or when submissions were made.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group scores and student counts for a specific lab. Use this when user asks about which group is best, group comparison, group performance, or group rankings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'. MUST be provided.",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a specific lab. Use when user asks about top students, best performers, leaderboard, or ranking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return, e.g. 5. Default is 5.",
                        "default": 5,
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a specific lab. Use when user asks about completion rate or what percentage completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                    }
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL sync to refresh data from autochecker. Use when user asks to refresh or update data.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

# System prompt for the LLM
SYSTEM_PROMPT = """You are an assistant for a Learning Management System (LMS). 
You have access to backend API tools that provide data about labs, students, scores, and analytics.

When the user asks a question:
1. First understand what they're asking
2. Call the appropriate tool(s) to get the data
3. Analyze the results
4. Provide a clear, helpful answer based on the actual data

Available tools:
- get_items: List all labs and tasks
- get_learners: List enrolled students and groups
- get_scores: Score distribution for a lab (4 buckets)
- get_pass_rates: Per-task pass rates and attempts for a lab
- get_timeline: Submissions per day for a lab
- get_groups: Per-group performance for a lab
- get_top_learners: Top N students for a lab
- get_completion_rate: Completion percentage for a lab
- trigger_sync: Refresh data from autochecker

For questions like "which lab has the lowest pass rate":
1. First call get_items to get all labs
2. Then call get_pass_rates for each lab
3. Compare the results and identify the lowest
4. Report the answer with specific numbers

Always be specific and include numbers from the data. If you don't have enough information, ask for clarification.
If the user's message is gibberish or unclear, politely explain what you can help with.
"""


class LlmService:
    """Service for interacting with LLM API with tool calling support."""

    def __init__(self, settings: BotSettings) -> None:
        """Initialize LLM service.

        Args:
            settings: Bot configuration settings.
        """
        self.settings = settings
        self.base_url = settings.llm_api_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_api_model
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _log_debug(self, message: str) -> None:
        """Log debug message to stderr."""
        print(f"[LLM] {message}", file=sys.stderr)

    def chat(self, messages: list[dict], use_tools: bool = True) -> dict:
        """Send a chat request to the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            use_tools: Whether to include tool definitions.

        Returns:
            LLM response dict.
        """
        if not self.base_url:
            msg = "LLM_API_BASE_URL not configured"
            raise ValueError(msg)

        url = f"{self.base_url.rstrip('/')}/chat/completions"

        payload = {
            "model": self.model or "coder-model",
            "messages": messages,
            "temperature": 0.1,
        }

        if use_tools:
            payload["tools"] = TOOLS
            payload["tool_choice"] = "auto"

        self._log_debug(f"Sending request to {url}")

        with httpx.Client() as client:
            response = client.post(url, headers=self._headers, json=payload, timeout=60.0)
            response.raise_for_status()
            result = response.json()

        self._log_debug(f"Got response: {json.dumps(result, indent=2)[:500]}")
        return result

    def execute_tool(self, tool_name: str, arguments: dict) -> Any:
        """Execute a tool by calling the appropriate backend endpoint.

        Args:
            tool_name: Name of the tool to execute.
            arguments: Tool arguments.

        Returns:
            Tool execution result.
        """
        from services.lms_client import LmsClient

        client = LmsClient(self.settings)

        self._log_debug(f"Executing tool: {tool_name}({arguments})")

        match tool_name:
            case "get_items":
                result = client.get_items()
            case "get_learners":
                result = client.get_learners()
            case "get_scores":
                lab = arguments.get("lab", "")
                result = client.get_scores(lab)
            case "get_pass_rates":
                lab = arguments.get("lab", "")
                result = client.get_pass_rates(lab)
            case "get_timeline":
                lab = arguments.get("lab", "")
                result = client.get_timeline(lab)
            case "get_groups":
                lab = arguments.get("lab", "")
                result = client.get_groups(lab)
            case "get_top_learners":
                lab = arguments.get("lab", "")
                limit = arguments.get("limit", 5)
                result = client.get_top_learners(lab, limit)
            case "get_completion_rate":
                lab = arguments.get("lab", "")
                result = client.get_completion_rate(lab)
            case "trigger_sync":
                result = client.trigger_sync()
            case _:
                msg = f"Unknown tool: {tool_name}"
                raise ValueError(msg)

        self._log_debug(f"Tool result: {json.dumps(result, default=str)[:300]}")
        return result

    def route(self, user_message: str) -> str:
        """Route a natural language message to appropriate tools and return response.

        Args:
            user_message: User's natural language query.

        Returns:
            Formatted response text.
        """
        # Initialize conversation with system prompt
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Get LLM response
            response = self.chat(messages, use_tools=True)
            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})

            # Check if LLM wants to call tools
            tool_calls = message.get("tool_calls", [])

            if not tool_calls:
                # LLM provided final answer
                content = message.get("content", "I don't have enough information to answer that.")
                return content or "I don't have enough information to answer that."

            # Add assistant message with tool calls to conversation
            messages.append(message)

            # Execute each tool call
            for tool_call in tool_calls:
                func = tool_call.get("function", {})
                tool_name = func.get("name", "")
                arguments_str = func.get("arguments", "{}")

                try:
                    arguments = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
                except json.JSONDecodeError:
                    arguments = {}

                try:
                    result = self.execute_tool(tool_name, arguments)
                    tool_result = json.dumps(result, default=str)
                    self._log_debug(f"[tool] Result: {tool_result[:200]}")
                except Exception as e:
                    tool_result = json.dumps({"error": str(e)})
                    self._log_debug(f"[tool] Error: {e}")

                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": tool_result,
                })

            self._log_debug(f"[summary] Feeding {len(tool_calls)} tool result(s) back to LLM")

        # If we get here, we hit max iterations
        return "I'm having trouble processing your request. Please try rephrasing."
