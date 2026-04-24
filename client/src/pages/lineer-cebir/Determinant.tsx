import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const Determinant: Component = () => (
  <SolverPage
    topic={{
      category: "Lineer Cebir",
      subcategory: "Determinant",
      title: "Determinant",
      description: "Matris determinantlarını Sarrus kuralı, kofaktör açılımı ve satır/sütun işlemleri ile hesaplayın. Cramer kuralı uygulamaları.",
      accentVar: "var(--accent-lineer)",
      placeholder: "Örnek: A = [[2, 1, 3], [4, -1, 2], [1, 5, -2]] matrisinin determinantını kofaktör açılımı ile hesaplayınız.",
    }}
  />
);

export default Determinant;
