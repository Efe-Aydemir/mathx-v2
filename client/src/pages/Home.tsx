import { For } from "solid-js";
import type { Component } from "solid-js";
import { A } from "@solidjs/router";
import { CATEGORIES } from "../lib/types";

const Home: Component = () => {
  return (
    <div class="home-page fade-in">
      <div class="home-hero">

        <h1 class="home-hero-title">
          Matematiği{" "}
          <span class="gradient-text">Adım Adım</span>{" "}
          Çöz
        </h1>
        <p class="home-hero-desc">
          Üniversite düzeyinde matematik problemlerinizi yapay zeka ile çözün.
          Soyut Matematik, Lineer Cebir, Çizge Teorisi ve Topoloji konularında
          detaylı, adım adım çözümler alın.
        </p>
      </div>

      <div class="home-categories">
        <For each={CATEGORIES}>
          {(category) => (
            <A
              href={category.topics[0].path}
              class="category-card"
              style={{
                "--card-accent": category.accentColor,
              }}
            >
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  height: "3px",
                  background: `linear-gradient(90deg, ${category.accentColor}, transparent)`,
                  opacity: 0,
                  transition: "opacity var(--transition-base)",
                }}
                class="category-card-stripe"
              />
              <span class="category-card-icon">{category.icon}</span>
              <h2 class="category-card-title">{category.name}</h2>
              <p class="category-card-desc">
                {getCategoryDescription(category.name)}
              </p>
              <div class="category-card-topics">
                <For each={category.topics}>
                  {(topic) => (
                    <span
                      class="category-card-topic"
                      style={{
                        "border-color": category.accentDimColor,
                        color: category.accentColor,
                      }}
                    >
                      {topic.name}
                    </span>
                  )}
                </For>
              </div>
            </A>
          )}
        </For>
      </div>
    </div>
  );
};

function getCategoryDescription(name: string): string {
  switch (name) {
    case "Soyut Matematik":
      return "Denklik bağıntıları, kısmi sıralama, ikili işlemler, gruplar ve halkalar konularında çözümler.";
    case "Lineer Cebir":
      return "Vektör uzayları, alt uzaylar, determinant, lineer dönüşümler ve lineer birleşim çözümleri.";
    case "Çizge Teorisi":
      return "Graf yapıları, ağaçlar, çevrimler ve bağlantılılık konularında detaylı çözümler.";
    case "Topoloji":
      return "Topolojik uzaylar, süreklilik, kompaktlık ve bağlantılılık konularında çözümler.";
    default:
      return "";
  }
}

export default Home;
