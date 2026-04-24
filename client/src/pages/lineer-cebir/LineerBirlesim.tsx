import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const LineerBirlesim: Component = () => (
  <SolverPage
    topic={{
      category: "Lineer Cebir",
      subcategory: "Lineer Birleşim",
      title: "Lineer Birleşim",
      description: "Lineer birleşim, lineer bağımsızlık, germe, baz ve boyut kavramlarını inceleyin. Vektörlerin bağımsızlık testleri.",
      accentVar: "var(--accent-lineer)",
      placeholder: "Örnek: v₁ = (1, 2, 3), v₂ = (4, 5, 6), v₃ = (7, 8, 9) vektörlerinin lineer bağımsız olup olmadığını belirleyiniz.",
    }}
  />
);

export default LineerBirlesim;
