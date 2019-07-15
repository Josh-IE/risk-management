<template>
  <v-app
    id="app"
    light
  >
    <v-navigation-drawer
      fixed
      v-model="drawer"
      app
    >
      <v-list dense>
        <v-list-tile @click="goHome">
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="indigo"
      dark
      fixed
      app
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-btn
        icon
        class="hidden-xs-only"
        @click="goBack"
      >
        <v-icon>arrow_back</v-icon>
      </v-btn>
      <v-toolbar-title>Brite App</v-toolbar-title>
    </v-toolbar>
    <v-content class="pt-2">
      <v-container
        grid-list-md
        text-xs-center
      >
        <router-view
          @loader="setLoader"
          @notifySuccess="showAlert"
        />
        <div
          v-if="this.loading"
          class="text-xs-center"
          :style="loadingStyle"
        >
          <v-progress-circular
            :size="70"
            :width="7"
            color="purple"
            indeterminate
          ></v-progress-circular>
        </div>
        <v-alert
          :value="successAlert"
          type="success"
          dismissible
          transition="scale-transition"
          :style="alertStyle"
        >
          Success: Request Success
        </v-alert>
        <v-alert
          :value="errorAlert"
          type="error"
          dismissible
          transition="scale-transition"
          :style="alertStyle"
        >Error: Request Failed
        </v-alert>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      drawer: false,
      loading: false,
      successAlert: false,
      errorAlert: false,
      loadingStyle: {
        position: 'fixed',
        top: '50vh',
        left: '50vw',
        transform: 'translate(-50%, -50%)'
      },
      alertStyle: {
        position: 'fixed',
        bottom: '0px',
        right: '0px'
      }
    }
  },
  methods: {
    setLoader (loading) {
      this.loading = loading
    },
    showAlert (success) {
      if (success) {
        this.successAlert = true
        setTimeout(() => {
          this.successAlert = false
        }, 3000)
      } else {
        this.errorAlert = true
        setTimeout(() => {
          this.errorAlert = false
        }, 3000)
      }
    },
    goHome: function () {
      this.$router.push({ name: 'risk-model-list' })
    },
    goBack: function () {
      this.$router.go(-1)
    }
  }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
