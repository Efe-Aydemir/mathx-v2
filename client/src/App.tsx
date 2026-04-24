import { createSignal } from "solid-js";
import type { Component, JSX } from "solid-js";
import { Router, Route } from "@solidjs/router";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import DenklikBagintisi from "./pages/soyut-matematik/DenklikBagintisi";
import KismiSiralama from "./pages/soyut-matematik/KismiSiralama";
import IkiliIslemler from "./pages/soyut-matematik/IkiliIslemler";
import IkiliIslemlerdeGruplar from "./pages/soyut-matematik/IkiliIslemlerdeGruplar";
import Halkalar from "./pages/soyut-matematik/Halkalar";
import VektorUzay from "./pages/lineer-cebir/VektorUzay";
import AltVektorUzay from "./pages/lineer-cebir/AltVektorUzay";
import Determinant from "./pages/lineer-cebir/Determinant";
import LineerDonusumler from "./pages/lineer-cebir/LineerDonusumler";
import LineerBirlesim from "./pages/lineer-cebir/LineerBirlesim";
import CizgeTeorisi from "./pages/CizgeTeorisi";
import Topoloji from "./pages/Topoloji";

const AppLayout: Component<{ children?: JSX.Element }> = (props) => {
  const [sidebarOpen, setSidebarOpen] = createSignal(false);

  const toggleSidebar = () => setSidebarOpen((prev) => !prev);
  const closeSidebar = () => setSidebarOpen(false);

  return (
    <div class="app-layout">
      <button
        class="mobile-menu-btn"
        onClick={toggleSidebar}
        aria-label="Menüyü aç/kapat"
      >
        {sidebarOpen() ? "✕" : "☰"}
      </button>

      <div
        class={`sidebar-overlay ${sidebarOpen() ? "open" : ""}`}
        onClick={closeSidebar}
      />

      <div
        class={`sidebar ${sidebarOpen() ? "open" : ""}`}
        onClick={(e) => {
          // Close sidebar when a link is clicked on mobile
          if ((e.target as HTMLElement).closest("a")) {
            closeSidebar();
          }
        }}
      >
        <Sidebar />
      </div>

      <main class="main-content">{props.children}</main>
    </div>
  );
};

const App: Component = () => {
  return (
    <Router root={AppLayout}>
      <Route path="/" component={Home} />

      {/* Soyut Matematik */}
      <Route path="/soyut-matematik/denklik-bagintisi" component={DenklikBagintisi} />
      <Route path="/soyut-matematik/kismi-siralama" component={KismiSiralama} />
      <Route path="/soyut-matematik/ikili-islemler" component={IkiliIslemler} />
      <Route path="/soyut-matematik/ikili-islemlerde-gruplar" component={IkiliIslemlerdeGruplar} />
      <Route path="/soyut-matematik/halkalar" component={Halkalar} />

      {/* Lineer Cebir */}
      <Route path="/lineer-cebir/vektor-uzay" component={VektorUzay} />
      <Route path="/lineer-cebir/alt-vektor-uzay" component={AltVektorUzay} />
      <Route path="/lineer-cebir/determinant" component={Determinant} />
      <Route path="/lineer-cebir/lineer-donusumler" component={LineerDonusumler} />
      <Route path="/lineer-cebir/lineer-birlesim" component={LineerBirlesim} />

      {/* Single Page Solvers */}
      <Route path="/cizge-teorisi" component={CizgeTeorisi} />
      <Route path="/topoloji" component={Topoloji} />
    </Router>
  );
};

export default App;
