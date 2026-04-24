import type { Component } from "solid-js";
import SolverPage from "../components/SolverPage";

const Topoloji: Component = () => (
  <SolverPage
    topic={{
      category: "Topoloji",
      subcategory: "Topoloji",
      title: "Topoloji",
      description: "Topolojik uzaylar, açık/kapalı kümeler, süreklilik, kompaktlık, bağlantılılık ve homeomorfizma problemlerini çözün.",
      accentVar: "var(--accent-topoloji)",
      placeholder: "Örnek: X = {a, b, c} kümesi üzerinde τ = {∅, {a}, {a,b}, X} ailesinin bir topoloji olup olmadığını gösteriniz.",
    }}
  />
);

export default Topoloji;
