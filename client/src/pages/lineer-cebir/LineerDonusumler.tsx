import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const LineerDonusumler: Component = () => (
  <SolverPage
    topic={{
      category: "Lineer Cebir",
      subcategory: "Lineer Dönüşümler",
      title: "Lineer Dönüşümler",
      description: "Lineer dönüşümlerin tanımı, çekirdeği, görüntüsü ve matris gösterimi. Boyut teoremi ve izomorfizma kavramları.",
      accentVar: "var(--accent-lineer)",
      placeholder: "Örnek: T: R³ → R² tanımlı T(x, y, z) = (x + 2y, 3z - y) dönüşümünün lineer olduğunu gösteriniz ve çekirdek ile görüntüsünü bulunuz.",
    }}
  />
);

export default LineerDonusumler;
