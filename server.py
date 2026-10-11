import hashlib
import os

from mcp.server.mcpserver import MCPServer, Context

EMAIL = "25f1001143@ds.study.iitm.ac.in"

mcp = MCPServer("exam-mcp-server")


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """
    Reads the exam challenge from HTTP headers and returns
    the first 16 lowercase hex characters of
    SHA-256(f"{challenge}:{normalized_email}").
    """
    headers = ctx.request_context.request.headers

    challenge = headers.get("x-exam-challenge", "").strip()

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    text_to_hash = f"{challenge}:{EMAIL}"
    digest = hashlib.sha256(text_to_hash.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        stateless_http=True,
        json_response=True,
    )