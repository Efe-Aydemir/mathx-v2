export interface SolveRequest {
  category: string;
  subcategory: string;
  question: string;
}

export interface TopicConfig {
  category: string;
  subcategory: string;
  title: string;
  description: string;
  accentVar: string;
  placeholder: string;
}

export interface CategoryGroup {
  name: string;
  icon: string;
  accentColor: string;
  accentDimColor: string;
  topics: {
    name: string;
    path: string;
    icon: string;
  }[];
}

export const CATEGORIES: CategoryGroup[] = [
  {
    name: "Soyut Matematik",
    icon: "🔮",
    accentColor: "var(--accent-soyut)",
    accentDimColor: "var(--accent-soyut-dim)",
    topics: [
      { name: "Denklik Bağıntısı", path: "/soyut-matematik/denklik-bagintisi", icon: "≡" },
      { name: "Kısmi Sıralama", path: "/soyut-matematik/kismi-siralama", icon: "⊑" },
      { name: "İkili İşlemler", path: "/soyut-matematik/ikili-islemler", icon: "⊕" },
      { name: "İkili İşlemlerde Gruplar", path: "/soyut-matematik/ikili-islemlerde-gruplar", icon: "𝔾" },
      { name: "Halkalar", path: "/soyut-matematik/halkalar", icon: "⊗" },
    ],
  },
  {
    name: "Lineer Cebir",
    icon: "📐",
    accentColor: "var(--accent-lineer)",
    accentDimColor: "var(--accent-lineer-dim)",
    topics: [
      { name: "Vektör Uzay", path: "/lineer-cebir/vektor-uzay", icon: "→" },
      { name: "Alt Vektör Uzay", path: "/lineer-cebir/alt-vektor-uzay", icon: "⊂" },
      { name: "Determinant", path: "/lineer-cebir/determinant", icon: "|⋅|" },
      { name: "Lineer Dönüşümler", path: "/lineer-cebir/lineer-donusumler", icon: "𝑇" },
      { name: "Lineer Birleşim", path: "/lineer-cebir/lineer-birlesim", icon: "∑" },
    ],
  },
  {
    name: "Çizge Teorisi",
    icon: "🔗",
    accentColor: "var(--accent-cizge)",
    accentDimColor: "var(--accent-cizge-dim)",
    topics: [
      { name: "Çizge Teorisi", path: "/cizge-teorisi", icon: "◉" },
    ],
  },
  {
    name: "Topoloji",
    icon: "🍩",
    accentColor: "var(--accent-topoloji)",
    accentDimColor: "var(--accent-topoloji-dim)",
    topics: [
      { name: "Topoloji", path: "/topoloji", icon: "𝕋" },
    ],
  },
];
