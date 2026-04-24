import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const KismiSiralama: Component = () => (
  <SolverPage
    topic={{
      category: "Soyut Matematik",
      subcategory: "Kısmi Sıralama Bağıntısı",
      title: "Kısmi Sıralama Bağıntısı",
      description: "Kısmi sıralama bağıntılarının refleksif, antisimetrik ve geçişli özelliklerini inceleyin. Hasse diyagramları ve sıralama problemlerini çözün.",
      accentVar: "var(--accent-soyut)",
      placeholder: "Örnek: ({1,2,3,6}, |) kısmi sıralı kümesinin Hasse diyagramını çiziniz ve en büyük, en küçük elemanları belirleyiniz.",
    }}
  />
);

export default KismiSiralama;
