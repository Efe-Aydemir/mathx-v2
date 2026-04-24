import type { Component } from "solid-js";
import SolverPage from "../components/SolverPage";

const CizgeTeorisi: Component = () => (
  <SolverPage
    topic={{
      category: "Çizge Teorisi",
      subcategory: "Çizge Teorisi",
      title: "Çizge Teorisi",
      description: "Graf yapıları, ağaçlar, Euler ve Hamilton yolları, çevrimler, bağlantılılık, renklendirme ve eşleştirme problemlerini çözün.",
      accentVar: "var(--accent-cizge)",
      placeholder: "Örnek: 6 düğümlü bir basit grafta her düğümün derecesi 3 ise, bu grafın kaç kenarı vardır? Böyle bir graf çiziniz.",
    }}
  />
);

export default CizgeTeorisi;
