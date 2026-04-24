import { createSignal, For, Show } from "solid-js";
import type { Component } from "solid-js";
import { A, useLocation } from "@solidjs/router";
import { CATEGORIES } from "../lib/types";

const Sidebar: Component = () => {
  const location = useLocation();
  const [openCategories, setOpenCategories] = createSignal<Set<string>>(
    new Set(CATEGORIES.map((c) => c.name))
  );

  const toggleCategory = (name: string) => {
    setOpenCategories((prev) => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
      }
      return next;
    });
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <A href="/" class="sidebar-logo">
          <div class="sidebar-logo-icon">∫</div>
          <div class="sidebar-logo-text">
            <span>Anti-MathX</span>
          </div>
        </A>
      </div>

      <nav class="sidebar-nav">
        <For each={CATEGORIES}>
          {(category) => (
            <div class="sidebar-category">
              <div
                class="sidebar-category-header"
                onClick={() => toggleCategory(category.name)}
              >
                <span
                  class="sidebar-category-dot"
                  style={{ background: category.accentColor }}
                />
                <span>{category.name}</span>
                <span
                  class={`sidebar-category-chevron ${openCategories().has(category.name) ? "open" : ""
                    }`}
                >
                  ›
                </span>
              </div>

              <Show when={openCategories().has(category.name)}>
                <div class="sidebar-category-links">
                  <For each={category.topics}>
                    {(topic) => (
                      <A
                        href={topic.path}
                        class={`sidebar-link ${isActive(topic.path) ? "active" : ""
                          }`}
                        style={{
                          "--link-accent": category.accentColor,
                        }}
                      >
                        <span
                          class="sidebar-link-icon"
                          style={{ color: category.accentColor }}
                        >
                          {topic.icon}
                        </span>
                        {topic.name}
                      </A>
                    )}
                  </For>
                </div>
              </Show>
            </div>
          )}
        </For>
      </nav>


    </aside>
  );
};

export default Sidebar;
