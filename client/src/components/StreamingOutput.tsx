import { Show } from "solid-js";
import type { Component } from "solid-js";
import MarkdownRenderer from "./MarkdownRenderer";

interface StreamingOutputProps {
  content: string;
  isStreaming: boolean;
}

const StreamingOutput: Component<StreamingOutputProps> = (props) => {
  return (
    <div class="solver-output-card fade-in">
      <div class="solver-output-header">
        <div class="solver-output-title">
          <Show when={props.isStreaming}>
            <span class="status-dot" />
          </Show>
          <span>
            {props.isStreaming ? "Çözüm oluşturuluyor..." : "Çözüm"}
          </span>
        </div>
      </div>
      <div class="solver-output-body">
        <Show
          when={props.content}
          fallback={
            <div class="solver-output-empty">
              <span class="solver-output-empty-icon">📝</span>
              <span>Sorunuzu yazıp "Çözümü Üret" butonuna tıklayın</span>
            </div>
          }
        >
          <MarkdownRenderer content={props.content} />
          <Show when={props.isStreaming}>
            <span class="typing-cursor" />
          </Show>
        </Show>
      </div>
    </div>
  );
};

export default StreamingOutput;
