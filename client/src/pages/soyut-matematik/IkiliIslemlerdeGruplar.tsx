import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const IkiliIslemlerdeGruplar: Component = () => (
  <SolverPage
    topic={{
      category: "Soyut Matematik",
      subcategory: "İkili İşlemlerde Gruplar",
      title: "İkili İşlemlerde Gruplar",
      description: "Grup aksiyomlarını, alt grupları, devirli grupları ve grup homomorfizmalarını inceleyin. Cayley tabloları ve grup yapılarını çözümleyin.",
      accentVar: "var(--accent-soyut)",
      placeholder: "Örnek: (Z_6, +_6) grubunun tüm alt gruplarını bulunuz ve her birinin devirli olup olmadığını belirleyiniz.",
    }}
  />
);

export default IkiliIslemlerdeGruplar;
