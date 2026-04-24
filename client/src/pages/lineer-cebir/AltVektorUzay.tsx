import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const AltVektorUzay: Component = () => (
  <SolverPage
    topic={{
      category: "Lineer Cebir",
      subcategory: "Alt Vektör Uzay",
      title: "Alt Vektör Uzay",
      description: "Alt uzay kriterlerini kontrol edin, alt uzay ispatları yapın ve toplam/kesişim alt uzaylarını inceleyin.",
      accentVar: "var(--accent-lineer)",
      placeholder: "Örnek: W = {(x, y, z) ∈ R³ | 2x - y + z = 0} kümesinin R³'ün bir alt vektör uzayı olduğunu gösteriniz.",
    }}
  />
);

export default AltVektorUzay;
