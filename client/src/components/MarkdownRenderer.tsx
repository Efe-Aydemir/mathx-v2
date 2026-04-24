import type { Component } from "solid-js";
import { SolidMarkdown } from "solid-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: Component<MarkdownRendererProps> = (props) => {
  return (
    <div class="markdown-content">
      <SolidMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex] as any}
      >
        {props.content}
      </SolidMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
