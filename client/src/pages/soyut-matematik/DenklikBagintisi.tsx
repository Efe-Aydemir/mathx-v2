import type { Component } from "solid-js";
import SolverPage from "../../components/SolverPage";

const DenklikBagintisi: Component = () => (
  <SolverPage
    topic={{
      category: "Soyut Matematik",
      subcategory: "Denklik Bağıntısı",
      title: "Denklik Bağıntısı",
      description: "Denklik bağıntılarının refleksif, simetrik ve geçişli özelliklerini inceleyin. Denklik sınıfları ve bölüm kümeleri problemlerini çözün.",
      accentVar: "var(--accent-soyut)",
      placeholder: "Örnek: A = {1, 2, 3, 4} kümesi üzerinde R = {(1,1), (2,2), (3,3), (4,4), (1,2), (2,1)} bağıntısının bir denklik bağıntısı olup olmadığını belirleyiniz.",
    }}
  />
);

export default DenklikBagintisi;
