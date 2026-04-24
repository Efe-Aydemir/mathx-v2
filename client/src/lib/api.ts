const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

export async function* streamSolution(
  category: string,
  subcategory: string,
  question: string
): AsyncGenerator<string> {
  const response = await fetch(`${API_BASE}/api/solve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, subcategory, question }),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API error (${response.status}): ${errorBody}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("Response body is not readable");
  }

  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete lines
      const lines = buffer.split("\n");
      // Keep the last potentially incomplete line in the buffer
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith("data: ")) {
          const data = trimmed.slice(6);
          if (data === "[DONE]") return;
          try {
            // Try parsing as JSON first (for structured SSE)
            const parsed = JSON.parse(data);
            if (parsed.token) {
              yield parsed.token;
            } else if (parsed.text) {
              yield parsed.text;
            } else if (typeof parsed === "string") {
              yield parsed;
            }
          } catch {
            // If not JSON, yield raw text
            yield data;
          }
        }
      }
    }

    // Process any remaining buffer
    if (buffer.trim().startsWith("data: ")) {
      const data = buffer.trim().slice(6);
      if (data !== "[DONE]") {
        try {
          const parsed = JSON.parse(data);
          if (parsed.token) yield parsed.token;
          else if (parsed.text) yield parsed.text;
        } catch {
          yield data;
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}
