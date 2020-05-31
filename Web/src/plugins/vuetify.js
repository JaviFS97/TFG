import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
  themes: {
    light: {
      primary: '#164E77',
      secondary: '#553f75',
      accent: '#82B1FF',
      error: '#e74a3b',
      info: '#36b9cc',
      success: '#1cc88a',
      warning: '#f6c23e',
    },
  },
},
  icons: {
    iconfont: 'mdi',
  },
});
