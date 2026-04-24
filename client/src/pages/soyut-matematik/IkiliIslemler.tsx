import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const IkiliIslemler: Component = () => (
  <SolverPage
    topic={{
      category: "Soyut Matematik",
      subcategory: "İkili İşlemler",
      title: "İkili İşlemler",
      description: "İkili işlemlerin değişme, birleşme, dağılma özelliklerini, birim ve ters eleman kavramlarını inceleyin.",
      accentVar: "var(--accent-soyut)",
      placeholder: "Örnek: Z kümesi üzerinde a * b = a + b - 2 işleminin değişme ve birleşme özelliklerini gösteriniz.",
    }}
  />
);

export default IkiliIslemler;
