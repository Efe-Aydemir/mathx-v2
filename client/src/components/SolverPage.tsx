import { createSignal } from "solid-js";
import type { Component } from "solid-js";
import { streamSolution } from "../lib/api";
import StreamingOutput from "./StreamingOutput";
import type { TopicConfig } from "../lib/types";

interface SolverPageProps {
  topic: TopicConfig;
}

const SolverPage: Component<SolverPageProps> = (props) => {
  const [question, setQuestion] = createSignal("");
  const [solution, setSolution] = createSignal("");
  const [isStreaming, setIsStreaming] = createSignal(false);
  const [error, setError] = createSignal("");

  const handleSolve = async () => {
    const q = question().trim();
    if (!q || isStreaming()) return;

    setSolution("");
    setError("");
    setIsStreaming(true);

    try {
      const stream = streamSolution(
        props.topic.category,
        props.topic.subcategory,
        q
      );

      for await (const chunk of stream) {
        setSolution((prev) => prev + chunk);
      }
    } catch (err: any) {
      setError(err.message || "Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setIsStreaming(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      handleSolve();
    }
  };

  return (
    <div class="solver-page fade-in">
      <div class="solver-breadcrumb">
        <a href="/">Ana Sayfa</a>
        <span class="solver-breadcrumb-sep">›</span>
        <span style={{ color: props.topic.accentVar }}>
          {props.topic.category}
        </span>
        <span class="solver-breadcrumb-sep">›</span>
        <span>{props.topic.subcategory}</span>
      </div>

      <h1
        class="solver-title"
        style={{ color: props.topic.accentVar }}
      >
        {props.topic.title}
      </h1>
      <p class="solver-subtitle">{props.topic.description}</p>

      <div class="solver-input-card">
        <label class="solver-input-label" for="question-input">
          Sorunuz
        </label>
        <textarea
          id="question-input"
          class="solver-textarea"
          placeholder={props.topic.placeholder}
          value={question()}
          onInput={(e) => setQuestion(e.currentTarget.value)}
          onKeyDown={handleKeyDown}
          disabled={isStreaming()}
        />
        <div class="solver-actions">
          <span
            style={{
              "font-size": "12px",
              color: "var(--text-tertiary)",
            }}
          >
            ⌘ + Enter
          </span>
          <button
            id="solve-button"
            class="solver-btn"
            style={{
              background: `linear-gradient(135deg, ${props.topic.accentVar}, ${props.topic.accentVar}dd)`,
              "box-shadow": `0 4px 16px ${props.topic.accentVar}33`,
            }}
            onClick={handleSolve}
            disabled={isStreaming() || !question().trim()}
          >
            {isStreaming() ? (
              <>
                <span class="solver-btn-spinner" />
                Çözülüyor...
              </>
            ) : (
              <>
                <span class="solver-btn-icon">✨</span>
                Çözümü Üret
              </>
            )}
          </button>
        </div>
      </div>

      {error() && (
        <div
          style={{
            padding: "12px 16px",
            "margin-bottom": "16px",
            background: "hsl(0, 60%, 15%)",
            border: "1px solid hsl(0, 60%, 30%)",
            "border-radius": "var(--radius-md)",
            color: "hsl(0, 80%, 70%)",
            "font-size": "13px",
          }}
        >
          ⚠️ {error()}
        </div>
      )}

      <StreamingOutput
        content={solution()}
        isStreaming={isStreaming()}
      />
    </div>
  );
};

export default SolverPage;
