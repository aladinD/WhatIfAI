import Vue from "vue";
import Router from "vue-router";
import MainNavbar from "./layout/MainNavbar.vue";
import MainFooter from "./layout/MainFooter.vue";
import MlDashboard from "./views/ML_Dashboard.vue";

Vue.use(Router);

export default new Router({
  routes: [


    {
      path: "/",
      name: "ml_dashboard",
      components: { default: MlDashboard, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 20 },
        footer: { backgroundColor: "black" }
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
