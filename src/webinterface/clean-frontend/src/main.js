import Vue from "vue";
import App from "./App.vue";
import router from "./router";

import MaterialKit from "./plugins/material-kit";

/* Notifications plugin für push notifications */
import Notifications from "./components/NotificationPlugin";

Vue.config.productionTip = false;

Vue.use(MaterialKit);
Vue.use(Notifications);

const NavbarStore = {
  showNavbar: false
};

Vue.mixin({
  data() {
    return {
      NavbarStore
    };
  }
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
