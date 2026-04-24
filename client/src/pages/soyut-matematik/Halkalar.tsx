import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const Halkalar: Component = () => (
  <SolverPage
    topic={{
      category: "Soyut Matematik",
      subcategory: "Halkalar",
      title: "Halkalar",
      description: "Halka aksiyomları, idealler, bölüm halkaları ve halka homomorfizmalarını inceleyin. Tamsayılar halkası ve polinom halkaları üzerinde çalışın.",
      accentVar: "var(--accent-soyut)",
      placeholder: "Örnek: (Z_12, +, ·) halkasında sıfır bölenlerini ve birimlerini bulunuz.",
    }}
  />
);

export default Halkalar;
