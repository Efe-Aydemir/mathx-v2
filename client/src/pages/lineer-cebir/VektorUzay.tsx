import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const VektorUzay: Component = () => (
  <SolverPage
    topic={{
      category: "Lineer Cebir",
      subcategory: "Vektör Uzay",
      title: "Vektör Uzay",
      description: "Vektör uzayı aksiyomlarını doğrulayın, standart uzayları inceleyin ve soyut vektör uzayları üzerinde çalışın.",
      accentVar: "var(--accent-lineer)",
      placeholder: "Örnek: V = {(x, y) ∈ R² | x + y = 0} kümesinin R üzerinde bir vektör uzayı olup olmadığını gösteriniz.",
    }}
  />
);

export default VektorUzay;
